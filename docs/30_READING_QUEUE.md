DOC: 30_READING_QUEUE | OWNER: Aarush | CADENCE: per-paper (update as items are read/added)
STATUS: active | LAST-UPDATED: 2026-07-17 | SUPERSEDES: reference_links.md (from lmao_21.zip)

# 30 — Reading Queue & Master Bibliography
Coverage Across the Horizon · seeds the literature system (feeds 31_PAPER_NOTES + 32_LIT_MATRIX).
Numbering matches the References section of the Idea Lock. Links stated as verified-on-16-July-2026 by the author;
IDs dated 2503+ are past Claude's Jan-2026 cutoff and are [UNVERIFIED] until an S0 web-resolve pass confirms them.

---

## READ FIRST — S0 positioning queue (mid–late Aug 2026)

The Idea Lock §8 S0 mandates four close reads. Mapping them to this sheet:

1. [8]  CP-for-TS benchmark incl. MSCP — 2601.18509   ← read #1 (closest benchmarking work)
2. [9]  AcMCP / MPID — 2410.13115
3. [7]  Conformal PID Control — 2307.16895
4. [ ]  O2CP — arXiv 2508.13362   ← **MISSING from the link sheet. Add it. Mandated by S0.**

Then, closest 2026 competition (read before declaring the wedge intact):
5. [15] DeRegiME — 2605.19231   (nearest territorial neighbour per fence table)
6. [16] Report the Floor — 2606.09473   (external validation of the gap — a chunk of G3 leans on this)

S0 exit criterion (from the Lock): wedge statement survives unchanged, or is amended in writing.

---

## WEDGE-CRITICAL — scrutinize, do not just file

These three are conditional-coverage machinery sitting close to W1/W2. At S0 they get a real read,
because if any already does horizon/channel-conditional coverage at scale, the wedge moves:
- [19] Conformal Prediction With Conditional Guarantees — Gibbs, Cherian, Candès, JRSS-B 2025 — 2305.12616
- [18] Conditional-Coverage Diagnostics — Dec 2025 — 2512.11779   (adjacent to the W1 audit)
- [13] MultiDimSPCI (ellipsoidal joint sets) — Xu, Jiang, Xie, ICML 2024 — 2403.03850

---

## A. Anchor triad (Idea Lock P1–P3)
- [1] Informer — Zhou et al., AAAI 2021 (Best Paper) — https://arxiv.org/abs/2012.07436
- [2] DLinear — Zeng et al., AAAI 2023 — https://arxiv.org/abs/2205.13504 · DOI: 10.1609/aaai.v37i9.26317
- [3] PatchTST — Nie et al., ICLR 2023 — https://arxiv.org/abs/2211.14730

## B. Gap evidence
- [4] ProbTS benchmark — Zhang et al., NeurIPS 2024 D&B — https://arxiv.org/abs/2310.07446

## C. Conformal / uncertainty line (machinery, baselines, nearest works)
- [5] ACI — Gibbs & Candès, NeurIPS 2021 — https://arxiv.org/abs/2106.00170
- [6] Online CP under arbitrary shifts — Gibbs & Candès, JMLR 2024 — https://arxiv.org/abs/2208.08401
- [7] Conformal PID Control — Angelopoulos, Candès, Tibshirani, NeurIPS 2023 — https://arxiv.org/abs/2307.16895
- [8] CP-for-TS benchmark incl. MSCP — Jan 2026 — https://arxiv.org/abs/2601.18509  [UNVERIFIED]
- [9] AcMCP / MPID — Wang & Hyndman, 2024 — https://arxiv.org/abs/2410.13115
- [10] Bellman Conformal Inference — Yang, Candès, Lei, 2024 — https://arxiv.org/abs/2402.05203
- [11] CopulaCPTS — Sun & Yu, 2022 — https://arxiv.org/abs/2212.03281
- [12] ConForME — COPA 2024, PMLR 230:345–365 — https://proceedings.mlr.press/v230/galvao-lopes24a.html
- [13] MultiDimSPCI — Xu, Jiang, Xie, ICML 2024 — https://arxiv.org/abs/2403.03850 · PMLR: https://proceedings.mlr.press/v235/xu24m.html
- [14] PatchTST + ACI for hour-ahead PV — Energies 18(18):5000, 2025 — https://www.mdpi.com/1996-1073/18/18/5000  [UNVERIFIED]
- [15] DeRegiME — May 2026 — https://arxiv.org/abs/2605.19231  [UNVERIFIED]
- [16] Report the Floor — Jun 2026 — https://arxiv.org/abs/2606.09473  [UNVERIFIED]
- [17] SAGA — May 2026 — https://arxiv.org/abs/2605.19014  [UNVERIFIED]
- [18] Conditional-Coverage Diagnostics — Dec 2025 — https://arxiv.org/abs/2512.11779  [UNVERIFIED]
- [19] CP With Conditional Guarantees — Gibbs, Cherian, Candès, JRSS-B 2025 — https://arxiv.org/abs/2305.12616 · DOI: 10.1093/jrsssb/qkaf008
- [20] Conformal Seasonal Pools — May 2026 — https://arxiv.org/abs/2605.03789  [UNVERIFIED]
- [21] Schlembach et al., Conformal Multistep Multivariate TSF — COPA 2022, PMLR 179:316–318 — https://proceedings.mlr.press/v179/schlembach22a.html
- [+] O2CP — optimization-based online multi-step CP, 2025 — https://arxiv.org/abs/2508.13362  [UNVERIFIED] (S0-mandated; was missing)

## D. Later LTSF context (synthesis, not core)
- [22] iTransformer — Liu et al., ICLR 2024 — https://arxiv.org/abs/2310.06625
- [23] TimeXer — Wang et al., NeurIPS 2024 — https://arxiv.org/abs/2402.19072
- [24] Chronos — Ansari et al., 2024 — https://arxiv.org/abs/2403.07815

## E. Datasets
- [25] BDG2 (paper) — Miller et al., Scientific Data 7:368, 2020 — https://doi.org/10.1038/s41597-020-00712-x
- BDG2 data (incl. ASHRAE GEPIII subset) — https://github.com/buds-lab/building-data-genome-project-2
- Canonical LTSF suite (ETT ×4, Electricity, Traffic, Weather, ILI) — via code repos below.

## F. Code repositories
- PatchTST official — https://github.com/yuqinie98/PatchTST
- Time-Series-Library (thuml) — https://github.com/thuml/Time-Series-Library
- iTransformer official — https://github.com/thuml/iTransformer
- ProbTS toolkit (Microsoft) — https://github.com/microsoft/ProbTS
- MultiDimSPCI official — https://github.com/hamrel-cxu/MultiDimSPCI
- conditional-conformal (Gibbs–Cherian–Candès) — https://github.com/jjcherian/conditional-conformal

## G. Chat-analysis only (not in locked reference list)
- EnbPI — Xu & Xie, ICML 2021, PMLR 139:11559–11569 (search title)
- SPCI — Xu & Xie, ICML 2023, PMLR 202:38707–38727 (search title)

## Open items
- O2CP (2508.13362) added above — confirm it resolves at S0.
- Dataset scope of [8] — confirm on close read (overlap with our wedge?).
- Venues of record for [9], [11] — final venues to confirm.
- All 2503+ IDs marked [UNVERIFIED] — resolve in the S0 web pass.
