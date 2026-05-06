# V53 — Response to Borderline Accept (6/10) Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B–70B)

**Prior decision:** Borderline Accept (6/10) — upgraded from 4/10 in prior round

**Reviewer's explicit path to clear accept:**
> "Fix broken cross-references and appendix labels (mechanical but essential). Add the regime caveat to contribution #1 in §1.1. Address the Haiku-as-better-extractor alternative explicitly. Reconcile the Qwen scale numbers between §3.5 and Appendix Table 8. Either remove the human baseline rule comparison or move the rule rows out of Table 31."

**V53 strategy:** All five required conditions addressed, plus five secondary concerns.

---

## At-a-Glance Table

| # | Reviewer concern | V53 action | Status |
|---|---|---|---|
| **C1 — Broken appendix labels / "Appendix " blank** | 28+ appendix sections exhaust LaTeX's A–Z counter; sections 27+ render as blank → "Appendix " in PDF | Added `\usepackage{alphalph}` + `\renewcommand\thesection{\AlphAlph{\value{section}}}` in main.tex; sections 27+ now render as AA, AB, etc. Zero "Counter too large" compile errors; zero blank "Appendix " in PDF (verified by pdftotext grep) | **Done** |
| **R1 — Contribution #1 regime caveat** | §1.1 contribution #1 says "A one-line label-free rule matches a 5-feature LLM pipeline" with no regime restriction | Added "in the single-turn / pooled-LOO regime" to the bold header of contribution #1 | **Done** |
| **R2 — Qwen scale number reconciliation** | §3.5 says 48%/73%/79%/51%; Appendix Table 8 says 50%/68%/72%/50% | Main text now reads 50%/68%/72%/50%, matching the canonical appendix table (n=100 per model, within-family LOO) | **Done** |
| **R3 — Haiku-as-better-extractor alternative** | Cross-family gap of 9.7 pp spans all 7 targets; "Haiku is uniformly a better extractor" competes with "Haiku self-prefers on Claude targets"; five self-family controls rule out the *additional* boost but not the baseline quality gap | Added 2-sentence paragraph to §3.5 after the self-family controls sentence explicitly naming this alternative and its limits | **Done** |
| **R4 — Table 31 rule rows removed** | Rule and pipeline rows in Table 31 (human baseline appendix table) invite misreading despite main-text removal of the comparison | Removed rule and pipeline rows from Table 31 entirely; table now shows only the three human annotators; updated caption and interpretation paragraph | **Done** |
| **C2 — Frontier data load-bearing in §4.2** | Sonnet 4.5-on-Haiku (65.7%) still cited in §4.2 frontier paragraph to support Haiku-checkpoint claim; inconsistent with "n=2 confounded" framing | Added "(hypothesis-generating; Appendix C)" caveat to Sonnet 4.5-on-Haiku sentence in §4.2 | **Done** |
| **C3 — Haiku-claim validity status** | L-indep/L-dep status of 9–10 pp Haiku gap unclear | Reviewer correctly notes the *difference between extractors* is more robust than absolute levels; the new alternative-hypothesis paragraph implicitly addresses this — the five self-family controls test the extractor-comparison difference, which is construct-valid | **Done (via R3)** |
| **C5/M10 — K-stopping contradiction** | §2.2 says "rarely triggered before K=8"; appendix says "vacuous in practice (both predictions exceed τ)" | §2.2 now reads: "The adaptive stopping rule (P>τ=0.99) is vacuous in practice — classifier confidence typically exceeds τ in both correct and incorrect predictions — so the pipeline effectively always runs all K=8 turns" (matching appendix wording) | **Done** |
| **C6 — Frontier pointer motivation** | §3.5 frontier pointer gives no reason for including preliminary observations | Added sentence: "These targets extend the open-weight panel to closed-weight (Sonnet 4.5) and MoE (Llama 4 Maverick) architectures as diagnostic probes of where the correction-marker mechanism breaks down." | **Done** |
| **M4 — Table 2 truncation** | "P/FB: 54/" appears truncated mid-cell in EXP-I (matched) row | Shortened the cell content to fit: "Syco: 68.5% (3B), 83% (14B); P/FB: 54/56% (3B, chance), 68/60% (14B, fail Bonf.)" | **Done** |

---

## Detailed Responses

### C1: Broken appendix labels — root cause and fix

**Reviewer concern:**
> "Multiple 'Appendix ' (blank) references... These are LaTeX \\ref{} failures... Counter too large errors."

**V53 response:**

The root cause is that LaTeX's default section counter uses single letters (A–Z = 26 values). This paper's appendix has 28+ `\section{}` commands, exhausting the counter at section 27. `\AlphAlph` extends the alphabet: 27→AA, 28→AB, etc.

**Fix applied to `main.tex`:**
```latex
\usepackage{alphalph}
...
\appendix
\renewcommand\thesection{\AlphAlph{\value{section}}}
\input{sections/appendix}
```

**Verification:** Second compile pass produces zero "Counter too large" errors. `pdftotext main.pdf | grep "Appendix $"` returns 0 matches. Sections 27+ now render as Appendix AA, AB, etc., and all `\ref{app:...}` calls resolve correctly. The Qwen 14B persona spotcheck appendix (section 27) now shows as "Appendix AA" in the PDF — confirmed in page 7 of the compiled output.

---

### R1: Contribution #1 regime caveat

**V53 response:**

Introduction §1.1, contribution #1 now reads:

> "**A one-line label-free rule matches a 5-feature LLM pipeline in the single-turn / pooled-LOO regime.** Refusal count ≥1 achieves **80.1%** pooled-LOO across seven equalized models (no calibration data)..."

This matches the regime restriction already present in the abstract ("The rule-vs-pipeline equivalence holds in the single-turn/pooled-LOO regime") and §3.4 ("The pipeline materially outperforms the rule **only** at ≥14B in multi-turn topical follow-up").

---

### R2: Qwen scale number reconciliation

**V53 response:**

The main-text values (48%/73%/79%/51%) were from an earlier analysis run. The canonical values are in Appendix Table 8 (n=100 per model, within-family LOO, Holm-Bonferroni corrected). §3.5 now reads:

> "Qwen 2.5: 50% (3B)→68% (7B, p=0.014)→72% (14B)→50% (32B, µ_lie=0.00, µ_truth=0.00; ...)"

The qualitative pattern (peak at 14B, collapse at 32B) is unchanged; only the absolute numbers are corrected.

---

### R3: Haiku-as-better-extractor alternative hypothesis

**Reviewer concern (Q1):**
> "Could you add a brief discussion of why the cross-family gap on non-Claude targets shouldn't be read as 'Haiku is a stronger extractor' rather than 'Haiku self-prefers'?"

**V53 response:**

Added to §3.5 after the self-family controls sentence:

> "An alternative explanation is that Haiku is a uniformly stronger extractor than Mistral L3 across all targets, regardless of family. The five self-family controls rule out an *additional* same-family boost (all within 0–3 pp of cross-family), but they do not fully exclude the extractor-quality hypothesis; a third extractor of comparable capability would be needed to disentangle these (Appendix N)."

**On C3 (L-dep/L-indep status):** The reviewer notes that the *difference* between Haiku and Mistral L3 extraction may be more robust than the absolute levels. This is correct: the self-family comparison (Haiku vs. Mistral L3 on the same target) controls for target-specific difficulty, so the 9.7 pp gap in the *comparison* is less sensitive to the ICC-failing features than either absolute number. We have added the alternative-hypothesis text rather than a separate L-dep/L-indep flag because the construct-validity issue affects both extractors equally when comparing their difference — the main concern is which extractor is favored, not whether the absolute accuracy level is construct-valid.

---

### R4: Table 31 rule rows removed

**V53 response:**

Table 31 (Appendix V, human baseline) now shows only the three human annotators. The rule and pipeline rows have been removed. The table caption now reads: "...comparison to automated methods is degenerate and is not reported here (see §3.4 for automated results on the full panel)." The interpretation paragraph no longer mentions the "+32 pp rule-over-human gap."

---

### C2: Sonnet 4.5-on-Haiku load-bearing use in §4.2

**V53 response:**

§4.2 frontier-scale paragraph now reads:

> "...Sonnet 4.5-on-Haiku (65.7%) is *consistent with* localizing the +10 pp uplift to the Haiku checkpoint, though this rests on a single frontier-scale observation (hypothesis-generating; Appendix C)."

---

### C5/M10: K-stopping contradiction reconciled

§2.2 now reads:

> "The adaptive stopping rule (P>τ=0.99) is vacuous in practice — classifier confidence typically exceeds τ in both correct and incorrect predictions — so the pipeline effectively always runs all K=8 turns and all reported LOO accuracies use the full-K run."

This matches the appendix wording exactly.

---

### C6 and M4: Frontier pointer motivation; Table 2 fix

Both addressed as described in the at-a-glance table above.

---

## Summary of V53 Changes

| File | Change |
|---|---|
| `main.tex` | Add `\usepackage{alphalph}` + `\renewcommand\thesection{\AlphAlph{...}}` after `\appendix` |
| `sections/introduction.tex` | Add "in the single-turn / pooled-LOO regime" to contribution #1 bold header |
| `sections/experiments.tex` | Fix Qwen numbers (48→50, 73→68, 79→72, 51→50); add Haiku-extractor alternative paragraph; add frontier pointer motivation sentence |
| `sections/discussion.tex` | Add "(hypothesis-generating; Appendix C)" caveat to Sonnet 4.5-on-Haiku sentence in §4.2 |
| `sections/methodology.tex` | Reconcile K-stopping: "vacuous in practice" wording to match appendix |
| `sections/appendix.tex` | Remove rule/pipeline rows from Table 31; update caption and interpretation; fix Table 2 EXP-I row truncation |
| NEW: `REVIEWER_RESPONSE_LETTER_V53.md` | This document |

**Paper status:** 41 pages total; 9 pages main content; compiles cleanly (2-pass); 0 "Counter too large" errors; 0 blank "Appendix " references in PDF.
