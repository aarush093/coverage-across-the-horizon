DOC: 21_DATASET_REGISTRY | OWNER: Aarush | CADENCE: per-dataset
STATUS: active | LAST-UPDATED: 2026-08-29 | SUPERSEDES: 2026-07-17 seed

# 21 — DATASET REGISTRY
| ID | Dataset | Channels/notes | Split protocol | Source | Status |
|----|---------|----------------|----------------|--------|--------|
| DS01 | ETTh1 | 7 ch, hourly | sequential, stride-24 calibration | ETDataset raw (zhouhaoyi) | **USED — S1–S4** |
| DS02 | ETTh2 | 7 ch, hourly | sequential | same | **USED — S1–S4** |
| DS03 | ETTm1 | 7 ch, 15-min | sequential | same | **USED — S1–S4** |
| DS04 | ETTm2 | 7 ch, 15-min | sequential | same | **USED — S1–S4** |
| DS05 | Electricity | 321 clients → 50 screened by a fixed published rule | sequential 70/10/20; calibration in spring 2014, test summer→winter (seasonal shift) | LSTNet release (laiguokun) — gzipped, ~18 MB, no account | **PROMOTED to PRIMARY S5 surface (D006)** — download hook was added on 2026-08-29 and lost with the container; must be re-added |
| DS06 | Traffic | 862 sensors | sequential | same | NOT USED — out of MVP scope |
| DS07 | Weather | 21 vars | sequential | same | NOT USED — Lock S1 named it; ETT×4 was run instead |
| DS08 | ILI | low-freq, nonstationary | sequential | same | NOT USED — S4 shift traces were to use it |
| DS09 | BDG2 | ~50 electricity meters of 3,053 | chronological 2016→2017 | buds-lab/building-data-genome-project-2 | **DEMOTED to gated extension (D006).** Meter CSV is Git LFS: raw fetch returns a 134-byte pointer, declared size 174,239,039 B; LFS media host 403 `host_not_allowed` from the sandbox. [FACT, verified 2026-08-29] **Untested on Aarush's laptop — a local `git lfs pull` is expected to work.** |

HYGIENE (binding, all datasets): sequential splits only; drop_last disabled; strided calibration windows; fixed published seed 2026.
**Open concern (Q07):** ETTh1/H=96 has n_cal=117 and n_test=117 windows after stride-24. Worst-cell coverage over a 42-cell grid on 117 test windows is a noisy statistic, and the smallest log-spaced horizon bucket is the noisiest cell of all. This is the likely mechanism behind the Electricity min-cell regression in EXP_S5_002.
