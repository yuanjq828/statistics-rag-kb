"""统计学案例分析数据"""

CASES = [
    {
        "id": "case_01",
        "title": "医疗药物效果评估",
        "field": "医学",
        "description": "某制药公司研发了一种新的降压药，需要评估其有效性。研究者招募了200名高血压患者，随机分为两组：实验组（100人）服用新药，对照组（100人）服用安慰剂。",
        "problem": "如何判断新药是否确实有效？需要考虑哪些统计因素？",
        "solution": """**分析方案**：

1. **数据收集**：记录每位患者实验前后的血压值
2. **描述统计**：计算两组血压下降值的均值、标准差
3. **假设检验**：使用独立样本t检验比较两组的平均降压效果
4. **置信区间**：计算新药相对于安慰剂的平均降压效果的95%置信区间
5. **效应量**：计算Cohen's d评估实际效果大小

**预期结果**：
- t检验p<0.05 → 新药有效
- 置信区间不包含0 → 效果显著
- 同时需要关注可能的副作用

**代码示例**：
```python
import numpy as np
from scipy import stats

# 模拟数据
np.random.seed(42)
experiment = np.random.normal(12, 5, 100)  # 实验组降压效果
control = np.random.normal(3, 5, 100)      # 对照组

# t检验
t_stat, p_value = stats.ttest_ind(experiment, control)
print(f"t统计量: {t_stat:.3f}")
print(f"p值: {p_value:.4f}")
```""",
        "concepts": ["t_test", "hypothesis_testing", "p_value", "confidence_interval", "descriptive_stats"],
        "difficulty": 3,
        "code_example": "import numpy as np\nfrom scipy import stats\n\nexperiment = np.random.normal(12, 5, 100)\ncontrol = np.random.normal(3, 5, 100)\nt_stat, p_value = stats.ttest_ind(experiment, control)\nprint(f't统计量: {t_stat:.3f}')\nprint(f'p值: {p_value:.4f}')"
    },
    {
        "id": "case_02",
        "title": "教育方法比较研究",
        "field": "教育学",
        "description": "为了比较三种不同的数学教学方法的效果，某中学将90名学生随机分配到3个班级，每个班级使用不同的教学方法。学期结束后进行统一考试。",
        "problem": "三种教学方法的效果是否存在显著差异？如果存在，哪种方法更好？",
        "solution": """**分析方案**：

1. **数据整理**：记录三组学生的期末考试成绩
2. **方差分析（ANOVA）**：使用单因素方差分析比较三组均值
3. **事后检验**：如果ANOVA显著，使用Tukey HSD找出差异来源
4. **效应量**：计算η²（eta-squared）评估方法对成绩影响的大小

**结果解读**：
- F值显著（p<0.05）→ 至少有一种方法与其他方法不同
- 事后检验 → 具体指出哪组与哪组有差异
- 箱线图可视化 → 直观展示三组分布

**代码示例**：
```python
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# 假设数据
method_a = [85, 88, 90, 82, 86, ...]
method_b = [78, 80, 75, 82, 79, ...]
method_c = [92, 95, 89, 94, 91, ...]

# 单因素ANOVA
f_stat, p_value = stats.f_oneway(method_a, method_b, method_c)
print(f"F值: {f_stat:.3f}, p值: {p_value:.4f}")
```""",
        "concepts": ["anova", "t_test", "p_value", "box_plot", "hypothesis_testing"],
        "difficulty": 3,
        "code_example": ""
    },
    {
        "id": "case_03",
        "title": "房价影响因素分析",
        "field": "经济学",
        "description": "一家房地产研究机构想分析影响房价的关键因素。收集了500套房源的数据，包括房价（万元）、面积（m²）、卧室数量、房龄（年）、距市中心距离（km）等变量。",
        "problem": "哪些因素对房价有显著影响？如何建立一个可靠的房价预测模型？",
        "solution": """**分析方案**：

1. **探索性数据分析**：相关性热图、散点图矩阵
2. **多元线性回归**：建立房价对各个自变量的回归模型
3. **变量筛选**：使用逐步回归或Lasso选择重要变量
4. **模型诊断**：检查残差正态性、异方差性、多重共线性(VIF)
5. **模型评估**：R²、调整R²、RMSE

**关键发现**（模拟）：
- 面积对房价影响最大（系数最大）
- 房龄与房价负相关
- 距市中心距离每增加1km，房价平均下降3%
- 模型R²=0.82，解释力良好

**代码示例**：
```python
import statsmodels.api as sm
import pandas as pd

# 假设数据
data = pd.DataFrame({
    'price': [...],
    'area': [...],
    'bedrooms': [...],
    'age': [...],
    'distance': [...]
})

X = data[['area', 'bedrooms', 'age', 'distance']]
X = sm.add_constant(X)
y = data['price']

model = sm.OLS(y, X).fit()
print(model.summary())
```""",
        "concepts": ["regression", "correlation", "r_squared", "descriptive_stats"],
        "difficulty": 4,
        "code_example": ""
    },
    {
        "id": "case_04",
        "title": "产品质量控制与六西格玛",
        "field": "工业工程",
        "description": "一家电子元件工厂的生产线上，某关键零件的规格要求为直径10±0.1mm。质量部门每天抽取50个产品进行测量，发现某些批次的不合格率偏高。",
        "problem": "如何判断生产过程是否处于受控状态？如何降低不合格率？",
        "solution": """**分析方案**：

1. **描述统计**：计算各批次均值、标准差、不合格率
2. **控制图**：绘制X̄-bar图和R图监控生产过程的稳定性
3. **过程能力分析**：计算Cpk和Ppk指标
4. **假设检验**：比较问题批次与正常批次的均值是否存在显著差异

**六西格玛标准**：
- 规格限：10±0.1mm（USL=10.1, LSL=9.9）
- 目标：Cpk ≥ 1.33（过程能力充足）
- 6σ水平意味着不合格率 < 3.4 ppm

**控制图解读**：
- 点超出控制限 → 过程失控
- 连续7点在均值同一侧 → 异常趋势
- 连续7点上升或下降 → 异常趋势""",
        "concepts": ["mean", "std_dev", "normal_distribution", "descriptive_stats"],
        "difficulty": 3,
        "code_example": ""
    },
    {
        "id": "case_05",
        "title": "A/B测试在电商中的应用",
        "field": "互联网/电商",
        "description": "某电商平台想测试新的首页设计是否能提高用户的点击购买转化率。将用户随机分为两组：控制组（旧设计，10000人）和实验组（新设计，10000人），记录是否发生购买。",
        "problem": "新设计是否显著提高了转化率？样本量是否足够？",
        "solution": """**分析方案**：

1. **假设设定**：
   - H₀: p新 = p旧（新设计无效果）
   - H₁: p新 > p旧（新设计提高转化率）

2. **数据收集**：
   - 控制组：800/10000人购买（转化率8.0%）
   - 实验组：920/10000人购买（转化率9.2%）

3. **两比例Z检验**：
   - Z = 2.98, p = 0.0014 < 0.05

4. **结论**：新设计显著提高了转化率（提升1.2个百分点）

**注意事项**：
- 随机分组确保两组可比
- 样本量由功效分析确定（power analysis）
- 需控制其他因素不变（如时间段、促销活动等）

**代码示例**：
```python
import statsmodels.api as sm

control = 800  # 控制组购买人数
control_n = 10000
treatment = 920  # 实验组购买人数
treatment_n = 10000

# 两比例Z检验
z_stat, p_value = sm.stats.proportions_ztest(
    [treatment, control],
    [treatment_n, control_n]
)
print(f"Z值: {z_stat:.3f}")
print(f"p值: {p_value:.4f}")
```""",
        "concepts": ["hypothesis_testing", "p_value", "type_error", "sampling_distribution", "z_score"],
        "difficulty": 3,
        "code_example": ""
    },
    {
        "id": "case_06",
        "title": "贝叶斯方法与垃圾邮件过滤",
        "field": "计算机科学/机器学习",
        "description": "电子邮件服务商需要构建一个垃圾邮件过滤器。可以使用朴素贝叶斯分类器，基于邮件中出现的词汇来判断邮件是否为垃圾邮件。",
        "problem": "如何利用贝叶斯定理计算一封包含特定关键词的邮件是垃圾邮件的概率？",
        "solution": """**贝叶斯垃圾邮件过滤原理**：

$$P(Spam|Words) = \\frac{P(Words|Spam)P(Spam)}{P(Words)}$$

**计算步骤**：
1. **先验概率**：P(Spam) = 垃圾邮件比例（如60%）
2. **似然**：P(关键词|Spam) = 该词在垃圾邮件中出现频率
3. **证据**：P(关键词) = 该词在所有邮件中出现频率
4. **后验概率**：代入贝叶斯公式计算

**示例**：
- 邮件包含"免费"和"中奖"两个词
- P(Spam) = 0.6, P(非Spam) = 0.4
- P("免费"|Spam) = 0.3, P("免费"|非Spam) = 0.05
- P("中奖"|Spam) = 0.2, P("中奖"|非Spam) = 0.01
- 计算得 P(Spam|"免费","中奖") ≈ 99.5% → 判定为垃圾邮件

**朴素贝叶斯假设**：特征条件独立（虽然现实中不成立，但效果依然很好）""",
        "concepts": ["bayes", "probability", "conditional_probability"],
        "difficulty": 3,
        "code_example": ""
    },
    {
        "id": "case_07",
        "title": "社会调查中的抽样设计",
        "field": "社会学",
        "description": "某研究机构要调查城市居民的月收入水平。城市人口100万，预算有限只能调查1000人。",
        "problem": "如何设计抽样方案才能保证样本代表总体？如何确定合适的样本量？",
        "solution": """**抽样方案设计**：

1. **分层抽样**：按区域（城区/郊区）和年龄段分层
2. **样本量计算**：基于置信水平和误差容忍度
   - 95%置信水平，3%误差容忍度
   - 需要样本量：n ≈ (1.96²×0.25)/0.03² ≈ 1067
3. **加权调整**：对样本进行事后加权，使人口学特征与总体一致
4. **标准误计算**：考虑复杂抽样设计的设计效应(Design Effect)

**中心极限定理的应用**：
- 虽然收入分布严重偏态，但样本均值的分布近似正态
- 可构建总体均值的置信区间
- 可进行子群体的比较分析

**注意事项**：
- 无应答偏差（低收入人群可能更不愿意透露收入）
- 回忆偏差（被调查者可能记不准具体收入）
- 社会期望偏差（可能虚报或瞒报）""",
        "concepts": ["central_limit_theorem", "confidence_interval", "inferential_stats", "sampling_distribution"],
        "difficulty": 4,
        "code_example": ""
    },
    {
        "id": "case_08",
        "title": "气候数据分析：全球变暖趋势",
        "field": "环境科学",
        "description": "气象研究者分析过去100年的全球平均气温数据，想确认是否存在显著的上升趋势，并预测未来气温变化。",
        "problem": "如何量化全球变暖的趋势？统计上是否显著？如何预测未来？",
        "solution": """**分析方案**：

1. **时间序列分解**：趋势、季节性和随机成分
2. **线性回归**：气温对年份回归，估计每十年升温速度
3. **自相关分析**：检查残差是否存在自相关
4. **Mann-Kendall检验**：非参数趋势检验
5. **预测区间**：给出未来气温的预测区间

**模拟发现**：
- 每十年升温约0.18°C（全球平均）
- 趋势的p值 < 0.001，极其显著
- 近50年升温速度明显加快

**回归模型**：
$$Temp_t = \\beta_0 + \\beta_1 Year_t + \\varepsilon_t$$

- $\\beta_1$ = 0.018 → 每年升温0.018°C
- R² = 0.78 → 年份解释了78%的气温变化""",
        "concepts": ["regression", "correlation", "r_squared", "hypothesis_testing", "descriptive_stats"],
        "difficulty": 4,
        "code_example": ""
    },
]
