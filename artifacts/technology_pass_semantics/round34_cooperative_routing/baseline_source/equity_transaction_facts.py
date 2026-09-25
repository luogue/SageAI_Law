"""Cross-clause transaction consistency with retained source pairs."""
import re


def structure_evidence(node, clauses):
    rows=[c.to_public_dict() for c in clauses if c.section_type in {'正式合同条款','附件'}]
    corpus='\n'.join(r['text'] for r in rows)
    out=[]
    if node=='equity_transaction_structure':
        subscriptions=[r for r in rows if re.search(r'作价[^。]{0,100}投入目标公司',r['text'])]
        transfers=[r for r in rows if re.search(r'向(?:甲方|乙方|原股东)[^。；]{0,15}受让[^。；]{0,80}股权',r['text'])]
        # A documented hybrid deal may expressly distinguish each leg.
        separated=re.search(r'(?:分别|另行)[^。]{0,50}(?:转让价款|存量股权)|(?:增资与转让|转让与增资)[^。]{0,30}(?:分别|两部分)',corpus)
        if subscriptions and transfers and not separated:
            out=subscriptions+transfers
            reason='出资流向目标公司与向原股东受让股权同时出现，未区分交易对价及各自股权来源，需核验增资与存量转让的结构冲突。'
    elif node=='equity_contribution_warranty_alignment':
        facts=[]
        for r in rows:
            m=re.search(r'(甲方|乙方)[^。；]{0,150}(房产所有权|土地使用权|设备|知识产权)[^。；]{0,100}作价[^。；]{0,80}投入目标公司',r['text'])
            if m:facts.append((m[1],m[2],r))
        for r in rows:
            if not re.search(r'不存在任何(?:抵押|担保|质押)',r['text']):continue
            asset=re.search(r'投入目标公司的(房产所有权|土地使用权|设备|知识产权)',r['text'])
            heading=' '.join(r.get('heading_path',[]))
            owner=re.search(r'(甲方|乙方)向(?:甲方|乙方)作出',heading)
            if not owner:
                # Parser may expose the declaring party only in a parent row.
                idx=rows.index(r)
                for parent in reversed(rows[:idx]):
                    owner=re.search(r'(甲方|乙方)向(?:甲方|乙方)作出',parent['text'])
                    if owner:break
            if asset and owner and facts and not any(a==owner[1] and b==asset[1] for a,b,_ in facts):
                out += [r]+[f[2] for f in facts]
        reason='出资条款与保证条款的义务主体或资产对象不一致；资产无负担保证的存在不证明其主体与标的绑定正确。'
    elif node=='equity_invalid_cross_reference':
        def number(s):
            if s.isdigit():return int(s)
            d={c:i for i,c in enumerate('零一二三四五六七八九')}
            if '十' in s:
                a,b=s.split('十');return (d.get(a,1)*10)+d.get(b,0)
            return d.get(s,0)
        declared={number(m[1]) for m in re.finditer(r'(?:^|\n)第([一二三四五六七八九十百\d]+)条',corpus)}
        for r in rows:
            for m in re.finditer(r'(?:本合同|本协议)第([一二三四五六七八九十百\d、，及和]+)条',r['text']):
                refs=[number(x) for x in re.split('[、，及和]',m[1]) if x]
                absent=sorted(set(refs)-declared)
                if absent:out.append({**r,'reason':'交叉引用指向正文不存在的条款：'+','.join(map(str,absent))})
        reason='交叉引用指向未定义的条款，相关存续义务范围无法据此确定。'
    else:return []
    for r in out:
        if re.search(r'作价[^。]{0,100}投入目标公司', r['text']):
            r['text'] = next(x.strip()+'。' for x in re.split(r'[。]',r['text']) if re.search(r'作价[^。]{0,100}投入目标公司',x))
        r['text'] = re.sub(r'\s+', ' ', r['text']).strip()
        r['quote'] = r['text']
    return [{**r,'reason':r.get('reason',reason),'scope_evidence_ids':list(dict.fromkeys(x['clause_id'] for x in out))} for r in out]


def corpus_consistency_gate(items, clauses):
    from review_v2.priority_checklist_helpers import PROFILES
    from review_v2.lease_semantics import corpus_facts
    from review_v2.sale_evidence import PROFILES as SALE, supports
    failures=[]
    for item in items:
        if item.get('coverage_status')=='不适用':continue
        node=item['node_id']; elements=item.get('coverage_elements',[])
        requirements=PROFILES.get(node,[])
        found=corpus_facts(clauses,requirements) if requirements else {}
        if node in SALE:
            found={e['element_id']:[c.to_public_dict() for c in clauses if c.section_type in {'正式合同条款','附件'} and supports(e,c.text)] for e in SALE[node]}
        audits=item.get('decision_trace',{}).get('element_absence_searches',[])
        for key,evidence in found.items():
            if not evidence:continue
            actual=next((e for e in elements if e['element_id']==key),{})
            if actual.get('status') in {'MISSING','NOT_APPLICABLE'} or any(a.get('element_id')==key and a.get('result')=='NOT_FOUND' for a in audits):
                failures.append({'requirement':'CORPUS_POSITIVE_VS_ABSENCE','root_cause':item['item_id']+':'+key,'current_status':'FAIL','failure_stage':'Full corpus consistency','evidence':evidence})
    return {'status':'BLOCKED' if failures else 'REPORT_READY','failures':failures}
