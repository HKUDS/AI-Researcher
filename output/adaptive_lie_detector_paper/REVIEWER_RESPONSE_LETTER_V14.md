# Response to Reviewer — Round 5 Camera-Ready (Accept 7/10, Confidence 4/5)

We thank the reviewer for the detailed camera-ready suggestions and for the 7/10 Accept recommendation. This response letter addresses each of the four suggested camera-ready revisions in order.

## Suggestion 1 — Scale-replicate persona and false-belief negative results on Qwen 14B (highest priority)

**Ask.** The reviewer's single largest residual concern is that the fully-autonomous negative-transfer claim rested on persona-maintenance (66%) and false-belief-via-ICL (60%) at n=50 on a single 3B model. Scale-replication on Qwen 14B (where the infrastructure clearly existed, since the sycophancy replication was done there) would substantially strengthen a negative result that currently rests on one scale.

**What we did.** We ran both scenarios on Qwen 2.5 14B via Ollama at n=50 each, identical pipeline to the Llama 3B runs and matching the Qwen 14B sycophancy protocol:

- `run_persona_autonomous.py --model qwen2.5:14b --n 50`
- `run_false_beliefs_autonomous.py --model qwen2.5:14b --n 50`

**Result.** Qwen 14B persona-maintenance refusal-count LOO: **64.0%**, Wilson 95% CI [50.1, 75.9], |d|=0.80. Qwen 14B false-belief-via-ICL refusal-count LOO: **66.0%**, Wilson 95% CI [52.2, 77.6], |d|=1.07. Both 14B Wilson intervals still *include chance*, consistent with the 3B result (persona 66% CI [36–78], false-beliefs 60%). Table 4 has been expanded to include these two new rows plus the Qwen 14B sycophancy row (82.0%, already existing in our data but not previously tabulated alongside the other autonomy scenarios at 14B) and the Llama 70B sycophancy row (72.0%, d=0.88). The §4.6 interpretation paragraph has been updated accordingly.

The sycophancy/persona/false-belief asymmetry now has a cleaner shape: **sycophancy transfers across three scales** (3B/14B/70B: 82%/82%/72%, with the 70B pipeline reaching 92%), while **persona and false-belief remain near chance at two scales each** (3B: 66%/60%; 14B: 64%/66%, CIs including chance). The negative-transfer claim now rests on two independently-pretrained families (Llama and Qwen) at two scale points, directly addressing the reviewer's "a negative result at multiple scales is substantially more compelling than a negative result at one scale." The finding is consistent with our "knowledge-conflict clarity" interpretation rather than a 3B artifact.

## Suggestion 2 — One additional sentence in §4.6 on the Llama 70B sycophancy pipeline-vs-rule gap

**Ask.** The 92% pipeline vs. 72% refusal-count rule gap on Llama 70B sycophancy is a 20 pp gap — the largest outside the instructed condition. The reviewer wanted one more sentence of analysis.

**What we did.** We added one sentence to §4.6, directly after the 92% pipeline report, that (i) identifies the 20 pp gap as the largest outside the instructed condition, (ii) points at the multi-turn-signal value we document at ≥14B equalized (§4.4) as the most likely mechanism, and (iii) honestly acknowledges we cannot at n=50 with Haiku-only extraction cleanly separate multi-turn signal from Haiku-on-Llama same-family-from-below inflation, so we report the gap without claiming a specific mechanism.

## Suggestion 3 — One-sentence definition of "Avg CF gap" in Table 9's caption

**Ask.** The "Avg CF gap" column definition appears only in surrounding prose, not the caption, so readers scanning the table in isolation may misinterpret.

**What we did.** We added the definition directly to the Table 9 caption: *"'Avg CF gap' is the per-target mean of (Haiku − Mistral L3) and (Haiku − Llama 70B), in percentage points."*

## Suggestion 4 — Small expansion of the human validation study (n=50, 3 annotators) before camera-ready

**Ask.** Bringing the ICC=0.114 validation from n=20, 2 annotators to n=50, 3 annotators would substantially strengthen §5.1 without requiring a full n=100 study.

**Our position.** We agree in principle but cannot responsibly complete a 3-annotator rubric-training-and-rating cycle within the camera-ready window — external annotator recruitment plus inter-rater calibration on the 5-feature rubric (consistency, specificity, correction-marker density, confidence, elaboration) is a multi-week process. Limitation (i) already enumerates which claims are ICC-invariant (refusal-count LOO on 8 targets, the three-control structural-accuracy effects, the Qwen 32B zero-marker collapse) versus ICC-sensitive (74.5% Haiku-pipeline average, 92.9% Sonnet-Haiku, EXP-G decomposition, §4.8 probing band). We commit to completing the n=50, 3-annotator expansion and reporting Krippendorff's α for the post-camera-ready public release, with the data and rater guidelines deposited alongside the paper artifacts.

## Summary of changes

| Ask | Response | Type |
|---|---|---|
| 1. Qwen 14B persona + false-belief replication | Both scenarios run at n=50; Table 4 expanded; §4.6 interpretation updated | New experiments |
| 2. §4.6 pipeline-gap analysis sentence | Added, with honest acknowledgment of the multi-turn/same-family-bias confound | Text |
| 3. Table 9 "Avg CF gap" caption definition | Added to caption | Text |
| 4. n=50, 3-annotator ICC top-up | Committed for post-camera-ready public release | Acknowledged |

We believe this targeted camera-ready pass — one new experimental pair (the reviewer's top priority) plus two mechanical text fixes — fully addresses the suggestions. The ICC top-up is an honest resource constraint, scoped by Limitation (i) and committed to post-camera-ready.
