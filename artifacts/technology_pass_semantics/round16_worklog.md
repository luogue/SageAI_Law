# Round16 verified patent transfer roles and conditions

Frozen input: `round16_patent_input/original.docx`, SHA256 `96e835caf28d80698e3b550631d2c657ac3611ba5e587b9e6bf8fe45a1b5a732`.
Baseline: full42, 965 PASS / 249 FAIL. The prior patent input remains a separate protection sample.

## Reproduction

Normal `/review-v2/file` upload, via the UI proxy, user identity 乙方, contract_type technology, use_llm false. `round16_before/report.json` has one original blocker / one expanded detail:

- EXACT_ELEMENT_REPORT_INVARIANT / Final Evidence Projection / TC-11-01 / technical_secret_applicability / INVALID_ABSENCE_SEARCH_TARGET / search_targets empty. No fact ID was supplied by this refusal object.

The reported title guarantee and refund mistakes were also reproduced, but were not the original Gate object. TC-12-01 was falsely PASS using knowledge/concealment-conditioned damages to cover broader no-fault compliant-use liability.

## First departures and changes

1. Perspective display constants hardcoded A as transferee and B as transferor. The role identity and party label are now combined only after resolving the actual declared role. Licence labels match longest first, so 被许可方 cannot match 许可方.
2. Patent disposition representation extraction lost the common list subject. Preserve the explicit guarantee header and exact continuous source through the assertion; stop inheritance at a new explicit party. Do not fabricate a concatenated quotation or transfer another party's representation.
3. Recipient's express right to demand a provider refund was not consumed as a refund remedy. It now yields the same remedy fact while retaining the whole conditional source.
4. Shared claim facts discarded knowledge/fault restrictions. Preserve condition and limited attributes; expose the explicit fault condition separately from the existence of a damages allocation. A limited fact cannot cover the broader compliant-use requirement.
5. Non-public technical-material scope was omitted from applicability despite express secrecy qualification. Recognize the directly qualified technical object, not ordinary technical documents alone.
6. Fact-selected exact excerpts were not propagated to the report candidates. `_attach_evidence_traceability` now carries explicit element sources through parser-owned binding. The semantic verifier still approves or rejects each candidate. Claim projection uses only sources owned by its elements, not all remedies in the claim theme.
7. A future invalidity disclaimer was treated as a current disclosure. Exclude that different proposition; do not restore it merely to maintain PASS.

Modified modules: perspective_resolution.py, technology_patent_transfer_analysis.py, technology_service_analysis.py, engine.py. New tests: test_transfer_verified_roles_and_conditions.py (9 cases, including normal upload and full Gate). No assertion migration or skipped/deleted tests.

## Validation checkpoints

- New tests: 9/9 PASS.
- Earlier related run: 86 PASS / 6 FAIL; all six failures existed in full42.
- `round16_after2/report.json`: REPORT_READY, zero blockers; title guarantee and refund COVERED, TC-12-01 PARTIAL with retained fault condition, correct 乙方 / 专利权受让方 display.
- Intermediate full43 batch0 was stopped after the final list-subject boundary protection was added. It is not a completed regression result.
- Final full44 completed: batch0 669 PASS / 142 FAIL; batch1 305 PASS / 107 FAIL; total **974 PASS / 249 FAIL / 0 SKIP**.
- Compared by test ID with full42: 9 added tests all PASS; zero historical status changes; zero newly failing; zero removed. No test migrations. The 249 historical failures are not claimed resolved.
- Final-version uploads: `round16_final_replay/report.json` (乙方 / 专利权受让方) and `round16_final_transferor/report.json` (甲方 / 专利权让与方) both REPORT_READY, zero original / expanded blockers. Reported engine hash matches the final file hash.
- All nine available protections REPORT_READY: entrusted development, prior patent transfer, cooperative development, cross-article confidentiality, patent licence, consulting, provider cap, balanced confidentiality and ancillary secret transfer. Their risk-group sets match Round15 exactly (13, 7, 11, 13, 13, 4, 6, 15, 19 respectively). See `round16_final2_live_manifest.json` plus the entrusted/prior-patent output directories.
- Evidence/state changes: TC-06-03 remains PARTIAL but title/authority is now COVERED; TC-12-01 PASS becomes PARTIAL with explicit fault condition; TC-12-02 remains PARTIAL but refund_remedy is now COVERED. TC-11-01 is PASS with exact confidentiality scope/duty sources, resolving the original applicability/projection blocker.
- Final comparison: `round16_final_comparison.json`. Module hashes were rechecked after both batches completed.

Final backend PID 304. Engine hash `ac22e335ff9042d088d011a722cbc11d7b21085dac5e491f066fbcc6b231f478`; patent analysis `74368d05a23af77508852593507e86ea950cef582c4a5f2d518acdb884105fb3`; service analysis `dcf9f4f75ad88c6130f49e563b0e0e8ed464d0ae15eed198b853e4bc000e3229`; perspective `8322cd543945d04f0550929a95a6d084dbc9df6e595fe6909cf4f92e440195fe`.
