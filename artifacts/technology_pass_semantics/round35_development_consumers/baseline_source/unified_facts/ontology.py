"""Evidence-local ontology checks, never a second extraction over the contract."""
import re


def principal_basis(expression):
    if not isinstance(expression,str):
        raise ValueError('BASE_EXPRESSION_REQUIRED')
    text=re.sub(r'\s+','',expression)
    if re.search(r'(?:未偿还|未偿|未还|尚未归还|尚未偿还|未清偿|剩余|实际占用|正常|逾期).{0,8}本金(?:余额)?|本金(?:剩余)?余额',text):
        return 'UNPAID_PRINCIPAL'
    if re.search(r'(?:应付未付|未付|未支付|拖欠|欠付).{0,5}利息|欠息',text):
        return 'UNPAID_INTEREST'
    if re.search(r'(?:原始|最初|全部|总额|总金额).{0,6}(?:借款|本金)|(?:借款|本金)(?:总额|总金额|全额)',text):
        return 'PRINCIPAL'
    raise ValueError('UNRESOLVED_BASE_EXPRESSION')


def evidence_supports(concept,value,refs):
    # Formatting normalization is for ontology matching only; bound original
    # quotes/spans are retained byte-for-character unchanged in the store.
    text=re.sub(r'\s+','','\n'.join(r['quote'] for r in refs))
    if value is not True:
        return True
    if concept.endswith(('loan_early_channel','loan_extension_channel')):
        purpose=text+' '.join(str(r.get('section','')) for r in refs)
        target=r'提前(?:还款|偿还|归还|清偿)|全部通知|所有通知|一切通知' if concept.endswith('loan_early_channel') else r'展期|延长借款|全部通知|所有通知|一切通知'
        return bool(re.search(r'书面|短信|微信|电子邮件|电子邮箱|邮件|电子系统|平台|电话|传真|当面|口头',text)
                    and re.search(r'通知|申请|提交|提出|告知',text) and re.search(target,purpose))
    if concept=='loan.compound':
        return bool(re.search(r'计收复利|计算复利|复利计算|复利计收|利滚利|利息计入本金|利息并入本金',text)
            and re.search(r'未付利息|未支付.{0,5}利息|欠息|未偿利息|利息计入本金|利息并入本金',text)
            and re.search(r'利率|百分之|%|％|每日|每月|每年|周期',text))
    if concept in {'loan.voucher_mechanism','loan.debt_instrument'}:
        return bool(re.search(r'借据|借条|欠条|收据|回单|回执|放款记录|转账(?:记录|凭证)|到账(?:凭证|证明)|支付凭证|电子凭证',text))
    return True


def validate_fact(fact):
    if fact['state']!='PRESENT':
        return
    value=fact['normalized_value']
    refs=fact['evidence']
    if not evidence_supports(fact['concept'],value,refs):
        raise ValueError('EVIDENCE_DOES_NOT_SUPPORT_ATTRIBUTE:'+fact['concept'])
    if isinstance(value,dict) and value.get('base_expression') is not None:
        expression=value['base_expression']
        if not any(expression in r['quote'] for r in refs):
            raise ValueError('BASE_EXPRESSION_NOT_IN_EVIDENCE')
        if principal_basis(expression)!=value['base']:
            raise ValueError('BASE_ONTOLOGY_DRIFT')
    elif isinstance(value,dict) and 'base_expression' in value and value['base']!='UNKNOWN':
        raise ValueError('BASE_WITHOUT_EXPLICIT_EXPRESSION')
