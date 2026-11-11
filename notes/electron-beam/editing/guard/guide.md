# guide guard: PASS (0 findings)

Base 5455de1 → eb/rhythm 700fd5f, `text/guide.py` (V's 4e8bc01; R made no change).

## guard.py
markers, maths, code, links, cites, quotes, numerals: all identical. The string literals were re-wrapped, but the code is identical after ast normalisation.

## Prose (no findings)
- The chain (tip → fields → probe → wafer → width, with chapters 1–6) is unchanged; only semicolons became full stops.
- The model list: the semicolons became sentences. "Field emission by tunnelling, and brightness and its conservation" now joins two items that the base separated with a semicolon. No item was added or dropped, and none changed in content.
- Verification claims: every number computed by code; every browser module except chapter eight's has a Python twin that must agree; the derivations are checked symbolically; published data are shown beside the model with their source; checks tables; two independent reviewers and the audit notes. All are kept, and none was strengthened.
