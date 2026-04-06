#!/usr/bin/env python3
"""
vc-diligence Streamlit Web界面

功能：
- 输入项目信息
- 实时预览Markdown报告
- 下载Markdown/PDF格式报告

用法：
    streamlit run streamlit_app.py
    或
    python -m streamlit run streamlit_app.py
"""

import streamlit as st
import datetime

VERSION = "v3.3"
OUTPUT_DIR = "memory"

st.set_page_config(
    page_title="vc-diligence 报告生成器",
    page_icon="📊",
    layout="wide"
)

# Stages
STAGES = {
    "天使/Pre-Seed": {"team": 40, "market": 30, "product": 20, "traction": 20, "biz": 10, "competition": 10, "finance": 5},
    "种子轮": {"team": 35, "market": 25, "product": 20, "traction": 25, "biz": 15, "competition": 10, "finance": 10},
    "A轮": {"team": 30, "market": 20, "product": 20, "traction": 30, "biz": 20, "competition": 10, "finance": 15},
    "B轮+": {"team": 20, "market": 15, "product": 15, "traction": 25, "biz": 25, "competition": 15, "finance": 25},
    "二级市场": {"team": 10, "market": 15, "product": 15, "traction": 20, "biz": 20, "competition": 15, "finance": 30},
}

RISK_LEVELS = ["🔴 致命", "🔴 高", "🟡 中", "🟢 低"]

def render_mermaid_table(rows):
    """渲染Mermaid格式竞品矩阵"""
    md = """```mermaid
graph LR
    subgraph 竞品对比"""
    for i, (competitor, stage, valuation, traction, pros, cons) in enumerate(rows):
        color = "#90EE90" if i == 0 else "#FFB6C1"
        md += f"""
        A{i}["{competitor}<br/>{stage} {valuation}"] --> B{i}["{traction}"]"""
    md += "\n```"
    return md


def build_report_content(project: str, stage: str, scores: dict, valuation: str, fdv: str, decision: str, red_flags: list, competitors: list, remarks: str) -> str:
    """构建完整报告内容"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    weights = STAGES.get(stage, STAGES["种子轮"])

    # Calculate weighted scores
    total = sum(scores[k] * weights[k] / 100 for k in scores)

    red_flags_md = "\n".join(
        f"| {i+1} | {r['flag']} | {r['level']} | {'⚠️ 是' if '致命' in r['level'] else '否'} | {r['note']} |"
        for i, r in enumerate(red_flags) if r['flag']
    )

    competitors_md = "\n".join(
        f"| {c['name']} | {c['stage']} | {c['valuation']} | {c['traction']} | {c['pros']} | {c['cons']} |"
        for c in competitors if c['name']
    )

    report = f"""# 尽调报告 — {project}

> **融资阶段**：{stage}  
> **分析时间**：{today}  
> **数据截止**：{today} | **版本**：{VERSION}

---

## 🎯 核心结论

**综合评分**：**{total:.1f}**/10  
**估值**：{valuation}  
**FDV/估值**：{fdv}  
**投资建议**：{decision}

{remarks}

---

## 📊 7维评分表

> {stage}权重配置

| 维度 | 评分(1-10) | 权重 | 加权分 | 说明 |
|------|:-----------:|:----:|:------:|------|
| 团队/创始人 | {scores['team']} | {weights['team']}% | {scores['team']*weights['team']/100:.2f} | {remarks} |
| 市场/时机 | {scores['market']} | {weights['market']}% | {scores['market']*weights['market']/100:.2f} | {remarks} |
| 产品/技术 | {scores['product']} | {weights['product']}% | {scores['product']*weights['product']/100:.2f} | {remarks} |
| Traction/PMF | {scores['traction']} | {weights['traction']}% | {scores['traction']*weights['traction']/100:.2f} | {remarks} |
| 商业模式/GTM | {scores['biz']} | {weights['biz']}% | {scores['biz']*weights['biz']/100:.2f} | {remarks} |
| 竞争/壁垒 | {scores['competition']} | {weights['competition']}% | {scores['competition']*weights['competition']/100:.2f} | {remarks} |
| 财务/资本 | {scores['finance']} | {weights['finance']}% | {scores['finance']*weights['finance']/100:.2f} | {remarks} |
| **总分** | | 100% | **{total:.2f}** | |

---

## 🚨 Red Flags 一览

| # | Red Flag | 风险等级 | 致命 | 备注 |
|---|----------|----------|------|------|
{red_flags_md or "| — | — | — | — |"}

---

## 💰 竞品对比

| 竞品 | 融资阶段 | 估值 | Traction | 优势 | 劣势 |
|------|---------|------|---------|------|------|
{competitors_md or "| — | — | — | — | — | — |"}

---

## 📋 竞品矩阵（Mermaid可视化）

{render_mermaid_table([(c['name'], c['stage'], c['valuation'], c['traction'], c['pros'], c['cons']) for c in competitors if c['name']])}

---

## ✅ 下一步行动

1. 创始人跟进：核实关键数据
2. 客户访谈：验证Traction真实性
3. 法律尽调：Cap Table和IP归属
4. 竞品对比：深度技术壁垒分析

---

*报告生成：{today} | vc-diligence {VERSION}*
"""
    return report


# ============ Streamlit UI ============

st.title("📊 vc-diligence 尽调报告生成器")
st.caption(f"{VERSION} | [GitHub](https://github.com/tonyfeng2018/vc-diligence)")

tab1, tab2 = st.tabs(["📋 报告生成", "ℹ️ 使用说明"])

with tab1:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📝 项目信息")
        project = st.text_input("项目名称", placeholder="例如：AgileBot")
        stage = st.selectbox("融资阶段", list(STAGES.keys()), index=1)

        st.markdown("### 📊 7维度评分")
        scores = {}
        for dim, key in [("团队/创始人", "team"), ("市场/时机", "market"), ("产品/技术", "product"),
                          ("Traction/PMF", "traction"), ("商业模式/GTM", "biz"),
                          ("竞争/壁垒", "competition"), ("财务/资本", "finance")]:
            scores[key] = st.slider(dim, 1, 10, 7)

        st.markdown("### 💰 估值与决策")
        valuation = st.text_input("估值", placeholder="例如：$45M Pre-money")
        fdv = st.text_input("FDV（代币项目）", placeholder="例如：$100M（Pre-TGE）")
        decision = st.selectbox("投资建议", ["✅ 建议投资", "🟡 谨慎投资", "❌ 不建议投资"])
        remarks = st.text_area("核心观点（3句话）", placeholder="描述投资逻辑和主要风险...")

        st.markdown("### 🚨 Red Flags")
        red_flags = []
        for i in range(3):
            with st.expander(f"Red Flag #{i+1}", expanded=i==0):
                flag = st.text_input(f"风险描述 #{i+1}", key=f"flag_{i}", placeholder="描述具体风险...")
                level = st.selectbox(f"风险等级 #{i+1}", RISK_LEVELS, key=f"level_{i}")
                note = st.text_input(f"备注 #{i+1}", key=f"note_{i}", placeholder="补充说明...")
                if flag:
                    red_flags.append({"flag": flag, "level": level, "note": note})

        st.markdown("### 🏢 竞品对比")
        competitors = []
        for i in range(4):
            with st.expander(f"竞品 #{i+1}"):
                c = {}
                c['name'] = st.text_input(f"竞品名称 #{i+1}", key=f"c_name_{i}", placeholder="例如：特斯拉Optimus")
                c['stage'] = st.text_input(f"融资阶段 #{i+1}", key=f"c_stage_{i}", placeholder="例如：B轮")
                c['valuation'] = st.text_input(f"估值 #{i+1}", key=f"c_val_{i}", placeholder="例如：$26亿")
                c['traction'] = st.text_input(f"Traction #{i+1}", key=f"c_trac_{i}", placeholder="例如：全球最多部署")
                c['pros'] = st.text_input(f"优势 #{i+1}", key=f"c_pros_{i}", placeholder="主要优势...")
                c['cons'] = st.text_input(f"劣势 #{i+1}", key=f"c_cons_{i}", placeholder="主要劣势...")
                competitors.append(c)

    with col2:
        st.subheader("👁️ 报告预览")
        if project:
            report = build_report_content(project, stage, scores, valuation, fdv, decision, red_flags, competitors, remarks)
            st.markdown(report)

            # Download button
            st.download_button(
                "📥 下载 Markdown 报告",
                report,
                file_name=f"vc-diligence-{datetime.datetime.now().strftime('%Y-%m-%d')}-{project}.md",
                mime="text/markdown"
            )
        else:
            st.info("👆 填写左侧项目信息，预览报告")

with tab2:
    st.markdown("""
    ## 🎯 vc-diligence 是什么？

    vc-diligence是一个VC投研尽调AI Skill，帮助投资人和分析师系统性分析项目。

    ### ⚡ 快速开始

    **在OpenClaw/Claude Code中发送：**
    ```
    帮我用vc-research框架分析 [项目名称]
    ```

    ### 📊 7维评估框架

    | 维度 | 天使轮 | A轮 | B轮+ |
    |------|:------:|:---:|:----:|
    | 团队 | 40% | 30% | 20% |
    | 市场 | 30% | 20% | 15% |
    | Traction | 20% | **30%** | 25% |
    | 财务 | 5% | 15% | **30%** |

    ### 🔴 Red Flags分级

    - **🔴致命**：直接否决（如数据造假）
    - **🔴高**：显著风险（降低仓位）
    - **🟡中**：一般风险（保持跟踪）
    - **🟢低**：可忽略

    ### 🔗 联动项目

    [startup-idea](https://github.com/tonyf2018/startup-idea) — 创业想法验证
    """)
