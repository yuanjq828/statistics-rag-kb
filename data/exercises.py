"""课后练习数据"""

EXERCISES = [
    # ===== 基础概念 =====
    {
        "id": "ex_001",
        "question": "以下哪个是描述统计的范畴？",
        "options": [
            "A. 用样本均值推断总体均值",
            "B. 计算一组数据的标准差",
            "C. 检验两组数据的差异是否显著",
            "D. 构建置信区间"
        ],
        "answer": "B",
        "explanation": "描述统计关注数据的整理、汇总和描述，计算标准差属于描述统计。A、C、D都属于推断统计的范畴。",
        "category": "choice",
        "difficulty": 1,
        "concepts": ["descriptive_stats", "inferential_stats"],
        "hint": '区分描述统计和推断统计的关键在于是否涉及"推断"'
    },
    {
        "id": "ex_002",
        "question": "推断统计的核心目的是什么？",
        "options": [
            "A. 整理和汇总数据",
            "B. 制作统计图表",
            "C. 利用样本信息推断总体特征",
            "D. 计算均值和中位数"
        ],
        "answer": "C",
        "explanation": "推断统计的核心是利用样本数据对总体特征进行推断，包括参数估计和假设检验。",
        "category": "choice",
        "difficulty": 1,
        "concepts": ["inferential_stats"],
        "hint": ""
    },

    # ===== 集中趋势 =====
    {
        "id": "ex_003",
        "question": "一组数据：2, 4, 6, 8, 100，这组数据的均值是？",
        "options": [
            "A. 6",
            "B. 24",
            "C. 100",
            "D. 8"
        ],
        "answer": "B",
        "explanation": "均值 = (2+4+6+8+100)/5 = 120/5 = 24。可以看出均值受极端值(100)的影响很大。",
        "category": "choice",
        "difficulty": 1,
        "concepts": ["mean"],
        "hint": "均值是所有数值加总后除以个数"
    },
    {
        "id": "ex_004",
        "question": "上题数据的中位数是？",
        "options": [
            "A. 2",
            "B. 6",
            "C. 8",
            "D. 24"
        ],
        "answer": "B",
        "explanation": "排序后为 2, 4, 6, 8, 100，中间位置是第3个数，即6。中位数不受极端值100的影响。",
        "category": "choice",
        "difficulty": 1,
        "concepts": ["median"],
        "hint": "先排序，再找中间位置的值"
    },
    {
        "id": "ex_005",
        "question": "对于偏态分布的数据，以下哪个集中趋势度量更合适？",
        "options": [
            "A. 均值",
            "B. 中位数",
            "C. 众数",
            "D. 方差"
        ],
        "answer": "B",
        "explanation": "中位数不受极端值影响，对于偏态分布（如收入分布），中位数比均值更能代表「典型「水平。",
        "category": "choice",
        "difficulty": 2,
        "concepts": ["mean", "median"],
        "hint": "哪个指标抗异常值干扰能力强？"
    },
    {
        "id": "ex_006",
        "question": "某鞋店一周内售出的鞋码为：38, 38, 39, 39, 39, 39, 40, 40, 41。这组数据的众数是？",
        "options": [
            "A. 38",
            "B. 39",
            "C. 40",
            "D. 不存在"
        ],
        "answer": "B",
        "explanation": "39出现了4次，出现频率最高。众数反映的是最「流行「的数值。",
        "category": "choice",
        "difficulty": 1,
        "concepts": ["mode"],
        "hint": "众数就是出现次数最多的数"
    },

    # ===== 离散程度 =====
    {
        "id": "ex_007",
        "question": "两组数据的均值相同，但标准差不同。标准差较大的组意味着什么？",
        "options": [
            "A. 数据更集中",
            "B. 数据更分散",
            "C. 数据量更大",
            "D. 数据更准确"
        ],
        "answer": "B",
        "explanation": "标准差衡量数据的离散程度。标准差越大，说明数据点偏离均值的程度越大，数据越分散。",
        "category": "choice",
        "difficulty": 1,
        "concepts": ["std_dev"],
        "hint": "标准差是「平均偏离程度「"
    },
    {
        "id": "ex_008",
        "question": "如果一组数据的方差为25，那么标准差是多少？",
        "options": [
            "A. 5",
            "B. 25",
            "C. 625",
            "D. 12.5"
        ],
        "answer": "A",
        "explanation": "标准差 = √方差 = √25 = 5。标准差的单位与原始数据相同，更易解释。",
        "category": "choice",
        "difficulty": 1,
        "concepts": ["std_dev", "variance"],
        "hint": "标准差是方差的平方根"
    },
    {
        "id": "ex_009",
        "question": "在正态分布中，约95%的数据落在均值±多少个标准差的范围内？",
        "options": [
            "A. 1个标准差",
            "B. 2个标准差",
            "C. 3个标准差",
            "D. 1.5个标准差"
        ],
        "answer": "B",
        "explanation": "根据68-95-99.7法则，约95%的数据落在均值±2个标准差的范围内（更精确地说，是±1.96个标准差）。",
        "category": "choice",
        "difficulty": 2,
        "concepts": ["normal_distribution", "std_dev"],
        "hint": "回忆68-95-99.7法则"
    },
    {
        "id": "ex_010",
        "question": "某班考试成绩均值70分，标准差10分。一名学生考了85分，他的Z分数是多少？",
        "options": [
            "A. 0.5",
            "B. 1.0",
            "C. 1.5",
            "D. 2.0"
        ],
        "answer": "C",
        "explanation": "Z = (85-70)/10 = 1.5，说明该生成绩高于均值1.5个标准差。",
        "category": "choice",
        "difficulty": 2,
        "concepts": ["z_score", "mean", "std_dev"],
        "hint": "Z = (x - μ)/σ"
    },

    # ===== 概率 =====
    {
        "id": "ex_011",
        "question": "掷一枚均匀的骰子，出现偶数点的概率是？",
        "options": [
            "A. 1/6",
            "B. 1/3",
            "C. 1/2",
            "D. 2/3"
        ],
        "answer": "C",
        "explanation": "骰子的偶数点有2,4,6共3种，总可能结果6种，P(偶数)=3/6=1/2。",
        "category": "choice",
        "difficulty": 1,
        "concepts": ["probability"],
        "hint": "概率 = 有利结果数/总可能结果数"
    },
    {
        "id": "ex_012",
        "question": "某疾病检测的准确率为99%，该疾病的患病率为1%。某人检测结果为阳性，他真正患病的概率约为多少？（假设假阳性率为1%）",
        "options": [
            "A. 99%",
            "B. 50%",
            "C. 1%",
            "D. 90%"
        ],
        "answer": "B",
        "explanation": "使用贝叶斯定理：P(病|+) = (0.99×0.01)/(0.99×0.01+0.01×0.99) ≈ 0.5 = 50%。这就是「基率谬误「的典型案例。",
        "category": "choice",
        "difficulty": 3,
        "concepts": ["bayes", "probability"],
        "hint": "先验概率很低时，即使检测准确率高，阳性结果的真阳性概率也可能不高"
    },

    # ===== 假设检验 =====
    {
        "id": "ex_013",
        "question": "在假设检验中，p值为0.03意味着什么？",
        "options": [
            "A. 原假设为真的概率是3%",
            "B. 备择假设为真的概率是97%",
            "C. 在原假设成立下，观察到当前或更极端结果的概率是3%",
            "D. 犯第二类错误的概率是3%"
        ],
        "answer": "C",
        "explanation": "p值的准确定义是：在原假设H₀成立的前提下，观察到当前样本结果或更极端结果的概率。p<0.05通常被认为具有统计显著性。",
        "category": "choice",
        "difficulty": 3,
        "concepts": ["p_value", "hypothesis_testing"],
        "hint": "p值不是原假设成立的概率！"
    },
    {
        "id": "ex_014",
        "question": "显著性水平α=0.05，p=0.07时，正确的结论是？",
        "options": [
            "A. 拒绝H₀，差异显著",
            "B. 接受H₀，没有差异",
            "C. 不拒绝H₀，没有足够证据证明差异显著",
            "D. 需要重新抽样"
        ],
        "answer": "C",
        "explanation": "p=0.07 > α=0.05，因此不能拒绝原假设。注意：不拒绝H₀不等于接受H₀，只是说明没有足够证据拒绝它。",
        "category": "choice",
        "difficulty": 3,
        "concepts": ["hypothesis_testing", "p_value"],
        "hint": "p > α 时不能拒绝原假设"
    },
    {
        "id": "ex_015",
        "question": "第一类错误（Type I Error）是指？",
        "options": [
            "A. 拒绝了一个真的原假设",
            "B. 接受了一个假的原假设",
            "C. 样本量太小",
            "D. 数据不符合正态分布"
        ],
        "answer": "A",
        "explanation": "第一类错误（假阳性）是错误地拒绝了一个本来为真的原假设。其概率由显著性水平α控制。",
        "category": "choice",
        "difficulty": 2,
        "concepts": ["type_error", "hypothesis_testing"],
        "hint": "宁可错杀一千（Type I）还是宁可放过一个（Type II）？"
    },

    # ===== t检验与相关分析 =====
    {
        "id": "ex_016",
        "question": "比较两种教学方法的效果，将学生随机分为两组，分别接受不同教学法后进行测试。应该使用哪种统计方法？",
        "options": [
            "A. 单样本t检验",
            "B. 独立样本t检验",
            "C. 配对样本t检验",
            "D. 卡方检验"
        ],
        "answer": "B",
        "explanation": "两组是独立的（不同的学生），比较均值差异，使用独立样本t检验。如果是同一组学生前后比较，则用配对t检验。",
        "category": "choice",
        "difficulty": 3,
        "concepts": ["t_test", "hypothesis_testing"],
        "hint": "两组数据是否来自同一批人？"
    },
    {
        "id": "ex_017",
        "question": "相关系数r=-0.85表示什么？",
        "options": [
            "A. 很强的正相关",
            "B. 很弱的负相关",
            "C. 很强的负相关",
            "D. 没有相关关系"
        ],
        "answer": "C",
        "explanation": "r=-0.85接近-1，表示很强的负相关关系——一个变量增大时，另一个变量显著减小。",
        "category": "choice",
        "difficulty": 2,
        "concepts": ["correlation"],
        "hint": "|r|越接近1，相关越强；正负号表示方向"
    },
    {
        "id": "ex_018",
        "question": "两个变量相关系数r=0.6，这意味着？",
        "options": [
            "A. 一个变量60%的变化由另一个变量引起",
            "B. 两个变量存在中等程度的正相关",
            "C. 两个变量之间没有因果关系",
            "D. 两个变量完全独立"
        ],
        "answer": "B",
        "explanation": "r=0.6表示中等偏强的正相关。相关不等于因果（A选项错误），但也不等于独立（D错误）。",
        "category": "choice",
        "difficulty": 2,
        "concepts": ["correlation", "regression"],
        "hint": "回顾相关强度的划分标准"
    },

    # ===== 综合应用题 =====
    {
        "id": "ex_019",
        "question": "一个95%的置信区间为 [50, 60]，正确的解释是？",
        "options": [
            "A. 总体均值有95%的概率落在50到60之间",
            "B. 样本均值有95%的概率落在50到60之间",
            "C. 如果重复抽样很多次，约95%的置信区间会包含总体均值",
            "D. 数据中95%的数值落在50到60之间"
        ],
        "answer": "C",
        "explanation": "置信区间的正确频率学派解释是：重复抽样多次，约95%的置信区间会包含总体真实值。它不是一个概率陈述。",
        "category": "choice",
        "difficulty": 3,
        "concepts": ["confidence_interval", "inferential_stats"],
        "hint": "置信区间是关于「方法「的可靠性，而不是关于具体区间的概率"
    },
    {
        "id": "ex_020",
        "question": "中心极限定理告诉我们：当样本量足够大时，样本均值的分布近似服从？",
        "options": [
            "A. 与总体分布相同的分布",
            "B. t分布",
            "C. 正态分布",
            "D. 卡方分布"
        ],
        "answer": "C",
        "explanation": "中心极限定理指出：无论总体分布形态如何，当样本量足够大时，样本均值的抽样分布趋近于正态分布。",
        "category": "choice",
        "difficulty": 2,
        "concepts": ["central_limit_theorem", "normal_distribution"],
        "hint": "CLT是统计学的「魔法「"
    },
    {
        "id": "ex_021",
        "question": "比较三种及以上组别的均值差异，应使用什么方法？",
        "options": [
            "A. 多次进行t检验",
            "B. 方差分析(ANOVA)",
            "C. 卡方检验",
            "D. 相关分析"
        ],
        "answer": "B",
        "explanation": "比较三组及以上均值差异应使用方差分析(ANOVA)。多次进行t检验会增加第一类错误的概率。",
        "category": "choice",
        "difficulty": 2,
        "concepts": ["anova", "t_test"],
        "hint": "多组比较不能用多次t检验，会累积误差"
    },
    {
        "id": "ex_022",
        "question": "在回归分析中，R²=0.64的含义是？",
        "options": [
            "A. 自变量解释了64%的因变量变异",
            "B. 因变量解释了64%的自变量变异",
            "C. 预测准确率为64%",
            "D. 64%的数据点落在回归线上"
        ],
        "answer": "A",
        "explanation": "R²（决定系数）表示回归模型能解释因变量变异的比例。R²=0.64意味着自变量能解释64%的因变量变化。",
        "category": "choice",
        "difficulty": 3,
        "concepts": ["r_squared", "regression"],
        "hint": "R²衡量的是「解释程度「"
    },
    {
        "id": "ex_023",
        "question": "已知X和Y的协方差为6，X的标准差为2，Y的标准差为3，X和Y的相关系数是？",
        "options": [
            "A. 0.5",
            "B. 1.0",
            "C. 0.8",
            "D. 0.6"
        ],
        "answer": "B",
        "explanation": "r = Cov(X,Y)/(σ_X×σ_Y) = 6/(2×3) = 1。这表示X和Y完全正相关。",
        "category": "choice",
        "difficulty": 3,
        "concepts": ["correlation"],
        "hint": "r = Cov(X,Y)/(σ_X·σ_Y)"
    },
    {
        "id": "ex_024",
        "question": "以下哪项措施可以减小置信区间的宽度？",
        "options": [
            "A. 降低置信水平（如95%→90%）",
            "B. 提高置信水平（如95%→99%）",
            "C. 减小样本量",
            "D. 增大数据的波动性"
        ],
        "answer": "A",
        "explanation": "降低置信水平会使置信区间变窄（但可靠程度降低）。增大样本量也会使区间变窄，而C和D都会使区间变宽。",
        "category": "choice",
        "difficulty": 3,
        "concepts": ["confidence_interval"],
        "hint": "置信区间宽度与置信水平成正比，与样本量成反比"
    },

    # ===== 开放性应用题 =====
    {
        "id": "ex_025",
        "question": "某公司员工月薪（千元）数据：3, 3.5, 4, 4, 4.5, 5, 5, 5.5, 6, 25。请计算：(1)均值和中位数；(2)哪个指标更能代表该公司的「典型「薪资水平？为什么？",
        "options": [],
        "answer": "(1) 均值=6.55千元，中位数=4.75千元 (2) 中位数更能代表典型薪资水平，因为CEO的25千元月薪严重拉高了均值",
        "explanation": "该题展示了均值对异常值的敏感性。CEO的高薪使均值从4.75提升到6.55，但中位数保持不变。在薪资研究中，中位数是更常用的指标。",
        "category": "calculation",
        "difficulty": 2,
        "concepts": ["mean", "median"],
        "hint": "先排序再计算中位数"
    },
    {
        "id": "ex_026",
        "question": "在A/B测试中，为什么我们不直接比较「足够多「的用户，而要使用统计检验？",
        "options": [],
        "answer": "核心原因：(1) 观察到的差异可能来自随机波动而非真实效果 (2) 统计检验量化了这种「巧合「的概率（p值） (3) 样本量总有限，无法排除偶然性 (4) 统计检验提供了标准化的决策框架",
        "explanation": "即使两组实际上没有差异，由于随机抽样误差，观察到的转化率也几乎不可能完全相同。统计检验帮我们判断「观察到的差异是真实的还是偶然的「。",
        "category": "essay",
        "difficulty": 3,
        "concepts": ["hypothesis_testing", "p_value", "sampling_distribution"],
        "hint": "思考随机性和抽样误差的作用"
    },
    {
        "id": "ex_027",
        "question": '某大学调查发现"学生使用手机的时间与学习成绩呈负相关(r=-0.3, p<0.01)"。请解释这个结果，并说明是否可以得出"使用手机导致成绩下降"的结论？',
        "options": [],
        "answer": '结果解释：(1) 两者存在弱的负相关(r=-0.3) (2) p<0.01表示相关显著。但不能推出因果关系，因为:可能存在混杂因素(如学习动机、自控力等)，也可能是成绩差的学生更爱玩手机(反向因果)。',
        "explanation": '相关不等于因果！这个例子很好地说明了"虚假相关"和"遗漏变量"问题。要通过实验设计(随机对照试验)才能确立因果关系。',
        "category": "essay",
        "difficulty": 3,
        "concepts": ["correlation", "regression"],
        "hint": "A与B相关，可能是A→B，B→A，或C→A且C→B"
    },

    # ===== 更多选择题 =====
    {
        "id": "ex_028",
        "question": "以下关于标准误（Standard Error）的说法，正确的是？",
        "options": [
            "A. 标准误等于标准差",
            "B. 标准误衡量的是样本均值的抽样误差",
            "C. 标准误与样本量无关",
            "D. 标准误越大越好"
        ],
        "answer": "B",
        "explanation": "标准误 = σ/√n，衡量的是样本均值的抽样误差。样本量越大，标准误越小，估计越精确。",
        "category": "choice",
        "difficulty": 3,
        "concepts": ["sampling_distribution", "std_dev"],
        "hint": "标准误是抽样分布的标准差"
    },
    {
        "id": "ex_029",
        "question": "卡方检验主要用于分析什么类型的数据？",
        "options": [
            "A. 连续型数据",
            "B. 分类型数据",
            "C. 时间序列数据",
            "D. 文本数据"
        ],
        "answer": "B",
        "explanation": "卡方检验（χ²检验）主要用于分类数据的分析，如检验两个分类变量是否独立、观测频数是否符合理论分布等。",
        "category": "choice",
        "difficulty": 2,
        "concepts": ["chi_square"],
        "hint": "卡方检验基于列联表"
    },
    {
        "id": "ex_030",
        "question": "在回归分析中，如果残差图呈现明显的「漏斗形「（随预测值增大，残差波动增大），这提示存在什么问题？",
        "options": [
            "A. 非线性关系",
            "B. 异方差性",
            "C. 多重共线性",
            "D. 自相关"
        ],
        "answer": "B",
        "explanation": "漏斗形残差图是异方差性（heteroscedasticity）的典型表现，即误差项的方差不恒定。这会影响到系数显著性检验和置信区间的有效性。",
        "category": "choice",
        "difficulty": 4,
        "concepts": ["regression"],
        "hint": "想象漏斗的形状：上宽下窄"
    },
]


def get_exercises_by_concept(concept_id: str) -> list:
    """根据概念获取相关练习"""
    return [ex for ex in EXERCISES if concept_id in ex["concepts"]]

def get_exercises_by_category(category: str) -> list:
    """根据类别获取练习（choice/calculation/essay）"""
    return [ex for ex in EXERCISES if ex["category"] == category]

def get_exercises_by_difficulty(difficulty: int) -> list:
    """根据难度获取练习"""
    return [ex for ex in EXERCISES if ex["difficulty"] == difficulty]
