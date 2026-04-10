import json
import os

META_PATH = r"c:\Users\mahes\OneDrive\Desktop\Python-Projects\footydj_mini_project\main_project_latex-main\skills\docs\extracted_meta.json"

TIKZ_MAP = {
    # [731] Stage 1 overview
    "graph TD\n    A[Raw Match Video] --> B[STAGE 1: Trimmer]\n    B -->|Bhattacharyya Distance| C[Fragments]\n    C --> D[STAGE 2: Processor]\n    D --> E[JSON Metadata]\n    E --> F[STAGE 3: Analyzer]\n    F --> G[Enriched Match Data]": r"""\begin{tikzpicture}[node distance=1.5cm]
    \node (A) [fill=blue!10, draw] {Raw Match Video};
    \node (B) [fill=blue!10, draw, right of=A] {STAGE 1: Trimmer};
    \node (C) [fill=blue!10, draw, right of=B] {Fragments};
    \node (D) [fill=blue!10, draw, right of=C] {STAGE 2: Processor};
    \node (E) [fill=blue!10, draw, right of=D] {JSON Metadata};
    \node (F) [fill=blue!10, draw, right of=E] {STAGE 3: Analyzer};
    \node (G) [fill=blue!10, draw, right of=F] {Enriched Match Data};
    \draw[->] (A) -- (B);
    \draw[->] (B) -- node[above] {\tiny Dist} (C);
    \draw[->] (C) -- (D);
    \draw[->] (D) -- (E);
    \draw[->] (E) -- (F);
    \draw[->] (F) -- (G);
\end{tikzpicture}""",

    # Sequence Diagram
    """sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant RAG
    participant Gemini
    participant VectorDB

    User->>Frontend: Type tactical question
    Frontend->>API: POST /api/chat {"query": "..."}
    API->>RAG: Process query
    RAG->>VectorDB: Retrieve relevant fragments
    VectorDB-->>RAG: Context chunks
    RAG->>Gemini: Generate response
    Gemini-->>RAG: Answer + reasoning

    RAG-->>API: Formatted response
    API-->>Frontend: {"answer": "...", "sources": [...]}
    Frontend->>User: Display in chat""": r"""\begin{tikzpicture}[node distance=1.2cm, every node/.style={font=\tiny}]
    \node (User) [draw, fill=blue!10] {User};
    \node (Frontend) [draw, fill=blue!10, right=of User] {Frontend};
    \node (API) [draw, fill=blue!10, right=of Frontend] {API};
    \node (RAG) [draw, fill=blue!10, right=of API] {RAG};
    \node (VDB) [draw, fill=blue!10, below=of RAG] {VectorDB};
    \node (Gem) [draw, fill=blue!10, right=of RAG] {Gemini};
    \draw[->] (User) -- (Frontend);
    \draw[->] (Frontend) -- (API);
    \draw[->] (API) -- (RAG);
    \draw[->] (RAG) -- (VDB);
    \draw[<->] (VDB) -- (RAG);
    \draw[->] (RAG) -- (Gem);
    \draw[->] (Gem) -- (RAG);
    \draw[->] (RAG) -- (API);
    \draw[->] (API) -- (Frontend);
    \draw[->] (Frontend) -- (User);
\end{tikzpicture}"""
}

def apply_tikz():
    if not os.path.exists(META_PATH):
        print("Error: extracted_meta.json not found.")
        return

    with open(META_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    for entry in data:
        if entry.get("type") == "diagram":
            content = entry["content"].replace("```mermaid\n", "").replace("\n```", "").strip()
            # Try exact match or fuzzy match (common prefixes)
            for m_key, t_val in TIKZ_MAP.items():
                if m_key.strip() in content:
                    entry["tikz_content"] = t_val
                    count += 1
                    break

    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Applied {count} TikZ conversions.")

if __name__ == "__main__":
    apply_tikz()
