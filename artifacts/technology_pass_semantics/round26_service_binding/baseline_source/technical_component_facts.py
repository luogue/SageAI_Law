"""Component lifecycle arrangements, separate from infringement remedies.

Selection, commercial licence compliance, operating fees and continuity are
not substitutes for third-party claim liability, defence or indemnification.
"""
import re
from review_v2.obligation_detail_elements import _segments, _element, _fact


def elements(clauses):
    definitions = {
        'component_selection_control': ('第三方组件选用权限', r'(?:[甲乙丙]方|开发方|提供方).{0,30}(?:可|有权|负责).{0,40}(?:选用|选择|使用).{0,50}(?:开源|第三方)'),
        'component_commercial_license_compliance': ('第三方组件商业许可合规要求', r'(?:应避免|不得|禁止|应确保).{0,40}(?:商业用途|商业许可|许可证)'),
        'component_license_cost_allocation': ('第三方组件及模型使用费用承担', r'(?:API|组件|(?:第三方|开源).{0,12}(?:软件|模型|中间件|数据库|服务接口)).{0,40}(?:费|价款).{0,40}(?:由.{0,12}承担|各承担|分担)'),
        'component_service_continuity': ('第三方服务停止或变更后的替代安排', r'(?:第三方|供应商).{0,35}(?:停止服务|中断|调整接口).{0,45}(?:替代|替换|迁移)'),
    }
    sources = {key: [] for key in definitions}
    for clause, heading, quote in _segments(clauses):
        text = re.sub(r'\s+', '', quote)
        if re.search(r'未(?:明确|约定)|尚无|无需', text):
            continue
        for key, (_, pattern) in definitions.items():
            if re.search(pattern, text):
                sources[key].append(_fact(clause, quote))
    return [_element(key, label, sources[key], source_fact_key='technology.components.' + key,
                     risk_relevant=False)
            for key, (label, _) in definitions.items()]
