"""Wiki卡片模块 - 用于展示统计学概念卡片"""

import re
from data.concepts import CONCEPTS, get_concept_by_id
from data.knowledge_graph_data import CATEGORY_META


# ===== 内联CSS样式 =====
WIKI_CARD_CSS = """
<style>
.wiki-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #333;
    line-height: 1.6;
}
.wiki-header {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 20px;
    padding-left: 16px;
}
.wiki-icon { font-size: 40px; line-height: 1; }
.wiki-title-group { flex: 1; }
.wiki-title { margin: 0; font-size: 1.6rem; color: #1a1a2e; }
.wiki-en-name { font-size: 0.9rem; color: #999; font-style: italic; display: block; margin-bottom: 6px; }
.wiki-meta-row { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.wiki-badge { display: inline-block; padding: 3px 12px; border-radius: 20px; color: white; font-size: 0.8rem; font-weight: 500; }
.wiki-difficulty { font-size: 0.85rem; color: #f59e0b; }
.wiki-summary {
    background: #f0f4ff; padding: 14px 18px; border-radius: 8px; margin-bottom: 16px;
    border-left: 4px solid #667eea; font-size: 0.95rem; color: #333;
    line-height: 1.7;
}
.wiki-description { margin-bottom: 16px; color: #444; line-height: 1.8; font-size: 0.95rem; }
.wiki-description p { margin: 8px 0 0 0; }
.wiki-formula {
    background: #f8f9fa; padding: 16px; border-radius: 8px; text-align: center;
    font-size: 1.2rem; margin-bottom: 16px; overflow-x: auto;
    border: 1px solid #e9ecef;
}
.wiki-example {
    background: #fffbeb; padding: 14px 18px; border-radius: 8px; margin-bottom: 16px;
    border-left: 4px solid #f59e0b; color: #444; font-size: 0.95rem; line-height: 1.7;
}
.wiki-example p { margin: 8px 0 0 0; }
.wiki-content { color: #444; line-height: 1.8; font-size: 0.95rem; margin-bottom: 16px; }
.wiki-content h4 { color: #1a1a2e; font-size: 1.2rem; margin: 20px 0 10px 0; padding-bottom: 6px; border-bottom: 2px solid #eef2ff; }
.wiki-content h5 { color: #444; font-size: 1.05rem; margin: 16px 0 8px 0; }
.wiki-content ul { padding-left: 20px; margin: 8px 0; }
.wiki-content li { margin-bottom: 4px; }
.wiki-content strong { color: #1a1a2e; }
.wiki-content code {
    background: #f0f0f0; padding: 2px 6px; border-radius: 4px; font-size: 0.9em;
    font-family: 'SF Mono', Monaco, monospace;
}
.wiki-content pre { background: #f5f5f5; padding: 12px; border-radius: 6px; overflow-x: auto; }
.wiki-table {
    width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 0.9rem;
}
.wiki-table th { background: #f0f4ff; padding: 8px 12px; text-align: left; font-weight: 600; border: 1px solid #e0e7ff; }
.wiki-table td { padding: 6px 12px; border: 1px solid #e0e7ff; }
.wiki-table tr:nth-child(even) { background: #fafaff; }
.wiki-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 16px; padding-top: 16px; border-top: 2px solid #f0f0f0; }
.tag { background: #eef2ff; color: #4f46e5; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; }
.latex-inline { color: #1a1a2e; }
.latex-block { text-align: center; padding: 8px; }
</style>
"""


def render_wiki_card(concept_id: str, include_formula: bool = True) -> str:
    """渲染单个概念的Wiki卡片HTML"""
    concept = get_concept_by_id(concept_id)
    if not concept:
        return "<div>未找到该概念</div>"

    meta = CATEGORY_META.get(concept["category"], {"color": "#999", "icon": "📄"})

    # 转换wiki_content中的markdown为基本HTML
    wiki_html = _markdown_to_html(concept.get("wiki_content", ""))

    # 处理公式（可选，默认为纯文本展示）
    formula_html = ""
    if concept.get("formula") and include_formula:
        formula_html = (
            '<div class="wiki-formula">'
            f'<div style="font-family:serif;font-size:1.2rem;padding:8px 0;">'
            f'{concept["formula"]}</div></div>'
        )

    summary = concept['summary']
    description = concept['description']
    example = concept['example']

    # 构建卡片HTML
    card_html = f"""
    <div class="wiki-card">
        <div class="wiki-header" style="border-left: 5px solid {meta['color']};">
            <span class="wiki-icon">{meta['icon']}</span>
            <div class="wiki-title-group">
                <h2 class="wiki-title">{concept['name']}</h2>
                <span class="wiki-en-name">{concept['name_en']}</span>
                <div class="wiki-meta-row">
                    <span class="wiki-badge" style="background: {meta['color']};">{concept['category']}</span>
                    <span class="wiki-difficulty">{'⭐' * concept['difficulty']}</span>
                </div>
            </div>
        </div>

        <div class="wiki-summary">
            <strong>📖 定义：</strong> {summary}
        </div>

        <div class="wiki-description">
            <strong>📝 详细解释：</strong>
            <p>{description}</p>
        </div>

        {formula_html}

        <div class="wiki-example">
            <strong>💡 实例：</strong>
            <p>{example}</p>
        </div>

        <div class="wiki-content">
            {wiki_html}
        </div>

        <div class="wiki-tags">
            {' '.join(f'<span class="tag">#{tag}</span>' for tag in concept['tags'])}
        </div>
    </div>
    """
    return WIKI_CARD_CSS + card_html


def render_wiki_card_standalone(concept_id: str, include_formula: bool = True) -> str:
    """生成完整的独立HTML页面"""
    card = render_wiki_card(concept_id, include_formula=include_formula)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Wiki卡片</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
</head>
<body style="background:#f5f7fa;padding:20px;margin:0;">
{card}
<script>
document.addEventListener("DOMContentLoaded", function() {{
    try {{
        renderMathInElement(document.body, {{
            delimiters: [
                {{left: '$$', right: '$$', display: true}},
                {{left: '$', right: '$', display: false}}
            ]
        }});
    }} catch(e) {{}}
}});
</script>
</body>
</html>"""


def render_wiki_card_minimal(concept_id: str) -> str:
    """简约版Wiki卡片（用于列表展示）"""
    concept = get_concept_by_id(concept_id)
    if not concept:
        return ""

    meta = CATEGORY_META.get(concept["category"], {"color": "#999", "icon": "📄"})

    return f"""
    <div style="display:flex;align-items:center;gap:12px;padding:10px 14px;background:white;
                border-radius:8px;margin-bottom:6px;border-left:3px solid {meta['color']};
                box-shadow:0 1px 3px rgba(0,0,0,0.06);">
        <span style="font-size:24px;">{meta['icon']}</span>
        <div style="flex:1;">
            <strong style="display:block;color:#333;">{concept['name']}</strong>
            <small style="color:#999;">{concept['name_en']}</small>
            <p style="margin:2px 0;font-size:0.85em;color:#666;">{concept['summary'][:80]}...</p>
        </div>
        <span style="display:inline-block;padding:2px 10px;border-radius:20px;color:white;
                    font-size:0.75rem;background:{meta['color']};">{concept['category']}</span>
    </div>
    """


def search_concepts(query: str) -> list:
    """搜索概念（支持中文和英文搜索）"""
    query = query.lower().strip()
    if not query:
        return []

    results = []
    for c in CONCEPTS:
        if (query in c["name"].lower() or
            query in c["name_en"].lower() or
            query in c["summary"].lower() or
            any(query in tag.lower() for tag in c["tags"])):
            results.append(c)
    return results


def _markdown_to_html(md: str) -> str:
    """将Markdown转换为整洁的HTML"""
    if not md:
        return ""

    html = md

    # 表格
    html = _convert_tables(html)

    # 代码块
    html = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    # 行内代码
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # 标题
    html = re.sub(r'^### (.+)$', r'<h5>\1</h5>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

    # 水平分割线
    html = re.sub(r'^---+\s*$', r'<hr>', html, flags=re.MULTILINE)

    # 粗体和斜体 (先处理粗体)
    html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', html)

    # 无序列表: 将连续的<li>用<ul>包裹
    html = re.sub(r'^[\s]*[-*]\s+(.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*?</li>(\s*<li>.*?</li>)*)', r'<ul>\1</ul>', html, flags=re.DOTALL)

    # 有序列表
    html = re.sub(r'^[\s]*\d+\.\s+(.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)

    # 段落: 将连续的文本行用<p>包裹（非标题/列表/表格/代码的行）
    lines = html.split('\n')
    result = []
    in_paragraph = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_paragraph:
                result.append('</p>')
                in_paragraph = False
            result.append('')
            continue
        if (stripped.startswith('<h') or stripped.startswith('<li') or
            stripped.startswith('<ul') or stripped.startswith('</ul') or
            stripped.startswith('<pre') or stripped.startswith('<table') or
            stripped.startswith('</table') or stripped.startswith('<tr') or
            stripped.startswith('<th') or stripped.startswith('<td') or
            stripped.startswith('<hr') or stripped.startswith('<li')):
            if in_paragraph:
                result.append('</p>')
                in_paragraph = False
            result.append(line)
            continue
        if not in_paragraph:
            result.append('<p>' + line)
            in_paragraph = True
        else:
            result.append('<br>' + line)
    if in_paragraph:
        result.append('</p>')

    html = '\n'.join(result)

    return html


def _convert_tables(html: str) -> str:
    """将Markdown表格转换为HTML表格"""
    # 简单表格转换
    table_pattern = r'(\|.+\|\n\|[-| ]+\|\n(\|.+\|\n?)*)'
    def replace_table(match):
        lines = match.group(0).strip().split('\n')
        if len(lines) < 2:
            return match.group(0)

        # 提取表头
        headers = [h.strip() for h in lines[0].split('|')[1:-1]]
        # 忽略分隔行
        # 提取数据行
        rows = []
        for line in lines[2:]:
            if line.strip().startswith('|'):
                cells = [c.strip() for c in line.split('|')[1:-1]]
                rows.append(cells)

        table_html = '<table class="wiki-table"><thead><tr>'
        for h in headers:
            table_html += f'<th>{h}</th>'
        table_html += '</tr></thead><tbody>'
        for row in rows:
            table_html += '<tr>'
            for cell in row:
                table_html += f'<td>{cell}</td>'
            table_html += '</tr>'
        table_html += '</tbody></table>'
        return table_html

    return re.sub(table_pattern, replace_table, html, flags=re.MULTILINE)
