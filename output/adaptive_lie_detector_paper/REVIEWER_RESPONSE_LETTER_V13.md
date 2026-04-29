# Response to Reviewer — Round 4 (Weak-Accept 6/10, Confidence 4/5)

We thank the reviewer for a careful, constructive review. The nine weaknesses (W1–W9), six detailed comments (C1–C6), and five follow-up questions (Q1–Q5) drove concrete changes in this revision. We summarize them below, tiered by whether they required new experiments (Tier 1), text-only revisions (Tier 2), or honest acknowledgment under resource constraints (Tier 3).

## Tier 1 — New experiments in this revision

### W4 / Q1 — Second attested-frontier cross-family extractor

**Ask.** Replicate the cross-family panel (Table 9 / §4.7) with a non-Anthropic extractor that is not Mistral Large 3, so the Haiku–Mistral-Large gap can be decomposed into (a) extractor capability vs. (b) same-family self-preference.

**What we did.** We added **Llama 3.3 70B Instruct** (AWS Bedrock, `us.meta.llama3-3-70b-instruct-v1:0`) as a second non-Anthropic extractor on the full 8-target equalized panel. All eight targets are re-scored from the identical saved transcripts (no new target-model inference), so any accuracy difference reflects extractor behavior only. Results are integrated into Table 9 as a fourth column and into §4.7 as a triangulation point for the Haiku–Mistral-Large gap.

**Result.** Llama-70B-extracted 5-feature pipeline: 7-target avg **66.9%** (vs. Mistral Large 64.7%, Haiku 74.3%); 8-target avg 66.0% (vs. Mistral Large 64.2%, Haiku 74.5%). The two non-Anthropic extractors agree within 3 pp on 7 of 8 targets and both land ≈9–10 pp below Haiku. The "Mistral Large is uniquely weak" hypothesis is therefore not supported: two independently-trained non-Anthropic frontier extractors produce nearly-identical accuracies, supporting a same-family self-preference reading of the Haiku uplift rather than asymmetric extractor capability. Table 9 now reports three extractor columns plus an "Avg CF gap" column, and §4.7 prose has been rewritten for the triangulation.

### Q5 / W1 (partial) — Sycophancy transfer at ≥70B scale

**Ask.** Does the sycophancy-transfer result (82% at 3B and 14B) hold at 70B scale, or is it a coincidence of the specific scales tested?

**What we did.** We ran `sycophancy_autonomous` on **Llama 3.3 70B** via Bedrock at $n=50$, identical pipeline to the 3B and 14B runs. The result is reported in §4.6 as a third scale point for the sycophancy transfer finding and is the cleanest response available to Q5 within the revision window.

### W9 — Finalize Qwen 14B EXP-K

**Ask.** Appendix J's "in progress at submission" footnote on the Qwen 14B EXP-K row is stale; the data existed at submission time.

**What we did.** We computed the refusal-count and 5-feature LOO on the saved `ollama_eval_qwen2_5_14b_pacchiardi_{related,unrelated}_latest.json` trials, expanded **Table 24 from 4 to 6 rows** (adding Qwen 14B unrelated/related), dropped the "in progress at submission" footnote from the caption and body, and updated the interpretation paragraph to incorporate the +29pp Qwen 14B pipeline delta as a second confirmation of the "≥14B scale needs related follow-ups" pattern.

## Tier 2 — Text-only revisions

### W3 — "Deployment candidate" → "baseline against which more robust detectors should be measured"

All instances of "deployment candidate" in `abstract.tex`, `introduction.tex`, `conclusion.tex`, and `discussion.tex` have been replaced with the reviewer's preferred phrasing. `grep -r "deployment candidate" sections/` returns zero matches.

### W5 — Mistral Large 3 Bedrock ID verification

The 675B parameter count in the Bedrock model identifier is not publicly attested by Mistral AI. Appendix A.9 "Model identification notes" has been expanded to state this explicitly and to position Mistral Large 3 as "AWS Bedrock's flagship Mistral-family model" rather than "an attested-frontier 675B model." We do not rely on the parameter count in any numerical claim.

### W6 — Explicit English-only scoping

Added an English-only sentence to the abstract, conclusion, and Limitations(h). Representative phrasing: *"All behavioral detection here is English-only; refusal-marker patterns are not validated on non-English prompts or stylistic variants."*

### W7 — Sycophancy-transfer nuance in abstract

The abstract previously said only "60–66%, near chance at n=50." It now also says: *"A semi-autonomous sycophancy condition is the one scenario that does transfer (82% at both 3B and 14B, Cohen's d ≈ 1.5), consistent with knowledge-conflict clarity (not deception autonomy) being the signal our rule actually tracks."* This mirrors the nuance the conclusion already carried.

### W8 — Demote pooled ≤7B vs ≥14B comparison

The pooled comparison is no longer used as a headline claim. Figure 6 caption now reads "pooled $p < 0.0001$, exploratory post-hoc comparison, not pre-registered," and the Discussion's §Feature-Extraction-Validity mitigator list replaces "pooled $\leq$7B vs. $\geq$14B comparison is significant" with within-family Holm-Bonferroni-surviving increments (Qwen 3B→7B $p=0.014$; Llama 8B→70B $p=0.004$), explicitly flagging the pooled version as exploratory and non-load-bearing.

### Detailed C1 — §3.2 pipeline summary

Expanded §3.2 from one paragraph to a full input/output/feature description: inputs (claim + target model + system prompt); process (interrogator LLM, feature extractor LLM); features (the full 5-dimensional list with descriptions: consistency, specificity, correction-marker density, confidence, elaboration); outputs (binary label + confidence).

### Detailed C2 — Table 2 per-model 95% CIs

Table 2 (`tab:refusal_only`) now includes a Wilson-score 95% CI column for the refusal-only LOO per target. Caption updated to document the CI methodology.

### Detailed C3 — §4.5 frontier n-for-power

Added a one-line power calculation to the Sonnet 4.5 frontier section: detecting a 4pp paired gap at 80% power, $\alpha=0.05$, requires $n \approx 410$ at $\rho=0.5$ or $n \approx 570$ at $\rho=0.3$; our $n=99$ is underpowered for this effect size by $4$–$6\times$, so "no significant difference" should not be read as evidence of no gap.

### Detailed C4 — §4.6 sycophancy-as-semi-autonomous defense

Added a ~200-word paragraph to §4.6 defending the "semi-autonomous" classification: (i) the system prompt instructs agreement, not lying, so the knowledge conflict is model-generated; (ii) we acknowledge the adversarial reading that sycophancy is effectively instructed deception with an extra reasoning step; (iii) we keep the label because the target behavior is agreement (not a pre-specified deception mode) and because the same RLHF-disposition pattern drives safety-literature concerns around deceptive alignment. The paragraph is intentionally self-contained so future reviewers can engage with the classification directly.

### Detailed C5 — §4.7 flip 7-target primary / 8-target parenthetical

The reviewer correctly noted that including Qwen 32B (which collapses to chance by construction under RLHF zero-marker behavior) in the headline cross-family average produces a *mechanically diluted* number, not a *more conservative* one. We have flipped the framing: **7-target 64.7% is now the primary interpretable summary** and 8-target 64.2% is a transparency diagnostic (the two differ by <1pp). This change is propagated to abstract, introduction, §4.7, and Table 9 averages row.

### Detailed C6 — Appendix A.4 mock validation flag

Renamed Appendix A.4 to "Algorithmic Sanity Checks (Mock Transcripts; Not Predictive of Real-Model Performance)" and added a leading disclaimer sentence making explicit that mock accuracies are sanity checks for algorithmic correctness and not predictive of real-model behavior.

## Tier 3 — Honest acknowledgment under resource constraints

### W2 / Q4 — ICC = 0.114, $n \geq 100$, 3+ annotators, Krippendorff's $\alpha$

A proper construct validation study ($n \geq 100$ transcripts, 3+ annotators, Krippendorff's $\alpha$) requires funded annotation work that is beyond this revision cycle. We commit to completing it for camera-ready if accepted.

In the meantime, we have enumerated in Discussion §5.5 Limitation (i) which claims do and do not depend on absolute feature levels:

- **Not dependent on levels** (ICC-invariant): refusal-count LOO on 8 targets; the three-control effects (each measures a structural accuracy gap, not a feature magnitude); the Qwen 32B zero-marker collapse (raw count observation).
- **Dependent on levels** (ICC-sensitive): the 74.5% Haiku-pipeline average, the 92.9% Sonnet-Haiku result, the EXP-G instructed-matched decomposition, and the §4.8 probing band.

Section 5.1 ("Construct Validity: the ICC=0.114 Caveat, Owned") already leads the Discussion with this caveat; the enumeration in Limitation (i) is a second, more actionable statement for readers who want to know which numbers to trust regardless of the pending validation.

### W1 (persona + false-belief scaling) / Q2 — $n=200$ per scenario at 3 scales

Persona and false-belief ICL at 3B scale require Ollama-local inference at ~8–15 min per trial. $200 \times 2 \text{ scenarios} \times 2 \text{ additional scales} \approx 100$–$200$ hours of local GPU wall-time is not feasible in the revision window. We acknowledge the CI widths explicitly (persona $d=0.3$ CI [36, 78]; false-belief $d=0.1$), keep the $n=50$ 3B pilots as uninformative pilots, and commit to persona $n \geq 100$ on Qwen 14B and Llama 3.3 70B for camera-ready.

**Partial mitigation**: the Llama 70B sycophancy run described in Q5 above adds a bona fide third scale point (3B / 14B / 70B) to the one scenario that does transfer (sycophancy), strengthening the "knowledge-conflict clarity, not autonomy" interpretation without a new persona or false-belief run.

### Q3 — Claude Opus 4.x frontier

Not run. Sonnet 4.5 was the latest/largest model we could afford at $n=100$. Adding Opus would be one additional frontier data point but not fundamentally change the frontier claim (already explicitly hedged as "sole frontier data point"). We commit to adding Opus for camera-ready if accepted and frontier resources permit.

## Summary of changes this revision

| Ask | Response | Tier |
|---|---|---|
| W1 persona/false-belief scaling | Acknowledged; Llama 70B sycophancy as partial mitigation | 1+3 |
| W2 ICC=0.114 proper validation | Committed to camera-ready; Limitation (i) enumerates dependency | 3 |
| W3 "deployment candidate" framing | Replaced throughout | 2 |
| W4 / Q1 second non-Anthropic extractor | Llama 3.3 70B added as 4th column / triangulation | 1 |
| W5 Mistral Large 3 ID | Explicit disclosure in Appendix A.9 | 2 |
| W6 English-only scoping | Abstract + conclusion + Limitation (h) | 2 |
| W7 sycophancy nuance in abstract | Added | 2 |
| W8 demote ≤7B vs ≥14B | Figure 6 caption + Discussion mitigator list | 2 |
| W9 Qwen 14B EXP-K finalize | Table 24 expanded to 6 rows | 1 |
| C1 §3.2 pipeline summary | Expanded | 2 |
| C2 Table 2 per-model 95% CIs | Wilson CIs added | 2 |
| C3 §4.5 n-for-power | Added | 2 |
| C4 §4.6 semi-autonomous defense | Added as full paragraph | 2 |
| C5 §4.7 7-target primary | Flipped, propagated to abstract/intro | 2 |
| C6 Appendix A.4 mock flag | Renamed + disclaimer | 2 |
| Q2 autonomy n=200 | Acknowledged; CI widths carried forward | 3 |
| Q3 Opus frontier | Committed to camera-ready | 3 |
| Q5 sycophancy at 70B | Llama 70B sycophancy at n=50 added | 1 |

We believe the three Tier-1 experimental additions (second extractor on the 8-target panel, sycophancy at a third scale, Qwen 14B EXP-K finalization) plus the full Tier-2 pass directly address the reviewer's concerns and would support movement from 6/10 weak-accept to a stronger accept.
