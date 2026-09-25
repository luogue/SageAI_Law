from copy import deepcopy
from types import SimpleNamespace
import re

import pytest

from backend.tests.test_construction_coverage_statistics import TEXT, report
from review_v2.clause_parser import parse_contract_clauses
from review_v2.construction_coverage import extract, coverage_failures, permit_attachment_assessment
from review_v2.construction_evidence import EXTERNAL_NODES
from review_v2.engine import review_contract_v2


def test_permit_attachment_is_optional_without_specific_exposure(report):
    row = next(r for r in report['items'] if r['item_id'] == 'CE-13-03')
    assert row['coverage_status'] == '部分覆盖'
    assert row['risk_severity'] == 'LOW'
    assert row['action_priority'] == 'C_OPTIMIZATION'
    assert row['decision_trace']['optional_without_specific_exposure']
    assert report['final_overview_summary']['recommended_action'] == 0
    assert report['final_overview_summary']['medium_risk'] == 0


@pytest.mark.parametrize('extra,expected', [
    ('', False),
    ('本工程施工许可证已被撤销。', True),
    ('本工程尚未取得施工许可证。', True),
    ('若施工许可证已被撤销，承包人应停止施工并通知发包人承担责任。', False),
])
def test_permit_exposure_requires_direct_evidence(extra, expected):
    text = '1.1 许可\n发包人应负责办理施工许可证，取得施工许可证后方可开工。\n2.1 状态\n' + extra
    assert permit_attachment_assessment(parse_contract_clauses(text))['specific_exposure'] is expected


@pytest.mark.parametrize('text', [
    '合同文件包括中标通知书。',
    '发包人应负责办理施工许可证。',
    '取得施工许可证后方可开工。',
])
def test_missing_permit_safeguards_do_not_receive_optional_exemption(text):
    assert permit_attachment_assessment(parse_contract_clauses(text))['specific_exposure']


def test_all_external_rules_remain_unverified(report):
    rows = [r for r in report['items'] if r['node_id'] in EXTERNAL_NODES]
    assert len(rows) == 6
    assert all(r['coverage_status'] == '待核验' and r['needs_manual_review'] for r in rows)
    for row in rows:
        forged = deepcopy(row)
        forged['coverage_status'] = '通过'
        assert coverage_failures([SimpleNamespace(**forged)])


@pytest.mark.parametrize('text,item_id', [
    ('双方承诺不串通投标。', 'CE-03-03'),
    ('承包人不得借用资质，不得挂靠。', 'CE-02-03'),
    ('双方按时付款。', 'CE-03-03'),
])
def test_clean_contract_text_cannot_prove_external_facts(text, item_id):
    result = review_contract_v2('建设工程施工合同\n1.1 约定\n' + text, 'construction', use_llm=False)
    row = next(r for r in result['items'] if r['item_id'] == item_id)
    assert row['coverage_status'] == '待核验'


@pytest.mark.parametrize('text,item_id', [
    ('双方约定通过虚假招标确定承包人。', 'CE-03-03'),
    ('承包人同意由施工队借用资质施工。', 'CE-02-03'),
])
def test_affirmative_external_adverse_agreement_is_not_erased(text, item_id):
    result = review_contract_v2('建设工程施工合同\n1.1 约定\n' + text, 'construction', use_llm=False)
    row = next(r for r in result['items'] if r['item_id'] == item_id)
    assert row['coverage_status'] == '风险条款'
    assert row['evidence_clauses']
    assert row['needs_manual_review']


def test_completion_uses_actual_determination_not_planned_date_or_reference(report):
    row = next(r for r in report['items'] if r['item_id'] == 'CE-07-02')
    assert row['coverage_status'] == '通过'
    assert all(r['location'] == '第二部分 通用条款 / 10.4' for r in row['evidence_clauses'])
    assert '以竣工验收合格之日为实际竣工日期' in row['evidence_clauses'][0]['text']
    assert not extract('completion_date_identification', parse_contract_clauses('10.3 质量\n实际竣工日期按照第10.4款约定确定。\n计划竣工日期为2028年9月29日。'))
    moved = extract('completion_date_identification', parse_contract_clauses('23.7 日期\n以竣工验收合格之日为实际竣工日期。'))
    assert moved and moved[0]['location'].endswith('23.7')


def test_all_pass_quotes_belong_to_their_actual_source_section(report):
    clauses = {c.clause_id: c for c in parse_contract_clauses(TEXT)}
    compact = lambda s: re.sub(r'\s+', '', s)
    for row in report['items']:
        if row['coverage_status'] != '通过':
            continue
        for evidence in row['evidence_clauses']:
            source = clauses[evidence['clause_id']]
            assert evidence['location'] == source.location, row['item_id']
            assert compact(evidence['text']) in compact(source.text), row['item_id']


@pytest.mark.parametrize('node,text', [
    ('employer_permit_assistance', '发包人承担差旅费，承包人负责办理进入厂家的许可。'),
    ('quality_standard_acceptance', '10.3 竣工验收质量不合格和重新验收'),
    ('quality_standard_acceptance', '根据专业工程施工图纸、现行计价标准计算结算价款。'),
    ('supplementary_agreement_boundary', '发包人拥有批准变更的权限。'),
    ('subcontract_to_qualified_party', '经发包人批准，承包人应将正在执行的分包合同转让至发包人名下。'),
])
def test_weak_or_different_relationship_does_not_supply_positive_evidence(node, text):
    assert not extract(node, parse_contract_clauses(text))
