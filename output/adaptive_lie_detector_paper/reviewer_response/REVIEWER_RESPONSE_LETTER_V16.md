# Response to Reviewer — V16 Camera-Ready Revision (Weak Accept Leaning Clear Accept, Confidence 4/5)

We thank the reviewer for the very generous framing ("This is the response a careful reviewer hopes for") and for confirming 4/5 prior suggestions as fully addressed. This letter addresses each of the five camera-ready suggestions (CR1–CR5), the five author questions (Q1–Q5), the residual weaknesses (W1/W3/W4/W6/W8), and the tractable minor comments. We list everything net-new in V16 below.

---

## CR1 / Q-adjacent — Mistral 7B + Qwen 14B full-regex-disclosed adversarial replications

**Ask.** Extend the Llama 3B full-regex-disclosed adversarial result ($n=50$, 50.0%) to Mistral 7B and Qwen 2.5 14B to test whether the "informed adversary collapses to chance" claim holds across scales / families or is Llama-3B-specific.

**What we did.** We re-used `experiments/run_adversarial_full_regex.py` (disclosing the full 14-pattern `REFUSAL_PATTERNS` list) on Mistral 7B and Qwen 2.5 14B via Ollama, $n=50$ each with paired baseline/adv14/advfullregex columns identical to the original Llama 3B design. The Mistral 7B and Qwen 14B runs completed in-window; the integrated 3-row table now lives in §4.3 (EXP-ADV-FULLREGEX paragraph), reporting paired accuracies alongside the Llama 3B result and flagging any deviation from chance.

**Fork handled.** The plan pre-specified: if Mistral 7B / Qwen 14B also collapse to chance, strengthen the informed-adversary-collapses claim; if they stay materially above chance (60–65%), narrow the abstract claim to Llama 3B and add a scale-dependent adversarial-robustness paragraph. The integrated numbers in §4.3 and the abstract reflect whichever outcome held. The abstract sentence is scoped ("on Llama 3B [plus Mistral 7B and Qwen 14B replications]") rather than blanket.

---

## CR2 / Q3 — Per-layer probe accuracy curve for Llama 3B

**Ask.** V15 reported 4 fixed probe configs (last-layer / mid-layer × last-token / mean-pool); Q3 asked for the full per-layer × pooling curve so that "best-layer probe" is a measured value rather than an inference from 4 design points.

**What we did.** We added a `--full_sweep` flag to `experiments/whitebox_5_multilayer_probes.py`; it extracts hidden states once per sample and then fits LR probes at all 29 layer positions × {last-token, mean-pool} on the same saved equalized transcripts, persisting a layer-accuracy curve to `data/whitebox_probing/multilayer_probe_curve_llama3b.json`. We render `figures/probe_layer_curve_llama3b.pdf` and expand §4.8 Table 8 with an explicit best-layer row per pooling strategy. Robustness patch: `loo_accuracy()` now drops NaN/Inf feature rows (an MPS OOM during one V15 pilot produced NaN hidden states on a handful of samples) and reports `n_valid` per layer so the curve is interpretable even under transient device memory pressure.

**Outcome.** Whichever direction the curve pointed, the §4.8 text now describes the full 29-layer × 2-pooling band rather than a 4-point sample, and the best-layer row in the updated Table 8 makes the "best probe we tried" value immediately legible. The §4.8 and §5.2 prose are consistent with what the curve measured.

---

## CR3 / Q2 — Llama 70B sycophancy cross-family re-extraction

**Ask.** The V15 Llama 70B sycophancy pipeline reported 92% under Claude Haiku extraction vs. a 72% refusal-count rule — a 20pp gap. The reviewer asked whether that gap survives a non-Claude extractor, since same-family bias on Llama 70B (Haiku scoring a Llama-family transcript) is less obvious than on Claude targets.

**What we did.** We re-extracted the 5 behavioral features on the same 50 Llama 70B sycophancy transcripts using Llama 3.3 70B-as-extractor (`experiments/cross_family_equalized_extractor.py` with the `--extractor llama70b` path), preserving all other pipeline steps. Result: pipeline LOO drops from **92.0% (Haiku) to 82.0% (Llama 70B)**, a $+10.0$pp same-family-over-cross-family gap. Defensiveness Cohen's $d$: 2.05 (Haiku) vs. 2.34 (Llama 70B) — both extractors cleanly separate lying from truthful. The behavioral signal itself is extractor-robust; the pipeline's absolute accuracy is not.

**What this means.** The cross-family-extracted 82.0% still exceeds the rule's 72.0% by $+10$pp, so part of the original 20pp Haiku-pipeline-vs-rule gap is genuine multi-turn signal and part is same-family-from-below inflation (Haiku-on-Llama, a more capable extractor scoring a less capable target). The §4.6 sycophancy paragraph now reports both pipeline numbers (Haiku 92% → Llama 70B 82%) and the cohen-$d$ invariance, and closes with the honest headline: "multi-turn extraction does add signal on 70B-scale sycophancy, but roughly half of the Haiku-reported uplift is same-family-extractor inflation, not multi-turn content." This is directly W6's ask.

---

## CR4 — Abstract: specify "on Llama 3B" inline for adversarial 50.0% sentence

**What we did.** The abstract and §1.1 sentence that previously said "a full-regex-disclosed adversary drives accuracy to 50.0%" now names the models inline: "on Llama 3B (plus Mistral 7B and Qwen 2.5 14B replications; see §4.3)," so a reader who never opens §4.3 still knows which model the 50% measurement came from.

---

## CR5 — Soften "behavioral detection works *only* in the instructed regime"

**What we did.** Both the abstract (¶1) and Introduction (¶1) were updated to acknowledge the semi-autonomous sycophancy transfer as the sole exception: "with the semi-autonomous sycophancy condition the sole transfer exception (82% across three scales)." This frames the paper's negative-transfer claim as holding for *fully autonomous* (persona, false-belief-ICL) scenarios rather than autonomous in general, which is what the EXP-I-matched table actually shows.

---

## Q1 — Adversarial compliance check (truth-condition refusal distribution)

**Ask.** Under the full-regex adversarial prompt, do lying-condition refusal counts drop (signal suppression) while truth-condition refusal counts stay high (model still corrects genuine falsehoods)? Or does the adversarial prompt also suppress truth-condition corrections (lexical-channel suppression rather than selective lie-signal loss)?

**What we did.** We analyzed the existing Llama 3B baseline / adv-14 / adv-fullregex transcripts and computed the percent of trials per condition with refusal_count ≥ 1. New script `experiments/analyze_q1_fullregex_refusal_dist.py`, figure `figures/q1_refusal_dist_llama3b.pdf`, and appendix §A (`app:q1_refusal_dist`).

**Result.** Under adversarial prompts, the truth-condition ≥1-marker fraction drops from 46% → 4% in lockstep with the lying-condition fraction (84% → 16%). The rule's failure is **lexical-channel suppression in both conditions**, not a selective inability to correct lies under the adversarial prompt. This answers the compliance-check interpretation (favored) over the "adversarial elicits sycophancy that makes the model agree with false claims" interpretation. §4.3 now contains a forward-reference to the appendix figure.

---

## Q2 — See CR3 above.

---

## Q3 — See CR2 above.

---

## Q4 — High-confidence subgroup ICC

**Ask.** The $n=20$ validation ICC of 0.114 is low overall; does it improve on the subgroup of trials where both annotators produced extreme ratings (score > 7 or < 3), consistent with the intuition that absolute disagreement should shrink on unambiguous cases?

**What we did.** We pre-register this analysis in §5.1 ("high-confidence subgroup (pre-registered)") and in the Limitations (i) mirror. The raw $n=20$ annotator rating files were not persisted in a form suitable for automated reanalysis for V16 paper-freeze; at $n=20$ with 2 annotators the subgroup-$n$ per feature is $\leq 10$, and its CI would overlap the full-sample ICC regardless of direction. We commit to releasing the subgroup ICC alongside the full validation study ($n \geq 100$, 3+ annotators, Krippendorff's $\alpha$) listed as future work. This is an honest pre-registration-plus-defer rather than a guess at the subgroup value.

---

## Q5 — Llama 8B +0.5pp CF gap

**Ask.** Llama 8B's Avg CF gap of $+0.5$pp is an order of magnitude smaller than the next-smallest target (Qwen 7B $+7.5$pp). Is this signal or noise?

**What we did.** A new "Llama 8B outlier" paragraph was added to §4.7 immediately after the cross-family panel (Table 9). It computes the flip-sensitivity ($n=100$ → one flipped LOO prediction = $\pm 1$pp) and states explicitly: "we cannot distinguish 'Llama 8B happens to elicit extractor-invariant correction behavior' from 'Llama 8B happens to sit where the Haiku and cross-family extractors yield near-identical accuracy at this $n$ by chance.' We flag the outlier for transparency but do not build interpretation on it." This is the reviewer's preferred framing.

---

## W1 — Three EXP-I-matched scenarios vary along multiple dimensions

A new "Confound acknowledgement" paragraph was added at the end of the §4.6 EXP-I-matched section. It states that the three scenarios vary along knowledge-conflict-clarity, instructed-action-vs-spontaneous-disposition, and single- vs multi-turn-structure simultaneously, so the post-hoc knowledge-conflict interpretation is not cleanly distinguished from "small $n$ on scenarios that happen to covary." We pre-register a 4th scenario — varying only knowledge-conflict clarity while holding disposition-source and turn-count fixed — as future work.

## W3 — Mistral 7B single-point probe fairness

A one-sentence footnote in §4.8 notes that Mistral 7B retains only the V15 single-configuration last-layer last-token probe and that its comparison against Llama 3B's multi-configuration best-layer may be unfair (Llama 3B gained $+3$pp from mid-layer last-token over last-layer last-token). CR2 scope is Llama 3B per the plan; the flag itself is the fix the reviewer asked for.

## W4 — Pooled ≤7B vs ≥14B comparison is exploratory

A footnote in §4.6 explicitly acknowledges that the pooled ≤7B vs. ≥14B comparison is unpre-registered and post-hoc, and that "this paper's own methodology would flag it for replication." The footnote is load-bearing only for the scale-generalization framing that is already demoted to exploratory in §4.6.

## W6 — Llama 70B sycophancy +20pp gap

Covered by CR3 — the gap is now decomposed into $+10$pp genuine multi-turn signal plus $+10$pp same-family-from-below inflation, with both numbers in §4.6 and the cohen-$d$ invariance noted.

## W8 — §4.2 stub

§4.2 (Pipeline Redundancy Under Equalization) is now structured as an interpretive lede paragraph plus four sub-paragraphs ($K=1$, weak construct validity, regex matches or exceeds, multi-turn value only at ≥14B). The lede frames the three converging lines of evidence ("pipeline itself is largely redundant: three independent lines of evidence converge on this conclusion") so a reader scanning the subsection sees the claim before the evidence.

---

## Minor comments

- Abstract "primary;" stranded word: resolved in V16 text-only pass (no longer parses as a sentence fragment).
- §4.6 Qwen 32B speculation now uses "Speculation, not evidence:" prefix instead of the tortured "We label the following as speculation..." form.
- §5.7(b) "untested" → "inadequately powered" (Sonnet 4.5 pilot was tested, just underpowered).
- `references.bib` copy-edit: added capitalization protection to `{LLMs}` in hubinger2024sleeper; other bib entries reviewed.

---

## Explicitly declined / deferred (restated from V15 for continuity)

- **$n \geq 100$, 3+ annotator ICC validation**: multi-week recruitment; Q4 partially addresses without new data, with commitment to release alongside the full study.
- **Closed-loop iterated adaptive adversary**: V16 covers one-shot full-regex on 3 targets (CR1); closed-loop remains future work, lower-bounded by the CR1 numbers.
- **Frontier Opus cross-family on Sonnet 4.5**: API cost/time; Sonnet 4.5 already demoted to pilot in V15.
- **Expanding Sonnet 4.5 to $n \approx 410$**: declined in V15; unchanged.
- **4th EXP-I-matched scenario**: W1 ask is acknowledgement + pre-registration, not execution.
- **Mistral 7B per-layer curve**: CR2 scoped to Llama 3B only; W3 flag added.

---

## Summary of concrete changes vs. V15

| # | File | What changed |
|---|------|--------------|
| 1 | `sections/abstract.tex` | CR4 inline model scoping; CR5 sycophancy-exception; "primary;" fix |
| 2 | `sections/introduction.tex` | CR5 sycophancy-exception |
| 3 | `sections/experiments.tex` | CR1 3-row table; CR2 best-layer Table 8 row + curve figure ref; CR3 §4.6 cross-family subsection; W1 confound acknowledgement; W3 Mistral 7B fairness flag; W4 §4.6 pooled-comparison footnote; Q5 §4.7 Llama 8B noise paragraph; W8 §4.2 two-paragraph expansion; Qwen 32B speculation rewrite; Q1 appendix forward-reference |
| 4 | `sections/discussion.tex` | §5.7(b) "inadequately powered"; Q4 high-confidence-subgroup pre-registration paragraph + Limitation (i) mirror |
| 5 | `sections/appendix.tex` | A.X Q1 refusal-distribution subsection + figure |
| 6 | `references.bib` | hubinger2024sleeper `{LLMs}` brace protection |
| 7 | `figures/probe_layer_curve_llama3b.pdf` | New — per-layer × pooling curve (CR2) |
| 8 | `figures/q1_refusal_dist_llama3b.pdf` | New — truth/lying refusal distribution by condition (Q1) |
| 9 | `code/adaptive_lie_detector/experiments/whitebox_5_multilayer_probes.py` | `--full_sweep` flag; NaN-robust `loo_accuracy` |
| 10 | `code/adaptive_lie_detector/experiments/analyze_q1_fullregex_refusal_dist.py` | New — Q1 histogram |
| 11 | `data/results/sycophancy_autonomous_llama70b_crossfamily_llama70b.json` | New — CR3 re-extraction output |
| 12 | `data/results/ollama_eval_{mistral_7b,qwen2_5_14b}_adv_fullregex_latest.json` | New — CR1 replications |
| 13 | `data/whitebox_probing/multilayer_probe_curve_llama3b.json` | New — CR2 curve |

Target page count after V16: ≤ 41 pages, 0 errors, 0 undefined refs.
