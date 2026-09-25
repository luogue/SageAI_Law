"""Canonical wording for a licence mode, shared by fact consumers."""
import re
from review_v2.proposition_scope import arrangement_matches

LICENSE_TYPE_PATTERN = r'(?:非独占|普通|(?<!非)独占|排他)(?:、[^,，。；;]{0,16})?(?:的)?(?:专利)?(?:实施|使用)?许可'


def declared_license_type(text):
    if re.search(r'既有许可|曾(?:于|向)|许可他人|后续改进|改进成果', text):
        return False
    if re.search(LICENSE_TYPE_PATTERN + r'[—－\-：:]*(?:是?指|定义)', text):
        return False
    return any(arrangement_matches(LICENSE_TYPE_PATTERN, text))
