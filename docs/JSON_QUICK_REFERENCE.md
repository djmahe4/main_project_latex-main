# JSON Files Quick Reference

Visual cheat sheet for the two JSON files in `docs/`.

---

## File Comparison at a Glance

```
┌──────────────────────────────────────────────────────────────────┐
│                     extracted_meta.json                          │
├──────────────────────────────────────────────────────────────────┤
│ STRUCTURE:  Array of objects                                     │
│ PURPOSE:    Raw codebase extraction                              │
│ CREATED BY: make scan → scan_codebase.py                        │
│ SIZE:       ~50 KB typical                                       │
│ EDIT:       ❌ Don't touch (auto-generated)                     │
│                                                                  │
│ [                                                                │
│   { "file": "src/main.py", "language": "py",                    │
│     "content": "\"\"\"Module docstring...\"\"\"", "type": "comment" },  │
│   { "file": "docs/arch.md", "language": "md",                   │
│     "content": "```mermaid...```", "type": "diagram" },          │
│   ...                                                            │
│ ]                                                                │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                     analysis_cache.json                          │
├──────────────────────────────────────────────────────────────────┤
│ STRUCTURE:  Object with sections                                 │
│ PURPOSE:    Project config + intelligence cache                 │
│ CREATED BY: macro_sync.py + agent proposals                     │
│ SIZE:       ~30 KB typical                                       │
│ EDIT:       ✅ Agent-safe (use proposals)                       │
│                                                                  │
│ {                                                                │
│   "project_name": "My Project",                                 │
│   "macros": { "\\tplProjectTitle": "...", ... },              │
│   "document_structure": { "chapters": [...] },                  │
│   "extracted_items": [...],                                     │
│   "mapping_proposals": [...],                                   │
│   "retrospective_report": { ... }                               │
│ }                                                                │
└──────────────────────────────────────────────────────────────────┘
```

---

## Formation Process

### extracted_meta.json

```
make scan
    ↓
Walk directory tree
    ↓
Find supported files (.py, .c, .cpp, .h, .ino, .js, .md, .sh)
    ↓
For each file:
  Apply language-specific regex patterns
  Extract comments/docstrings/diagrams
    ↓
Filter trivial comments (< 8 chars)
    ↓
Build JSON array with:
  - file path
  - language
  - content (full snippet)
  - type (comment or diagram)
    ↓
Save to docs/extracted_meta.json
```

### analysis_cache.json

```
manual init OR macro_sync.py
    ↓
Populate sections:
  ├─ project_name
  ├─ macros (read from config.tex)
  ├─ document_structure (chapters)
  ├─ extracted_items (copy from extracted_meta.json)
  ├─ mapping_proposals (auto-generate correlations)
  └─ retrospective_report (gap analysis)
    ↓
Save to docs/analysis_cache.json
    ↓
Agent reviews proposals and marks as:
  - pending (needs review)
  - accepted (generate LaTeX)
  - rejected (skip)
```

---

## Data Flow (Best Practice)

```
1️⃣ make scan              extracted_meta.json    (codebase → JSON)
                                  ↓
2️⃣ make sync              analysis_cache.json    (config + extracted)
                                  ↓
3️⃣ Agent reviews          analysis_cache.json    (mark proposals)
                                  ↓
4️⃣ make all + generate    chapters/generated/    (LaTeX from proposals)
```

---

## Key Fields Explained

### extracted_meta.json

```json
{
  "file": "path/to/source.py",        /* Relative path from root */
  "language": "py",                   /* File type: py,cpp,c,sh,js,md */
  "content": "Full comment text",      /* May span multiple lines */
  "type": "comment"                   /* "comment" OR "diagram" */
}
```

### analysis_cache.json

```json
{
  "project_name": "...",              /* Title */

  "macros": {                         /* \tpl* LaTeX macros */
    "\\tplProjectTitle": "value",
    "\\tplStudentA": "Name",
    ...
  },

  "document_structure": {             /* Chapter definitions */
    "chapters": [
      { "id": "chap_1", "title": "...", "file": "...", },
      ...
    ]
  },

  "extracted_items": [                /* Linked to extracted_meta.json */
    { "id": "ext_1", "file": "...", "content": "...", "linked": false }
  ],

  "mapping_proposals": [              /* Code → Chapter suggestions */
    {
      "item_id": "ext_1",
      "chapter_id": "chap_5",
      "confidence": 0.92,
      "status": "pending",            /* accepted/rejected/pending */
      "reasoning": "..."
    }
  ],

  "retrospective_report": {           /* Gap analysis */
    "issues": ["..."],
    "suggestions": ["..."],
    "unmapped_items": ["ext_2", "ext_5"],
    "undocumented_chapters": ["chap_7"]
  }
}
```

---

## Common Commands

### Generate / Update

```bash
# Scan all source files for documentation
make scan

# Sync metadata to config + generate proposals
make sync

# View extracted metadata
cat docs/extracted_meta.json | jq '.'

# View project metadata in cache
cat docs/analysis_cache.json | jq '.macros'
```

### Analyze

```bash
# Count snippets by language
cat docs/extracted_meta.json | jq 'group_by(.language) | map({lang: .[0].language, count: length})'

# Find all diagrams
cat docs/extracted_meta.json | jq '.[] | select(.type == "diagram")'

# View pending proposals
cat docs/analysis_cache.json | jq '.mapping_proposals[] | select(.status == "pending")'

# See unmapped items (gap analysis)
cat docs/analysis_cache.json | jq '.retrospective_report.unmapped_items'
```

### Edit

```bash
# Manually update a proposal
nano docs/analysis_cache.json

# Regenerate cache after manual edits
make sync
```

---

## Language Support (scan_codebase.py)

| Language | Extensions | Comment Pattern |
|----------|-----------|-----------------|
| Python | `.py` | `"""docstrings"""`, `#comments` |
| C | `.c` | `/* */`, `//` |
| C++ | `.cpp`, `.h` | `/* */`, `//` |
| Arduino | `.ino` | `/* */`, `//` |
| JavaScript | `.js` | `/* */`, `//` |
| Shell | `.sh` | `#comments` |
| Markdown | `.md` | ` ```mermaid...``` ` |

Ignored directories: `.git`, `node_modules`, `vendor`, `.gemini`, `logs`

---

## Size Reference

| Project Type | Lines of Code | extracted_meta.json | analysis_cache.json |
|---|---|---|---|
| Tiny | < 1K LOC | 2–5 KB | 20 KB |
| Small | 1K–5K | 5–10 KB | 25 KB |
| Medium | 5K–50K | 20–50 KB | 30–40 KB |
| Large | 50K–500K | 100–300 KB | 50–100 KB |
| Huge | > 500K | 500+ KB | 150+ KB |

**Tip:** Remove old comments before scanning to keep files smaller.

---

## When to Use Each

### Use extracted_meta.json for:
- ✅ Browsing all extracted documentation
- ✅ Finding specific code snippets by language
- ✅ Identifying where diagrams are
- ✅ Searching for comments containing keywords

### Use analysis_cache.json for:
- ✅ Getting project metadata (title, authors, etc.)
- ✅ Viewing chapter structure
- ✅ Checking mapping proposals
- ✅ Gap analysis (undocumented chapters)
- ✅ Agent processing (read + update proposals)

---

## JSON Validation

Check file integrity:

```bash
# Validate extracted metadata
python -m json.tool docs/extracted_meta.json > /dev/null && echo "✓ Valid"

# Validate analysis cache
python -m json.tool docs/analysis_cache.json > /dev/null && echo "✓ Valid"

# Pretty-print (readable format)
python -m json.tool docs/extracted_meta.json | less
```

---

## Troubleshooting Table

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| `extracted_meta.json` is empty | No code files matched | Check file extensions; ensure comments > 8 chars |
| `extracted_meta.json` is huge | Too many trivial comments | Clean up comments; use `--ignore` to skip dirs |
| `analysis_cache.json` not updating | Need to re-scan first | Run `make scan` then `make sync` |
| Wrong mappings | Tags not recognized | Use format: `@title: Value` in code |
| File corruption | Manual editing error | Restore from git: `git checkout docs/*.json` |

---

## For Agents

When processing these files:

1. **READ** analysis_cache.json
2. **FILTER** mapping_proposals where status == "pending"
3. **LOOKUP** corresponding item in extracted_items
4. **GENERATE** LaTeX content
5. **UPDATE** proposal status → "accepted"
6. **WRITE** back analysis_cache.json

```python
# Pseudo-code
cache = json.load('docs/analysis_cache.json')
for prop in cache['mapping_proposals']:
    if prop['status'] == 'pending':
        item = cache['extracted_items'][prop['item_id']]
        chapter = cache['document_structure']['chapters'][prop['chapter_id']]
        tex = generate_latex(item, chapter)
        write_file(f"chapters/generated/{prop['id']}.tex", tex)
        prop['status'] = 'accepted'
json.dump(cache, 'docs/analysis_cache.json')
```

---

## Best Practices

✅ **DO:**
- Run `make scan` before `make sync`
- Review gap analysis in retrospective_report
- Mark proposals as "accepted" before generating LaTeX
- Commit analysis_cache.json (not extracted_meta.json)
- Use @tags in code for automatic sync

❌ **DON'T:**
- Edit extracted_meta.json manually (regenerated by make scan)
- Commit large extracted_meta.json (100+ KB)
- Ignore gap analysis issues (may miss documentation)
- Skip proposal review before accepting

---

## See Also

- **Full Documentation:** `docs/JSON_SCHEMA_DOCUMENTATION.md`
- **Extraction Script:** `skills/latex-template-architect/scripts/scan_codebase.py`
- **Sync Script:** `skills/latex-template-architect/scripts/macro_sync.py`
- **Automation Workflows:** `skills/latex-template-architect/workflows.md`
