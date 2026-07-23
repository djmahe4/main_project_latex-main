# Code Documentation Architect Skill

> **Universal SDLC Artifact Documentation Protocol** — Reusable across any software project

---

## 📚 What This Skill Does

Bridges **source code** and **documentation** by:
1. Extracting structured metadata (`@doc:*` annotations) from code
2. Validating bidirectional mappings (code ↔ docs)
3. Generating formatted documentation (LaTeX, Markdown, HTML)
4. Ensuring traceability across the entire SDLC

---

## 🎯 Design Principle

**This skill is project-agnostic.** It defines a universal protocol that can be:
- ✅ Applied to **any software project** (Python, Java, C++, JavaScript, etc.)
- ✅ Used with **any documentation backend** (LaTeX, Markdown, Sphinx, etc.)
- ✅ Customized for **specific project needs** (see `customization.md`)

---

## 📂 Skill Structure

```
code-documentation-architect/
├── README.md                    ← You are here
├── skill.md                     ← Universal protocol (33KB) — AI-model friendly
├── rules.md                     ← Mapping rules & constraints (modular reference)
├── protocols.md                 ← SDLC checkpoints & verification gates 
├── customization.md             ← FootyDJ-specific configuration
└── scripts/
    ├── extract_code_docs.py     (TODO)
    ├── validate_mappings.py     (TODO)
    ├── generate_tables.py       (TODO)
    └── lint_docstrings.py       (TODO)
```

---

## 🚀 Quick Start

### 1. Read the Universal Skill

Start with **[skill.md](./skill.md)** to understand:
- Core concepts and annotation protocol
- Phase-by-phase artifact documentation
- Bidirectional mapping workflow

### 2. Review Project-Specific Customization

For FootyDJ, read **[customization.md](./customization.md)**:
- Chapter mappings
- Component-specific fields
- LaTeX output format

### 3. Use Reference Documents

**For quick lookup:**
- **[rules.md](./rules.md)** — Artifact ID mapping table, constraints, error codes
- **[protocols.md](./protocols.md)** — SDLC checkpoints, quality gates, escalation procedures

### 4. Implement Scripts

Implement or use:
```bash
make extract      # Parse @doc:* annotations
make validate     # Cross-check code ↔ docs
make generate     # Create .tex snippets
make lint         # Enforce docstring format
make sync         # Full extraction → validation → generation
```

---

## 📋 Artifact ID Reference

| Phase | Prefix | Chapter | Example |
| :--- | :--- | :--- | :--- |
| 📋 Requirements | `REQ-`, `USE-CASE-` | Ch. 3 | `REQ-001` |
| 🏗️ Design | `ARCH-`, `SEQ-`, `CLASS-` | Ch. 5 | `ARCH-001` |
| 💻 Implementation | `CODE-`, `API-`, `CONFIG-` | Ch. 6 | `CODE-001` |
| ✅ Testing | `TC-`, `TEST-SUITE-` | Ch. 7 | `TC-001` |
| 📊 Results | `PERF-`, `METRIC-`, `COVERAGE-` | Ch. 8 | `PERF-001` |

---

## 🔄 Workflow Example

### Write Code with Annotations

```python
# src/module.py
"""
@doc:chapter: System Implementation
@doc:section: Core Module
@doc:artifact_id: CODE-001
@doc:title: My Module
@doc:description: Does X, Y, Z.
"""
```

### Extract Metadata

```bash
make extract
# → docs/code_metadata.json
```

### Validate Mappings

```bash
make validate
# → docs/mapping_graph.json (all code ↔ docs links)
```

### Generate Documentation

```bash
make generate
# → Updated ch6_system_implementation.tex
```

### Build Final Output

```bash
latexmk -pdf main.tex  # or make build
# → main.pdf with synchronized code + docs
```

---

## 🛠️ For Different Projects

### Using This Skill in a New Project

1. **Copy the skill** to your project's `skills/` directory
2. **Create your own `customization.md`**:
   - Define your chapter structure
   - Map artifact prefixes to chapters
   - Specify documentation backend (LaTeX, Markdown, etc.)
3. **Implement scripts** in `scripts/`:
   - `extract_code_docs.py`
   - `validate_mappings.py`
   - `generate_tables.py`
   - etc.
4. **Add `@doc:*` annotations** to your source code
5. **Run `make sync`** to generate documentation

### Example Customizations

- **Academic Reports** (like FootyDJ): LaTeX backend, structured chapters
- **Open Source Projects**: Markdown backend, GitHub wiki deployment
- **Enterprise Systems**: Sphinx backend, internal doc portal
- **APIs**: ReDoc/Swagger backend, auto-generated API docs

---

## ❓ FAQ

**Q: Is this only for LaTeX?**  
A: No! It's backend-agnostic. See `skill.md` Section 7 for Markdown, Sphinx, and HTML integration.

**Q: Can I customize the artifact ID prefixes?**  
A: Yes, but discouraged for consistency. See `rules.md` Section 7 for reserved keywords and `customization.md` for modifying only for your project.

**Q: What if my project doesn't use Python?**  
A: The protocol is language-agnostic. Adapt the annotation syntax for Java (`/** @doc:* */`), C++ (`/// @doc:*`), etc.

**Q: How do I ensure code-doc synchronization?**  
A: Use the **validation gateway** (`make validate`) before all commits (pre-commit hook).

---

## 📚 Related Skills

- **[latex-template-architect](../latex-template-architect/)** — LaTeX document generation (v3.5)
- **[latex-template-architect/skill.md](../latex-template-architect/skill.md)** — Full LaTeX protocol reference

---

## 🤝 Contribution

To improve this skill:
1. Review `skill.md` for clarity and completeness
2. Add language-specific annotation examples (Java, C++, etc.)
3. Implement additional backend generators (Sphinx, ReDoc)
4. Share your project-specific `customization.md` for reference

---

## 📞 Support

- **General Questions**: Refer to `skill.md` Section 1-7
- **Rules & Constraints**: Check `rules.md`
- **SDLC Checkpoints**: See `protocols.md`
- **Project-Specific Issues**: Review `customization.md` (FootyDJ example)

---

## 📝 Version History

| Version | Date | Changes |
| :--- | :--- | :--- |
| 1.0 | 2026-04-08 | Initial release: universal, reusable SDLC protocol |

---

**Last Updated**: 2026-04-08  
**Status**: Active & Reusable  
**Applicable Projects**: Any software project with structured documentation needs

