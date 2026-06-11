def abstract(problem):
    return f"问题本质: {problem}"

def main_contradiction(problem):
    return f"主要矛盾: {problem}"

def boundary(problem):
    return f"问题边界: {problem}"

def verify(conclusion, problem):
    return f"验证结果: 结论 '{conclusion}' 与问题 '{problem}' 一致"

def classify_intent(problem):
    intent_keywords = {
        "路径规划": {
            "keywords": ["怎么学", "怎么规划", "顺序", "系统学习", "零基础", "规划", "时间"],
            "examples": [
                "我想转行做后端开发，零基础该怎么学？",
                "我想考雅思7分，3个月时间怎么规划？",
                "我想系统学习马克思主义政治经济学，应该按照什么顺序去读？"
            ]
        },
        "概念理解与抽象": {
            "keywords": ["是什么", "什么意思", "区别", "大白话", "通俗", "怎么理解"],
            "examples": [
                "能不能用大白话给我讲讲什么是Transformer架构？",
                "量子纠缠到底是怎么回事？",
                "过拟合和欠拟合到底怎么理解？"
            ]
        },
        "资源与工具推荐": {
            "keywords": ["推荐", "有哪些", "有没有", "工具", "软件", "APP", "教程", "书"],
            "examples": [
                "有哪些适合新手练手的开源项目？",
                "学剪辑有没有什么靠谱的免费教程推荐？",
                "手机有没有好用的APP可以查阅原著？"
            ]
        },
        "瓶颈突破与反馈": {
            "keywords": ["怎么解决", "为什么", "老是", "总是", "挂", "坚持不过", "不下去", "脱节"],
            "examples": [
                "我代码都能看懂，但自己一写就废，这是为什么？",
                "背了单词老是忘，是不是我记忆方法有问题？",
                "Loss曲线一直震荡不下降，可能是什么原因？"
            ]
        },
        "执行监督与动力": {
            "keywords": ["不想", "坚持", "打卡", "提醒", "分心", "动力", "焦虑", "怎么破"],
            "examples": [
                "我今天又不想学习了，怎么破？",
                "帮我制定一个每天2小时的打卡计划",
                "最近学不进去，总是分心怎么办？"
            ]
        },
        "效果评估与诊断": {
            "keywords": ["考考我", "看看", "怎么样", "评估", "诊断", "进度", "多久", "对不对"],
            "examples": [
                "我刚学完MySQL，你能出几道题考考我吗？",
                "帮我看看这段代码写得怎么样？",
                "按照我现在的进度，大概多久能达到入职水平？"
            ]
        },
        "跨域融合与实战": {
            "keywords": ["怎么用", "结合起来", "结合", "跨", "分析", "项目", "落地", "辅助"],
            "examples": [
                "我学了Python，但不知道怎么用它来分析销售数据",
                "我是做HR的，想学点心理学知识来辅助面试",
                "我想用NLP技术去分析古代哲学文献"
            ]
        }
    }

    problem_lower = problem.lower()

    for intent, data in intent_keywords.items():
        for keyword in data["keywords"]:
            if keyword in problem_lower:
                return intent, f"识别到关键词: {keyword}"

    return "未分类", "未能识别问题类型，请尝试重新描述问题"

def classify_domain(problem):
    domain_keywords = {
        "金融": ["投资", "股票", "基金", "债券", "理财", "财务", "通胀", "货币", "银行", "保险", "审计", "财报", "估值"],
        "法律": ["法律", "法规", "合同", "诉讼", "判决", "案例", "条文", "条款", "违法", "犯罪", "侵权", "辩护", "仲裁"],
        "教育": ["学习", "考试", "课程", "教学", "培训", "学校", "大学", "学历", "成绩", "作业", "课堂", "老师", "学生", "雅思", "托福"],
        "工程": ["代码", "编程", "开发", "架构", "算法", "软件", "硬件", "电路", "机械", "建筑", "施工", "项目", "测试", "部署"],
        "社科": ["社会", "政治", "哲学", "历史", "文化", "心理", "伦理", "社会学", "人类学", "政治学", "马克思主义", "社会学"],
        "医疗": ["疾病", "治疗", "药物", "医生", "医院", "诊断", "症状", "健康", "医学", "临床", "手术", "疫苗"],
        "商业": ["营销", "运营", "管理", "战略", "市场", "客户", "产品", "销售", "品牌", "电商", "商业模式"],
        "自然科学": ["物理", "化学", "生物", "数学", "量子", "相对论", "基因", "细胞", "分子", "天文"]
    }

    problem_lower = problem.lower()
    matched_domains = []

    for domain, keywords in domain_keywords.items():
        for keyword in keywords:
            if keyword in problem_lower:
                if domain not in matched_domains:
                    matched_domains.append(domain)

    if matched_domains:
        return matched_domains[0], f"识别到领域关键词"

    return "通用", "未能明确领域，按通用问题处理"