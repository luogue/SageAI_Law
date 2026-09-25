"""Shared material-disposition evidence, qualified by actor, object and scope.

Deleting one workstation's electronic files is an existing arrangement, but it
does not establish return/destruction of every material, copy and backup.  The
same scoped facts can be consumed by ownership and confidentiality reviews.
"""
from __future__ import annotations

import re
from typing import Any


_PARTY = r"被许可[方人]|(?<!被)许可[方人]|受让方|让与方|出让方|委托方|受托方|开发方|卖方|买方|甲方|乙方|丙方|双方|各方"
_EVENT = r"(?:合同)?(?:终止|解除|届满|履行完毕)|项目(?:结束|完成)|保密目的(?:完成|实现)|资料不再需要"
_ACTIONS = {"return": "返还", "delete": "删除|清除", "destroy": "销毁", "retain": "保存|保留|留存"}
_OBJECTS = {
    "material": r"(?<!电子)(?<!技术)(?<!保密)(?<!原始)(?:项目|研发|研究|开发)?资料|全部文件|所有文件",
    "electronic_material": r"电子(?:资料|文件|数据)",
    "technical_material": r"(?<!秘密)技术(?:资料|文件)|开发文档|研发记录",
    "technical_secret_material": r"技术秘密(?:资料|文件)?|保密(?:资料|信息|文件|材料)",
    "source_code": r"源代码|源程序",
    "original_material": r"原始资料|原件",
    "copy": r"复制件|副本",
    "backup": r"备份(?:文件|数据)?",
    "counterparty_data": r"(?:业务|生产|销售|测试|客户)数据|客户资料|技术反馈",
}
_LABELS = {
    "material": "项目资料", "electronic_material": "电子资料", "technical_material": "技术资料",
    "technical_secret_material": "技术秘密及保密资料", "source_code": "源代码",
    "original_material": "原始资料", "copy": "复制件及副本", "backup": "备份资料",
    "counterparty_data": "对方提供的数据",
}
_DISPOSAL = {"return", "delete", "destroy"}
_ACTION_START = r"(?:返还|删除|销毁|清除|保存|保留|留存)"
_COORDINATED_PREDICATE = rf"(?:由)?(?:{_PARTY})|将|把|(?:应当|应|须|必须|立即|继续)*{_ACTION_START}"


def _compact(text):
    return re.sub(r"\s+", "", str(text))


def _actor(text):
    found = re.search(rf"({_PARTY})(?=应当|应|须|必须|不得|无需|无须|可以|可|负责|对|返还|删除|销毁|清除|保存|保留|留存)", text)
    if not found:
        found = re.search(rf"由({_PARTY})(?:负责)?(?=返还|删除|销毁|清除|保存|保留|留存|处置)", text)
    return found.group(1) if found else ""


def _owner(text):
    # Ownership/provision and quantity modifiers may be combined, e.g.
    # '甲方所提供的全部资料'.  Do not consume modal duties or instructions:
    # '甲方要求返还的资料' alone does not prove that those materials belong to A.
    modifiers = r"(?:(?:所|其)?提供的?|所属的?|持有的?|所有的?|全部|所有|相关|各项|的)*"
    owned_object = r"资料|数据|技术资料|技术秘密资料|保密资料|电子资料|原始资料|原件|复制件|副本|备份|源代码|(?:业务|生产|销售|测试|客户)数据|客户资料|技术反馈"
    found = re.search(rf"({_PARTY}){modifiers}(?={owned_object})", text)
    return found.group(1) if found else "COUNTERPARTY" if re.search(r"对方(?:提供的?|的)?(?:资料|数据|技术资料)", text) else ""


def _named_objects(text):
    specific = {key: pattern for key, pattern in _OBJECTS.items() if key != "material"}
    named = [key for key, pattern in specific.items() if re.search(pattern, text)]
    # Mask complete typed spans before matching the generic parent.  Fixed
    # lookbehinds cannot reliably exclude every suffix (e.g. 技术秘密资料).
    generic_text = text
    for pattern in specific.values():
        generic_text = re.sub(pattern, lambda match: " " * len(match.group(0)), generic_text)
    if re.search(_OBJECTS["material"], generic_text):
        named.insert(0, "material")
    return named


def extract_scoped_material_disposition_facts(clauses) -> list[dict[str, Any]]:
    """Extract literal obligations without expanding actors, objects or media."""
    facts = []
    for clause in clauses:
        if getattr(clause, "party_obligation", True) is False:
            continue
        context = " ".join([*(getattr(clause, "heading_path", None) or []), getattr(clause, "title", "") or ""])
        last_disposal = []
        last_data_context = None
        for sentence in re.split(r"[。；;\n]", clause.text):
            quote = sentence.strip()
            text = _compact(quote)
            if not text:
                continue
            after_end = bool(re.search(_EVENT, text + context))
            actor = ""
            owner = ""
            sentence_disposals = []
            sentence_data_context = None
            sentence_named_objects = set()
            # A conjunction followed by another predicate starts a new binding
            # window.  Merely sharing a sentence cannot pair its every object
            # with its every verb (or carry A's obligation over to B).
            parts = re.split(
                rf"[，,]|但是|但|而|(?:并且|并|以及|及|和|、|后)(?={_COORDINATED_PREDICATE})",
                text,
            )
            for part in parts:
                if re.search(r'未(?:另行)?(?:约定|明确|规定)|尚无', part):
                    # A mentioned deletion inside “未约定删除后的证明”
                    # is not an operative promise to delete that object.
                    continue
                explicit_actor = _actor(part)
                if explicit_actor:
                    if actor and explicit_actor != actor:
                        owner = ""
                    actor = explicit_actor
                explicit_owner = _owner(part)
                if explicit_owner:
                    owner = explicit_owner
                object_types = _named_objects(part)
                sentence_named_objects.update(object_types)
                if "counterparty_data" in object_types and not re.search(r"不存在|不含|不包含|未提供|未收集|无需提供", part):
                    sentence_data_context = {
                        "clause_id": clause.clause_id, "quote": quote,
                        "actor": actor or "UNKNOWN", "material_owner": owner or "UNKNOWN",
                        "object_type": "counterparty_data",
                    }
                context_source = None
                if not object_types and re.search(r"相关数据|上述数据|该等数据|这些数据", part):
                    antecedent = sentence_data_context or last_data_context
                    # A same-clause reference needs an actual named antecedent
                    # and the same explicitly identified holder.  It cannot
                    # invent copies/backups, change owners or bridge clauses.
                    if antecedent and actor and antecedent["actor"] == actor and (
                        not owner or owner == antecedent["material_owner"]
                    ):
                        object_types = [antecedent["object_type"]]
                        owner = antecedent["material_owner"]
                        context_source = dict(antecedent)
                if not object_types:
                    continue
                for action, pattern in _ACTIONS.items():
                    action_match = re.search(pattern, part)
                    if not action_match:
                        continue
                    if not after_end:
                        continue  # routine delivery, testing and refund are other events
                    prefix = part[max(0, action_match.start() - 12):action_match.start()]
                    negated = bool(re.search(r"(?:无需|无须|不必|不得|不予|不再|不)(?:继续)?$", prefix))
                    storage = re.search(r"(?:项目)?(?:工作电脑|办公电脑|服务器|云盘|移动存储设备|存储设备|存储介质|终端|邮箱)(?:中|内|上)(?:的)?", part)
                    bounded = bool(storage or re.search(r"仅|部分|特定|指定|(?:要求|选择).{0,30}的", part))
                    deferred = bool(re.search(r"另行(?:协商|约定|商定)|具体.{0,8}待定|原则上", part))
                    for object_type in object_types:
                        row = {
                            "clause_id": clause.clause_id,
                            "quote": quote,
                            "location": getattr(clause, "location", ""),
                            "source_domain": "MATERIAL_DISPOSITION",
                            "actor": actor or "UNKNOWN",
                            "material_owner": owner or "UNKNOWN",
                            "object_type": object_type,
                            "action": action,
                            "post_contract": after_end,
                            "storage_scope": storage.group(0) if storage else "",
                            "scope_limited": bounded,
                            "deferred": deferred,
                            "polarity": "NEGATED" if negated else "AFFIRMATIVE",
                        }
                        if context_source:
                            row["context_source"] = context_source
                            row["antecedent_quote"] = context_source["quote"]
                        if row not in facts:
                            facts.append(row)
                        if action in _DISPOSAL and not negated:
                            sentence_disposals.append(row)
            if sentence_disposals:
                last_disposal = sentence_disposals
            if sentence_data_context:
                last_data_context = sentence_data_context
            elif sentence_named_objects:
                last_data_context = None
            # A standalone written-confirmation sentence can refer to the same
            # actor's preceding disposal, but not to product acceptance.
            confirmation = re.search(r"(?:书面确认|书面证明|确认书|证明书|销毁证明|删除证明|处置确认)", text)
            confirmation_event = re.search(r"返还|删除|销毁|清除|资料处置", text)
            confirmation_anaphora = re.search(r"上述(?:资料)?处置|前述处置|该项处置|该等资料|对此|此项处置", text)
            unrelated_confirmation = re.search(r"费用结算|付款|结算结果|验收|交付验收|工期确认", text)
            if confirmation and (confirmation_event or confirmation_anaphora) and not unrelated_confirmation and not re.search(r"无需|无须|不必|未约定|未明确", text):
                explicit_actor = _actor(text)
                for antecedent in last_disposal:
                    if explicit_actor and explicit_actor != antecedent["actor"]:
                        continue
                    row = {**antecedent, "action": "confirmation", "quote": quote,
                           "antecedent_quote": antecedent["quote"]}
                    if row not in facts:
                        facts.append(row)
    return facts


def _applies_to_actor(fact, actor):
    return fact["actor"] == actor or fact["actor"] in {"双方", "各方"}


def _fact_identity(key, actor, object_type, material_owner):
    return {
        "canonical_fact_key": key,
        "scope": "POST_CONTRACT_ALL_LOCATIONS" + (f":OWNER={material_owner}" if material_owner else ""),
        "party": actor,
        "object": object_type,
    }


def material_disposition_elements(clauses, *, actor, object_types=("material", "copy", "backup"), material_owner=None):
    """Build one shared state set for the requested actor and material objects.

    A broad material requirement may have partial support from an identified
    subset.  An unrelated object's fact cannot prove a specific object's duty.
    No-retention permission is not a deletion mechanism, nor a usage permission.
    """
    facts = extract_scoped_material_disposition_facts(clauses)
    applicable = [fact for fact in facts if _applies_to_actor(fact, actor)
                  and (not material_owner or fact["material_owner"] in {material_owner, "COUNTERPARTY"})]
    result = []
    for object_type in object_types:
        if object_type not in _LABELS:
            raise ValueError(f"Unknown material object type: {object_type}")
        label = f"{actor}在项目结束后的{_LABELS[object_type]}返还、删除或销毁"
        direct = [fact for fact in applicable if fact["object_type"] == object_type and fact["action"] in _DISPOSAL
                  and fact["polarity"] == "AFFIRMATIVE"]
        subset = []
        if object_type == "material":
            subset = [fact for fact in applicable if fact["object_type"] not in {"copy", "backup"}
                      and fact["action"] in _DISPOSAL and fact["polarity"] == "AFFIRMATIVE"]
        complete = [fact for fact in direct if not fact["scope_limited"] and not fact["deferred"]]
        support = complete or direct or subset
        contrary = [fact for fact in applicable if fact["object_type"] == object_type
                    and ((fact["action"] in _DISPOSAL and fact["polarity"] == "NEGATED")
                         or (fact["action"] == "retain" and fact["polarity"] == "AFFIRMATIVE"))]
        status = "COVERED" if complete else "PARTIALLY_COVERED" if support else "MISSING"
        # Keep an existing retention arrangement as presence, with the exact
        # bargain separate for risk direction; never manufacture external use.
        if contrary:
            status = "PARTIALLY_COVERED"
            support = [*support, *contrary]
        residual = f"{actor}对未纳入现有处置范围的{_LABELS[object_type]}及其他保存载体的处置安排" if support else label
        row = {
            "element_id": object_type + "_disposition",
            "source_fact_key": object_type + "_disposition",
            "required_fact": label,
            "status": status,
            "proposition": "；".join(dict.fromkeys(fact["quote"] for fact in support)) if support else label,
            "obligated_party": actor,
            "material_owner": material_owner or "UNSPECIFIED",
            "object_type": object_type,
            "residual_gap": residual if status != "COVERED" else "",
            "search_targets": [residual if status != "COVERED" else label],
            "risk_relevant": True,
            "supporting_evidence": support,
            "bound_evidence_ids": list(dict.fromkeys(fact["clause_id"] for fact in support)),
            "fact_identity": _fact_identity(object_type + "_disposition", actor, object_type, material_owner),
        }
        if contrary:
            row["retention_or_denial_facts"] = contrary
        result.append(row)
    confirmation = [fact for fact in applicable if fact["action"] == "confirmation"]
    label = f"{actor}完成资料返还、删除或销毁后的书面处置确认"
    complete_confirmation = [fact for fact in confirmation if fact["object_type"] == "material"
                             and not fact["scope_limited"] and not fact["deferred"]]
    confirmation_status = "COVERED" if complete_confirmation else "PARTIALLY_COVERED" if confirmation else "MISSING"
    confirmation_residual = f"{actor}对未纳入现有确认范围的资料处置出具书面确认" if confirmation else label
    result.append({
        "element_id": "material_disposal_confirmation", "source_fact_key": "material_disposal_confirmation",
        "required_fact": label, "status": confirmation_status,
        "proposition": "；".join(dict.fromkeys(fact["quote"] for fact in confirmation)) if confirmation else label,
        "obligated_party": actor, "material_owner": material_owner or "UNSPECIFIED", "object_type": "disposition_confirmation",
        "residual_gap": "" if complete_confirmation else confirmation_residual,
        "search_targets": [label if complete_confirmation else confirmation_residual], "risk_relevant": True,
        "supporting_evidence": confirmation, "bound_evidence_ids": list(dict.fromkeys(fact["clause_id"] for fact in confirmation)),
        "fact_identity": _fact_identity("material_disposal_confirmation", actor, "disposition_confirmation", material_owner),
    })
    for row in result:
        row["underlying_issue_title"] = "项目结束后的资料处置机制"
    return result
