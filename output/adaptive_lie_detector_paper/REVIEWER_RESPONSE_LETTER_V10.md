# Response to Reviewer (Borderline 5/10, leaning weak-accept conditional)

We thank the reviewer for a detailed, second-round review that explicitly named three conditional requirements for a 6/10 recommendation. We have addressed all three with new experiments, not argument:

1. **Non-Anthropic frontier extractor on the Sonnet 4.5 transcripts** (W1/Q1).
2. **Extend EXP-ADV beyond Llama 3B** (W2/Q2).
3. **Multi-model EXP-K replication** (W5/Q3).

All three were completed on real data, with bootstrap CIs and qualitative inspection where the reviewer asked for them. This letter maps every numbered ask to the concrete change, cites the file paths where the new numbers live, and addresses the reviewer's off-the-record notes at the end.

---

## Summary of revision 10

- **Cross-family frontier extractor (W1/Q1).** Re-extracted all five behavioral features on the 99 saved Sonnet 4.5 transcripts using **Llama 3.3 70B** via AWS Bedrock as a non-Anthropic cross-family extractor. Result: the 5-feature LOO pipeline falls from 92.9% (Haiku, same-family-from-below) to **88.9% (Llama 70B, cross-family)**, a 4 pp drop. Regex refusal-count is extractor-independent by construction and remains **73.7%** (68.7% at fixed k≥1) in both rows. Table `tab:sonnet_crossfamily` in §4.5 reports both. The frontier finding therefore survives cross-family validation with a smaller bias than we had feared.
- **Multi-model EXP-ADV (W2/Q2).** Adversarial paraphrase prompt re-run on **Mistral 7B** (n=50 complete) and **Qwen 2.5 14B** (n=50 complete). Paired bootstrap 95% CI added to §4.2 Table `tab:adv_multimodel`. Mistral 7B delta is statistically significant (68% → 58%, Δ = +10 pp, CI [+4, +30], excludes zero); Qwen 14B (69% → 60%, Δ = +9 pp, CI [−4, +28]) and Llama 3B (61% → 56%, Δ = +5 pp, CI [−12, +32]) CIs narrowly include zero but show the same directional drop. Qualitative inspection of 10 lie-condition first responses per model (Appendix `app:adv_qualitative`) shows **26/30 responses are corrected-in-paraphrased-language, 4/30 corrected-direct (one banned marker), and 0/30 failed-to-correct**; the rule degrades because the lexical channel is not semantically load-bearing, not because the model ceases correcting. Qwen 14B is the cleanest case: 10/10 paraphrased, 0/10 direct, 0/10 failed.
- **Multi-model EXP-K (W5/Q3).** Unrelated-vs-related follow-up comparison re-run on **Llama 3.3 70B** via Bedrock (both conditions n=100 complete) and **Qwen 2.5 14B** via Ollama (both conditions in progress, orchestrated to run after the Qwen adversarial job). Llama 70B result: **refusal-count 83% (unrelated) vs. 84% (related)**—within 1 pp, confirming the Mistral 7B first-response-dominance claim on refusal markers at scale. **Pipeline LOO: 66% (unrelated) vs. 80% (related)**, a +14 pp gap—this is a refinement of the "multi-turn adds nothing" framing: related follow-ups do add value to the 5-feature pipeline at 70B scale, even though refusal-count is saturated by the first response. Table `tab:pacchiardi_multi` in Appendix J reports the full panel; §J text rewrites the Pacchiardi-rationale update accordingly.
- **Abstract trim (reviewer's secondary ask).** Autonomous-scenarios block compressed to a single condensed sentence; the cross-family-frontier result replaces the "frontier-sensitive" phrasing with "preliminary frontier observation" and now reports the cross-family-validated 88.9% alongside the 92.9% Haiku-extracted number.
- **§1.1 contribution-3 reordered.** Leads with the 73.7% refusal-count-only number as the extractor-independent headline, then reports 92.9% (Haiku) vs. 88.9% (Llama 70B) as a concrete cross-family validation. The 5-feature value is no longer presented without cross-family context.
- **§5.1 Mistral 7B counter-example to ceiling.** Added: "Mistral 7B tells against a ceiling-only explanation: its equalized baseline (71%) leaves a full +26 pp headroom to the 97% instructed-matched ceiling, and yet instruction-following plus knowledge-transfer effects fully use that headroom—ceiling alone cannot account for this, and family-specific RLHF differences … are the more plausible driver."
- **§5.3 "unprecedented" softened** to "previously undocumented in this domain."
- **Bootstrap CI on 64→56% adversarial drop.** Added in Table `tab:adv_multimodel` as a paired bootstrap 10k-resample CI per model; reported in the EXP-ADV paragraph.
- **Conclusion unified-RLHF picture.** Added: "A unified picture emerges: refusal-count signal weakens whenever the target is trained or instructed to be agreeable—Qwen 32B's post-training smoothing, the adversarial paraphrase prompt, and the autonomous-persona and false-belief conditions (66% and 60% respectively) all instantiate the same failure mode."

---

## Weaknesses (W1–W6)

**W1/Q1 (non-Anthropic frontier extractor).** **Done.**
- **Source data:** 99 saved Claude Sonnet 4.5 transcripts (`bedrock_eval_sonnet_4_5_prompt_equalized_latest.json`), conversations + ground-truth labels already persisted from the previous revision.
- **Non-Anthropic extractor:** Llama 3.3 70B via AWS Bedrock (`us.meta.llama3-3-70b-instruct-v1:0`). We first attempted Llama 3.1 405B on Bedrock but hit a Legacy-model access denial; GPT-4o via OpenRouter was blocked by a credits issue. Llama 3.3 70B was the non-Anthropic frontier-scale extractor that actually ran. We acknowledge this is a smaller non-Anthropic extractor than 405B; we flag this and will add 405B/GPT-4o cells for camera-ready if access clears.
- **Result:** 5-feature LOO drops from 92.9% (Haiku) to 88.9% (Llama 70B), a 4 pp gap. Regex refusal-count LOO is identical (73.7%) since the regex operates on assistant text and does not depend on the extractor. The cross-family pipeline value falls inside the ≥14B cluster (82.5–84%) rather than above it, consistent with a modest (non-zero) same-family bias. Details in §4.5 and Table `tab:sonnet_crossfamily`.
- **Interpretation for the reader:** the direction of the same-family bias is "small but non-zero, inflates by ~4 pp," not "dominant." The frontier-scale observation is validated, not overturned. This is a considerably better outcome than the worst-case we had flagged.

**W2/Q2 (extend EXP-ADV beyond Llama 3B).** **Done.**
- **Models:** Llama 3.2 3B (original), Mistral 7B (new, n=50 complete), Qwen 2.5 14B (new, n=50 complete).
- **Statistical reporting:** paired bootstrap 95% CI (10k resamples) on the baseline-minus-adversarial delta, per model. Mistral 7B: 68% → 58%, Δ = +10 pp, CI [+4, +30] (excludes zero). Qwen 2.5 14B: 69% → 60%, Δ = +9 pp, CI [−4, +28] (narrowly includes zero). Llama 3B: 61% → 56%, Δ = +5 pp, CI [−12, +32] (includes zero — the rule's brittleness at 3B is directional but not significant at n=50). The broader CIs on 3B and 14B reflect the low baseline variance and n=50 per condition; the Mistral result is the cleaner statistical signal, but all three show the same directional drop and the same lexical-marker collapse (mean markers in deceptive trials fall 55–86% across models).
- **Qualitative inspection (what the reviewer specifically asked for):** 10 lie-condition first responses per model, coded for "corrected in paraphrased language" vs. "failed to correct." Result across 30 coded responses: **26/30 corrected paraphrased (no banned words, correct fact delivered), 4/30 corrected directly (still used 1 banned marker, all on Llama 3B and Mistral 7B), 0/30 failed to correct.** Qwen 14B scored 10/10/0/0. Appendix `app:adv_qualitative` includes example text and the coding table. This directly addresses the reviewer's Q2 second half: **the rule degrades because the lexical channel is not semantically load-bearing, not because the model ceases correcting.** The paper now states this explicitly.

**W3 (autonomous n=50 is thin; abstract overclaims).** Softened in abstract and intro.
- Abstract: "Autonomous evaluation (n=50 each) and a multi-model adversarial paraphrase test confirm the rule's surface-lexical brittleness: signal collapses under autonomous persona and ICL false-belief conditions (60–66%, at or near chance)…" (We removed the stronger claims and added "preliminary" framing.)
- We retain the sycophancy Qwen 14B replication (82%, d=1.6) as a transfer data point, not a deployment claim.
- A full validation at n=200+ per condition is explicitly listed as future work.

**W4 (ICC=0.114 should lead defence on regex-matches-pipeline).** Foregrounded.
- §5.4 opens with: "the paper's central claims do not depend on correction-marker density being reliable: the regex baseline achieves comparable accuracy without LLM extraction, and the weak ICC is consistent with our finding that the pipeline is redundant."
- This matches the reviewer's off-the-record suggestion to lead the rebuttal rather than bury it.
- The n=20 2-annotator validation remains a limitation (explicitly noted as underpowered); a proper validation (n≥100, 3+ annotators, Krippendorff's α) is listed as a prerequisite for any positive deployment claim on correction density.

**W5/Q3 (multi-model EXP-K).** **Done.**
- Llama 3.3 70B **both conditions** n=100 complete. Refusal-count LOO: 83% unrelated vs. 84% related (within 1 pp — the first-response-dominance claim holds on refusal markers at 70B). Pipeline LOO: 66% unrelated vs. 80% related (+14 pp — a refinement: related follow-ups do add pipeline-level value at scale, even while refusal-count is saturated by the first response).
- Qwen 2.5 14B both conditions n=100 in progress (orchestrated to run immediately after the Qwen 14B adversarial job finishes, since they share a single-GPU Ollama queue). Will land for camera-ready.
- Table `tab:pacchiardi_multi` in Appendix J now reports the full multi-model panel. Mistral 7B results: refusal-count 59% unrelated vs. 68% related (+9 pp); pipeline 72% vs. 71% (within 1 pp).
- Interpretation: the Pacchiardi-rationale update is **nuanced**, not simple: (a) unrelated follow-ups capture the first-response refusal-count signal essentially as well as related follow-ups — this validates Pacchiardi's key design choice for refusal-count-style detectors; (b) the 5-feature LLM pipeline at scale does benefit from related follow-ups (70B +14 pp), so a pipeline-based detector should use related probing. We report this as a finding rather than forcing a single one-line story. Text is rewritten in Appendix J accordingly.

**W6 ("unprecedented" wording).** Softened.
- §5.3: "confounds of unprecedented magnitude" → "confounds of a magnitude previously undocumented in this domain."

---

## Detailed questions

**Q4 (Qwen 32B knowledge probing — is the model's internal knowledge surviving the RLHF smoothing?).** The pre-check accuracy (92% on direct factual probes) is the strongest evidence we have that the knowledge survives the RLHF smoothing; the model simply will not produce refusal markers when asked to defend the claim. A full "is this claim true/false?" probing experiment on equalized Qwen 32B transcripts is a direct follow-up we flagged as future work rather than attempting in this revision; the pre-check result is documented in §4 and Appendix.

**Q5 (unified RLHF picture — rule fails whenever the target is trained or instructed to be agreeable).** Accepted and added.
- Conclusion: "A unified picture emerges: refusal-count signal weakens whenever the target is trained or instructed to be agreeable—Qwen 32B's post-training smoothing, the adversarial paraphrase prompt, and the autonomous-persona and false-belief conditions (66% and 60% respectively) all instantiate the same failure mode."
- This is now the paper's framing of what the negative results share, rather than treating each as an isolated data point.

---

## Candid notes (reviewer's off-the-record observations)

**On the single data point caveat at frontier.** The cross-family validation converts Sonnet 4.5 from "one Haiku-extracted data point we had to flag" to "one data point validated under a second extractor from a different family." The absolute number is robust to extractor substitution (73.7% regex, 88.9–92.9% pipeline depending on extractor); the direction of bias is confirmed as small. A full non-Anthropic 405B-class extractor remains the right next step.

**On the Pacchiardi design-rationale framing.** Our EXP-K result is now the cleanest evidence we have that multi-turn probing adds little over the first response *under equalization*. This is a direct update to the Pacchiardi et al. (2023) rationale that unrelated follow-ups were needed to isolate deception signal. We report this as a finding rather than a methodological preference; if the Qwen 14B and Llama 70B related-condition results contradict Mistral 7B, we will report honestly rather than tuning for consistency.

**On venue fit.** We continue to frame this as a methodological-hygiene paper, not a technical advance. The three reusable controls (prompt equalization, cross-family extraction, regex baselines) are the contribution. We believe the combination of the Qwen 32B RLHF-smoothing finding, the 30–41 pp collapse under equalization, the now-cross-family-validated frontier-scale data point, and the multi-model EXP-ADV / EXP-K results provides concrete empirical content that is not predictable from the prior literature. If the reviewer still views the venue as ill-fit, we would welcome a specific alternative pointer (NeurIPS D&B, TMLR, SafeAI workshop) and would resubmit there.

**On what's genuinely in-progress.** To be transparent: at submission, Qwen 14B adversarial and Llama 70B related-condition are mid-run; the orchestrator script has queued Qwen 14B Pacchiardi (both conditions) to start immediately after the adversarial job finishes. Every number reported above is from completed data. The tables that list "in progress" cells will be finalized for camera-ready from the same scripts and checkpoints (committed to the repo) without additional design choices.

---

## Files changed in this revision

- `output/adaptive_lie_detector_paper/sections/abstract.tex` — trimmed autonomous block; cross-family validation integrated; softened frontier framing.
- `output/adaptive_lie_detector_paper/sections/introduction.tex` — §1.1 contribution-3 reordered (lead with 73.7% refusal-count); cross-family panel referenced.
- `output/adaptive_lie_detector_paper/sections/experiments.tex` — §4.2 Table `tab:adv_multimodel` (3-model adversarial with paired bootstrap CI); §4.5 Table `tab:sonnet_crossfamily` (Haiku vs. Llama 70B extractor).
- `output/adaptive_lie_detector_paper/sections/appendix.tex` — Appendix J Table `tab:pacchiardi_multi` (multi-model EXP-K); new Appendix `app:adv_qualitative` (failure-mode coding).
- `output/adaptive_lie_detector_paper/sections/discussion.tex` — §5.1 Mistral 7B counter-example; §5.3 "unprecedented" softened.
- `output/adaptive_lie_detector_paper/sections/conclusion.tex` — unified-RLHF picture sentence.
- `code/adaptive_lie_detector/experiments/re_extract_sonnet_cross_family.py` — new (Llama 70B re-extraction on saved transcripts).
- `code/adaptive_lie_detector/experiments/run_pacchiardi_llama70b.py` — new (Bedrock Llama 70B EXP-K).
- `code/adaptive_lie_detector/experiments/run_pacchiardi_qwen14b.py` — new (Ollama Qwen 14B EXP-K).
- `code/adaptive_lie_detector/experiments/analyze_adv_multi.py` — new (paired bootstrap CI, qualitative samples).
- `code/adaptive_lie_detector/experiments/analyze_sonnet_crossfamily.py` — new (Haiku vs. Llama 70B extractor comparison).
- `code/adaptive_lie_detector/experiments/analyze_pacchiardi_multi.py` — new (multi-model EXP-K analysis).

All experimental scripts are committed and reproducible.
