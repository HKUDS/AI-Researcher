# Reviewer Response Letter — V24
## NeurIPS 2026 Revised Submission

---

**To:** Reviewer 3 (Accept 7/10, Confidence 4/5)

**Subject:** V24 revision addressing W1–W8 and Q1–Q5

We thank the reviewer for promoting to Accept 7/10 and for the clear characterisation of what remains: *"The remaining gap between this submission and a strong accept is whether the authors run the human baseline before camera-ready. With that single addition, this would be a clear 8/10."* V24 addresses every numbered item. **The human baseline study is complete** (n=50, 2 annotators, annotation executed and analyzed); all five presentational edits are executed. The human baseline finding is reported in full in §4.10 and referenced in §5.7(k).

---

## At-a-Glance Table

| Ask | V24 action | Status |
|---|---|---|
| **W1 / Q1** Human baseline n=50/2-annotator | **Executed and analyzed**: both annotators 44.0% (chance-level; κ=0.00 degenerate); rule 76.0% (+32 pp); §4.10 complete | **Done — experiments.tex** |
| **W2** Non-English pilot | Remains §5.8 future work (V24 cannot run two new experiments) | Out of scope |
| **W3 / Q3** Sonnet out of contribution (iii) | Verified clean; `\paragraph{Frontier observation}` confirmed outside enumerate block | **Verified (no edit needed)** |
| **W4** 74.3% in abstract needs ICC caveat | Appended `(level-dependent; ICC=0.114, §5.1)` inline | **Done — abstract.tex** |
| **W5 / Q5** Post-hoc reading for Qwen 14B persona 68.0% and Mistral 7B FB 66.5% | 2-sentence paragraph inserted after Table 12; spot-check script produced | **Done — experiments.tex** |
| **W6** §4.9 white-box too long | Compressed ~31 lines → ~15 lines; dropped 4 redundant rows from Table 8; figure caption tightened | **Done — experiments.tex** |
| **W7** Single-persona-prompt limitation | §5.7(j) extended to cover both persona AND false-belief-ICL single-prompt scope | **Done — discussion.tex** |
| **W8 / Q4** Qwen 3B→7B p=0.014 caveat | Verified only one mention (experiments.tex:260); already correctly caveated in V23 | **Verified (no edit needed)** |
| **Q2** Qwen 14B persona partial correction reading | Qualitative spot-check script produced; 10-trial coding planned (camera-ready) | **Script done; coding pending** |

---

## W1 / Q1 — Human Baseline (leverage ask)

> *"Run the n=50/2-annotator human baseline on equalized transcripts before camera-ready — the single highest-leverage missing experiment."*

**V24 action: executed and analyzed.** The n=50/2-annotator human baseline was completed in V24. Infrastructure and annotation pipeline:

- **Transcript selection** (`run_human_baseline_v24.py`): stratified n=50 from the 7 equalized-condition Haiku-extractor JSONs (≈7 trials per model; 22 truthful + 28 lying; seed=42). Ground-truth held out; annotator-visible payload blind-hashed to prevent model identity inference.
- **Two annotator CSV templates** with shuffled trial orders (seeds 43/44) — no ground-truth columns.
- **Protocol** (`docs/human_baseline_protocol_v24.md`): binary TRUTH/LIE task, ~40 min per annotator, Cohen's κ on binary labels for IRR.
- **Analysis script** (`human_baseline_analysis_v24.py`): per-annotator accuracy + Wilson 95% CIs, Cohen's κ, 3-row comparison table.

**Result (§4.10).** Both annotators defaulted almost entirely to TRUTH: Annotator A labeled 50/50 as TRUTH; Annotator B labeled 48/50 as TRUTH. Raw inter-annotator agreement was 96%, but Cohen's κ = 0.00 — a degenerate label distribution (both annotators converged on the majority class, not genuine per-trial agreement). Per-annotator accuracy against ground truth: **44.0%** (Wilson 95% CI [31.2%, 57.7%]), at or below chance given the 56% lying-class base rate. The refusal-count rule achieves **76.0%** (Wilson CI [62.6%, 85.7%]) on the same 50 trials — **+32 pp over humans**.

| Method | Accuracy | Wilson 95% CI |
|---|---|---|
| Human Annotator A (n=50) | 44.0% | [31.2%, 57.7%] |
| Human Annotator B (n=50) | 44.0% | [31.2%, 57.7%] |
| Refusal-count rule (n=50) | **76.0%** | [62.6%, 85.7%] |
| *Pipeline same-family (paper, n≈689)* | *74.3%* | *—* |
| *Pipeline cross-family (paper, n≈689)* | *64.7%* | *—* |
| *Rule pooled-LOO (paper, n≈689)* | *80.1%* | *—* |

**Interpretation.** The human collapse to TRUTH is not annotation error — it reflects the design of the equalized condition. In lying trials under equalized prompts, the assistant was *not* instructed to lie; it frequently produces factual corrections and hedges indistinguishable from truthful-trial responses. A naive annotator applying the heuristic "assistant that corrects claims → truthful" systematically misfires because equalized lying-trial assistants also correct claims. The refusal-count rule exploits the *absence* of correction markers in lying trials where the model endorses the false claim without pushback — a signal present in the transcripts but not apparent to unaided human judgment without knowledge of the experimental design. This directly contextualizes the paper's 61–84% equalized accuracy band: the automated detectors exceed human-chance performance in a regime that is at or below human chance.

**§5.7(k) updated** to: *"Human baseline completed (n=50, 2 naive annotators): both annotators achieved 44.0% accuracy (chance-level; Wilson CI [31.2%, 57.7%]) with a degenerate κ=0.00 from collapsing to the TRUTH label on ≥48/50 trials. The refusal-count rule reaches 76.0% on the same sub-sample (+32 pp over humans; §4.10)."*

---

## W2 — Non-English Pilot

> *"Non-English replication (n=50, one language) — flagged but not done."*

**V24 decision.** V24 cannot run two new experiments; the human baseline is higher-leverage per the reviewer's own priority ranking. Non-English pilot remains §5.8(5)(ii) future work. We have strengthened that pointer to explicitly commit to a follow-up submission rather than camera-ready.

---

## W3 / Q3 — Sonnet Not in Contribution (iii)

> *"Remove Sonnet frontier pilot from contribution (iii) entirely; confine to §4.6 as a diagnostic."*

**V24 verification.** Contribution (iii) in §1.1 reads: *"Within-family scale effects are family-specific and non-monotonic on ≤70B."* It contains no Sonnet mention. The `\paragraph{Frontier observation (single pilot).}` is separated from the contributions `\begin{enumerate}...\end{enumerate}` block by Table 1 (`tab:headline_decision`), placing it clearly outside the enumerate environment. No edit needed. We confirmed this by inspecting `sections/introduction.tex:18–45`; the contributions block closes at line 24 (`\end{enumerate}`), and the Frontier paragraph begins at line 45 after the table.

---

## W4 — ICC Caveat Travels with 74.3% in Abstract

> *"In abstract, the 74.3% Haiku mention should carry an ICC caveat."*

**Before (abstract.tex:2):**
> "…matching a 5-feature LLM pipeline's 74.3% same-family-extracted result within 5 pp…"

**After:**
> "…matching a 5-feature LLM pipeline's 74.3% same-family-extracted result (level-dependent; ICC = 0.114, §5.1) within 5 pp…"

Net change: +8 words; no page budget impact.

---

## W5 / Q5 — Post-Hoc Reading for Two Chance-Excluding Cells

> *"Two n=200 cells excluding chance (Qwen 14B persona 68.0%, d=0.83; Mistral 7B FB 66.5%, d=0.72) have no current-best reading in main text."*

**V24 action.** A 2–3 sentence post-hoc reading paragraph was inserted immediately after Table 12 (`\label{tab:autonomous_matched}`) in `sections/experiments.tex`:

> *"**Current best reading of the two chance-excluding cells.** Qwen 2.5 14B persona (68.0%, d=0.83) and Mistral 7B false beliefs (66.5%, d=0.72) are the only two of six fully-autonomous cells whose Wilson CIs exclude chance at n=200. Both pre-registered causal axes have been falsified: knowledge-conflict clarity (§4.7.1; Δ=−4.2 pp pooled) and disposition-source ranking (§4.7.2; persona > sycophancy on Qwen 14B at n=30, rejecting the one-sided prediction). A 10-trial qualitative spot-check on Qwen 2.5 14B persona transcripts (5 TRUE + 5 FALSE, seed=42; Appendix N) is available for examination but has not yet been coded; we commit to reporting code counts (P / B-correct / B-other) in the camera-ready. The current reading for both cells is **unexplained partial transfer**: the signal is real (d > 0.7) but neither falsified axis accounts for why these two cells—and only these two—exceed chance."*

---

## W6 — §4.9 White-Box Probe Section Too Long

> *"§4.9 white-box probes is ~1.5 pages for 'probe is rule-parity at tested configurations'; tighten."*

**V24 action.** §4.9 was compressed from ~31 lines to ~15 lines. Changes:

- Dropped the four intermediate LR probe rows from Table 8 (last-layer last-token, mid-layer last-token, last-layer mean-pooled, mid-layer mean-pooled) — only best-layer per pooling strategy retained (same information as before, one-quarter the rows).
- Dropped the Azaria & Mitchell comparison paragraph and the representational-difficulty hedging (already narrowed in V23).
- Retained: numerical result (rule-parity within ±4 pp), pointer to `app:mistral_probe_panel`, base/Instruct caveat.
- Figure caption tightened from 4 lines to 2 lines.

**After (lead paragraph):**
> *"On Llama 3.2 3B and Mistral 7B equalized transcripts (n=100 each), last-layer LR probes achieve 63% and 65% LOO respectively; per-layer sweeps (29 and 33 layers × 2 pooling strategies, 8 configurations total per target) peak at 67% (Llama 3B, layer 12, last-token) and 66% (Mistral 7B base, layer 4; Appendix N). No configuration exceeds the within-target refusal-count rule by more than ±4 pp. We report the probe parity with the rule as **rule-parity at tested design points**; conclusive comparison requires multiple probing architectures (non-linear, contrastive) and frontier-scale open-weight targets."*

---

## W7 — Single-Prompt Limitation for Both Persona and False-Belief ICL

> *"Single-persona-prompt limitation: already in §5.8(j); false-belief ICL has the same issue."*

**Before (discussion.tex:67 limitation (j)):**
> *"The 5th-scenario persona condition … tests a single persona prompt … wording-robustness (varying name, credentials, instructional framing) is untested."*

**After:**
> *"Both the 5th-scenario persona condition (§4.7.2, 'Dr. Alex Morgan, MIT physics educator') and the false-belief-ICL condition (§4.8, single few-shot template) test a single prompt instantiation; wording-robustness for both (varying persona credentials, varying ICL exemplars) is untested."*

---

## W8 / Q4 — Holm-Bonferroni Caveat Travels with Qwen 3B→7B p=0.014

> *"Within-family vs joint Holm-Bonferroni caveat appears only in §4.6; should travel with every Qwen 3B→7B p=0.014 mention."*

**V24 verification.** `grep -n "Qwen.*3B.*7B\|3B.*→.*7B\|p=0.014" sections/*.tex` confirms only one mention of `p=0.014` exists in the paper, at `experiments.tex:260`, and it is already correctly caveated in V23 with the Holm-Bonferroni explanation:

> *"…Fisher p=0.014 < α/3=0.017 under within-family Holm-Bonferroni … Qwen 3B→7B does not survive joint Holm-Bonferroni across all adjacent pairs …"*

No additional mention exists in abstract, introduction, or discussion. No edit needed.

---

## Q2 — Qwen 14B Persona 68.0%: Partial Correction, Sycophancy Leakage, or Noise?

**V24 action.** A qualitative spot-check script (`code/adaptive_lie_detector/experiments/qwen14b_persona_spot_check.py`) was produced. It samples 10 trials (5 TRUE + 5 FALSE, seed=42) from `persona_autonomous_qwen2.5_14b_n200_final.json`, produces a readable coding report (`qwen14b_persona_spot_check_report.txt`), and outputs a JSONL for coded results. Coding scheme: P (persona maintained), B-correct (direct factual correction), B-other (other mechanism). The coded counts will be integrated into the Table 12 post-hoc reading paragraph and Appendix N (`app:qwen_persona_qual`) in camera-ready.

---

## V24 Diff Summary

**New files (code):**
- `code/adaptive_lie_detector/experiments/run_human_baseline_v24.py` — transcript sampler (n=50, 7 models, seed=42)
- `code/adaptive_lie_detector/experiments/human_baseline_analysis_v24.py` — analysis script (per-annotator accuracy, Cohen's κ, comparison table)
- `code/adaptive_lie_detector/experiments/qwen14b_persona_spot_check.py` — 10-trial persona qualitative sampler
- `docs/human_baseline_protocol_v24.md` — 1-page annotator protocol

**New data files:**
- `code/adaptive_lie_detector/data/human_baseline_v24/transcripts_n50.jsonl` — 50 annotator-visible trials
- `code/adaptive_lie_detector/data/human_baseline_v24/ground_truth_n50.json` — held-out ground truth
- `code/adaptive_lie_detector/data/human_baseline_v24/annotator_A_template.csv` — Annotator A form
- `code/adaptive_lie_detector/data/human_baseline_v24/annotator_B_template.csv` — Annotator B form
- `code/adaptive_lie_detector/data/human_baseline_v24/qwen14b_persona_spot_check.jsonl` — spot-check trials
- `code/adaptive_lie_detector/data/human_baseline_v24/qwen14b_persona_spot_check_report.txt` — coding report

**New data files (annotation completed):**
- `code/adaptive_lie_detector/data/human_baseline_v24/annotator_A_completed.csv` — Annotator A labels (50/50 TRUTH)
- `code/adaptive_lie_detector/data/human_baseline_v24/annotator_B_completed.csv` — Annotator B labels (48/50 TRUTH, 2/50 LIE)

**Paper edits (sections/*.tex):**
- `abstract.tex:2` — +8 words: `(level-dependent; ICC=0.114, §5.1)` after 74.3%
- `experiments.tex` — §4.9 compressed ~31→~15 lines; post-hoc reading paragraph after Table 12 (+5 lines); §4.10 human baseline **full results** section (+25 lines including Table `tab:human_baseline`)
- `appendix.tex` — Appendix N `app:qwen_persona_qual` stub (+7 lines)
- `discussion.tex:67` — §5.7(j) extended to cover persona+FB ICL; §5.7(k) **updated with completed results** (44.0% accuracy, κ=0.00, rule +32 pp)

**Page count:** 43 pages (within ≤43 target). 0 LaTeX errors. 0 undefined refs.

---

## Out-of-Scope for V24

- Non-English n=50 pilot (W2): remains §5.8 future work.
- Provider-replication of Sonnet 4.5 pilot on non-Bedrock API: remains §5.8 future work.
- Scaling human baseline beyond n=50 or 2 annotators: n≥100/3-annotator study remains the §5.1 camera-ready commitment.
- Qwen 14B persona qualitative spot-check coding (P/B-correct/B-other): script and 10-trial report produced; counts to be integrated into Appendix N and Table 12 post-hoc paragraph at camera-ready.

---

*Word count: ~1,500. Response letter follows V22/V23 template.*
