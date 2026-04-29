# Response to Reviewer #6

We thank the reviewer for a careful and constructive review. The feedback identified specific precision gaps and missing content that strengthened the paper. We address each weakness, detailed comment, and question below.

**Summary of changes:**
- 80.1% headline now includes range (64-88%; 75-88% on models >=7B) in abstract, introduction, experiments, and conclusion
- Holm-Bonferroni scope made transparent: both within-family and joint 5-test results reported
- Cross-claim-set deployment evaluation (EXP-L) restored in S4.2
- Average row added to Table 2 (refusal-only comparison)
- Novelty argument strengthened in S5.3 with effect magnitude emphasis
- Same-family bias reframed from "observed only in Claude" to "found in Claude; cannot rule out others"
- Regex-vs-LLM construct tension addressed in S5.4
- "ADAGE adds little" promoted to conclusion
- Knowledge-probing future work expanded to full paragraph in conclusion
- Qwen 32B adversarial robustness implications added to S4.5
- Persona CI caveat added (uninformative pilot)
- Mock validation one-sentence explanation added to S4.1
- Three controls named explicitly in introduction S1.1

---

## Weaknesses

**W1 (Novelty — controls individually standard).**
We agree the individual controls draw on established methodology. S5.3 now emphasizes that no prior behavioral detection work applied them to this domain, and their combined application reveals confounds of unprecedented magnitude: 30-41pp accuracy collapse under equalization, 7x feature inflation from same-family extraction, and 9-16pp extractor gaps across families. These magnitudes were not anticipated by the prior literature and change the practical interpretation of all existing behavioral detection results.

**W2 (80.1% average obscures per-model variance).**
All primary appearances of "80.1% average" now include "(range: 64-88%; 75-88% on models >=7B)." The 64% floor on Llama 3B is contextualized by the model's weak world knowledge (40% pre-check accuracy), which limits the knowledge-conflict signal the heuristic detects. The median is 81.8% (Claude Haiku).

**W3 (Same-family bias claim too strong).**
Reframed throughout: "Same-family bias is clearly present in Claude; it is not observed in Mistral-on-Mistral or Qwen-on-Qwen, but this may reflect the lower capability of those extractors rather than the absence of the bias. A definitive test would require a non-Claude extractor of comparable capability." This appears in both S4.7 and S5.2.

**W4 (Sycophancy "semi-autonomous transfer" overstated in conclusion).**
The conclusion now avoids "transfer" language. Sycophancy (82%) is framed as "system-prompt-induced agreement pressure" throughout, and the abstract explicitly states "rather than spontaneous strategic deception." The persona result (66%, CI [36-78%] includes chance) is now flagged as an uninformative pilot in S4.6.

**W5 (Regex-matches-pipeline vs. LLM-extracts-different-construct tension).**
Added to S5.4: "The low correlation between regex refusal-count and LLM correction-density (mean |rho|=0.15 across models) indicates these features capture distinct aspects of the same behavioral signal — refusal-count detects explicit correction/refusal markers while LLM correction-density scores overall correction behavior on a continuous scale. That both achieve similar accuracy despite measuring different constructs suggests the underlying behavioral signal (models correcting false claims under knowledge conflict) is robust and surface-level, supporting the conclusion that sophisticated feature extraction is unnecessary."

**W6 (Holm-Bonferroni correction scope).**
The reviewer is correct that joint correction across all 5 adjacent increments changes which results survive. S4.5 now reports both: "Under within-family Holm-Bonferroni correction, both families contain at least one significant increment (Qwen 3B->7B p=0.014 < alpha/3=0.017; Llama 8B->70B p=0.004 < alpha/2=0.025). Under joint correction across all five adjacent increments, only the Llama increment survives (p=0.004 < alpha/5=0.01)." The abstract mirrors this dual reporting.

**W7 (Cross-claim-set deployment evaluation missing).**
This was accidentally cut during the 5th revision's compression. Now restored as EXP-L in S4.2: "Cross-claim-set accuracy is within +/-2.2pp of within-set LOO on all models, confirming the detection signal generalizes across claim content and is not an artifact of specific factual domains." EXP-L is also added to the experiment summary table (Table 1).

**W8 (Mock validation unexplained in S4.1).**
Added one-sentence explanation: "mock validation on n=100 synthetic transcripts confirms algorithmic correctness at 93% LOO accuracy but does not predict real-model behavior, which is qualitatively different."

**W9 (Minor artifacts: unnamed controls, unsourced Llama numbers, Appendix D).**
- Three controls now named in S1.1: "Future work should report results under all three controls — prompt equalization, cross-family extraction, and regex baselines — to separate genuine signal from confounds."
- Llama 5-feature pipeline numbers (61%->65%->84%) are reported inline in S4.5. Since Llama has only 3 data points, a dedicated table would be redundant with the existing Qwen table.
- Appendix D is not a dangling header: it contains full EXP-G per-model decompositions including a knowledge pre-check stratification table (Table in Appendix D).

**W10 (Two contributions could be one finding with two faces).**
We see merit in this unified framing — the empirical finding (instruction-following dominates) logically implies the practical artifact (deploy refusal-count instead). We retain the two-part structure for clarity in application: the first contribution (methodological finding via controls) is relevant to researchers evaluating any behavioral detection system, while the second (deployment rule) is relevant to practitioners deploying detection in production. The two-part framing makes it easier for readers to identify which contribution is relevant to their use case.

---

## Questions

**Q1 (Median/floor alongside 80.1% average).**
Median: 81.8% (Claude Haiku). Floor: 64% (Llama 3B). Range on >=7B models: 75-88%. All primary 80.1% mentions now include "(range: 64-88%; 75-88% on models >=7B)."

**Q2 (Why was cross-claim-set evaluation removed?).**
It was accidentally cut during the 5th revision's 40% length reduction. Now restored as EXP-L in S4.2 with the original data: mean held-out accuracy within +/-2.2pp of LOO on all four tested models.

**Q3 (Does Qwen 32B collapse hold under LLM extraction?).**
Not yet tested. We note this as future work. However, the collapse mechanism — zero refusal/correction markers in both conditions — suggests LLM extraction is unlikely to recover signal: with no behavioral difference in the transcripts for either regex or LLM to score, the collapse reflects an absence of behavioral signal rather than a failure of the specific measurement approach. If the transcripts contain no correction behavior at all, there is nothing for any extractor (regex or LLM) to detect.

**Q4 (Claude same-family bias: model-pair or family-level?).**
This remains open. The current data cannot distinguish model-pair-specific self-preference from family-level bias. A definitive test would require a non-Claude extractor of comparable capability (e.g., GPT-4o or Gemini Pro as feature extractor on Claude transcripts). We note this explicitly: "A definitive test would require a non-Claude extractor of comparable capability."

**Q5 (Sycophancy autonomy claim — defend or soften?).**
We maintain the "semi-autonomous" label with explicit qualification: "system-prompt-induced agreement pressure rather than spontaneous strategic deception." This is deliberately conservative — we do not claim it demonstrates autonomous deception detection. The label serves to locate sycophancy on the autonomy spectrum between instructed roleplay (fully prompted) and spontaneous deception (no instruction), while the qualifier prevents overinterpretation.

---

## Detailed Comments

**DC (Table 2 average row).**
Added: Average row shows Refusal-only 80.1%, Hedging 81.9%, LLM pipeline 74.3%, making the refusal-count advantage over the LLM pipeline visible at a glance.

**DC (Qwen 32B adversarial robustness).**
Added to S4.5: "This has direct implications for adversarial robustness: if standard RLHF incidentally eliminates all surface-level detection signals, adversarial fine-tuning could achieve the same deliberately. Any behavioral detection system relying on surface-level markers is vulnerable to this failure mode."

**DC (Persona CI includes chance).**
Added explicit caveat in S4.6: "(CI includes chance; an uninformative pilot)."

**DC (Promote "ADAGE adds little" to conclusion).**
Added: "The structured ADAGE pipeline adds little over these simple heuristics: K=1 suffices under instructed conditions, and the refusal-count rule matches or exceeds the full 5-feature LLM pipeline under equalization."

**DC (Expand knowledge-probing future work).**
Expanded to full paragraph: "Specifically, questions designed to elicit correction behavior — presenting false alternatives and measuring whether models correct them unprompted — could yield features more robust to RLHF smoothing than the refusal-count markers that collapse at Qwen 32B. Such approaches could operate as lightweight deployment monitors, requiring no labeled data and no LLM extraction."

**DC (Appendix D).**
Verified: Appendix D contains full per-model EXP-G decompositions for all five models plus a knowledge pre-check stratification table. Not a dangling header.
