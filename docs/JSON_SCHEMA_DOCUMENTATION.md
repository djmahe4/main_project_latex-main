# JSON Files Documentation

Complete guide to understanding the JSON files in the `docs/` directory and how they are formed.

## Overview

The LaTeX Template Architect uses two JSON files as the **intelligence layer** for AI-driven documentation generation:

| File | Purpose | Created By | Size | Updated |
|------|---------|-----------|------|---------|
| `docs/extracted_meta.json` | Raw codebase metadata extraction | `scan_codebase.py` | ~50KB avg | `make scan` |
| `docs/analysis_cache.json` | Curated cache + project config | `macro_sync.py` + manual | ~30KB avg | `make sync` or agent |

---

## 1. `extracted_meta.json` (Codebase Extraction Output)

### Purpose
Stores **raw extracted documentation** from project source code. Acts as an intelligence cache for comment scanning, docstrings, and Mermaid diagrams.

### Formation Process

```
Step 1: User runs → make scan
                    ↓
Step 2: scan_codebase.py starts
        - Walks entire project tree
        - Skips: .git, node_modules, vendor, .gemini, logs
        - Finds files: .py, .c, .cpp, .h, .ino, .js, .md, .sh
                    ↓
Step 3: For each file, extract comments using regex:
        - Python:  """docstrings""", '''docstrings''', #comments
        - C/C++:   /* block comments */, //line comments
        - Shell:   #comments only
        - Mermaid: ```mermaid...``` code blocks in .md
                    ↓
Step 4: Filter out trivial comments (< 8 chars)
                    ↓
Step 5: Build JSON array with extracted items
                    ↓
Step 6: Write to docs/extracted_meta.json
```

### Schema & Structure

```json
[
  {
    "file": "path/to/source/file.py",
    "language": "py",
    "content": "Full extracted comment or docstring text",
    "type": "comment" or "diagram"
  },
  {
    "file": "docs/architecture.md",
    "language": "md",
    "content": "```mermaid\ngraph TD\n  A --> B\n```",
    "type": "diagram"
  }
]
```

### Field Descriptions

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `file` | string | `src/main.py` | Relative path from project root |
| `language` | string | `py`, `cpp`, `sh`, `md` | File extension (without `.`) |
| `content` | string | Full comment text | May span multiple lines; preserves formatting |
| `type` | string | `"comment"` or `"diagram"` | Auto-detected: "diagram" if contains "mermaid" |

### Example: Real Output

```json
[
  {
    "file": "compile.sh",
    "language": "sh",
    "content": "#!/bin/bash",
    "type": "comment"
  },
  {
    "file": "src/main.py",
    "language": "py",
    "content": "\"\"\"\nModule: Main Controller\nThis module handles central logic.\n\"\"\"",
    "type": "comment"
  },
  {
    "file": "docs/system.md",
    "language": "md",
    "content": "```mermaid\ngraph LR\n  Input --> Processing --> Output\n```",
    "type": "diagram"
  },
  {
    "file": "firmware/sensor.ino",
    "language": "ino",
    "content": "// @component: Sensor Firmware\n// @logic: Read data every 100ms",
    "type": "comment"
  }
]
```

### Key Characteristics

✅ **Flat Array** — No nesting; each item is independent
✅ **Language-Agnostic** — Supports 8+ programming languages
✅ **Preserves Formatting** — Keeps indentation and newlines
✅ **Searchable** — Easy to grep/filter by language or content
✅ **Raw Data** — No processing or transformation applied (yet)

### Generation Command

```bash
make scan
# OR
python scripts/scan_codebase.py --source . --output docs/extracted_meta.json --ignore .git node_modules vendor
```

### Customization

```bash
# Scan specific directory only
make scan --source src/

# Custom output location
python scripts/scan_codebase.py --source . --output my_metadata.json

# Custom ignore list
python scripts/scan_codebase.py --ignore .git __pycache__ .env
```

### Size Management

Typical file sizes:
- Small project (< 5K LOC): 5–10 KB
- Medium project (5K–50K LOC): 20–50 KB
- Large project (> 50K LOC): 100 KB+

**Optimize by:**
- Excluding unnecessary directories via `--ignore`
- Cleaning old comments before scanning
- Using focused comment blocks only

---

## 2. `analysis_cache.json` (Curated Configuration Cache)

### Purpose
**Master configuration file** containing:
1. Project metadata (title, authors, faculty)
2. Document structure (chapter definitions)
3. Extracted items (references to `extracted_meta.json`)
4. Mapping proposals (code → chapter assignments)
5. Retrospective analysis (gaps, issues, suggestions)

### Formation Process

```
Step 1: analysis_cache.json initialized manually OR via agent
                    ↓
Step 2: Populate with project details:
        - Read Preamble/config.tex
        - Extract \tpl* macro values
        - Store in "macros" section
        - Create "document_structure" with chapter list
                    ↓
Step 3: Link extracted_meta.json results:
        - Copy extracted items into "extracted_items"
        - Create "mapping_proposals" (code → chapters)
                    ↓
Step 4: Run gap analysis:
        - Find unmapped code
        - Identify undocumented chapters
        - Store in "retrospective_report"
                    ↓
Step 5: Write to docs/analysis_cache.json
        (or update existing with new proposals)
```

### Schema & Structure

```json
{
  "project_name": "string",
  "macros": {
    "\\tplKey": "value",
    "...": "..."
  },
  "document_structure": {
    "chapters": [
      { "id": "chap_id", "title": "Chapter Title", "file": "path/to/file.tex" },
      "..."
    ]
  },
  "extracted_items": [
    { "id": "item_1", "file": "source_file", "content": "snippet", "linked": false },
    "..."
  ],
  "mapping_proposals": [
    { "item_id": "item_1", "chapter_id": "chap_5", "confidence": 0.85, "status": "pending" },
    "..."
  ],
  "retrospective_report": {
    "issues": [ "List of issues found", "..." ],
    "suggestions": [ "Suggestions for improvement", "..." ],
    "last_analysis": "2026-03-30T17:21:25Z"
  },
  "last_updated": "ISO timestamp"
}
```

### Field Descriptions

#### 1. `project_name` (string)
Project title extracted from config or provided by user.

```json
"project_name": "FIRMAI: AI-Powered IoT Firmware Vulnerability Analyzer"
```

#### 2. `macros` (object)
All `\tpl*` LaTeX macros and their current values. Used by:
- `macro_sync.py` to auto-update config.tex
- Agents to retrieve project metadata
- PDF generation for cover pages

```json
"macros": {
  "\\tplProjectTitle": "FIRMAI: AI-Powered IoT Firmware...",
  "\\tplStudentA": "ABHIRAM G NAIR",
  "\\tplRegA": "PRC22CSOT001",
  "\\tplCourseName": "Project Phase II",
  "\\tplDepartmentName": "Internet of Things & Cyber Security",
  "\\tplCollegeName": "Providence College of Engineering, Chengannur",
  "\\tplProjectGuide": "Ms. Praseetha S Nair",
  "...": "..."
}
```

#### 3. `document_structure` (object)
Defines expected chapters and their mappings.

```json
"document_structure": {
  "chapters": [
    {
      "id": "chap_intro",
      "title": "Introduction",
      "file": "chapters/ch1_introduction.tex"
    },
    {
      "id": "chap_lit",
      "title": "Literature Review",
      "file": "chapters/ch2_literature_review.tex"
    },
    {
      "id": "chap_method",
      "title": "Methodology",
      "file": "chapters/ch4_methodology.tex"
    },
    "..."
  ]
}
```

#### 4. `extracted_items` (array)
References to extracted code/documentation. Each item:
- Comes from `extracted_meta.json`
- Has unique ID for tracking
- Marked as linked/unlinked

```json
"extracted_items": [
  {
    "id": "ext_001",
    "file": "src/main.py",
    "language": "py",
    "content": "\"\"\"Main Controller Module\"\"\"",
    "type": "comment",
    "linked": false,  // Not yet assigned to any chapter
    "confidence": null
  },
  {
    "id": "ext_002",
    "file": "docs/architecture.md",
    "language": "md",
    "content": "```mermaid graph...```",
    "type": "diagram",
    "linked": true,  // Assigned to a chapter
    "confidence": 0.92
  }
]
```

#### 5. `mapping_proposals` (array)
Suggestions for which code snippets belong in which chapters.

```json
"mapping_proposals": [
  {
    "item_id": "ext_001",
    "chapter_id": "chap_intro",
    "confidence": 0.78,
    "status": "pending",  // "pending", "accepted", "rejected"
    "reasoning": "Project overview should include main architecture",
    "suggested_section": "1.2 Architecture Overview"
  },
  {
    "item_id": "ext_002",
    "chapter_id": "chap_design",
    "confidence": 0.95,
    "status": "accepted",
    "reasoning": "Mermaid diagram directly relates to system design chapter"
  }
]
```

#### 6. `retrospective_report` (object)
Gap analysis results showing what's missing or needs improvement.

```json
"retrospective_report": {
  "issues": [
    "Chapter 7 (Testing) has no extracted documentation",
    "3 code snippets are not linked to any chapter",
    "Sensor firmware module (IoT code) lacks docstrings"
  ],
  "suggestions": [
    "Add testing documentation to src/tests/",
    "Create docstrings for firmware module",
    "Add architecture diagram to system design chapter"
  ],
  "last_analysis": "2026-03-30T17:21:25Z",
  "unmapped_items": ["ext_005", "ext_006", "ext_012"],
  "undocumented_chapters": ["chap_test", "chap_concl"]
}
```

#### 7. `last_updated` (ISO timestamp)
When the cache was last updated.

```json
"last_updated": "2026-03-30T17:21:25Z"
```

### Complete Example

```json
{
  "project_name": "FIRMAI: AI-Powered IoT Firmware Vulnerability Analyzer",
  "macros": {
    "\\tplProjectTitle": "FIRMAI: AI-Powered IoT Firmware Vulnerability Analyzer",
    "\\tplCourseName": "Project Phase II",
    "\\tplCourseCode": "coursecode",
    "\\tplProjectYear": "March 2026",
    "\\tplDepartmentName": "Internet of Things & Cyber Security (CSOT)",
    "\\tplCollegeName": "Providence College of Engineering, Chengannur",
    "\\tplRomanFont": "Times New Roman",
    "\\tplSansFont": "Arial",
    "\\tplMonoFont": "Courier New",
    "\\tplMonoFontColor": "0019D4",
    "\\tplSubmissionDate": "\\today",
    "\\tplStudentA": "ABHIRAM G NAIR",
    "\\tplRegA": "PRC22CSOT001",
    "\\tplStudentB": "NAVOMI TITUS",
    "\\tplRegB": "PRC22CSOT019",
    "\\tplStudentC": "SPANDANA NAIR",
    "\\tplRegC": "PRC22CSOT025",
    "\\tplStudentD": "VIGNESH S KUMAR",
    "\\tplRegD": "PRC22CSOT028",
    "\\tplPrincipalName": "PrincipalName",
    "\\tplHODName": "Ms. Salitha M.K",
    "\\tplProjectGuide": "Ms. Praseetha S Nair",
    "\\tplProjectGuideDesignation": "Assistant Professor",
    "\\tplProjectCoordinator": "Ms. Salitha M.K",
    "\\tplProjectCoordinatorDesignation": "Assistant Professor"
  },
  "document_structure": {
    "chapters": [
      { "id": "chap_intro", "title": "Introduction", "file": "chapters/ch1_introduction.tex" },
      { "id": "chap_lit", "title": "Literature Review", "file": "chapters/ch2_literature_review.tex" },
      { "id": "chap_analysis", "title": "System Analysis", "file": "chapters/ch3_system_analysis.tex" },
      { "id": "chap_method", "title": "Methodology", "file": "chapters/ch4_methodology.tex" },
      { "id": "chap_design", "title": "System Design", "file": "chapters/ch5_system_design.tex" },
      { "id": "chap_impl", "title": "System Implementation", "file": "chapters/ch6_system_implementation.tex" },
      { "id": "chap_test", "title": "Testing", "file": "chapters/ch7_testing.tex" },
      { "id": "chap_results", "title": "Results", "file": "chapters/ch8_results.tex" },
      { "id": "chap_concl", "title": "Conclusions", "file": "chapters/ch9_conclusions.tex" }
    ]
  },
  "extracted_items": [],
  "mapping_proposals": [],
  "retrospective_report": {
    "issues": [],
    "suggestions": [],
    "last_analysis": null
  },
  "last_updated": "2026-03-30T17:21:25Z"
}
```

---

## 3. Data Flow: How They Work Together

### Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ User Project (Cloned Template)                                  │
│  ├── main.tex                                                   │
│  ├── Preamble/config.tex           ← User fills project details │
│  ├── chapters/*.tex                                             │
│  ├── src/ (optional project code)  ← Source for scanning       │
│  └── docs/                                                       │
│      ├── analysis_cache.json       ← This file                  │
│      └── extracted_meta.json       ← This file                  │
└─────────────────────────────────────────────────────────────────┘
                        │
                        │ "make scan"
                        ▼
        ┌───────────────────────────────┐
        │ scan_codebase.py              │
        │ • Walk source tree            │
        │ • Extract comments/diagrams   │
        │ • Apply language regex        │
        └───────────────────────────────┘
                        │
                        │ writes
                        ▼
        ┌───────────────────────────────┐
        │ extracted_meta.json (NEW)     │
        │ [                             │
        │   { "file": "...",            │
        │     "language": "py",         │
        │     "content": "...",         │
        │     "type": "comment" },      │
        │   ...                         │
        │ ]                             │
        └───────────────────────────────┘
                        │
                        │ "make sync"
                        ▼
        ┌───────────────────────────────┐
        │ macro_sync.py                 │
        │ • Read config.tex macros      │
        │ • Read extracted_meta.json    │
        │ • Match @tags to macros       │
        │ • Generate mappings           │
        └───────────────────────────────┘
                        │
                        │ updates / writes
                        ▼
        ┌───────────────────────────────┐
        │ analysis_cache.json (UPDATED) │
        │ {                             │
        │   "project_name": "...",      │
        │   "macros": {...},            │
        │   "document_structure": {...},│
        │   "extracted_items": [...],   │
        │   "mapping_proposals": [...], │
        │   "retrospective_report": {...}
        │ }                             │
        └───────────────────────────────┘
                        │
        Agent / Developer reviews & accepts proposals
                        │
                        ▼
        ┌───────────────────────────────┐
        │ Analysis Cache (FINALIZED)    │
        │ (Mapping proposals marked     │
        │  as "accepted")               │
        └───────────────────────────────┘
                        │
                        │ Agent reads proposals
                        ▼
        ┌───────────────────────────────┐
        │ Generate LaTeX Chapters       │
        │ chapters/generated/*.tex      │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │ "make all"                    │
        │ (Full LaTeX compilation)      │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │ examples/main.pdf (FINAL)     │
        └───────────────────────────────┘
```

---

## 4. Interaction Between JSON Files

| Phase | File | Role | Action |
|-------|------|------|--------|
| **Scan** | `extracted_meta.json` | Primary output | Stores all extracted snippets |
| **Sync** | `extracted_meta.json` | Input | Read to find @tags |
| **Sync** | `analysis_cache.json` | Output | Update with extracted items + proposals |
| **Mapping** | `analysis_cache.json` | Configuration | Agent reads proposals |
| **Mapping** | `extracted_meta.json` | Reference | Lookup snippet details by ID |
| **Retrospect** | `analysis_cache.json` | Report | Gap analysis results |

---

## 5. Key Differences

### extracted_meta.json

✅ **What it is:**
- Raw extraction results
- Array-based (flat, simple)
- Output of `scan_codebase.py`
- Read-only (don't edit manually)

❌ **Not for:**
- Project configuration
- Manual editing
- Human-readable documentation

### analysis_cache.json

✅ **What it is:**
- Master cache + configuration
- Object-based (hierarchical)
- Curated by agent + user input
- Central intelligence store

❌ **NOT:**
- Generated by Python scripts alone
- Overwritten by `make scan`
- Replaceable by manual config

**Key:** `extracted_meta.json` is A **temporary working cache**, while `analysis_cache.json` is the **persistent project intelligence store**.

---

## 6. Common Operations

### View All Extracted Code

```bash
# Pretty-print extracted metadata
cat docs/extracted_meta.json | jq '.'

# Count snippets by language
cat docs/extracted_meta.json | jq 'group_by(.language) | map({language: .[0].language, count: length})'

# Find all diagrams
cat docs/extracted_meta.json | jq '.[] | select(.type == "diagram")'

# Export just the content
cat docs/extracted_meta.json | jq '.[] | .content' > all_docs.txt
```

### Check Project Metadata in Cache

```bash
# View all project macros
cat docs/analysis_cache.json | jq '.macros'

# View chapter structure
cat docs/analysis_cache.json | jq '.document_structure.chapters'

# Find mapping proposals for a specific chapter
cat docs/analysis_cache.json | jq '.mapping_proposals[] | select(.chapter_id == "chap_design")'

# List all undocumented chapters
cat docs/analysis_cache.json | jq '.retrospective_report.undocumented_chapters'
```

### Update Extracted Items Manually

If you need to manually fix a mapping:

```bash
# Edit the analysis_cache.json
nano docs/analysis_cache.json

# Change status from "pending" to "accepted"
# OR add new mapping manually

# Restart cache generation
make sync
```

---

## 7. Troubleshooting

### Issue: `extracted_meta.json` is empty

**Cause:** No code files matched patterns, or all ignored.

**Solution:**
```bash
# Check what's being scanned
python scripts/scan_codebase.py --source . --ignore .git

# Verify file extensions are supported (.py, .c, .cpp, .h, .ino, .js, .md, .sh)
# Check files don't have trivial comments (< 8 chars)
```

### Issue: `analysis_cache.json` not updating

**Cause:** `extracted_meta.json` not regenerated.

**Solution:**
```bash
make scan  # Force re-extract
make sync  # Then re-sync
```

### Issue: Wrong mappings in cache

**Cause:** `@tag` format in code comments not recognized.

**Solution:**
```python
# Use this format in code:
# @title: My Project
# @guide: Professor Name

# Or check MAPPING_RULES in macro_sync.py
```

---

## 8. Integration with Agent Automation

When an agent processes the cache:

1. **Read** `analysis_cache.json`
2. **Extract** `mapping_proposals` where `status == "pending"`
3. **Review** `retrospective_report.issues`
4. **Generate** LaTeX for accepted proposals
5. **Update** `mapping_proposals[].status` to "accepted"
6. **Write** back to `docs/analysis_cache.json`

Example agent flow:
```python
import json

# Load cache
with open('docs/analysis_cache.json') as f:
    cache = json.load(f)

# Find pending proposals
pending = [p for p in cache['mapping_proposals'] if p['status'] == 'pending']

# Process each
for proposal in pending:
    item = cache['extracted_items'][proposal['item_id']]
    chapter = proposal['chapter_id']

    # Generate LaTeX content from item + chapter context
    tex_content = generate_tex(item, cache['document_structure'], chapter)

    # Write to generated file
    with open(f"chapters/generated/{chapter}_{item['id']}.tex", 'w') as f:
        f.write(tex_content)

    # Mark as accepted
    proposal['status'] = 'accepted'

# Save updated cache
with open('docs/analysis_cache.json', 'w') as f:
    json.dump(cache, f, indent=2)
```

---

## 9. JSON Schema Validation

For IDE/tool integration, here's the schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "LaTeX Template - Extracted Metadata",
  "type": "array",
  "items": {
    "type": "object",
    "required": ["file", "language", "content", "type"],
    "properties": {
      "file": { "type": "string" },
      "language": { "type": "string", "enum": ["py", "cpp", "c", "h", "ino", "js", "sh", "md"] },
      "content": { "type": "string" },
      "type": { "type": "string", "enum": ["comment", "diagram"] }
    }
  }
}
```

---

## Summary

| Aspect | extracted_meta.json | analysis_cache.json |
|--------|------------------|------------------|
| **Type** | Array | Object |
| **Created By** | scan_codebase.py | macro_sync.py + agent |
| **Size** | ~50 KB (typical) | ~30 KB (typical) |
| **Frequency** | Regenerated per scan | Updated per sync/agent |
| **Editable?** | No (auto-generated) | Yes (agent-safe) |
| **Purpose** | Raw code extraction | Project intelligence |
| **User Modified?** | Never directly | Via agent proposals |

---

## See Also

- `skills/latex-template-architect/skill.md` — Automation workflows
- `Preamble/config.tex` — Macro definitions (stored in analysis_cache.json)
- `skills/latex-template-architect/scripts/scan_codebase.py` — Extraction logic
- `skills/latex-template-architect/scripts/macro_sync.py` — Sync logic
