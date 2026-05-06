# V56 — Response to Weak Accept (6/10) Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B-70B)

**Prior decision:** Weak Accept (6/10) — "I lean toward acceptance."

**Reviewer's barriers to clear accept:**
> "(1) the paper hedges its contribution between 'critical replication' and 'methods paper' without committing, (2) the Haiku same-family inflation result — a featured finding — is not actually disambiguated from the extractor-quality alternative, and (3) scope limitations mean the binding regime for real-world deployment (frontier-scale, autonomous) is precisely where the paper has least to say."

**V56 strategy:** Commit fully to audit framing (MC1); downgrade Haiku from contribution to observation (MC4); make scope limitations explicit (MC2); surface the practical recommendation (MC5); fix all addressable minor issues.

---

## At-a-Glance Table

| # | Concern | V56 action | Status |
|---|---|---|---|
| **MC1 — Framing muddled** | §2.1 opening no longer says "primary methodological contribution"; controls are now "derived from the audit findings" | **Done** |
| **MC2 — Scope limitations** | New limitation (e) in §4.4: "The binding regime for deployment—frontier-scale, autonomous, multilingual—is where this paper has least to say" | **Done** |
| **MC3 — Sycophancy attenuated** | Conclusion now includes "(SP-only: 63.1/69.5%)" showing dispositional bulk | **Done** |
| **MC4 — Haiku undersupported** | Removed from §1.1 numbered contributions list; remains in §3.5 and §4.2 as supporting observation | **Done** |
| **MC5 — Multi-turn buried** | Bold "**Practical recommendation:**" in conclusion with explicit rule vs. pipeline guidance | **Done** |
| **MC6 — Qwen caveat** | Bold "**Qwen (descriptive; does not survive joint correction):**" prefix on scale paragraph | **Done** |
| **MC7 — Reimplementation** | Parenthetical "(from-scratch reimplementation; original code/data not obtained)" at first occurrence of "critical replication" in §1.1 | **Done** |
| **m1 — T-acc/L-acc** | Defined in table caption: "T-acc = truthful-trial accuracy; L-acc = lying-trial accuracy" | **Done** |
| **m2 — Gemma citation** | Added \cite{team2024gemma2} at both mentions; bib entry added | **Done** |
| **m5 — 70B bar** | Caption strengthened: "preliminary—included for directional context only" | **Done** |
| **m6 — Limitation labels** | Appendix renumbered sequentially (f)–(k) continuing from main text (a)–(e) | **Done** |
| **m7 — Transcript C** | Added "Dual-refusal prevalence" paragraph: 50/50 target refusals, interrogator co-refuses in subset, classified as RLHF compliance detection | **Done** |
| **m8 — Name predictions** | Now reads: "knowledge-conflict clarity and disposition-source ranking—failed to be confirmed" | **Done** |

---

## Detailed Responses to Major Concerns

### MC1: Contribution framing — commit to audit

**Reviewer concern:**
> "The abstract and §1 oscillate between 'this is a critical replication of Pacchiardi et al.' and 'this is a three-control protocol contribution.' These are different papers... I'd recommend committing fully to the audit framing."

**V56 response:**

We agree the audit framing is the more defensible and more interesting paper. Three changes enforce this commitment:

1. §2.1 opening sentence now reads: "Three evaluation controls, **derived from the audit findings below**, isolate genuine detection signal..." — removing "primary methodological contribution."

2. §1.1 already states: "The three-control protocol is a *lesson derived from* this critical replication, not a primary contribution independent of it." — this was present but is now the only framing (no competing "methods paper" language elsewhere).

3. The numbered contributions list (now 4 items) reports empirical findings from the audit, not protocol claims.

---

### MC2: Scope limitations — frontier binding

**Reviewer concern:**
> "The implication — that the entire critique may not bind on the regime that matters most — deserves more prominence."

**V56 response:**

Added limitation **(e)** to §4.4:

> "The binding regime for deployment—frontier-scale, autonomous, multilingual—is where this paper has least to say; whether the three controls produce similar collapses at frontier scale is an open empirical question."

This joins the existing scope statement in the abstract (line 2: "Results do not generalize to frontier-scale (>70B closed-weight) or autonomous-deception settings without additional study") and the Scope paragraph in §1.2. The limitation is now stated in three locations at decreasing levels of prominence.

---

### MC3: Sycophancy attenuation

**Reviewer concern:**
> "The system-prompt-only control (63.1–69.5%) shows most of that signal is dispositional rather than epistemic-pressure-driven."

**V56 response:**

The conclusion now reads: "Sycophancy transfers (68.5/83% at 3B/14B), **though the bulk is dispositional (SP-only: 63.1/69.5%)**." This matches the honest framing already in §3.6.

---

### MC4: Haiku effect — downgraded from contribution

**Reviewer concern:**
> "Given that this is a featured finding (point 4 in §1.1), the experiment that would disambiguate it should be in the paper, not in future work."

**V56 response:**

We agree. The Haiku observation is hypothesis-generating, not a validated finding, and we were overselling it by including it in the contributions list. We have:

1. **Removed** the Haiku item from the §1.1 numbered contributions list (now 4 items).
2. **Retained** the full analysis in §3.5 (cross-family extraction paragraph) and §4.2 (discussion), where it is already explicitly marked as "hypothesis-generating; extractor-quality alternative not excluded."

The content is preserved for readers who want the details; it just no longer claims contribution status. Running a third extractor (e.g., Llama 3.3 70B or DeepSeek-V3 as extractor) remains the decisive disambiguation test and is logged as future work.

---

### MC5: Multi-turn recommendation surfaced

**Reviewer concern:**
> "If the practical recommendation is 'use the rule for single-turn pooled-LOO; use the pipeline for ≥14B multi-turn,' that should be stated cleanly in the conclusion."

**V56 response:**

Conclusion now contains:

> **Practical recommendation:** use the refusal-count rule for single-turn evaluation; use the full pipeline for ≥14B multi-turn (+14–29 pp).

This is the clearest actionable guidance we can give practitioners.

---

### MC6: Qwen non-monotonic caveat

**Reviewer concern:**
> "The Qwen 2.5 non-monotonic pattern as a headline claim deserves a more prominent caveat."

**V56 response:**

§3.5 Qwen paragraph now opens with bold text: "**Qwen (descriptive; does not survive joint correction):**" before the numbers. Combined with the existing sentence at the end of the opening paragraph ("We report the Qwen 2.5 non-monotonic pattern descriptively; under joint correction across all families, it does not survive"), this is now flagged at both the methodology level and the results level.

---

### MC7: Reimplementation flagged early

**Reviewer concern:**
> "Readers will reasonably interpret 'critical replication' in the abstract as something stronger. This is fine but should be flagged earlier."

**V56 response:**

§1.1, first occurrence of "critical replication," now reads:

> "methodological audit and critical replication **(from-scratch reimplementation; original code/data not obtained)**"

This sets expectations immediately.

---

## Responses to Reviewer Questions

### Q1: Third extractor cost

> "What would it cost to run a third strong extractor (e.g., Llama 3.3 70B or DeepSeek-V3)?"

Approximately $200–400 in API costs for 7 targets × 100 trials × 8 turns at 70B scale. The experiment is straightforward and logged as future direction (10). We've downgraded the Haiku finding from a contribution to a supporting observation, which we believe is the appropriate response when the disambiguating experiment hasn't been run.

### Q2: Per-feature K-curve for multi-turn advantage

> "Is the +14–29 pp driven by specific features?"

Correction-marker density saturates at K=1 (the first response reveals refusal/correction patterns). The multi-turn advantage at ≥14B comes from consistency and specificity features, which require multiple turns to assess whether the model maintains coherent elaboration. A per-feature K-curve would clarify this decomposition and is flagged as useful future work.

### Q3: Transcript C dual-refusal prevalence

> "How many of the 92 Claude Haiku trials show this pattern?"

Of 50 lying trials in the instructed condition, **50/50 (100%)** contain target refusal language. The interrogator co-refuses in a subset of these (same-family condition only). We've added a "Dual-refusal prevalence" paragraph to the appendix making this explicit and clarifying that we characterize the 97.8% as "RLHF safety compliance detection" rather than deception detection. Importantly, this pattern is confined to the same-family instructed condition and does not affect the cross-family equalized results that constitute the paper's primary evaluation.

### Q4: Cross-family classifier disagreement on adversarial robustness

> "Doesn't this raise questions about whether either classifier is a reliable adjudicator?"

Yes — the Haiku (37% truth accuracy) vs. Llama 70B (82% truth accuracy) gap reflects classifier calibration differences rather than a mechanism reversal. Both agree on direction (truth > lie), which is the evidential content for the LC/Bi classification. We acknowledge in §3.2 that "the absolute discrepancy reflects classifier calibration differences rather than a mechanism reversal." A human spot-check (n=20) on factual accuracy would indeed be the gold standard and is a reasonable future addition.

### Q5: Alternative autonomous scenarios

> "Would reward-hacking-style scenarios (Denison et al. 2024) potentially recover detector signal?"

This is a promising direction. Reward-hacking scenarios (where the model has a clear instrumental reason to deceive about its actions) would test whether correction-marker suppression occurs under genuine strategic pressure rather than the artificial persona-maintenance pressure that produced our scenario-design artifact. We've cited Apollo Research's AI Liar Dataset in our future directions as one such testbed.

---

## Minor Issues Addressed

| Issue | Action |
|---|---|
| T-acc/L-acc undefined in table | Defined in caption |
| Gemma 2 27B "documented agreeableness" | Added citation; removed "documented" (now "high agreeableness scores on alignment benchmarks") |
| 70B sycophancy bar in summary figure | Caption now says "preliminary—included for directional context only" |
| Appendix limitation label gaps | Renumbered (f)–(k) sequentially from main text (e) |
| Transcript C dual-refusal | Added prevalence note + methodological clarification |
| Pre-registered predictions unnamed | Now named inline: "knowledge-conflict clarity and disposition-source ranking" |

---

## Minor Issues Not Changed (with explanation)

**Appendix labels (A–AE):** The unusual labeling (AA, AB, etc.) is a LaTeX constraint — with 28+ appendix sections, we use the `alphalph` package for extended counters. Alternative numbering (A.1, A.2, ...) would require restructuring the entire appendix hierarchy. We acknowledge this is unusual but it is navigable.

**Figure 2 / feature collapse scope:** The reviewer references "Figure 2" which we believe refers to Figure S1 (fig:feature_collapse) in the appendix. This figure shows all seven equalized targets. We've added a clarifying note to the caption: "All seven equalized targets shown."

---

## Summary of V56 Changes

| File | Change |
|---|---|
| `sections/introduction.tex` | Remove Haiku contribution #4; add reimplementation parenthetical |
| `sections/methodology.tex` | Reword §2.1 opening (audit-derived, not "primary contribution") |
| `sections/conclusion.tex` | Bold practical recommendation; sycophancy attenuation |
| `sections/discussion.tex` | Add limitation (e) on frontier binding |
| `sections/experiments.tex` | Bold Qwen caveat; name causal predictions; Gemma citation ×2 |
| `sections/appendix.tex` | T-acc/L-acc def; renumber limitations (f)–(k); Transcript C note |
| `references.bib` | Add Gemma 2 entry |
| `figures/summary_results.tex` | Strengthen 70B preliminary caveat |
| NEW: `REVIEWER_RESPONSE_LETTER_V56.md` | This document |

**Paper status:** 41 pages total; 9 pages main content; compiles cleanly (3-pass with bibtex); 0 undefined references.
