from review_v2.clause_parser import parse_contract_clauses
from review_v2.material_disposition import extract_scoped_material_disposition_facts, material_disposition_elements


def states(text, actor="乙方", **kwargs):
    return {row["element_id"]: row for row in material_disposition_elements(parse_contract_clauses(text), actor=actor, **kwargs)}


def test_workstation_electronic_deletion_is_only_partial_material_disposition():
    text = "第一条 资料使用\n合同履行完毕后，乙方应停止将甲方资料用于本项目以外的用途，并删除项目工作电脑中的相关电子资料。"
    rows = states(text)
    assert rows["material_disposition"]["status"] == "PARTIALLY_COVERED"
    source = rows["material_disposition"]["supporting_evidence"][0]
    assert source["actor"] == "乙方"
    assert source["material_owner"] == "甲方"
    assert source["storage_scope"] == "项目工作电脑中的"
    assert rows["copy_disposition"]["status"] == "MISSING"
    assert rows["backup_disposition"]["status"] == "MISSING"
    assert rows["material_disposal_confirmation"]["status"] == "MISSING"


def test_party_a_obligation_cannot_cover_party_b():
    text = "第一条 资料处置\n合同终止后甲方应删除电子资料。"
    assert states(text, "甲方")["material_disposition"]["status"] == "PARTIALLY_COVERED"
    assert all(row["status"] == "MISSING" for row in states(text, "乙方").values())


def test_mixed_subjects_preserve_own_objects():
    text = "第一条 资料处置\n合同终止后，甲方应返还保密资料，乙方应删除技术资料。"
    a = states(text, "甲方", object_types=("technical_material", "technical_secret_material"))
    b = states(text, "乙方", object_types=("technical_material", "technical_secret_material"))
    assert a["technical_secret_material_disposition"]["status"] == "COVERED"
    assert a["technical_material_disposition"]["status"] == "MISSING"
    assert b["technical_material_disposition"]["status"] == "COVERED"
    assert b["technical_secret_material_disposition"]["status"] == "MISSING"


def test_disposal_requires_post_contract_event_and_material_object():
    text = "第一条 验收\n乙方应删除测试中不合格的产品数据。验收失败后甲方要求返还全部款项。"
    assert extract_scoped_material_disposition_facts(parse_contract_clauses(text)) == []


def test_all_material_return_does_not_implicitly_delete_copies_and_backups():
    rows = states("第一条 资料处置\n合同终止后，乙方应返还甲方全部资料。")
    assert rows["material_disposition"]["status"] == "COVERED"
    assert rows["copy_disposition"]["status"] == "MISSING"
    assert rows["backup_disposition"]["status"] == "MISSING"


def test_copy_retention_cannot_become_technical_secret_or_external_use():
    text = "第一条 合同终止\n乙方应返还原始资料，但乙方可以继续保存项目复制件。"
    rows = states(text)
    assert rows["copy_disposition"]["status"] == "PARTIALLY_COVERED"
    assert rows["copy_disposition"]["retention_or_denial_facts"]
    assert rows["backup_disposition"]["status"] == "MISSING"
    assert not any("外部使用" in row["proposition"] for row in rows.values())


def test_each_explicit_object_and_written_confirmation_is_covered():
    text = "第一条 合同终止\n乙方应返还全部资料，删除所有复制件及备份文件，并向甲方提供书面处置确认。"
    rows = states(text)
    assert all(row["status"] == "COVERED" for row in rows.values()), rows


def test_unrelated_acceptance_confirmation_is_not_disposal_confirmation():
    text = "第一条 合同终止\n乙方应返还全部资料。甲方应书面确认产品验收结果。"
    assert states(text)["material_disposal_confirmation"]["status"] == "MISSING"


def test_owner_filter_does_not_consume_different_owners_material():
    text = "第一条 合同终止\n乙方应删除丙方资料。"
    assert states(text, material_owner="甲方")["material_disposition"]["status"] == "MISSING"


def test_general_electronic_material_deletion_does_not_prove_source_code_deletion():
    text = "第一条 合同终止\n乙方应删除所有电子资料。"
    rows = states(text, object_types=("electronic_material", "source_code", "technical_secret_material"))
    assert rows["electronic_material_disposition"]["status"] == "COVERED"
    assert rows["source_code_disposition"]["status"] == "MISSING"
    assert rows["technical_secret_material_disposition"]["status"] == "MISSING"


def test_fact_identity_is_shared_but_never_merges_actors_or_objects():
    text = "第一条 合同终止\n乙方应返还全部资料。"
    first = states(text)
    second = states(text)
    assert first["material_disposition"]["fact_identity"] == second["material_disposition"]["fact_identity"]
    assert set(first["material_disposition"]["fact_identity"]) == {"canonical_fact_key", "scope", "party", "object"}
    assert first["material_disposition"]["fact_identity"] != states(text, "甲方")["material_disposition"]["fact_identity"]
    assert first["material_disposition"]["fact_identity"] != first["copy_disposition"]["fact_identity"]
    assert first["material_disposition"]["fact_identity"] != states(text, material_owner="甲方")["material_disposition"]["fact_identity"]


def test_coordinated_actions_cannot_reverse_subject_or_expand_objects():
    text = "第一条 合同终止\n乙方应删除电子资料并由甲方返还全部资料。"
    b = states(text)
    a = states(text, "甲方")
    assert b["material_disposition"]["status"] == "PARTIALLY_COVERED"
    assert a["material_disposition"]["status"] == "COVERED"
    facts = extract_scoped_material_disposition_facts(parse_contract_clauses(text))
    assert not any(f["actor"] == "乙方" and f["action"] == "return" for f in facts)
    assert not any(f["actor"] == "甲方" and f["action"] == "delete" for f in facts)


def test_retention_and_return_each_bind_only_their_own_object():
    facts = extract_scoped_material_disposition_facts(parse_contract_clauses(
        "第一条 合同终止\n乙方应返还全部资料并保留全部备份。"))
    assert {(fact["object_type"], fact["action"]) for fact in facts} == {("material", "return"), ("backup", "retain")}
    facts = extract_scoped_material_disposition_facts(parse_contract_clauses(
        "第一条 合同终止\n乙方应返还全部资料并将全部备份保留。"))
    assert {(fact["object_type"], fact["action"]) for fact in facts} == {("material", "return"), ("backup", "retain")}


def test_disposal_cannot_turn_later_financial_confirmation_into_disposal_proof():
    text = "第一条 合同终止\n乙方应删除工作电脑中的电子资料。乙方应书面确认费用结算结果。"
    assert states(text)["material_disposal_confirmation"]["status"] == "MISSING"
    text = "第一条 合同终止\n乙方应删除工作电脑中的电子资料并书面确认费用结算结果。"
    assert states(text)["material_disposal_confirmation"]["status"] == "MISSING"


def test_scope_limited_confirmation_does_not_prove_all_material_confirmation():
    text = "第一条 合同终止\n乙方应删除项目工作电脑中的相关电子资料并向甲方书面确认删除结果。"
    row = states(text)["material_disposal_confirmation"]
    assert row["status"] == "PARTIALLY_COVERED"
    assert row["supporting_evidence"][0]["scope_limited"] is True
    assert "未纳入现有确认范围" in row["residual_gap"]


def test_technical_secret_suffix_and_provider_selected_scope_do_not_cover_all_materials():
    text = "第一条 保密资料\n合同终止后，被许可方应返还或销毁许可方要求返还或销毁的技术秘密资料。"
    facts = extract_scoped_material_disposition_facts(parse_contract_clauses(text))
    assert facts
    assert {fact["object_type"] for fact in facts} == {"technical_secret_material"}
    assert all(fact["scope_limited"] for fact in facts)
    rows = states(text, "被许可方", object_types=("material", "technical_secret_material", "copy", "backup"))
    assert rows["material_disposition"]["status"] == "PARTIALLY_COVERED"
    assert rows["technical_secret_material_disposition"]["status"] == "PARTIALLY_COVERED"
    assert rows["copy_disposition"]["status"] == "MISSING"
    assert rows["backup_disposition"]["status"] == "MISSING"


def test_same_clause_data_reference_retains_exact_holder_owner_and_antecedent():
    text = "第一条 数据\n许可方对被许可方提供的生产数据、销售数据、测试数据及客户资料承担保密义务。合同终止后，许可方可以为科研、成果展示、项目申报、融资及教学目的继续保存并使用相关数据。"
    facts = extract_scoped_material_disposition_facts(parse_contract_clauses(text))
    retained = [fact for fact in facts if fact["action"] == "retain"]
    assert len(retained) == 1, facts
    fact = retained[0]
    assert fact["actor"] == "许可方"
    assert fact["material_owner"] == "被许可方"
    assert fact["object_type"] == "counterparty_data"
    assert "相关数据" in fact["quote"]
    assert "生产数据" not in fact["quote"]
    assert "生产数据" in fact["context_source"]["quote"]
    assert fact["context_source"]["clause_id"] == fact["clause_id"]
    assert not any(fact["object_type"] in {"material", "copy", "backup"} for fact in facts)


def test_data_reference_does_not_invent_missing_antecedent_or_cross_clause():
    absent = "第一条 数据\n合同终止后，许可方可以继续保存相关数据。"
    assert not extract_scoped_material_disposition_facts(parse_contract_clauses(absent))
    separate = "第一条 数据\n许可方对被许可方提供的生产数据承担保密义务。\n第二条 留存\n合同终止后，许可方可以继续保存相关数据。"
    assert not extract_scoped_material_disposition_facts(parse_contract_clauses(separate))


def test_data_reference_cannot_change_holder_or_reuse_different_object_context():
    changed_holder = "第一条 数据\n许可方对被许可方提供的生产数据承担保密义务。合同终止后，被许可方可以继续保存相关数据。"
    assert not extract_scoped_material_disposition_facts(parse_contract_clauses(changed_holder))
    changed_object = "第一条 数据\n许可方对被许可方提供的生产数据承担保密义务。许可方另行收到被许可方提供的源代码。合同终止后，许可方可以继续保存相关数据。"
    assert not extract_scoped_material_disposition_facts(parse_contract_clauses(changed_object))
    negated = "第一条 数据\n许可方未收集被许可方的生产数据。合同终止后，许可方可以继续保存相关数据。"
    assert not extract_scoped_material_disposition_facts(parse_contract_clauses(negated))


def test_owner_filter_accepts_explicit_owner_with_quantity_and_provision_modifiers():
    for material_phrase in ("甲方全部资料", "甲方所有资料", "甲方提供的全部资料", "甲方所提供的所有资料", "甲方其提供的全部资料"):
        rows = states(f"第一条 合同终止\n乙方应返还{material_phrase}。", material_owner="甲方")
        row = rows["material_disposition"]
        assert row["status"] == "COVERED", (material_phrase, row)
        assert all(fact["actor"] == "乙方" and fact["material_owner"] == "甲方" for fact in row["supporting_evidence"])


def test_owner_filter_does_not_erase_or_expand_limited_electronic_deletion():
    text = "第一条 合同终止\n乙方应删除项目工作电脑中的甲方所提供的全部电子资料。"
    row = states(text, material_owner="甲方")["material_disposition"]
    assert row["status"] == "PARTIALLY_COVERED"
    assert row["supporting_evidence"][0]["material_owner"] == "甲方"
    assert row["supporting_evidence"][0]["actor"] == "乙方"
    assert row["supporting_evidence"][0]["scope_limited"] is True
    assert states(text, material_owner="丙方")["material_disposition"]["status"] == "MISSING"


def test_party_request_is_not_itself_ownership_proof():
    text = "第一条 合同终止\n乙方应返还甲方要求返还的全部资料。"
    facts = extract_scoped_material_disposition_facts(parse_contract_clauses(text))
    assert facts and all(fact["material_owner"] == "UNKNOWN" for fact in facts)
    assert states(text, material_owner="甲方")["material_disposition"]["status"] == "MISSING"
