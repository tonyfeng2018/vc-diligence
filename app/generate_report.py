#!/usr/bin/env python3
"""
vc-diligence 报告生成器 CLI工具

功能：
- 输入项目名称和融资阶段
- 生成结构化Markdown/HTML/PDF尽调报告
- 自动存档到 memory/ 目录

用法：
    python generate_report.py --project "AgileBot" --stage "A轮" --format md --output ./report.md
"""

import argparse
import sys
from datetime import datetime

VERSION = "v3.3"
OUTPUT_DIR = "memory"


def build_report_template(project: str, stage: str) -> str:
    """生成vc-research框架标准报告模板"""
    today = datetime.now().strftime("%Y-%m-%d")
    stage_weight = get_stage_weights(stage)

    template = f"""# 尽调报告 — {project}

> **融资阶段**：{stage}  
> **分析时间**：{today}  
> **数据截止**：{today} | **版本**：{VERSION}  
> **分析师关注点**：请填写本项目的核心投资关注点

---

## 🎯 核心结论

**综合评分**：X/10  
**估值合理性**：[偏高/合理/偏低]  
**投资建议**：[建议投资/谨慎投资/不建议投资]

理由：2-3句话总结

---

## 📊 7维评分表

> {stage}权重配置

| 维度 | 评分 | 权重 | 加权分 | 量化依据 | 一句话说明 |
|------|------|------|--------|---------|----------|
| 团队/创始人 | X | {stage_weight['team']}% | X.XX | [量化] | [一句话] |
| 市场/时机 | X | {stage_weight['market']}% | X.XX | [量化] | [一句话] |
| 产品/技术 | X | {stage_weight['product']}% | X.XX | [量化] | [一句话] |
| Traction/PMF | X | {stage_weight['traction']}% | X.XX | [量化] | [一句话] |
| 商业模式/GTM | X | {stage_weight['biz']}% | X.XX | [量化] | [一句话] |
| 竞争/壁垒 | X | {stage_weight['competition']}% | X.XX | [量化] | [一句话] |
| 财务/资本 | X | {stage_weight['finance']}% | X.XX | [量化] | [一句话] |
| **总分** | | 100% | **X.X** | | |

---

## 💰 估值对比表

| 公司/项目 | 融资阶段 | 估值 | 核心指标 | 备注 |
|-----------|---------|------|---------|------|
| [本公司] | {stage} | [估值] | [指标] | [备注] |
| 竞品A | [阶段] | [估值] | [指标] | [备注] |
| 竞品B | [阶段] | [估值] | [指标] | [备注] |

**估值判断**：[比竞品贵/便宜/相当]，理由：[一句话]

---

## 🚨 Red Flags 一览

| # | Red Flag | 风险等级 | 致命 | 备注 |
|---|----------|----------|------|------|
| 1 | [如：To C付费意愿存疑] | 🔴致命 | ⚠️ 是 | [说明] |
| 2 | [如：数据量太少] | 🔴高 | ⚠️ 是 | [说明] |
| 3 | [如：竞争加剧] | 🟡中 | ⚠️ 否 | [说明] |

---

## 🎯 投资决策矩阵（带触发条件）

| 情景 | 估值/价格 | 建议仓位 | 条件 | 行动 |
|------|----------|----------|------|------|
| 乐观 | [区间] | [X%] | — | [行动] |
| **条件加注** | — | [Y%] | [核心KPI达标] | 加注 |
| **核心KPI** | — | — | [不达标条件] | 放弃 |
| 中性 | [区间] | [X%] | — | [行动] |
| 悲观 | [区间] | [X%] | — | [行动] |

---

## ✅ 下一步检查清单

| # | 动作 | 时间 | 方式 | 具体内容 |
|---|------|------|------|---------|
| 1 | [动作] | [时间] | [方式] | [具体内容] |
| 2 | [验证数据] | [X天内] | [文件/演示] | [要Traction数据/财务明细] |
| 3 | [客户访谈] | [X天内] | [电话/拜访] | [找XX个真实客户] |

---

## ⚠️ 数据完整性声明

> ✅/⚠️ [完整数据来源说明]
>
> - [数据项]：[来源]
> - ⚠️ [待验证项]：[需要创始人/实时数据补充]

---

## 7维阶段权重参考

| 维度 | 天使/Pre-Seed | Seed | A轮 | B轮+ | 二级市场 |
|------|:------------:|:----:|:---:|:----:|:--------:|
| 团队/创始人 | 40% | 35% | 30% | 20% | 10% |
| 市场/时机 | 30% | 25% | 20% | 15% | 15% |
| 产品/技术 | 20% | 20% | 20% | 15% | 15% |
| Traction/PMF | 20% | 25% | 30% | 25% | 20% |
| 商业模式/GTM | 10% | 15% | 20% | 25% | 20% |
| 竞争/壁垒 | 10% | 10% | 10% | 15% | 15% |
| 财务/资本 | 5% | 10% | 15% | 25% | 30% |

---

**本报告生成时间：2026-04-06 | 版本：VERSION
---
**Last updated**: 2026-04-06
**Author**: Tony F
**Email**: tongfweb3@gmail.com
"""
    return template


def get_stage_weights(stage: str) -> dict:
    """根据融资阶段返回权重配置"""
    weights = {
        "天使": {"team": 40, "market": 30, "product": 20, "traction": 20, "biz": 10, "competition": 10, "finance": 5},
        "种子": {"team": 35, "market": 25, "product": 20, "traction": 25, "biz": 15, "competition": 10, "finance": 10},
        "A轮": {"team": 30, "market": 20, "product": 20, "traction": 30, "biz": 20, "competition": 10, "finance": 15},
        "B轮": {"team": 20, "market": 15, "product": 15, "traction": 25, "biz": 25, "competition": 15, "finance": 25},
        "二级": {"team": 10, "market": 15, "product": 15, "traction": 20, "biz": 20, "competition": 15, "finance": 30},
    }
    for key in weights:
        if key in stage:
            return weights[key]
    return weights["种子"]


def generate_markdown(project: str, stage: str, output_path: str):
    """生成Markdown格式报告"""
    content = build_report_template(project, stage)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Markdown报告已生成: {output_path}")


def generate_html(project: str, stage: str, output_path: str):
    """生成HTML格式报告"""
    md_content = build_report_template(project, stage)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>尽调报告 — {project}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; color: #333; line-height: 1.6; }}
h1 {{ color: #1a1a2e; border-bottom: 3px solid #e74c3c; padding-bottom: 10px; }}
h2 {{ color: #2c3e50; margin-top: 30px; }}
blockquote {{ background: #f8f9fa; border-left: 4px solid #e74c3c; padding: 12px; margin: 16px 0; }}
table {{ border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 14px; }}
th {{ background: #2c3e50; color: white; padding: 10px; text-align: left; }}
td {{ padding: 8px; border: 1px solid #ddd; }}
tr:nth-child(even) {{ background: #f9f9f9; }}
.red {{ color: #e74c3c; font-weight: bold; }}
.orange {{ color: #e67e22; }}
.green {{ color: #27ae60; }}
.mono {{ font-family: "SF Mono", Monaco, monospace; background: #f4f4f4; padding: 2px 6px; }}
</style>
</head>
<body>
<h1>📊 尽调报告 — {project}</h1>
<blockquote>
<strong>融资阶段</strong>：{stage} | <strong>版本</strong>：{VERSION} | <strong>日期</strong>：{datetime.now().strftime('%Y-%m-%d')}
</blockquote>
<div style="margin-top:40px">
<p><em>本报告为vc-research框架自动生成模板。请根据实际调研填充内容。</em></p>
<p>📁 完整使用方式请参考：<a href="https://github.com/tonyfeng2018/vc-diligence">vc-diligence GitHub</a></p>
</div>
</body>
</html>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML报告已生成: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="vc-diligence 报告生成器")
    parser.add_argument("--project", "-p", required=True, help="项目名称")
    parser.add_argument("--stage", "-s", default="种子轮", help="融资阶段（天使/种子/A轮/B轮+/二级）")
    parser.add_argument("--format", "-f", default="md", choices=["md", "html", "both"], help="输出格式")
    parser.add_argument("--output", "-o", default=None, help="输出文件路径")
    args = parser.parse_args()

    project = args.project
    stage = args.stage

    if args.output:
        base = args.output
        if "." not in base:
            base = f"{base}.{args.format}"

        if args.format in ("md", "both"):
            generate_markdown(project, stage, base if args.format == "md" else base.replace(".html", ".md"))
        if args.format in ("html", "both"):
            generate_html(project, stage, base if args.format == "html" else base.replace(".md", ".html"))
    else:
        # Interactive mode
        print(f"\n📊 vc-diligence 报告生成器 {VERSION}")
        print(f"项目: {project} | 阶段: {stage}")
        print()
        print("生成模板报告到 memory/ 目录...")

        import os
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filename = f"{OUTPUT_DIR}/vc-diligence-{datetime.now().strftime('%Y-%m-%d')}-{project}.md"
        generate_markdown(project, stage, filename)
        print()
        print("💡 提示: 在OpenClaw/Claude Code中使用vc-research Skill可获得完整分析")


if __name__ == "__main__":
    main()
