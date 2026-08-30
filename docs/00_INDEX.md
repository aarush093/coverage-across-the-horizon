DOC: 00_INDEX | OWNER: Aarush | CADENCE: on every doc create/retire
STATUS: active | LAST-UPDATED: 2026-07-17 | SUPERSEDES: none

# 00 — INDEX (single source of truth for what exists)
Flat namespace manifest. If two docs' headers conflict, this file wins the tiebreak on "which is canonical."
Build philosophy: MVP-first + lazy instantiation. Tier-4 writing docs are deliberately NOT built yet (S6/Dec).

| ID | Title | Tier | Status | Owner | Cadence | Lives in |
|----|-------|------|--------|-------|---------|----------|
| 00_INDEX | This manifest | 0 | active | Aarush | on change | PK |
| 01_IDEA_LOCK | Constitution (the PDF) | 0 | active (frozen) | Aarush | delta-only | PK (rename PDF to 01_IDEA_LOCK) |
| 02_OPERATING_RULES | Full rulebook + 12 roles | 0 | active | Aarush | rare | PK |
| 10_DECISION_LOG | Every decision | 1 | active | Aarush | per-decision | PK |
| 11_RISK_REGISTER | Risks (from Lock §12) | 1 | active | Shared | monthly + trigger | PK |
| 12_PROGRESS_TRACKER | Stage status (Lock §8) | 1 | active | Aarush | weekly | PK |
| 13_OPEN_QUESTIONS | Unknowns / tech debt | 1 | active | Shared | continuous | PK |
| 14_WEDGE_SCAN_LOG | Monthly wedge scan | 1 | active | Aarush | monthly (1st Mon) | GOOGLE DRIVE (machine-writable) |
| 20_EXPERIMENT_REGISTRY | Experiment ledger | 2 | template | Aarush | per-experiment | PK (fills at S1) |
| 21_DATASET_REGISTRY | Datasets | 2 | seeded | Aarush | per-dataset | PK |
| 22_MODEL_REGISTRY | Backbones/seeds | 2 | seeded | Aarush | per-model | PK |
| 23_METRIC_REGISTRY | Metric definitions | 2 | seeded | Aarush | rare | PK |
| 24_FAILURE_REGISTRY | What broke & why | 2 | template | Shared | per-failure | PK |
| 30_READING_QUEUE | Bibliography + queue | 3 | active | Aarush | per-paper | PK |
| 31_PAPER_NOTES | Per-paper note template | 3 | template | Claude drafts | per-paper | PK |
| 32_LIT_MATRIX | Connected lit graph | 3 | seeded | Shared | per-paper | PK |
| 43_REVIEWER_2 | Anticipated attacks | 4 | seeded-early | Shared | as insight arrives | PK |
| 50_RESEARCH_LOG | Rolling daily/session log | 5 | active | Aarush | per-session | PK |

## Deferred (instantiate at S6 / Dec 2026 — building now would only rot):
40_MANUSCRIPT, 41_CONTRIBUTION_CLAIMS, 42_VALIDITY, 44_PUB_TARGETS, 45_FUTURE_WORK.
(41 note: contribution claims C1–C4 already live verbatim in the Idea Lock §6; 41 splits out only when drafting starts.)

## Where things live (important):
- Most docs: chat-Project Knowledge (PK) — you upload the .md files.
- 14_WEDGE_SCAN_LOG: Google Drive — so the Cowork scheduled task can auto-append. (Already created.)
- Code + real version control: git (github/aarush093) — NOT Claude. PK holds distilled notes only, never raw PDFs.
