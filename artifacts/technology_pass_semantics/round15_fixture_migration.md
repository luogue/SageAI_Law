# Development upload fixture stabilization

The shared fixture `uploaded_report` in `test_technology_exact_truth_pipeline.py` previously read the mutable UI scratch document `test_data/122 测试2.docx`.

The Round14/full35 input was entrusted development, preserved at `round14_entrusted_input/original.docx`, SHA256 `0d435596e1bfc8def44bef5e7ed67520d2b7fe645a51a5ba5a484686816f2a15`.

The present user input is patent-right transfer, frozen separately at `round15_patent_input/original.docx`, SHA256 `86a5970531a486d6610b6fd5ebe9875d6d86073ccc57462c8ee38781d5594b8e`. TC-05-04 is correctly not applicable to that transaction, so it cannot satisfy the development-exit fixture's PARTIAL assertion.

Changed only the shared fixture path back to the preserved development input. No assertions changed, no tests removed/skipped, and the new patent upload remains independently tested. This is one fixture migration affecting two test consumers, not an implementation recovery:

- test_production_route_confidentiality_truth_is_covered
- test_production_route_exit_has_exact_positive_and_separate_absence

After migration the exit regression passes. The confidentiality assertion remains a pre-existing failure, as in full35; the incidental apparent recovery on a different patent input is not counted as a historical repair.
