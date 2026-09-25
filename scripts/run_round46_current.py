"""Round46 真实接口验收：对 33 技术咨询合同跑 /review-v2/file 双立场。

不覆盖旧证据：输出到 artifacts/technology_pass_semantics/round46_consulting_generalization/
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import requests

ROOT = Path(r"F:/ai/Sage")
OUT = ROOT / "artifacts" / "technology_pass_semantics" / "round46_consulting_generalization"
INPUT = OUT / "input.docx"
URL = "http://127.0.0.1:8016/review-v2/file"
PY = sys.executable


def make_token() -> str:
    code = ("from dotenv import load_dotenv; load_dotenv('backend/.env'); "
            "from auth.utils import create_access_token; "
            "print(create_access_token({'user_id':'1'}))")
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "backend") + os.pathsep + str(ROOT)
    res = subprocess.run([PY, "-X", "utf8", "-c", code], cwd=str(ROOT), env=env,
                         capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0 or not res.stdout.strip():
        raise RuntimeError(f"token 生成失败: {res.stderr[:300]}")
    return res.stdout.strip().splitlines()[-1].strip()


def run(party: str, token: str):
    with open(INPUT, "rb") as fh:
        files = {"file": ("input.docx", fh.read(),
                          "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    data = {
        "contract_type": "technology",
        "use_llm": "true",
        "include_low_risk": "true",
        "profile_json": json.dumps({"user_identity": party}, ensure_ascii=False),
    }
    resp = requests.post(URL, headers={"Authorization": f"Bearer {token}"},
                         files=files, data=data, timeout=900)
    resp.raise_for_status()
    return resp.json()


def main():
    token = make_token()
    summary = {}
    for slug, party in (("party_a", "甲方"), ("party_b", "乙方")):
        print(f"--- {party} 请求中...")
        result = run(party, token)
        dest = OUT / f"final_{slug}"
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "report.json").write_text(
            json.dumps(result, ensure_ascii=False), encoding="utf-8")
        (dest / "report.md").write_text(result.get("result", ""), encoding="utf-8")
        gate = result.get("release_quality_gate", {})
        summary[slug] = {
            "review_run_id": result.get("review_run_id"),
            "review_task_id": result.get("review_task_id"),
            "gate": gate.get("status"),
            "failures": len(gate.get("failures") or []),
        }
        print(f"    {party} HTTP=200 gate={gate.get('status')} "
              f"run={result.get('review_run_id')}")
    (OUT / "acceptance.json").write_text(
        json.dumps({"round": "Round46", "runs": summary}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print("acceptance 写入:", OUT / "acceptance.json")


if __name__ == "__main__":
    main()
