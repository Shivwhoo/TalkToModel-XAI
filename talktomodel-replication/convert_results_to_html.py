"""
Generates a publication-styled, print-ready HTML report from EXPERIMENTAL_RESULTS_DOCUMENT.md.
Open the resulting HTML in any browser (Chrome, Edge, Brave) and press Ctrl+P -> Save as PDF.
"""

import os
import re

def markdown_to_html(md_text):
    html_lines = []
    in_table = False
    table_header = True
    in_list = False
    
    lines = md_text.splitlines()
    for line in lines:
        stripped = line.strip()
        
        # Blank line
        if not stripped:
            if in_table:
                html_lines.append("</tbody></table></div>")
                in_table = False
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue
            
        # Headers
        if stripped.startswith("# "):
            html_lines.append(f"<h1 class='doc-title'>{stripped[2:]}</h1>")
            continue
        elif stripped.startswith("## "):
            html_lines.append(f"<h2 class='section-title'>{stripped[3:]}</h2>")
            continue
        elif stripped.startswith("### "):
            html_lines.append(f"<h3 class='subsection-title'>{stripped[4:]}</h3>")
            continue
        elif stripped.startswith("#### "):
            html_lines.append(f"<h4 class='subsubsection-title'>{stripped[5:]}</h4>")
            continue
            
        # Horizontal rules
        if stripped == "---":
            html_lines.append("<hr class='divider'>")
            continue
            
        # Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            # Check separator line
            if all(re.match(r"^:?-+:?$", c) for c in cells):
                table_header = False
                continue
                
            if not in_table:
                in_table = True
                table_header = True
                html_lines.append("<div class='table-container'><table><thead><tr>")
                for c in cells:
                    html_lines.append(f"<th>{c}</th>")
                html_lines.append("</tr></thead><tbody>")
            else:
                html_lines.append("<tr>")
                for c in cells:
                    html_lines.append(f"<td>{c}</td>")
                html_lines.append("</tr>")
            continue
        elif in_table:
            html_lines.append("</tbody></table></div>")
            in_table = False
            
        # Unordered list
        if stripped.startswith("* ") or stripped.startswith("- "):
            content = stripped[2:]
            if not in_list:
                in_list = True
                html_lines.append("<ul>")
            html_lines.append(f"<li>{content}</li>")
            continue
        elif in_list:
            html_lines.append("</ul>")
            in_list = False
            
        # Ordered list
        m_ol = re.match(r"^(\d+)\.\s+(.*)", stripped)
        if m_ol:
            html_lines.append(f"<p class='ol-item'><b>{m_ol.group(1)}.</b> {m_ol.group(2)}</p>")
            continue
            
        # Blockquotes or callouts
        if stripped.startswith("> "):
            html_lines.append(f"<blockquote class='callout'>{stripped[2:]}</blockquote>")
            continue
            
        # Regular paragraph
        html_lines.append(f"<p>{stripped}</p>")

    if in_table:
        html_lines.append("</tbody></table></div>")
    if in_list:
        html_lines.append("</ul>")
        
    full_html = "\n".join(html_lines)
    
    # Inline formatting (bold, italic, code, links)
    full_html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", full_html)
    full_html = re.sub(r"\*(.*?)\*", r"<em>\1</em>", full_html)
    full_html = re.sub(r"`(.*?)`", r"<code>\1</code>", full_html)
    
    # Replace markdown links with HTML links or images
    def link_replacer(match):
        text, url = match.groups()
        if url.endswith(('.png', '.jpg', '.jpeg')):
            clean_url = url.replace("file:///c:/Users/Sachin/Desktop/talktomodel-replication/", "")
            return f"<div class='img-container'><img src='{clean_url}' alt='{text}'><p class='caption'>{text}</p></div>"
        return f"<a href='{url}' target='_blank'>{text}</a>"
        
    full_html = re.sub(r"\[(.*?)\]\((.*?)\)", link_replacer, full_html)
    return full_html

def main():
    md_file = "EXPERIMENTAL_RESULTS_DOCUMENT.md"
    out_file = "Experimental_Results_and_Comparison.html"
    
    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()
        
    body_html = markdown_to_html(md_text)
    
    styled_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>TalkToModel Phase 2 Experimental Results & Comparison</title>
<style>
  @page {{
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
  }}
  body {{
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.55;
    color: #2c3e50;
    max-width: 900px;
    margin: 0 auto;
    padding: 25px;
    background-color: #fff;
  }}
  h1.doc-title {{
    font-size: 24px;
    font-weight: 800;
    color: #1a365d;
    border-bottom: 3px solid #2b6cb0;
    padding-bottom: 8px;
    margin-top: 0;
  }}
  h2.section-title {{
    font-size: 18px;
    font-weight: 700;
    color: #2b6cb0;
    border-bottom: 1.5px solid #e2e8f0;
    padding-bottom: 5px;
    margin-top: 25px;
  }}
  h3.subsection-title {{
    font-size: 15px;
    font-weight: 700;
    color: #2d3748;
    margin-top: 18px;
    margin-bottom: 6px;
  }}
  h4.subsubsection-title {{
    font-size: 13px;
    font-weight: 600;
    color: #4a5568;
    margin-top: 12px;
  }}
  p, li {{
    font-size: 13px;
  }}
  .table-container {{
    margin: 12px 0 16px 0;
    overflow-x: auto;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    margin-bottom: 8px;
  }}
  th, td {{
    padding: 7px 10px;
    text-align: left;
    border: 1px solid #cbd5e0;
  }}
  th {{
    background-color: #edf2f7;
    font-weight: 700;
    color: #1a202c;
  }}
  tr:nth-child(even) {{
    background-color: #f7fafc;
  }}
  code {{
    background-color: #edf2f7;
    color: #805ad5;
    padding: 2px 5px;
    border-radius: 4px;
    font-family: Consolas, monospace;
    font-size: 11.5px;
  }}
  .callout {{
    background-color: #ebf8ff;
    border-left: 4px solid #3182ce;
    padding: 10px 14px;
    margin: 12px 0;
    font-size: 12.5px;
    border-radius: 0 4px 4px 0;
  }}
  .divider {{
    border: 0;
    height: 1px;
    background: #e2e8f0;
    margin: 20px 0;
  }}
  .img-container {{
    text-align: center;
    margin: 15px 0;
  }}
  .img-container img {{
    max-width: 100%;
    height: auto;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.06);
  }}
  .caption {{
    font-size: 11px;
    color: #718096;
    margin-top: 4px;
    font-style: italic;
  }}
  @media print {{
    body {{
      padding: 0;
    }}
    .table-container {{
      page-break-inside: avoid;
    }}
    h2.section-title {{
      page-break-after: avoid;
    }}
  }}
</style>
</head>
<body>
{body_html}
</body>
</html>"""

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(styled_html)
        
    print(f"Generated printable report HTML: {out_file}")
    print("To convert to PDF: Open this file in your browser and press Ctrl+P -> 'Save as PDF'.")

if __name__ == "__main__":
    main()

