# examples/

This directory stores all compiled output from the build process,
**mirroring the repository structure** so each artifact is easy to trace back to its source.

```
examples/
├── main.pdf              ← compiled from main.tex  (via compile.sh)
└── docs/
    └── diagrams/
        ├── structure.png ← generated from docs/diagrams/structure.mmd  (via mmdc)
        └── build-flow.png← generated from docs/diagrams/build-flow.mmd (via mmdc)
```

## Regenerate diagrams

```bash
npm install -g @mermaid-js/mermaid-cli

mmdc -i docs/diagrams/structure.mmd  -o examples/docs/diagrams/structure.png
mmdc -i docs/diagrams/build-flow.mmd -o examples/docs/diagrams/build-flow.png
```

## Recompile PDF

```bash
./compile.sh
# Output → examples/main.pdf
```
