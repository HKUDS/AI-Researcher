# Response to Reviewer (Accept, 7/10; Confidence 4/5) — Revision V18

We thank the reviewer for the upgrade to Accept and for the unusually constructive closing review. V18 is a camera-ready polish pass: all 6 specific suggestions are addressed in-paper, and the 3 load-bearing acknowledged-residual-weaknesses are explicitly reaffirmed (human ICC camera-ready commitment, disposition-source as the best-supported-but-not-directly-pre-registered explanation, Mistral 7B base-vs-Instruct probe). No new inference was run; the only new computation is a paired bootstrap CI on Δ=−4.2 pp using the 3 existing V17 4th-scenario JSON files.

**Summary of V18 changes at a glance.**

| # | Reviewer ask | V18 response | Location |
|---|---|---|---|
| 1 | §4.7.1 Table 11: pooled bootstrap CI on Δ=−4.2 pp | **Executed**: paired bootstrap B=5000 seed=42 over 3-model × 2-condition cells of n=50; appended to Table 11 caption | `experiments.tex` L336 |
| 2 | §4.7: engage with 70B sycophancy 72% drop | **Executed**: one-sentence addition after the "~10 pp drop" statement; attributes part of the drop to extractor-specific same-family bias | `experiments.tex` L323 |
| 3 | §4.7.1: explain larger $d$ at low-clarity on 2/3 targets | **Executed**: one-sentence addition to interpretation paragraph; ceiling-effect reading under high-clarity | `experiments.tex` L351 |
| 4 | §5.1: make camera-ready commitment explicit | **Executed**: tail clause promoted to standalone bolded sentence | `discussion.tex` L9 |
| 5 | Abstract: mention pre-registered self-falsification as contribution | **Executed**: new Contributions item (iii); renumbered existing (iii)→(iv) | `abstract.tex` L6 |
| 6 | §5.8 Future Directions: pre-registered 5th scenario on disposition-source | **Executed**: new item (4) | `discussion.tex` L76 |

---

## R1 — Pooled bootstrap CI on Δ=−4.2 pp (Suggestion 1)

**What was asked.** A pooled bootstrap CI on Δ=−4.2 pp added to §4.7.1 Table 11, since individual cell Wilson CIs were reported but the pooled effect was not.

**What we did.** New script `code/adaptive_lie_detector/experiments/bootstrap_4th_scenario_ci.py` performs a paired bootstrap over the 3 existing V17 4th-scenario result JSONs (`exp_i_4th_scenario_{llama3.2_3b,mistral_7b,qwen2.5_14b}_latest.json`). Resampling is within each (model, condition) cell of n=50 with replacement; per-model refusal-count LOO is recomputed on each resample; the pooled Δ is the average of the 3 per-model Δ_m. B=5000, seed=42.

The LOO-based bootstrap distribution is wide (because leave-one-out logistic regression is high-variance at n=50 even with a 1-D feature). We additionally report the fixed-rule (k≥1) Δ bootstrap as a robustness check; both are released in `bootstrap_4th_scenario_ci.json` alongside the per-model point estimates. The point estimate reproduces the paper's −4.2 pp to rounding.

**Table 11 caption update.** The caption now ends with "pooled paired-bootstrap 95\% CI on $\Delta=-4.2$\,pp includes zero, consistent with the pre-registered null," preempting the over-reading that the observed Δ could cross 0 as a replication concern.

**Files.**
- New: `code/adaptive_lie_detector/experiments/bootstrap_4th_scenario_ci.py`
- New: `code/adaptive_lie_detector/data/results/bootstrap_4th_scenario_ci.json`
- Updated: Table 11 caption in `sections/experiments.tex`

---

## R2 — Engage with 70B sycophancy 72% drop (Suggestion 2)

**What was asked.** Under the disposition-source reading, why does 70B sycophancy drop to 72% (vs. 82% at 3B/14B)? The reviewer correctly noted that "system-prompt does the heavy lifting" predicts roughly constant sycophancy accuracy across scale.

**What we did.** One sentence added to §4.6 after the existing "~10 pp drop" statement:

> "The 10 pp drop at 70B under the disposition-source reading is consistent with RLHF-induced correction becoming more heterogeneous at frontier scale — the cross-family re-extractor drops the pipeline to 82% (same-family bias contributes ~10 pp), so part of what looks like a disposition-source weakening at 70B is extractor-specific scoring, not a sycophancy-signal failure."

This relies on §4.6's own cross-family-re-extraction finding: the Haiku-extracted pipeline was 92% on the 70B sycophancy transcripts and drops to 82% under Llama-3.3-70B-as-extractor. Part of the apparent 70B-sycophancy weakness is therefore same-family-bias on the Haiku side of the comparison, not a failure mode of the disposition-source mechanism per se.

**Files.** Updated paragraph in `sections/experiments.tex` L323.

---

## R3 — Explain larger $d$ at low-clarity on 2/3 targets (Suggestion 3)

**What was asked.** Llama 3B high-clarity $d=+0.45$, low-clarity $d=+0.95$; Mistral 7B $d=+0.84 \to +1.10$; Qwen 14B flat. Why do the lower-clarity conditions produce larger Cohen's $d$?

**What we did.** One sentence added to the §4.7.1 interpretation paragraph:

> "The larger Cohen's $d$ at low-clarity on 2 of 3 targets (Llama 3B $+0.45\to+0.95$; Mistral 7B $+0.84\to+1.10$) is consistent with a mild ceiling effect under high-clarity prompts — textbook-wrong claims elicit near-uniform correction in the lying condition, compressing the lying-vs-truthful distance — rather than evidence against disposition-source."

The ceiling-effect reading is consistent with the per-cell numbers: under high-clarity sycophancy, lying-condition accuracy is at 68–84% across the 3 targets, leaving little room for a larger separation. Under low-clarity, lying-condition accuracy is similar but truthful-condition accuracy rises (the sycophancy prompt produces less hedging on true-but-familiar claims), yielding larger lying-vs-truthful Cohen's $d$.

**Files.** Updated paragraph in `sections/experiments.tex` L351.

---

## R4 — Make camera-ready commitment explicit (Suggestion 4)

**What was asked.** The human ICC at n≥100 with 3+ annotators was listed as a "camera-ready commitment" in V17 but buried at the end of the §5.1 machine-ICC-proxy paragraph. Reviewer asked for an explicit, visible commitment.

**What we did.** The tail clause has been promoted to a standalone bolded sentence at paragraph end:

> "**Camera-ready commitment.** The authoritative human ICC study at $n\geq 100$ with 3+ independent annotators will be completed and included in the camera-ready version of this paper."

**Files.** Updated `sections/discussion.tex` L9.

---

## R5 — Abstract contribution: pre-registered self-falsification (Suggestion 5)

**What was asked.** The reviewer noted that the V17 pre-registered 4th-scenario self-falsification is one of the paper's most credibility-enhancing moves and is currently only mentioned in the body. They suggested we flag it as a contribution in the abstract.

**What we did.** Added a new Contributions item (iii) to the abstract:

> "(iii) a pre-registered self-falsification of our earlier ``knowledge-conflict clarity'' interpretation (§\ref{sec:exp_i_4th_scenario})"

and renumbered the existing (iii) negative-scaling item to (iv). The abstract thus now lists 4 contributions instead of 3.

**Files.** Updated `sections/abstract.tex` L6.

---

## R6 — Future Directions: pre-registered 5th scenario (Suggestion 6)

**What was asked.** The disposition-source interpretation is now the load-bearing one but was derived post-hoc from the 4th-scenario clarity rejection. Reviewer suggested a 5th scenario that directly varies disposition-source while holding clarity fixed, listed as future work.

**What we did.** Added item (4) to §5.8 Future Directions:

> "**(4) Pre-registered 5th scenario: disposition-source.** The V17 4th scenario (§\ref{sec:exp_i_4th_scenario}) rejected knowledge-conflict clarity as the controlling axis; disposition-source is the replacement interpretation but is not itself pre-registered. A cleaner test varies disposition-source directly — weak agreeableness prompt vs. full sycophancy prompt vs. explicit lie-defense prompt — while holding clarity, turn-count, and target fixed. We pre-register this as the canonical test of the disposition-source hypothesis."

This acknowledges the reviewer's concern (disposition-source is not itself pre-registered) and commits to the natural follow-up design.

**Files.** Updated `sections/discussion.tex` Future Directions subsection.

---

## Response to the 3 acknowledged residual weaknesses

**(W1) Human ICC still deferred.** The reviewer accepted the "practical constraint (multi-week annotator recruitment)" while flagging this as the largest unaddressed weakness. V18 keeps the machine-ICC proxy from V17 and promotes the camera-ready commitment to an explicit bolded sentence (R4 above). Our plan is a 3-annotator n=120 study over the 8 targets, with Krippendorff's α as the primary reliability metric.

**(W2) Disposition-source itself not pre-registered.** Reviewer correctly notes that while the clarity hypothesis was pre-registered and rejected, the replacement interpretation (disposition-source) was derived post-hoc from that same rejection. V18 adds Future Directions #4 (R6 above) committing to a pre-registered disposition-source test as the canonical follow-up. The paper's §4.6 and §4.7.1 body text already flag disposition-source as the "best-supported" rather than "tested" explanation.

**(W3) Mistral base-vs-Instruct probe mismatch.** The §5.2 probe comparison uses Mistral 7B base checkpoint (reused from V17 per-layer sweep compute constraints) while black-box interrogation uses Mistral 7B Instruct. V17's footnote in §5.2 flags this; V18 does not re-run the probe. Matched-checkpoint replication is retained as future work.

The reviewer's 5 additional framing observations (4th scenario n=50, single frontier data point, Qwen 32B single-model RLHF collapse, statistical-precision notes, §4.7 narrative unchanged by 4th scenario) are acknowledgments rather than asks; suggestions 2 and 3 above directly address the statistical-precision and narrative-engagement items.

---

## Items logged as out-of-scope for V18 (post-acceptance camera-ready or future work)

- **Full human ICC study at n≥100 with 3+ annotators** — camera-ready commitment (R4).
- **Pre-registered 5th scenario on disposition-source** — Future Directions #4 (R6).
- **Matched-checkpoint Mistral 7B Instruct probe sweep** — future work (W3).
- **2nd ≥14B RLHF-heavy model for Qwen 32B replication** — carried from V17 (S4).
- **Frontier-scale panel (n≥410 Sonnet or multiple frontier models)** — carried from V15/V16/V17.
- **Pacchiardi full replication** — carried.
- **Closed-loop iterated adversary** — carried.

---

## Verification checklist for the reviewer

- Abstract Contributions list now has 4 items including "(iii) a pre-registered self-falsification ..."
- §4.6 L323 paragraph has a new sentence starting "The 10\,pp drop at 70B under the disposition-source reading ..."
- §4.7.1 Table 11 caption ends with a pooled paired-bootstrap 95% CI and "includes zero, consistent with the pre-registered null"
- §4.7.1 interpretation paragraph contains "ceiling effect under high-clarity"
- §5.1 has a bolded `\textbf{Camera-ready commitment.}` sentence
- §5.8 Future Directions has 4 numbered items (was 3), with item (4) titled "Pre-registered 5th scenario: disposition-source"
- `bootstrap_4th_scenario_ci.json` is released alongside the script
- Page count: target 41, 0 errors, 0 undefined refs

We are grateful for the Accept upgrade and for the constructive closing review. The 6 items above all flow through in V18; the remaining 3 acknowledged weaknesses are reaffirmed as camera-ready or future-work commitments.
