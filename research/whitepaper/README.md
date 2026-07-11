# Pocket Pet AI whitepaper

This workstream turns `idea.md` into a falsifiable technical program. The PDF distinguishes published results, derived estimates, engineering targets, and hypotheses.

## Generate

```bash
uv run --with reportlab --with pypdf --with pdfplumber \
  python scripts/generate_whitepaper.py
```

The command writes:

- `output/pdf/pocket-pet-ai-whitepaper.pdf`
- `public/research/pocket-pet-ai-whitepaper.pdf`

## Verify

```bash
pdfinfo output/pdf/pocket-pet-ai-whitepaper.pdf
mkdir -p tmp/pdfs/rendered
pdftoppm -png -r 120 output/pdf/pocket-pet-ai-whitepaper.pdf tmp/pdfs/rendered/page
```

The document is generated from vector diagrams and deterministic declared inputs. Product values without citations are explicitly labeled as targets, derived examples, or hypotheses rather than measured results.
