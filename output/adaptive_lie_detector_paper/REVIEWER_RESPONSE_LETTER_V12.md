# Response to Reviewer (Round 3: 6/10 weak-accept, promising 7/10 accept conditional)

We thank the reviewer for moving us from 5/10 to 6/10 with a substantive, detailed review. This revision addresses all four items the reviewer named as conditional 7/10 upgrades, plus the Q4 clarification. None required new target inference or new human-subjects work; three were text fixes and one was a short cross-family re-extraction (~7 min of Bedrock calls on already-saved transcripts).

---

## Summary of round-3 changes

1. **Qwen 2.5 32B added to the cross-family panel** (Q2, W7). Table 9 is now an 8-target panel. New 8-target cross-family average: **64.2%** (was 64.7% on 7 targets); new 8-target Haiku average: **74.5%** (was 74.3%); new gap: **+10.3 pp** (was +9.7 pp). The Qwen 32B row shows the RLHF-collapse story directly in the panel: refusal-count LOO 50.0% (chance by construction — zero refusal markers in both conditions), Mistral-Large pipeline 60.6%, Haiku pipeline 75.8%. Footnote `$^\ddagger$` explains the collapse mechanism. Both headlines (8-target primary, 7-target parenthetical) are propagated to abstract and §1.1.

2. **Table 2 vs Table 9 caption clarification** (Q1, W7). The numerical discrepancy the reviewer flagged is real but **not an error**: Table 2 uses pooled-LOO over the combined 7-model 689-trial dataset (single shared threshold optimization, matching a shared-deployment regime); Table 9 uses per-target LOO (threshold optimized per target). Both table captions now state this explicitly and cross-reference each other so readers see immediately why the numbers differ. Reviewer's hypothesis was in the right direction (different threshold regimes) but the actual difference is pooled-vs-per-target LOO, not fixed-k vs LOO-optimized.

3. **§5.4 framing aligned with §4.7** (W6). The stale rev-10 sentence "The 9–16 pp gap ... primarily reflects extractor capability differences rather than same-family bias" has been replaced with §4.7's correctly agnostic framing: "Whether the 9–16 pp gap ... reflects RLHF self-preference or capability asymmetry ... remains open. The gap is directionally positive on all seven targets ... consistent with either hypothesis; disambiguating would require a non-Claude extractor of comparable capability, which we list as future work."

4. **§5.2 "signal floor" softened to "preliminary evidence"** (W4, W9). The reviewer flagged "genuine signal floor" as the strongest claim in the paper resting on the thinnest evidence. We agree — on reflection the claim rests on two probes at one layer, one pooling strategy, with a base/Instruct checkpoint mismatch on one of them. §5.2 and §4.8 both now say "preliminary evidence consistent with representation-level difficulty at the tested configurations" and explicitly list "multiple probing architectures (intermediate layers, mean-pooled representations, non-linear probes) and frontier-scale open-weight targets" as what a conclusive comparison would require.

5. **Sonnet bootstrap CI procedure documented in §4.5** (Q4). Added one sentence explaining that pairing is by trial index on the identical 99 saved transcripts — both extractors score the same conversations, so the CI reflects between-extractor variance on fixed transcripts and does not include within-extractor re-prompting noise. The numerical result ([−3.0, +11.1], includes zero) is unchanged.

---

## Mapping W/Q items

### Blocking 7/10 conditions

**W7/Q1 (Table 2 vs Table 9 clarification).** **Done.** Both captions now state the threshold regime:
- Table 2 caption: "Refusal-count and hedging columns use LOO cross-validation on the pooled 7-model dataset (689 trials; a single shared threshold is optimized across targets), matching a shared-deployment regime; for a per-target-calibrated comparison against cross-family extraction, see Table 9."
- Table 9 caption: "Refusal-count column uses per-target LOO (threshold optimized independently per target), so values differ from Table 2 (pooled-LOO on 689 trials): the two tables correspond to different deployment regimes (per-target calibration here vs. shared threshold there), not different data."

**W7/Q2 (Qwen 32B in cross-family panel).** **Done.** We ran Mistral Large re-extraction on the 99 saved Qwen 32B equalized transcripts and added the row. The row:

| Target | n | Refusal-count LOO | Haiku pipeline | Mistral-Large pipeline | Gap |
|---|---:|---:|---:|---:|---:|
| Qwen 2.5 32B`$^\ddagger$` | 99 | 50.0% | 75.8% | 60.6% | +15.2 |

`$^\ddagger$` footnote: "Qwen 2.5 32B produces zero refusal markers in both conditions under RLHF agreeableness smoothing (§4 Qwen scale sweep); the rule collapses to chance by construction; included for transparency."

**Updated averages:** 8-target mean cross-family 64.2%, Haiku 74.5%, gap +10.3 pp. 7-target subset (excluding 32B) in italics below the primary average for readers tracking round-2 continuity.

Addition changes the paper's headlines as follows:
- Abstract: "5-feature pipeline average drops from 74.5% to **64.2% (8-target panel; gap +10.3 pp)**, with the 7-target subset excluding the Qwen 2.5 32B RLHF-collapse row at 64.7%."
- §1.1 contribution-1: same change, with the 7-target number as parenthetical continuity.
- §4.7 headline paragraph: "If a single conservative headline is required, it is the 8-target cross-family pipeline at 64.2%."

**W6 (§5.4 vs §4.7 inconsistency).** **Done.** §5.4 line 27 replaced; §5.4 now says "remains open," aligned with §4.7.

**W4 (§5.2 signal-floor overreach).** **Done.** §5.2 `sec:blackbox_vs_whitebox` softened throughout. §4.8 `sec:whitebox_probing` (the original source of the "signal floor" language) also softened in the same direction. The data point (63–65% band within ±2 pp of the rule, on 2 targets) is unchanged; the interpretive label is now "preliminary evidence consistent with" rather than "signal floor."

### Follow-up questions (Q1–Q5)

**Q1** — resolved by Table caption edits (see W7 above).

**Q2** — resolved by Qwen 32B addition (see W7 above).

**Q3** (Mistral 7B Instruct probe). **Not attempted; honest acknowledgment.** We considered running an informal Instruct probe but did not because (a) the Mistral 7B Instruct checkpoint is not locally cached and a full download would have exceeded the revision window, (b) we did not want to report a number we did not measure. Our predicted direction, based on SAPLMA-style literature: Instruct checkpoints typically score comparably or within ~5 pp of base checkpoints on last-layer LR probes at the same scale. We do not expect the Instruct probe to exceed the base probe by more than a few percentage points (certainly not to 90%), but we state this as a prediction rather than a measurement. The §4.8 footnote explicitly frames 65% as a lower bound for the Instruct variant; we do not claim an upper bound.

**Q4** (Sonnet bootstrap detail). **Clarified in §4.5.** Pairing is by trial index on the identical 99 saved transcripts — both extractors score the same conversations, so the CI reflects between-extractor variance on fixed transcripts and does not include within-extractor re-prompting noise. The target conversation itself was generated once via Sonnet inference and then frozen; the only stochasticity the bootstrap captures is over the sampled-with-replacement subset of trial indices. Numerical result unchanged: 95% CI [−3.0, +11.1], includes zero.

**Q5** (unified "agreeable target → no signal" hypothesis). **Accepted as future-work framing; not formalized in this revision.** We agree with the reviewer that this is the most interesting synthesis of the paper's findings (Qwen 32B RLHF smoothing + adversarial paraphrase + persona + false-belief conditions all sharing the same failure mode). A formal test — e.g., training a cross-target "agreeableness" classifier on a separate dataset and regressing per-target rule accuracy on its predictions — is the right next paper, not this paper. We have added a sentence to future work crediting the reviewer's synthesis.

---

## Carried-over items (no changes needed this round; reviewer accepted in round 2)

The reviewer explicitly accepted, from round 2:
- **W1** / **W2** — 7-target cross-family panel and white-box probing baseline were both called "genuinely informative."
- **W3** — frontier bootstrap CI properly demoted to "non-significant rather than evidence of measurable bias."
- **W5** — autonomy-first framing accepted as the right headline.
- **W8** — abstract trim to 367 words (now ~373 after the 8-target addition; still under 400).
- **W9** — white-box probe accepted as a real data point, with the Mistral base/Instruct caveat acknowledged.

---

## Candid notes

**On the narrowness of the probing baseline**: we agree with the reviewer. Two probes, one layer, one pooling strategy, one checkpoint mismatch — this is genuinely narrow, and we have softened the §5.2 language accordingly. The Qwen 14B probe is a known gap (shard download did not complete); we report this honestly in §4.8 and do not claim Qwen 14B probing. The right extension is a future-work grant: multiple probing architectures × multiple pooling strategies × Qwen 14B and larger open-weight targets where hidden states are accessible.

**On the Q3 Instruct-checkpoint gap**: this is a real limitation we did not close. Our best honest answer is "expected direction is probe↑ by a few pp, not to 90%." If the reviewer wants a measured number, we can commit to completing this for the camera-ready version given one additional cycle.

**On Q5 as a research direction**: the "agreeable target → no signal" synthesis is, on reflection, the cleanest way to describe what links Qwen 32B, adversarial paraphrase, persona, and false-belief failures. The conclusion section already uses this unified-picture framing; a formalized cross-target agreeableness predictor is a natural follow-up paper.

---

## Files changed in this revision

**New data**:
- `code/adaptive_lie_detector/data/results/cross_family_equalized_qwen32b_mistral_large.json` — Mistral Large re-extraction on 99 Qwen 32B equalized transcripts (n=99).

**Modified analysis**:
- `code/adaptive_lie_detector/experiments/analyze_equalized_crossfamily_panel.py` — appended Qwen 32B TARGETS tuple; re-ran to regenerate `output/adaptive_lie_detector_paper/crossfamily_panel.json` with 8 rows.

**Paper edits**:
- `sections/abstract.tex` — 8-target cross-family headline; now ~373 words.
- `sections/introduction.tex` — §1.1 contribution-1 updated with 8-target cross-family average and 7-target continuity parenthetical.
- `sections/experiments.tex` — Table 2 caption: pooled-LOO clarification. Table 9: Qwen 32B row + `$^\ddagger$` footnote + updated caption + updated averages + updated §4.7 headline paragraph. §4.8 `sec:whitebox_probing`: "signal floor" softened to "preliminary evidence consistent with." §4.5 Sonnet paragraph: bootstrap pairing clarified.
- `sections/discussion.tex` — §5.4 line 27 framing aligned with §4.7. §5.2 `sec:blackbox_vs_whitebox` softened to "preliminary evidence."

All experimental scripts are committed; the Qwen 32B re-extraction is reproducible from the saved conversations in `ollama_eval_qwen2_5_32b_prompt_equalized_latest.json`.

---

## Trajectory summary

- **Round 1 (weak reject, pre-revision)**: regex-matches-pipeline framing was the headline; single-extractor numbers; no white-box comparison.
- **Round 2 (5/10 borderline → 6/10 weak-accept)**: 7-target cross-family panel; 2-target white-box probe; autonomy-first framing; Sonnet bootstrap CI includes zero; ICC promoted to §5.1.
- **Round 3 (this revision; 6/10 → 7/10 conditional)**: Qwen 32B added (8-target panel); Table 2/9 caption clarity; §5.4↔§4.7 alignment; §5.2 "signal floor" softened; Q4 bootstrap procedure documented. No new framing drift; consistent with the reviewer-suggested conclusions the paper already defends.

We believe this revision addresses every conditional 7/10-upgrade item the reviewer named and fully clarifies the Q4 follow-up. Q3 remains the one acknowledged gap; we have stated our predicted direction and committed to measuring it in camera-ready if requested.
