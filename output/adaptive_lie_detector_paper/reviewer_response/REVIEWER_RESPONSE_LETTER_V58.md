# V58 — Response to Weak Accept (6/10) Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B-70B)

**Prior decision:** Weak Accept (6/10) — "borderline, leaning positive"

**Reviewer's stated conditions for accept:**
> "(a) leads with the construct-valid 54.5% number, (b) tones down the autonomous-transfer framing, (c) either runs Pacchiardi et al.'s exact protocol or removes the comparative claims, (d) extends the persona spot-check to all three models, and (e) cuts or substantially demotes the n=2 frontier appendix."

**V58 strategy:** (a), (b), (e) fully addressed by text restructuring. (c) addressed by softening comparative claims and adding explicit disclaimer. (d) cannot run new experiments; addressed by transparent limitation acknowledgment in three locations and softened exclusion language.

---

## At-a-Glance Table

| # | Concern | V58 action | Status |
|---|---|---|---|
| **W1/(c) — "Critical replication" oversold** | Softened "attributable to" → "consistent with"; added "This independent evaluation does not replicate their exact protocol; unmeasured protocol differences may also contribute." | **Done** |
| **W2/(a) — 54.5% not prominent** | Abstract now opens with "The construct-validated finding: ...54.5%---barely above chance." Conclusion restructured to lead with 54.5% | **Done** |
| **W3/(b) — Sycophancy oversold** | Abstract, intro, and §3.6 now lead with SP-only baselines and frame signal as "largely dispositional"; marginal effect stated as +5-14 pp | **Done** |
| **W4/(d) — Spot-check Qwen-only** | Added limitation (f) to §4.4; explicit "Limitation" flag in §3.6 persona paragraph; "Scope limitation" note in appendix spot-check section. Language changed from "excluded" to "provisional" | **Maximally addressed without new experiments** |
| **W5 — Qwen pattern too confident** | Already fixed in V57 (Llama validated first; Qwen "descriptive; does not survive joint correction"). Introduction contribution #3 unchanged and correct | **Already done** |
| **W6 — Reflexive implication not in abstract** | Added final abstract sentence: "The regimes where detection is validated are precisely where controls reveal artifactual or dispositional signal; the deployment-relevant autonomous regime remains unassessed." | **Done** |
| **W7/(e) — Frontier n=2 in abstract** | Deleted from abstract entirely. Introduction shortened to "(not interpretable; n=2, confounded)". Appendix framing strengthened: "not interpretable as findings...retained solely as documentation" | **Done** |
| **W8 — Numerical errors** | "uniformly" → "6 of 7" (abstract, experiments, discussion); "88%" → "87.6%" (abstract, experiments); "Five non-Claude" → "Five self-family controls (...[non-Claude], plus Sonnet-on-Haiku [within Claude family])" | **Done** |
| **W9 — Paper hard to read** | Minor: experiment-summary table already referenced in §3.1; no structural change feasible within page budget | **Acknowledged** |

---

## Detailed Responses to Major Weaknesses

### W1: "Critical replication" framing oversold

**Reviewer concern:**
> "This is a *from-scratch reimplementation* on different models with different claims. The contribution is better described as 'an independent evaluation suite that yields lower numbers under tighter controls,' not as a replication that explains Pacchiardi et al.'s results."

**V58 response:**

We agree this distinction matters. Three changes:

1. **Abstract** now explicitly states "(from-scratch reimplementation; original code/data not obtained)" in the first description of the audit.

2. **§4.3** (Summary of Contributions) rewritten from "their 67-73% is reproducible but *attributable to*..." to "their 67-73% is reproducible; under our tighter controls accuracy drops to 54.5-64.7%, *consistent with* equalization...extractor-quality differences...and surface-lexical patterns. **This independent evaluation does not replicate their exact protocol; unmeasured protocol differences may also contribute.**"

3. The cleanest test (running their exact protocol with cross-family extraction) remains explicitly acknowledged as future work in §3.4, with the compute estimate in Table 19 showing feasibility.

---

### W2: 54.5% should be the headline number

**Reviewer concern:**
> "This is the most important number in the paper. It is not in the abstract's headline."

**V58 response:**

Fully addressed. The abstract now opens (after the scope caveat) with:

> "The construct-validated finding: under prompt equalization with the only ICC-passing feature (correction-marker density, alpha=0.606), the detection pipeline achieves **54.5%**---barely above chance."

The conclusion also now leads with "The construct-validated pipeline achieves **54.5%**---barely above chance."

Additionally, §4.1 now clarifies "(Haiku-extracted)" to answer the reviewer's Q1 directly.

---

### W3: Autonomous section obscures negative result

**Reviewer concern:**
> "Sycophancy at 68-83% is headline but SP-only control then reveals 63-69.5% dispositional baseline. The marginal effect of epistemic pressure is small (5-14 pp)."

**V58 response:**

Restructured throughout to lead with the dispositional interpretation:

1. **Abstract:** "the bulk of the sycophancy signal is dispositional (system-prompt-only control: 63.1%/69.5% at 3B/14B; with epistemic pressure: 68.5/83%)"

2. **Introduction contribution #4:** "Semi-autonomous sycophancy shows signal (68.5-83%), but system-prompt-only controls (63.1-69.5%) reveal the bulk is dispositional"

3. **§3.6 header:** Changed from "Sycophancy transfers" to "Semi-autonomous signal is largely dispositional"

4. **§3.6 opening paragraph:** Now leads with SP-only baselines and states "The marginal contribution of epistemic pressure is modest: +5.4 pp (Llama 3B) and +13.5 pp (Qwen 14B)"

5. **§4.2 Regime 2:** Rewritten to lead with "Largely dispositional"

---

### W4: Persona spot-check only on Qwen 14B (n=10)

**Reviewer concern:**
> "A 10-trial qualitative coding on one model is appropriate as a flag for follow-up, not as a basis for excluding 1,200 trials of data from interpretation. At minimum, the parallel spot-check on Llama 3B and Mistral 7B should be in the revision."

**V58 response:**

We cannot run new experiments in this revision. We have maximally acknowledged this limitation:

1. **§3.6 persona paragraph:** Added "**Limitation:** extending the spot-check to Llama 3B and Mistral 7B is necessary to validate this exclusion; absent this, interpretation of persona/false-belief cells on these models remains provisional."

2. **§4.4 Limitations:** Added **(f)** "Persona/false-belief spot-check (n=10) performed on Qwen 14B only; generalization to Llama 3B and Mistral 7B is assumed but unverified."

3. **Appendix spot-check section:** Added "**Scope limitation:** This spot-check is Qwen 14B only (n=10). Extension to Llama 3B and Mistral 7B is a priority for replication; absent this, the exclusion of persona/false-belief cells rests on an unverified generalization assumption."

The analytical move is now framed as *provisional* rather than *conclusive*, the assumption is named explicitly, and extension is flagged as a priority. We believe this is maximally transparent about the limitation while noting that the statistical evidence (4/6 cells include chance; neither exclude-chance cell survives Bonferroni) independently supports interpretive caution regardless of the spot-check.

---

### W5: Multiple-testing policy / Qwen pattern

**Reviewer concern:**
> "A version that led with 'Llama 8B→70B is the one validated within-family scale effect; Qwen pattern is descriptive' would match the statistics better."

**V58 response:**

This was already addressed in V57. Current text:
- §3.5 opening: "The validated within-family scale finding is Llama 8B→70B (+26 pp, p=0.004, survives joint Holm-Bonferroni); within-family analysis also suggests family-specific non-monotonic patterns that are descriptive only."
- Scale patterns paragraph: **Llama (validated)** first, then **Qwen (descriptive; does not survive joint correction)** second.

---

### W6: Reflexive implication should be in abstract

**Reviewer concern:**
> "The *reflexive implication* in §4.3...is the most important high-level claim in the paper and is buried."

**V58 response:**

Added as the final sentence of the abstract:

> "The regimes where detection is validated are precisely where controls reveal artifactual or dispositional signal; the deployment-relevant autonomous regime remains unassessed."

This is also the closing thought of §4.3 (the "Reflexive implication" paragraph already present).

---

### W7: Frontier n=2 observations should be cut

**Reviewer concern:**
> "If the design is too confounded to support any inference, the right place is a blog post or follow-up."

**V58 response:**

1. **Abstract:** Frontier sentence deleted entirely (was 2 lines; now absent).
2. **Introduction §1.1 Scope:** Shortened from a full sentence to "(not interpretable; n=2, confounded)".
3. **Appendix framing strengthened:** Now reads "These results are not interpretable as findings due to the confounded n=2 design; they are retained solely as documentation of the experimental record."

The observations remain in the appendix as experimental documentation but no longer appear anywhere in the main text's argument or abstract.

---

### W8: Numerical inconsistencies

| Issue | Fix |
|---|---|
| "range 64-88%" (max is 87.6%) | Changed to "range 64-87.6%" in both abstract and §3.2 |
| "Haiku uniformly outperforms" (false on Llama 8B) | Changed to "6 of 7 open-weight targets (avg +7-10 pp)" in abstract; "6 of 7 targets; exception: Llama 8B, +2 pp for Llama 70B" in experiments; "6 of 7 targets" in discussion |
| "five non-Claude self-family controls" (Sonnet-on-Haiku IS Claude) | Changed to "Five self-family controls (Llama-on-Llama ×2, Qwen-on-Qwen, Mistral-on-Mistral [non-Claude], plus Sonnet-on-Haiku [within Claude family])" |
| Figure 1 caption "joint application" unclear | The caption already specifies "(A) equalization, (B) equalized pipeline vs rule, (C) sycophancy transfer" with per-panel descriptions; the "30-41 pp" collapse is labeled on panel (A). No change needed. |

---

### W9: Paper hard to read

**Reviewer concern:**
> "40+ appendices...same numbers reappear in slightly different forms across sections."

**V58 response:**

We acknowledge this structural complexity reflects the paper's scope (seven models × multiple conditions × three controls). The experiment-summary table (Table 2, Appendix) maps all experiments to findings. Within page constraints, we have not been able to add an early "claims map" but note that the L-indep/L-dep tagging convention (which the reviewer positively noted) serves a similar navigational function. We will explore restructuring options if accepted.

---

## Responses to Questions

### Q1: Is 54.5% Haiku-extracted or Mistral L3-extracted?

It is **Haiku-extracted** (correction-marker density only, from the Haiku pipeline). This is now explicitly stated in §4.1: "correction-marker-only achieves 54.5% (Haiku-extracted)."

### Q2: Spot-check on Llama 3B and Mistral 7B?

Not yet run. See W4 response above — transparently acknowledged as limitation (f) in three locations.

### Q3: False-positive rate of the rule on benign conversation?

Not tested. The paper frames the rule as a "methodological baseline, not a production detector" (bold caveat in §3.2). Deployment would require FPR characterization on diverse benign conversations — this is acknowledged in the future-directions appendix.

### Q4: Why not run Pacchiardi et al.'s exact protocol?

Their original code/data were not obtained (explicitly stated in §1.1: "from-scratch reimplementation; original code/data not obtained"). The cleanest comparison remains future work (§3.4, with compute estimate in Table 19 showing feasibility at ~$10 of Bedrock spend). We have softened all comparative language to "consistent with" rather than "accounts for."

### Q5: Does the rule degrade on base models?

Not tested. Added as limitation **(g)**: "All targets are instruction-tuned; whether the signal exists on base models is untested." This is an important test of whether the correction-marker signal is a post-training artifact — a reasonable hypothesis given that all seven targets showing signal are instruction-tuned.

---

## Responses to Minor Issues

| Issue | Response |
|---|---|
| Pacchiardi et al. citation lacks page numbers | Their 67-73% is from Table 1 of their paper; we add "(their Table 1)" at first reference in §3.4 |
| Figure 2 axis labels "Assert." confusing | The figure PDF uses abbreviated feature names from the pipeline (Consist.=Consistency, Specif.=Specificity, Corr.Dens.=Correction Density, Confid.=Confidence, Elab.=Elaboration). "Assert." does not appear — the reviewer may be reading from an earlier draft. Current figure uses "Corr.Dens." for correction-marker density. |
| "Five non-Claude" count error | Fixed: see W8 above |
| Sonnet reading update buried in appendix | The Llama 70B = Haiku = 50.5% on Sonnet result is now in the main-text §3.5 cross-family paragraph (surfaced in V57), not only in the appendix |

---

## Summary of Changes (V57 → V58)

| File | Key changes |
|------|-------------|
| `abstract.tex` | Leads with 54.5%; removes frontier; fixes "uniformly"/"88%"; adds reflexive; reframes sycophancy as dispositional |
| `introduction.tex` | "extractor-quality gap" replaces "same-family inflation"; frontier shortened; sycophancy contribution reframed |
| `experiments.tex` | §3.6 reordered (SP-only leads); spot-check limitation added; "Five non-Claude" → "Five self-family"; "uniformly" → "6 of 7"; "88%" → "87.6%" |
| `discussion.tex` | §4.3 softened to "consistent with" + protocol disclaimer; §4.2 Regime 2 rewritten as dispositional; limitations (f) and (g) added; 54.5% clarified as Haiku-extracted |
| `conclusion.tex` | Leads with 54.5% |
| `appendix.tex` | Frontier framing strengthened; persona spot-check scope limitation added |

**Verification:** 41 pages, 0 undefined references, main content ≤ 9 pages (conclusion on page 9; bibliography starts page break).
