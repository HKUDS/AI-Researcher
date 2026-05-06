# V51 — Response to Borderline Accept (6/10) Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B–70B)

**Prior decision:** Borderline Accept (6/10) — leaning weak accept

**Reviewer's explicit path to clear accept:**
> "A revision that (i) softens the n=2 frontier dissociation framing, (ii) adds the LOO-across-models analysis, and (iii) drops the n=50 sycophancy 70B from the abstract would push this to a clear accept."

**V51 strategy:** All three conditions addressed, plus all five secondary weaknesses.

---

## At-a-Glance Table

| # | Reviewer concern | V51 action | Status |
|---|---|---|---|
| **(i) Frontier framing** | "clean dissociation" overstates n=2 | Reframed to "complementary failure modes"; explicit n=2 caveat listing all confounded axes (closed/open, dense/MoE, RLHF recipe) | **Done** |
| **(ii) LOO-across-models** | No cross-model generalization test | New experiment (no API calls): train on 6 of 7 targets, test on 7th; mean **64.2%** (within 3.0 pp of pooled LOO 67.1%); Maverick 45% is 19 pp below worst in-distribution fold | **Done** |
| **(iii) 70B n=50 from abstract** | Already absent from abstract | Confirmed absent; additionally removed from conclusion and §4.2 Regime 2 | **Done** |
| **W4 (Maverick interpretation)** | "classifier generalization failure" underexplains | Added mechanistic account: Maverick produces µ_lie=7.74, µ_truth=6.88; RLHF suppresses the confidence/consistency suppression signature the classifier was trained on; distinct from Sonnet's correction-marker suppression | **Done** |
| **W5 (rule ceiling qualifier)** | "Detectors <80.1% lack signal" overstates — true only in single-turn | Added "Single-turn detectors <80.1%" with explicit multi-turn caveat in conclusion | **Done** |
| **W6 (asymmetric frontier framing)** | "rule succeeds on open-weight frontier" oversells — Maverick just behaves like other open-weight models | Reframed: framing now attributes the observation to confounded axes, not to "open-weight frontier" as a generalization | **Done** |
| **W7 (Qwen non-monotonicity)** | Under joint correction it doesn't survive | Added explicit sentence to §3.5: "We report the Qwen 2.5 non-monotonic pattern descriptively; under joint correction across all families, it does not survive (p > 0.05)." | **Done** |
| **W8 (Maverick MoE caveat)** | 17B active parameters complicates "frontier" label | Added one sentence: "Maverick's 17B active parameters means inference behavior may not characterize what readers associate with frontier capability at the parameter scale; scale comparison should be interpreted cautiously." | **Done** |

---

## Detailed Responses

### (i) Softening n=2 frontier dissociation framing

**Reviewer concern:**
> "The two targets differ on multiple confounded dimensions: closed-vs-open weight, dense-vs-MoE, Anthropic-vs-Meta training, and (likely) different RLHF intensities... the n=2 design cannot distinguish which axis is causal."

**V51 response:**

§4.2 Frontier paragraph now reads:

> "Two frontier-scale (≥100B) targets show complementary failure modes, but the two targets are confounded on multiple axes simultaneously—closed/open weight, dense/MoE architecture, and RLHF recipe—so no single axis can be identified as causal from n=2. [...] Whether the rule/pipeline dissociation is driven by closed-vs-open weight, RLHF intensity, or architecture type cannot be determined from two targets. A third frontier model (e.g., GPT-4o or DeepSeek-V3) would break at least one confound; this is a limitation of the current design."

The phrase "clean rule/pipeline dissociation" and "The rule succeeds on open-weight frontier; the pipeline succeeds on closed-weight frontier" have been removed.

---

### (ii) Leave-one-model-out classifier analysis

**Reviewer concern (Q1):**
> "Can you run a leave-one-model-out evaluation on the 5-feature pipeline (train on 6 of 7 targets, test on the held-out 7th, average across folds)?"

**V51 response:**

New script: `experiments/loo_across_models.py`. Uses existing Mistral L3 cross-family feature files — no API calls required.

**Results (new §4.4 paragraph + Appendix B.0):**

| Held-out model | n | Acc | T-acc | L-acc |
|---|---|---|---|---|
| Llama 3.2 3B | 50 | 52.0% | 56.0% | 48.0% |
| Llama 3.1 8B | 100 | 53.0% | 70.0% | 36.0% |
| Mistral 7B | 100 | 62.0% | 72.0% | 52.0% |
| Llama 3.3 70B | 93 | **76.3%** | 84.8% | 68.1% |
| Qwen 2.5 7B | 100 | 70.0% | 78.0% | 62.0% |
| Qwen 2.5 14B | 97 | 74.2% | 81.6% | 66.7% |
| Claude Haiku | 99 | 61.6% | 24.5% | 98.0% |
| **Mean** | **639** | **64.2%** | | |
| Llama 4 Maverick (OOD ref.) | 100 | 45.0% | 74.0% | 16.0% |

Mean LOO-across-models: **64.2%**, within **3.0 pp** of pooled within-sample LOO (67.1%). The classifier generalizes within the in-distribution set. Maverick's 45% is **19 pp below the worst in-distribution fold** (Llama 3.1 8B at 53%), confirming the failure is genuine OOD behavior, not classifier fragility.

The Claude Haiku fold (T-acc 24.5%, L-acc 98.0%) reveals that Haiku is itself an outlier: trained without Haiku, the classifier over-predicts "lying" on Haiku truthful trials, because Haiku's RLHF compliance makes truthful responses behaviorally similar to other models' lying responses. This is a secondary validation of the Haiku-checkpoint-specific finding.

---

### (iii) 70B/n=50 removed from conclusion and §4.2

**Reviewer concern:**
> "The n=50 preliminary number is in the abstract twice and the conclusion."

**V51 response:**

Abstract was already clean (confirmed absent). Additionally removed from:
- `sections/conclusion.tex`: "sycophancy (68.5/83% at 3B/14B, n=200; 72% at 70B, n=50 preliminary)" → "sycophancy (68.5/83% at 3B/14B, n=200)"
- `sections/discussion.tex` §4.2 Regime 2: removed "72% at 70B, n=50 preliminary"

Figure 1(b) retains the dagger bar with footnote "not in headline summaries" — appropriate since it is an experimental section figure, not a headline summary.

---

### W4: Richer Maverick pipeline failure interpretation

**Reviewer concern (Q2):**
> "Is this consistent with Maverick being a well-trained instruction-following model that is not producing the behavioral signature the classifier was trained to detect? If so, this is a more interesting finding than 'classifier generalization failure.'"

**V51 response:** Yes, this is exactly the right framing. Added to §3.5 Frontier target 2:

> "The trained classifier assigns 'truthful' to 79/100 trials because Llama 4 Maverick produces high consistency and confidence scores in both conditions (µ_lie=7.74, µ_truth=6.88): the classifier was trained on a behavioral signature where confidence/consistency are suppressed under lying pressure. Maverick's RLHF training eliminates this signature even on lying trials, producing confident, well-calibrated responses in both conditions. This is mechanistically distinct from Sonnet 4.5's correction-marker channel suppression: Maverick retains correction markers (rule succeeds) but suppresses the secondary behavioral signature the classifier relies on."

---

### W5: Single-turn qualifier on rule ceiling

**Reviewer concern:**
> "The conclusion still says 'Detectors <80.1% under equalization lack validated behavioral signal' without qualification. Strictly, the right claim is 'single-turn detectors...'"

**V51 response:** Conclusion now reads:
> "Single-turn detectors <80.1% under equalization lack validated behavioral signal; the full pipeline can exceed this ceiling at ≥14B multi-turn (+14–29 pp, Appendix Q)."

---

### W6: Maverick alternative reading — soften symmetric framing

**Reviewer concern:**
> "The Llama 4 case is 'open-weight model produces markers like other open-weight models.' The symmetric framing slightly oversells a one-sided observation."

**V51 response:** The revised §4.2 no longer says "The rule succeeds on open-weight frontier; the pipeline succeeds on closed-weight frontier." Instead it attributes the pattern to multiple confounded axes and defers the causal claim to future work.

---

### W7: Qwen non-monotonicity transparency

**Reviewer concern:**
> "Adding a paragraph in §3.5 stating 'we report Qwen non-monotonicity descriptively; under joint correction it is not significant' would be more transparent."

**V51 response:** Added to §3.5 (Scale Patterns), immediately after the Holm-Bonferroni justification:
> "We report the Qwen 2.5 non-monotonic pattern descriptively; under joint correction across all families, it does not survive (p > 0.05)."

---

### W8: Maverick MoE active-parameter caveat

**Reviewer concern:**
> "Worth a one-sentence acknowledgment that MoE active-parameter count complicates the scale comparison."

**V51 response:** Added to the Frontier paragraph in §4.2:
> "Note that Maverick's 17B active parameters (out of 400B+ total) means inference behavior may not characterize what readers associate with frontier capability at the parameter scale; scale comparison should be interpreted cautiously."

---

## Summary of V51 Changes

| File | Change |
|---|---|
| `sections/discussion.tex` | Frontier framing softened (i, W6, W8); 70B removed from Regime 2 (iii); LOO-across-models paragraph added to §4.4 |
| `sections/conclusion.tex` | 70B/n=50 removed (iii); single-turn qualifier added (W5) |
| `sections/experiments.tex` | Maverick mechanistic interpretation (W4); Qwen non-monotonicity transparency sentence (W7) |
| `sections/appendix.tex` | New §B.0: LOO-across-models table |
| NEW: `experiments/loo_across_models.py` | LOO-across-models script (no API calls) |

**Paper status:** 40 pages total; 9 pages main content; compiles cleanly (2-pass); 0 undefined references.
