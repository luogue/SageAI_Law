"""测试：检查 additional_instructions 被哪个规则拦截"""
import re

text = """明确承包人优先受偿权可通过向执行法院提交书面函件等方式行使，不限于诉讼或仲裁。

合同中应约定优先受偿权6个月期限自发包人应付工程款之日起算，并确保及时主张权利，避免超期失权。"""

INJECTION_PATTERNS = [
    r"忽略.*?(所有|之前|上述|以下|一切|全部|系统).*?(指令|规则|要求|指示|设定|提示词|prompt)",
    r"忘记.*?(所有|之前|上述|系统|你的).*?(指令|规则|要求|提示词|设定)",
    r"无视.*?(上面|上述|之前|系统|指令|规则)",
    r"跳过.*?(规则|指令|限制|检测|检查)",
    r"不要.*?(遵守|执行|听从|理会|跟从).*?(指令|规则|要求|指示)",
    r"从现在开始.*?(作为|你是|你的身份是)",
    r"disregard.*?(all|previous|above).*?(instructions?|rules?|prompts?)",
    r"ignore.*?(all|previous|above|system).*?(instructions?|rules?|prompts?)",
    r"forget.*?(all|your|previous|above).*?(instructions?|rules?|prompts?)",
    r"do not.*?(follow|obey|comply).*?(instructions?|rules?|prompts?)",
    r"don't.*?(follow|obey|comply|listen).*?(instructions?|rules?)",
    r"override.*?(system|instructions?|prompts?)",
    r"you are.*?(no longer|not).*?(an?|the).*?(assistant|AI|bot)",
    r"you are now.*?(free|unrestricted|a different)",
    r"start.*?(fresh|over|new).*?(ignore|forget)",
    r"输出.*?(你的|系统|内部|原始|初始).*?(指令|提示词|prompt|设定|配置|规则)",
    r"打印.*?(你的|系统|内部|原始).*?(指令|提示词|prompt|设定|规则)",
    r"展示.*?(你的|系统|内部).*?(指令|提示词|prompt|设定)",
    r"显示.*?(你的|系统|内部).*?(指令|提示词|prompt)",
    r"告诉.*?我.*?(你的|系统|内部).*?(指令|提示词|prompt|设定|规则)",
    r"泄露.*?(你的|系统).*?(指令|提示词|prompt)",
    r"print.*?(your|system|internal|original).*?(instructions?|prompts?|settings?|rules?|config)",
    r"show.*?(your|system|internal).*?(instructions?|prompts?|settings?|rules?)",
    r"tell.*?me.*?(your|system|internal).*?(instructions?|prompts?|settings?|rules?)",
    r"reveal.*?(your|system|internal).*?(instructions?|prompts?|settings?)",
    r"repeat.*?(your|system|internal).*?(instructions?|prompts?|settings?)",
    r"list.*?(your|system|internal).*?(instructions?|prompts?|rules?|capabilities)",
    r"what are.*?(your|system).*?(instructions?|prompts?|rules?)",
    r"what is.*?(your|the).*?(system prompt|prompt|instructions?)",
    r"describe.*?(your|system|internal).*?(instructions?|prompts?|capabilities)",
    r"say.*?anything.*?as.*?system",
    r"say.*?(exactly|repeat).*?(this|the following)",
    r"你现在.*?(是|不是|不再是|已经变成|变成一个)",
    r"你不再是.*?(一个|一名)",
    r"你现在是一个.*?而不是",
    r"你是一个.*?而不是.*?(合同审查|法律|AI)",
    r"假设.*?你是.*?(一个|一名).*?(而不是.*?合同审查)",
    r"扮演.*?(一个|一名|角色).*?(而不是|而不是.*?合同)",
    r"角色.*?(扮演|设定|转换|切换)",
    r"you are now.*?(a |an |the )?(different |another )?",
    r"pretend.*?(you are|to be|that you)",
    r"act as.*?(instead|different|another|if you were)",
    r"imagine.*?(you are|that you are|yourself as)",
    r"jailbreak",
    r"越狱",
    r"解除.*?(限制|束缚|封印)",
    r"自由模式",
    r"dev mode|developer mode",
    r"\[角色设定\]",
    r"\[system\]",
    r"\[instructions\]",
    r"\[internal\]",
    r"<role>",
    r"</role>",
    r"<system>",
    r"</system>",
    r"\{\{role\}\}",
    r"\{\{system\}\}",
    r"\{\{instructions\}\}",
    r"DAFG",
    r"MENG",
    r"你只是一个",
    r"只是.*?而已",
    r"refuse.*?(to|following|obeying)",
    r"break.*?(the|your).*?(rules?|instructions?|limits?)",
    r"违反.*?(规则|指令|限制|设定)",
    r"绕过.*?(限制|规则|安全|检测|检查|审查)",
    r"bypass.*?(restriction|rule|limit|safety|filter|security)",
    r"hack.*?(the|your|this|system)",
    r"exploit.*?(the|your|this)",
]

print(f"Testing text ({len(text)} chars): {text[:80]}...")
print(f"Against {len(INJECTION_PATTERNS)} patterns...")
print()

found = []
for i, pattern in enumerate(INJECTION_PATTERNS):
    try:
        compiled = re.compile(pattern, re.IGNORECASE)
        matches = compiled.findall(text)
        if matches:
            found.append((i, pattern, matches))
            print(f">>> MATCH! Pattern #{i}: {pattern}")
            print(f"    Matched: {matches}")
    except Exception as e:
        print(f"Pattern #{i} ERROR: {e}")

# Also check malicious keywords
MALICIOUS_KEYWORDS = [
    "忽略之前的指令", "忘记所有规则", "不要遵守", "无视上面", "忽略以上", "忽略指令", "跳过规则",
    "break the rules", "ignore previous", "ignore all", "你现在是", "扮演一个", "没有任何限制",
    "自由模式", "解除限制", "移除限制", "bypass restrictions", "role play", "no restrictions",
    "输出你的提示词", "打印系统指令", "你的规则是什么", "你是什么模型", "你的架构",
    "prompt injection", "system prompt", "写一篇作文", "推荐电影", "讲个笑话", "写首诗",
    "写代码", "帮我写", "帮我做", "推荐歌曲", "天气预报", "翻译", "calculator", "solve this",
    "write an essay", "tell me a joke"
]

print()
print("=== Checking malicious keywords ===")
text_lower = text.lower()
kw_found = []
for kw in MALICIOUS_KEYWORDS:
    if kw.lower() in text_lower:
        kw_found.append(kw)
        print(f">>> KEYWORD MATCH: {kw}")

if not found and not kw_found:
    print("NO MATCHES FOUND - text would pass all checks")
else:
    print(f"\nTotal: {len(found)} pattern matches, {len(kw_found)} keyword matches")
