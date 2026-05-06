# V60 — Response to Weak Accept (6/10) Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B-70B)

**Prior decision:** Weak Accept (6/10)

**Reviewer's stated conditions for 7/10:**
> "With responsive rebuttal addressing W1 (softer Pacchiardi-specific framing), W3 (extended persona spot-check), and Q2/Q3 (base-model and benign-conversation baselines), I would be willing to move to 7."

**V60 strategy:** W1, W3, Q2, and Q3 were already addressed in V58/V59 revisions. V60 additionally addresses the presentation and structural issues (W2, W4-W6, W8) and minor fixes needed for 8/10.

---

## At-a-Glance Table

| # | Concern | V60 action | Status |
|---|---|---|---|
| **W1 — Pacchiardi framing** | Already addressed V59: §4.3 reframed as "independent evaluation suite...whether these fully explain the specific gap remains untested" | **Pre-resolved** |
| **W2 — Frontier caveat in conclusion** | Added explicit scope sentence: "These findings scope to English instructed-roleplay on open-weight models ≤70B; whether the three controls produce comparable collapses at frontier scale is an open empirical question" | **Done** |
| **W3 — Persona spot-check** | Already addressed V59: cells reported as "null detector results with scenario-design artifact as leading candidate explanation" (not "excluded") | **Pre-resolved** |
| **W4 — Machine-rater ICC too long** | Shortened from ~12 lines to 4 lines: key numbers only, removed redundant Qwen 32B detail and motivation paragraph | **Done** |
| **W5 — Human baseline degenerate** | Removed 3-line interpretation paragraph (inferrable from table caption); kept table and 2-line result | **Done** |
| **W6 — Figure 1(b) 70B marking** | X-tick label now reads "70B† (n=50)" — preliminary nature visible without reading caption | **Done** |
| **W8 — Structural redundancy** | §4.2 Regimes 2 and 3 trimmed to cross-references (removed verbatim repetition of §3.6 content) | **Done** |
| **Q2 — Base-model** | Already addressed V59: "Paradigm boundaries" paragraph explains RLHF-response-style hypothesis and names the specific test (Mistral-7B-v0.1 sweep) | **Pre-resolved** |
| **Q3 — FPR on benign output** | Already addressed V59: "Paradigm boundaries" paragraph acknowledges unmeasured FPR and its implication for deployment utility | **Pre-resolved** |
| **M1 — "defensiveness" terminology** | Fixed to "correction-marker density 0.77" in machine-ICC section | **Done** |
| **M2 — Missing Mistral 7B sycophancy** | Fixed §3.6 text: "Three scenarios on Llama 3B and Qwen 14B; persona and false-belief on Mistral 7B" (matches Table 7, which has no Mistral sycophancy row) | **Done** |
| **M3 — Figure 1 caption "excluded"** | Updated to "null results" per V59 language consistency | **Done** |

---

## Detailed Responses

### W1: Pacchiardi-specific framing (pre-resolved in V59)

**Reviewer concern:**
> "The paper implicitly attributes Pacchiardi et al.'s reported 67-73% to the confounds documented here, but the authors did not replicate their exact protocol."

**V60 response:**

This was addressed in V59. §4.3 now reads:

> "The primary contribution is a **methodological audit**: we provide an independent evaluation suite that, under tighter controls, yields construct-valid accuracy of 54.5--64.7%---substantially below Pacchiardi et al.'s reported 67--73% (their Table 1). The three controls identify instruction-following (30--41 pp), extractor-quality differences (+7--10 pp), and surface-lexical patterns as contributors to inflated accuracy in the general paradigm; whether these fully explain the specific gap to Pacchiardi et al. remains untested absent a direct replication of their protocol."

The contribution is framed as "lower numbers under tighter controls" without claiming to definitively explain Pacchiardi's specific numbers.

---

### W2: Frontier caveat in conclusion

**Reviewer concern:**
> "The conclusion should explicitly acknowledge that these results may not generalize to frontier-scale models."

**V60 response:**

Added to conclusion:

> "These findings scope to English instructed-roleplay on open-weight models ≤70B; whether the three controls produce comparable collapses at frontier scale (>100B, closed-weight) is an open empirical question (two confounded observations in Appendix~D are insufficient to extrapolate)."

---

### W3: Persona spot-check (pre-resolved in V59)

**Reviewer concern:**
> "The persona exclusion rests on a 10-trial spot-check of one model. Either extend to other models or soften the claim."

**V60 response:**

Addressed in V59. Three locations updated:
1. §3.6 header: "yield null detector results"
2. §3.6 persona paragraph: "We report persona/false-belief cells as **null detector results**, with the scenario-design artifact as the leading candidate explanation (whether it generalizes to Llama 3B and Mistral 7B is unverified---limitation (f))"
3. §4.2 Regime 3: concise cross-reference

Cells are no longer "excluded" but reported as null results with an identified candidate explanation.

---

### W4: Machine-rater ICC section shortened

**Reviewer concern:**
> "The machine-rater ICC appendix section is disproportionately long for a supplementary proxy that the paper itself says does not substitute for human ICC."

**V60 response:**

Shortened from ~12 lines to 4 lines. Removed: motivation paragraph, Qwen 32B collapse detail (already in §3.5), raw file release note, detailed "defensiveness jump" explanation. Retained: the key numbers (pooled ICC, per-feature ICC) and the caveat that it doesn't substitute for human ICC.

---

### W5: Human baseline section shortened

**Reviewer concern:**
> "The human baseline is degenerate (κ=0.00). The interpretation paragraph restates what the table already shows."

**V60 response:**

Removed the 3-line interpretation paragraph. The table caption ("All annotators collapsed to TRUTH; comparison to automated methods is degenerate") already conveys the key point. The section now consists of a 2-line result statement plus the table.

---

### W6: Figure 1(b) 70B marking

**Reviewer concern:**
> "The 70B sycophancy bar (n=50) is not prominently marked as preliminary. The dagger is easy to miss."

**V60 response:**

X-tick label changed from "Syco 70B†" to "70B† (n=50)" — the sample size is now visible directly on the axis without requiring the reader to find the caption footnote.

---

### W8: Structural redundancy

**Reviewer concern:**
> "§4.2 repeats information from §3.6 verbatim. The regimes should cross-reference rather than restate."

**V60 response:**

- §4.2 Regime 2 trimmed from full restatement to: "Largely dispositional (§3.6): marginal epistemic-pressure contribution is +5--14 pp over the system-prompt-only baseline."
- §4.2 Regime 3 trimmed to: "Null results; scenario-design artifact as leading candidate explanation (§3.6). Whether this generalizes beyond the Qwen 14B spot-check is unverified (limitation (f))."

---

### Q2/Q3: Base-model and FPR (pre-resolved in V59)

**Reviewer concern:**
> "Has a base-model been tested? What is the false-positive rate on benign conversation?"

**V60 response:**

Addressed in V59 via the "Paradigm boundaries" paragraph in §4.3:

> "**Paradigm boundaries.** Two untested conditions bound interpretation: **(i)** if refusal markers are RLHF-induced (as suggested by their absence on Qwen 32B and sensitivity to adversarial style constraints), the entire paradigm documented here detects post-training response styles under knowledge conflict, not deception per se---a base-model sweep (e.g., Mistral-7B-v0.1) would test this directly; **(ii)** the false-positive rate on benign (non-knowledge-conflict) outputs is unmeasured---if instruction-tuned models produce refusal markers at non-trivial base rates in ordinary conversation, the 80.1% on a balanced panel overstates deployment utility."

---

### Minor fixes

| Issue | Response |
|---|---|
| "defensiveness 0.77" in machine-ICC | Fixed to "correction-marker density 0.77" — this was the feature label from an earlier draft; the feature measured is correction-marker density |
| Mistral 7B sycophancy missing from Table 7 | §3.6 text corrected: sycophancy was run on Llama 3B and Qwen 14B only; Mistral 7B received persona and false-belief scenarios. Table 7 is correct; the prose now matches |
| Figure 1 caption says "excluded" | Updated to "null results" for consistency with V59 framing throughout |

---

## Summary of Changes (V59 → V60)

| File | Key changes |
|------|-------------|
| `figures/summary_results.tex` | 70B x-tick → "70B† (n=50)"; caption "excluded" → "null results" |
| `sections/experiments.tex` | §3.6 Mistral 7B sycophancy text corrected to match Table 7 |
| `sections/appendix.tex` | Machine-rater ICC shortened (~60%); human baseline interpretation paragraph removed; "defensiveness" → "correction-marker density" |
| `sections/conclusion.tex` | Frontier-scale scope caveat added |
| `sections/discussion.tex` | §4.2 Regimes 2/3 trimmed to cross-references |

**Verification:** 41 pages, 0 undefined references, main content ≤ 9 pages.
