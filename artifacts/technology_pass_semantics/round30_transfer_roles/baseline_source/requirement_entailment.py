"""Text-level support for requirements whose topic alone is not evidence.

These predicates inspect the quoted source, never a renderer's assigned tag.
They describe what a source can prove, not whether the whole rule passes.
"""
import re


SECRET_IDENTITY_REQUIREMENT = "technical_secret_identity_and_delivery_scope"


def technical_secret_identity_support(text):
    """Return the actual identity/scope facts stated in this source span.

    A grant, restriction, liability or historical licence that merely says
    'this technical secret' does not identify it or list its deliverables.
    """
    compact = re.sub(r"\s+", "", str(text or ""))
    facts = {}
    for sentence in re.split(r"[。；;]", compact):
        named = re.search(r"(?:技术秘密|专有技术|合同技术)(?:的)?名称[：:为]+([^，。；]{2,100})", sentence)
        if named and not re.search(r"^(?:未|尚未|待|另行|[_＿—-]+$)", named[1]):
            facts["identity_name"] = "技术秘密或专有技术名称有明确记载"
        possession = re.search(r"(?:拥有|持有|提供|许可(?!方|人)|转让(?!方|人))([^，。；]{3,50}?)(?:专有技术|技术秘密)", sentence)
        if possession and not re.search(r"本项|本合同|上述|相关|有权|第三方|保证|禁止|擅自|不得|违反|同意|所需|必要", possession[0]):
            facts["identity_name"] = "技术秘密或专有技术名称有明确记载"
        content = re.search(
            r"(?:技术秘密|专有技术|技术资料|许可技术)[”\"’']?(?:的)?(?:内容|范围|边界|主要包括|包括|是指|系指|指的是)"
            r"[：:为是]*([^。；]{3,200})", sentence,
        )
        if content and not re.search(r"^(?:未|尚未|不明确|待|另行|不足|不完整)", content[1]):
            facts["technical_scope"] = "技术秘密内容或技术资料范围有明确记载"
        if re.search(r"技术秘密|专有技术|合同技术", sentence) and re.search(
            r"(?:范围为|技术边界为|范围包括)[^。；]{3,120}", sentence,
        ):
            facts["technical_scope"] = "技术秘密内容或技术资料范围有明确记载"
        # A named deliverable or schedule is a delivery fact, not proof of all
        # the other identity fields. Payment references stay weaker than scope.
        if re.search(r"技术资料(?:交付|交接)清单|技术秘密(?:资料)?清单|技术秘密说明书|算法及源代码交付清单", sentence):
            if not re.search(r"(?:未|没有|尚未|无需|不提供).{0,12}(?:清单|说明书)", sentence):
                facts["delivery_content"] = "技术资料清单或技术秘密说明文件已列明"
    return facts
