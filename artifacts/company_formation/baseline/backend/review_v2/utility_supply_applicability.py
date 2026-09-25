"""Explicit important-user identity evidence, not inferred industry risk."""
import re


def extract_applicability_facts(clauses):
    positive, negative = [], []
    identity = r"(?:(?:特级|一级|二级|临时性)?重要(?:电力)?用户)"
    party = r"(?:乙方|用电方|用户|本企业|本单位|本项目)"
    for clause in clauses:
        for sentence in re.split(r"[。；;\n]", clause.text):
            # Conditional examples and future identification are not present identity.
            if re.search(r"若|如果|如属于|如为|是否|待认定|拟认定|尚未认定", sentence):
                continue
            no = re.search(rf"{party}[^。；]{{0,15}}(?:不属于|不是|非|不被认定为){identity}", sentence)
            yes = re.search(rf"{party}[^。；]{{0,40}}(?:属于|为|是|认定为|列为)(?:经[^。；]{{0,20}}认定的)?{identity}", sentence)
            if no or yes:
                row = dict(clause_id=clause.clause_id, location=clause.location, quote=sentence.strip())
                (negative if no else positive).append(row)
    value = None if (positive and negative) or not (positive or negative) else bool(positive)
    return {"is_important_user": dict(value=value, label="属于经确认的重要用户",
            evidence=positive + negative, searched_clause_ids=[c.clause_id for c in clauses],
            verification_instruction="请核验用户是否属于经确认的重要用户，并提供用户分级、主管部门认定或相关用户资料；工业生产、容量和连续生产本身不构成身份认定。")}
