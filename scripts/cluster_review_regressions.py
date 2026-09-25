"""Inventory failing regression assertions without changing tests or outcomes.

Buckets are primary failure symptoms, not a claim that every downstream failed
assertion is an independent defect. Keep full traces for root-cause inspection.
"""
import argparse
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


def bucket(row, diagnosed_baseline=False):
    message, name = row['message'], row['test']
    if ((diagnosed_baseline and 'test_entrusted_development_contract_review::' in name)
            or "unexpected keyword argument 'presentation'" in message
            or "name 'report' is not defined" in message
            or 'one_uncertain_item() takes' in message):
        return '测试输入串线、报告对象回读及失效测试钩子'
    if re.search(r'KeyError|StopIteration|IndexError|NameError', message):
        return '事实节点/派生结果丢失或测试接口异常'
    if re.search(r'BLOCKED|REPORT_READY|PASSED|EVIDENCE_INSUFFICIENT', message):
        return '发布门禁/要素证据链不完整'
    if re.search(r"C\d{4}|EV-[a-z0-9]|SRC-|条.*项|source_clause|source_location", message) and not (' in \'# ' in message):
        return '精确引文、条款定位及证据标识不一致'
    if re.search(r'NOT_APPLICABLE|不适用|APPLICABLE|ENTRUSTED|TECHNOLOGY_|TECHNICAL_|PATENT_|GENERAL_|contract_category|contract_family|主体类型', message):
        return '交易分类、主体或条件适用性'
    if re.search(r'ADVERSE|CONFLICTING|风险条款|风险.*方|风险.*中|风险.*高', message):
        return '不利方向/冲突事实被覆盖或丢失'
    if re.search(r'MISSING|COVERED|PARTIAL|UNCERTAIN|缺失|部分覆盖|通过|待核验|PRESENT', message):
        return '正向事实召回与多要素覆盖归一'
    if re.search(r'count|summary|总数|数量|聚合|主题数|规则级|assert \d+ == \d+', message + name):
        return '聚合、统计与报告投影'
    return '建议/判断文本及其他语义断言'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('xml', nargs='+', type=Path)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--diagnosed-baseline', action='store_true',
                   help='Account for the confirmed 12*.docx fixture collision in the original run only.')
    args = p.parse_args()
    rows = []
    for path in args.xml:
        for case in ET.parse(path).iter('testcase'):
            failure = case.find('failure')
            if failure is None:
                failure = case.find('error')
            if failure is None:
                continue
            row = {'test': case.get('classname') + '::' + case.get('name'),
                   'message': failure.get('message', ''), 'trace': failure.text or ''}
            row['cluster'] = bucket(row, args.diagnosed_baseline)
            rows.append(row)
    counts = Counter(row['cluster'] for row in rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({'failure_count': len(rows), 'clusters': dict(counts.most_common()),
                                      'failures': rows}, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps({'failure_count': len(rows), 'clusters': dict(counts.most_common())}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
