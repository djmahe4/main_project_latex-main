import json
import os
import re
import argparse

# Config
META_PATH = "skills/docs/extracted_meta.json"
CHAPTERS_DIR = "chapters"
OUTPUT_MARKER = "%% --- FOOTYDJ AUTOSYNC BEGIN ---"
END_MARKER = "%% --- FOOTYDJ AUTOSYNC END ---"

def clean_latex(text):
    if "[" in text and "]" in text:
        # Check if they match global config macros
        text = text.replace("[FastAPI Backend]", "\\tplFastAPI")
        text = text.replace("[Google Gemini]", "\\tplGemini")
        text = text.replace("[Tactical RAG Agent]", "\\tplRAG")
        text = text.replace("[VectorDB]", "\\tplVectorDB")
        # Strip remaining bracketed noise
        text = re.sub(r'\[([a-zA-Z0-9_ -]{3,})\]', r'\1', text)

    # Escape common LaTeX characters for raw text
    return text.replace("_", "\\_").replace("#", "\\#").replace("&", "\\&").replace("$", "\\$").replace("%", "\\%")

def markdown_to_latex(text, entry_type="comment"):
    """Converts basic Markdown structures to LaTeX."""
    if entry_type == "list":
        lines = text.split('\n')
        latex_lines = ["\\begin{itemize}"]
        for line in lines:
            item = re.sub(r'^[ \t]*[-*+][ \t]*', '', line).strip()
            if item:
                latex_lines.append(f"  \\item {clean_latex(item)}")
        latex_lines.append("\\end{itemize}")
        return "\n".join(latex_lines)
    
    if entry_type == "table":
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if len(lines) < 2: return clean_latex(text)
        
        # Simple markdown table parser
        rows = []
        for line in lines:
            if '---|' in line: continue # skip separator
            cols = [col.strip() for col in line.split('|') if col.strip()]
            if cols: rows.append(cols)
        
        if not rows: return clean_latex(text)
        
        col_count = len(rows[0])
        col_def = "|" + "c|" * col_count
        latex_table = [f"\\begin{{center}}\n\\begin{{tabular}}{{{col_def}}}\n\\hline"]
        for i, row in enumerate(rows):
            latex_row = " & ".join([clean_latex(c) for c in row]) + " \\\\"
            latex_table.append(latex_row + " \\hline")
        latex_table.append("\\end{tabular}\n\\end{center}")
        return "\n".join(latex_table)

    if text.startswith("#"):
        level = text.count("#", 0, text.find(" "))
        header_text = text.lstrip("# ").strip()
        if level == 1: return f"\\section{{{clean_latex(header_text)}}}"
        if level == 2: return f"\\subsection{{{clean_latex(header_text)}}}"
        return f"\\subsubsection{{{clean_latex(header_text)}}}"

    return clean_latex(text)

def sync_chapters():
    if not os.path.exists(META_PATH):
        print(f"Error: {META_PATH} not found.")
        return

    with open(META_PATH, "r", encoding="utf-8") as f:
        meta_data = json.load(f)

    # Group by chapter
    chapters = {}
    for entry in meta_data:
        ch = entry.get("chapter", "appendices")
        if ch not in chapters:
            chapters[ch] = []
        chapters[ch].append(entry)

    for ch_id, entries in chapters.items():
        if ch_id == "INTERNAL": continue
        
        file_path = os.path.join(CHAPTERS_DIR, f"{ch_id}.tex")
        if not os.path.exists(file_path):
            print(f"Skipping {ch_id}: File not found.")
            continue

        # Build content block
        latex_content = [f"\n{OUTPUT_MARKER}\n"]
        
        # Organize by file to avoid repeating file headers
        files_seen = {}
        for entry in entries:
            fname = entry["file"]
            if fname not in files_seen:
                latex_content.append(f"\\subsection{{Source: {clean_latex(fname)}}}\n")
                files_seen[fname] = True
            
            content = entry["content"]
            entry_type = entry.get("type", "comment")
            
            # SKIP: Consumed entries that are now part of a narrative
            if entry_type == "consumed":
                continue

            if entry_type == "diagram":
                # Look for pre-converted TikZ content in tikz_library.json
                tikz_path = os.path.join(os.path.dirname(__file__), "tikz_library.json")
                tikz_content = None
                if os.path.exists(tikz_path):
                    with open(tikz_path, "r", encoding="utf-8") as f_tikz:
                        library = json.load(f_tikz)
                        clean_m = content.replace("```mermaid", "").replace("```", "").strip()
                        for m_key, t_val in library.items():
                            if m_key.strip() in clean_m:
                                tikz_content = t_val
                                break
                
                if tikz_content:
                    latex_content.append(f"%% --- TIKZ DIAGRAM START ---\n{tikz_content}\n%% --- TIKZ DIAGRAM END ---\n")
                else:
                    latex_content.append(f"%% [MERMAID_DIAGRAM_START]\n{content}\n%% [MERMAID_DIAGRAM_END]\n")
            else:
                # Resolve placeholders in ANY entry that isn't a diagram (which is handled above)
                content = clean_latex(content)
                
                # FINAL FAILSAFE: If placeholders like [above] still exist, they are likely diagram noise
                content = re.sub(r'\[(above|below|left|right|User|Frontend UI|frag_[0-9]+|r1 r2 t|3x3|DEBUG|playerIndex|alt)\]', '', content, flags=re.IGNORECASE)
                
                if entry_type == "narrative":
                    # Strip LLM chatter
                    content = re.sub(r'^(Here is the|Sure, here is|.*converted narrative paragraph.*?:)', '', content, flags=re.IGNORECASE).strip()
                    latex_content.append(f"{content}\n\n")
                elif entry_type == "comment" and (content.count('{') != content.count('}') or "[" in content or "_" in content):
                    # SAFETY: If it looks like code or has leftovers, wrap in verbatim
                    latex_content.append(f"\\begin{{verbatim}}\n{content}\n\\end{{verbatim}}\n\n")
                else:
                    converted = markdown_to_latex(content, entry_type)
                    latex_content.append(f"{converted}\n\n")

        latex_content.append(f"{END_MARKER}\n")
        new_block = "".join(latex_content)

        # Update file
        with open(file_path, "r", encoding="utf-8") as f:
            full_text = f.read()

        if OUTPUT_MARKER in full_text:
            # Overwrite between markers
            pattern = re.compile(rf"{re.escape(OUTPUT_MARKER)}.*?{re.escape(END_MARKER)}", re.DOTALL)
            updated_text = pattern.sub(new_block.replace('\\', '\\\\'), full_text)
        else:
            # Append to bottom
            updated_text = full_text.rstrip() + "\n" + new_block

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_text)
        print(f"Updated {ch_id}.tex")

if __name__ == "__main__":
    sync_chapters()
