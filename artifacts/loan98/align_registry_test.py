from pathlib import Path
p=Path('backend/tests/test_loan_applicability_and_consistency.py');s=p.read_text(encoding='utf8').replace('<= {"COMMON-23-01"}','<= {"REG-06-01"}');p.write_text(s,encoding='utf8')
