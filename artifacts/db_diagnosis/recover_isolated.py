"""Reproducible salvage and field comparisons, ONLY from preserved evidence."""
import collections
import hashlib
import json
import shutil
import sqlite3
import subprocess
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / 'artifacts' / 'db_recovery'
SOURCE = ROOT / 'evidence' / 'app.db'
OUT = ROOT / 'candidates_official'

def q(name):
    return '"' + name.replace('"', '""') + '"'

def ro(path):
    return sqlite3.connect(path.resolve().as_uri() + '?mode=ro&immutable=1', uri=True)

def digest(value):
    return hashlib.sha256(repr(value).encode('utf-8')).hexdigest()

def check(db):
    result = {}
    for name in ('integrity_check', 'quick_check', 'foreign_key_check'):
        try:
            result[name] = db.execute('PRAGMA ' + name).fetchall()
        except sqlite3.Error as error:
            result[name] = {'error': str(error)}
    return result

def main():
    global SOURCE, OUT
    parser = argparse.ArgumentParser()
    parser.add_argument('--latest', action='store_true')
    args = parser.parse_args()
    if args.latest:
        SOURCE = ROOT / 'latest_materialized' / 'app.db'
        OUT = ROOT / 'candidates_latest'
    OUT.mkdir(exist_ok=False)
    source = ro(SOURCE)
    schema = source.execute('SELECT type,name,tbl_name,sql FROM sqlite_schema WHERE sql IS NOT NULL ORDER BY type,name').fetchall()
    tables = [r[1] for r in schema if r[0] == 'table' and not r[1].startswith('sqlite_')]
    columns = {t: [r[1] for r in source.execute('PRAGMA table_info(' + q(t) + ')')] for t in tables}
    baseline = {t: source.execute('SELECT * FROM ' + q(t) + ' ORDER BY rowid').fetchall() for t in tables if t != 'task_record'}
    ids = [r[0] for r in source.execute('SELECT id FROM task_record INDEXED BY ix_task_record_id')]
    tasks, failed = [], []
    for ident in ids:
        try:
            tasks.append(source.execute('SELECT * FROM task_record WHERE rowid=?', (ident,)).fetchone())
        except sqlite3.Error:
            failed.append(ident)
    baseline['task_record'] = tasks
    partial = {}
    # Covering indexes can still expose fields without reading the damaged table B-tree.
    for name, *_ in source.execute("SELECT name FROM sqlite_schema WHERE type='index' AND tbl_name='task_record'"):
        indexed = [r[2] for r in source.execute('PRAGMA index_info(' + q(name) + ')') if r[2]]
        selected = list(dict.fromkeys(['id'] + indexed))
        try:
            rows = source.execute('SELECT ' + ','.join(map(q, selected)) + ' FROM task_record INDEXED BY ' + q(name)).fetchall()
            for row in rows:
                if row[0] in failed:
                    partial.setdefault(str(row[0]), {}).update(dict(zip(selected, row)))
        except sqlite3.Error:
            pass
    # Full values are retained locally for salvage, not printed in the report.
    (OUT / 'task-salvage.json').write_text(json.dumps({'columns': columns['task_record'], 'complete': tasks, 'partial': partial}, ensure_ascii=False, indent=2), encoding='utf-8')
    logical = sqlite3.connect(OUT / 'logical.db')
    for typ, name, table, sql in schema:
        if typ == 'table' and not name.startswith('sqlite_'):
            logical.execute(sql)
    for table, rows in baseline.items():
        logical.executemany('INSERT INTO ' + q(table) + ' VALUES(' + ','.join('?' for _ in columns[table]) + ')', rows)
    for typ, name, table, sql in schema:
        if typ in ('index', 'trigger', 'view'):
            logical.execute(sql)
    logical.commit()
    logical.close()
    cli = str(ROOT / 'tools' / 'sqlite3.exe')
    report = {'sqlite_cli': subprocess.check_output([cli, '-version'], text=True).strip(),
              'baseline': {'table_counts': {t:len(v) for t,v in baseline.items()}, 'indexed_task_ids': ids, 'unreadable_task_ids':failed},
              'partial_fields': {key: list(value) for key,value in partial.items()}, 'methods': {}}
    for label, command in [('recover', '.recover'), ('recover_ignore_freelist', '.recover --ignore-freelist')]:
        sql_path = OUT / (label + '.sql')
        with sql_path.open('wb') as output:
            recovery = subprocess.run([cli, '-readonly', SOURCE.as_uri() + '?immutable=1', command], stdout=output, stderr=subprocess.PIPE)
        with sql_path.open('rb') as input_file:
            imported = subprocess.run([cli, '-bail', str(OUT / (label + '.db'))], stdin=input_file, capture_output=True)
        report['methods'][label] = {'recover_exit': recovery.returncode, 'recover_stderr': recovery.stderr.decode(errors='replace'),
                                    'import_exit': imported.returncode, 'import_stderr': imported.stderr.decode(errors='replace')}
    for label in ('logical', 'recover', 'recover_ignore_freelist'):
        db = ro(OUT / (label + '.db'))
        result = report['methods'].setdefault(label, {})
        result.update(check(db))
        actual_schema = db.execute('SELECT type,name,tbl_name,sql FROM sqlite_schema WHERE sql IS NOT NULL ORDER BY type,name').fetchall()
        result['schema_exact_equal'] = actual_schema == schema
        result['tables'] = {}
        for table in tables:
            try:
                actual = db.execute('SELECT * FROM ' + q(table) + ' ORDER BY rowid').fetchall()
                original = {r[0]:r for r in baseline[table]}
                rebuilt = {r[0]:r for r in actual}
                differences = []
                for ident in original.keys() & rebuilt.keys():
                    for field, a, b in zip(columns[table], original[ident], rebuilt[ident]):
                        if a != b:
                            differences.append({'id':ident,'field':field,'source_sha256':digest(a),'candidate_sha256':digest(b)})
                result['tables'][table] = {'count':len(actual),'baseline_count':len(original), 'missing_ids':sorted(original.keys()-rebuilt.keys()),
                                          'extra_ids':sorted(rebuilt.keys()-original.keys()),'field_differences': differences,
                                          'duplicate_primary_keys':len(actual)-len(rebuilt), 'all_readable_rows_exact': all(rebuilt.get(k)==v for k,v in original.items())}
                if table == 'task_record':
                    result['damaged_task_salvage'] = {str(k): {'present':k in rebuilt, 'known_index_fields_match': all(rebuilt[k][columns[table].index(f)]==v for f,v in partial.get(str(k),{}).items()) if k in rebuilt else False} for k in failed}
            except sqlite3.Error as error:
                result['tables'][table] = {'error':str(error)}
        extra = [r[1] for r in actual_schema if r[0]=='table' and r[1] not in tables and not r[1].startswith('sqlite_')]
        result['extra_tables'] = {t:db.execute('SELECT count(*) FROM '+q(t)).fetchone()[0] for t in extra}
        # record_id has no declared FK: report existing orphan links, never silently delete them.
        try:
            result['task_report_orphans'] = [r[0] for r in db.execute('SELECT t.id FROM task_record t LEFT JOIN record r ON t.record_id=r.id WHERE t.record_id IS NOT NULL AND r.id IS NULL')]
        except sqlite3.Error:
            pass
        db.close()
    source.close()
    (ROOT / ('data-differences-latest.json' if args.latest else 'data-differences.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({label:{'checks':{k:v for k,v in result.items() if k in ('integrity_check','quick_check','foreign_key_check','recover_exit','recover_stderr','import_exit','extra_tables','schema_exact_equal','task_report_orphans')},'tasks':result['tables'].get('task_record'), 'salvage':result.get('damaged_task_salvage')} for label,result in report['methods'].items()},ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
