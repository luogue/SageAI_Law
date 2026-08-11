"""Tests for legacy contract review fallback behavior."""

import asyncio

import main
from reasoning.llm_client import AllModelsFailedError
from tasks import TaskStatus, create_task, get_task


def test_legacy_batch_review_completes_with_fallback_when_all_models_fail(monkeypatch):
    async def fake_run_inference_with_progress(*args, **kwargs):
        raise AllModelsFailedError()

    monkeypatch.setattr(main, "run_inference_with_progress", fake_run_inference_with_progress)

    contract_text = (
        "房屋租赁合同\n"
        "甲方将位于上海市浦东新区的房屋出租给乙方居住使用，租期一年。"
        "租金每月三千元，押金三千元，乙方应按期支付租金并合理使用房屋。"
        "合同期满后双方办理交接并结清水电费用。"
        "甲方应保证房屋具备基本居住条件，乙方不得擅自改变房屋用途。"
        "双方发生争议时，应先友好协商；协商不成的，可依法向有管辖权的人民法院起诉。"
    )
    task = create_task("fallback-contract.txt", len(contract_text.encode("utf-8")))

    asyncio.run(
        main.process_contract_task(
            task.task_id,
            contract_text.encode("utf-8"),
            "fallback-contract.txt",
            "",
            file_hash=None,
        )
    )

    finished = get_task(task.task_id)
    assert finished is not None
    assert finished.status == TaskStatus.COMPLETED
    assert finished.progress == 100
    assert finished.error is None
    assert "合同审查报告（降级模式）" in finished.result
    assert "大模型服务暂时不可用" in finished.result
    assert finished.metadata["degraded"] is True
    assert finished.remaining_bonus is None
    assert finished.record_id is None
