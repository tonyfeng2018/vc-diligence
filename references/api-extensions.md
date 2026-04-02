# 尽调数据源 API 扩展指南

## 概述

vc-research 默认使用公开搜索数据。接入以下 API 可大幅提升数据深度和可信度。

---

## API 接入优先级

| 优先级 | API | 用途 | 成本 |
|--------|-----|------|------|
| 🥇 必须 | 百度搜索/NewsAPI | 实时新闻 | 免费 |
| 🥈 推荐 | 天眼查/企查查 | 工商数据 | 免费额度 |
| 🥉 可选 | IT桔子 | 融资数据 | 免费额度 |
| 🥉 可选 | Crunchbase | 全球融资 | 付费 |

---

## 1. 天眼查 API（推荐）

### 接入方式

```python
import requests

TIANYANCHA_TOKEN = "your_tianyancha_token"

def get_company_info(company_name):
    """
    获取公司基本信息
    返回：注册资本、成立时间、经营状态、股东结构
    """
    url = f"https://api.tianyancha.com/api/open/v2/company"
    headers = {"Authorization": TIANYANCHA_TOKEN}
    params = {"name": company_name}
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    return response.json()

def get_company_finance(company_name):
    """
    获取公司融资历史
    返回：历史融资轮次、金额、投资方
    """
    url = f"https://api.tianyancha.com/api/open/v2/company/fund"
    headers = {"Authorization": TIANYANCHA_TOKEN}
    params = {"name": company_name}
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    return response.json()

def get_company_team(company_name):
    """
    获取公司核心团队
    返回：创始人背景、高管名单
    """
    url = f"https://api.tianyancha.com/api/open/v2/company/staff"
    headers = {"Authorization": TIANYANCHA_TOKEN}
    params = {"name": company_name}
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    return response.json()
```

### 响应示例

```json
{
  "company_name": "MiniMax",
  "legal_representative": "闫俊杰",
  "registered_capital": "1000万",
  "established_date": "2021-12",
  "business_status": "存续",
  "shareholders": [
    {"name": "闫俊杰", "share_ratio": "60%"},
    {"name": "XX投资", "share_ratio": "40%"}
  ],
  "fundraising_history": [
    {"round": "天使", "amount": "数千万", "date": "2022-01", "investors": ["高瓴"]},
    {"round": "A轮", "amount": "超2亿美元", "date": "2023-06", "investors": ["腾讯", "高瓴"]}
  ]
}
```

### 申请方式

1. 访问 https://www.tianyancha.com/cloud
2. 注册账号并实名认证
3. 申请免费API额度（每天100次）
4. 获取 Token

---

## 2. 企查查 API

```python
QICHACHA_TOKEN = "your_qichacha_token"

def get_company_basic(company_name):
    """
    获取公司工商信息
    """
    url = "https://api.qcc.com/api/company/basic"
    headers = {"Token": QICHACHA_TOKEN}
    params = {"keyWord": company_name}
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    return response.json()

def get_company_finance(company_name):
    """
    获取公司财务数据（如有披露）
    """
    url = "https://api.qcc.com/api/finance"
    headers = {"Token": QICHACHA_TOKEN}
    params = {"keyWord": company_name}
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    return response.json()
```

---

## 3. IT桔子 API（融资数据）

### 接入方式

```python
ITJUZI_TOKEN = "your_itjuzi_token"

def get_funding_events(company_name):
    """
    获取公司历史融资事件
    返回：轮次、金额、日期、投资方
    """
    url = "https://www.itjuzi.com/api/companies"
    headers = {"Authorization": ITJUZI_TOKEN}
    params = {"name": company_name}
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    return response.json()

def get_sector_overview(sector_name):
    """
    获取赛道概况
    返回：市场规模、主要玩家、融资趋势
    """
    url = "https://www.itjuzi.com/api/sectors"
    headers = {"Authorization": ITJUZI_TOKEN}
    params = {"name": sector_name}
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    return response.json()
```

### 响应示例

```json
{
  "company_name": "MiniMax",
  "fundraising_events": [
    {
      "round": "天使轮",
      "date": "2022-01",
      "amount": "5000万人民币",
      "investors": ["高瓴资本"]
    },
    {
      "round": "A轮",
      "date": "2023-06",
      "amount": "超2亿美元",
      "investors": ["腾讯投资", "高瓴资本", "米哈游"]
    }
  ],
  "valuation_trend": [
    {"date": "2022-01", "valuation": "1亿"},
    {"date": "2023-06", "valuation": "12亿"}
  ]
}
```

---

## 4. NewsAPI（新闻数据）

```python
NEWS_API_KEY = "your_newsapi_key"

def get_company_news(company_name, days=30):
    """
    获取公司最近新闻
    返回：标题、摘要、日期、情感倾向
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": company_name,
        "apiKey": NEWS_API_KEY,
        "language": "zh",
        "sortBy": "publishedAt",
        "pageSize": 20,
        "from": f"{days}days ago"
    }
    
    response = requests.get(url, params=params, timeout=10)
    return response.json()

def get_sentiment(news_data):
    """
    情感分析：正面/中性/负面
    用豆包模型分析新闻情感
    """
    headlines = [article['title'] for article in news_data.get('articles', [])]
    
    prompt = f"""
    分析以下新闻标题的情感倾向（正面/中性/负面）：
    {headlines}
    
    返回格式：
    - 正面新闻：X条
    - 中性新闻：X条  
    - 负面新闻：X条
    - 重点关注：[列出需要关注的风险事件]
    """
    
    # 调用豆包模型
    response = calls.doubao(prompt)
    return response
```

---

## 5. 火山云豆包模型扩展

```python
import requests

DOUBAO_API_KEY = "your_doubao_api_key"

def analyze_with_doubao(content, task_type="analysis"):
    """
    用豆包模型分析内容
    task_type: analysis/summary/risk
    """
    endpoint = "https://ark.cn-beijing.volces.com/api/v3/beta/chat/completions"
    
    prompts = {
        "analysis": f"分析以下创业项目，给出6维评分（团队/市场/产品/商业/竞争/财务）：{content}",
        "summary": f"总结以下尽调信息，提取关键亮点和风险：{content}",
        "risk": f"识别以下项目的主要风险点：{content}"
    }
    
    headers = {
        "Authorization": f"Bearer {DOUBAO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "doubao-pro-32k",
        "messages": [{"role": "user", "content": prompts[task_type]}],
        "temperature": 0.3  # 低温度，更确定性输出
    }
    
    response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
    return response.json()
```

---

## 6. 完整尽调数据整合

```python
def full_diligence(company_name):
    """
    完整尽调数据采集
    并行调用所有数据源
    """
    import concurrent.futures
    
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # 并行发起所有请求
        future_to_source = {
            executor.submit(get_company_info, company_name): "tianyancha",
            executor.submit(get_funding_events, company_name): "itjuzi", 
            executor.submit(get_company_news, company_name): "news",
            executor.submit(search_competitors, company_name): "search"
        }
        
        for future in concurrent.futures.as_completed(future_to_source):
            source = future_to_source[future]
            try:
                results[source] = future.result()
            except Exception as e:
                results[source] = {"error": str(e)}
    
    # 用豆包模型整合分析
    analysis = analyze_with_doubao(str(results), task_type="analysis")
    
    return {
        "raw_data": results,
        "analysis": analysis,
        "timestamp": datetime.now().isoformat()
    }
```

---

## API 成本对比

| API | 免费额度 | 超出费用 | 推荐场景 |
|-----|---------|----------|---------|
| 天眼查 | 100次/天 | 0.1元/次 | 必接，工商数据 |
| 企查查 | 100次/天 | 0.1元/次 | 备选，工商数据 |
| IT桔子 | 50次/天 | 付费 | 推荐，融资数据 |
| NewsAPI | 100次/天 | $0.5/100次 | 推荐，新闻数据 |
| 豆包API | 100万token/月 | 0.003元/千token | 核心，文本分析 |

---

## 安全注意事项

1. **Token 存储**：不要硬编码在代码里，用环境变量
2. **频率限制**：所有API都有QPS限制，并发请求要加锁
3. **数据校验**：API返回数据需验证，防止注入攻击
4. **缓存**：相同请求24小时内不重复调用，节省成本
