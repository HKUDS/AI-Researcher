# Response to Reviewer (Weak Reject, 5/10; Confidence 4/5)

We thank the reviewer for the exceptionally detailed and constructive review. The three headline asks --- (a) a frontier-scale model, (b) an adversarial robustness test, and (c) a restructure that leads with the regex finding rather than the ADAGE pipeline --- have all been addressed concretely in revision 9. This letter maps every numbered concern (W1--W8, DC1--DC6, Q1--Q5, and the "candid notes") to the specific change made.

**Summary of changes (revision 9).**
- **New experiment 1 (frontier scale, W6/Q4):** Claude Sonnet 4.5 equalized, $n=100$, Bedrock. Results integrated into Section 4.5 (§sec:sonnet_frontier), the abstract, and §1.2.
- **New experiment 2 (adversarial robustness, W7/Q1):** One-shot adversarial paraphrase prompt on Llama 3B, $n=50$. Results in Section 4.1 (§sec:adversarial_paraphrase), referenced from conclusion and abstract.
- **Restructure (W4, candid notes):** Abstract now leads with the 80.1% regex rule. §1.1 contributions are reordered regex-first. §1.3 duplicate contribution list removed (now a one-paragraph roadmap). Methodology §3.2 introduces ADAGE explicitly as "a standard behavioral-detection pipeline we use as a comparison baseline."
- **EXP-G both ranges (DC1):** Abstract reports +7.5--15 pp (clean, 14B/70B) *and* +26--31 pp (upper bound, 3B/8B/7B with KT confound) prominently. Discussion §5.1 adds Qwen 14B ceiling-effect explanation (Q3).
- **Pacchiardi EXP-K (Q5):** Already in §2.2 related work (line 14) with the "within 1 pp" summary; appendix retained for full detail.
- **Deployment language (W2):** "deployment-viable" → "deployment candidate" in conclusion and abstract, with the adversarial-paraphrase brittleness result cited.
- **Not-pre-registered caveat (DC2):** Added to §4.5 pooled ≤7B vs ≥14B comparison.
- **Mock validation (DC5):** Appendix A.4 compressed from 1 table + 4 paragraphs to 1 paragraph.
- **Haiku 97.8% flag (DC3):** Already in abstract ("driven by RLHF safety compliance, not deception detection per se"); discussion §5.2 retains the full mechanism explanation.

---

## Weaknesses (W1--W8)

**W1 (novelty vs Pacchiardi).**
EXP-K now occupies a full paragraph in §2.2 (end of Pacchiardi paragraph): related and unrelated follow-ups are within 1 pp (72% vs 71% LOO, Mistral 7B equalized, $n=100$), "consistent with the detection signal residing primarily in the target's first response to the claim rather than in subsequent probing." This directly updates the Pacchiardi design rationale rather than treating ADAGE as a novel advance over it. We also cite Pacchiardi's instructed-without-equalization as a contrast that motivates our three controls.

**W2 (deployment tension).**
Addressed on three fronts. (1) Terminology: "deployment-viable" → "deployment candidate" in abstract and conclusion. (2) Explicit fragility: we state the rule "inherits the fragility of RLHF-shaped behavior" (Qwen 32B = 50%) and of lexical markers under adversarial paraphrase. (3) Empirical: the adversarial paraphrase experiment (§sec:adversarial_paraphrase) quantifies the drop on Llama 3B. We no longer claim the rule is production-ready; we claim it is a label-free baseline worth measuring new detectors against.

**W3 (autonomous $n=50$ is thin).**
Acknowledged. §4.6 now frames the autonomous pilots as "preliminary matched-format evaluation" whose CIs include chance for persona and false-beliefs conditions. We retain the section because the sycophancy replication at Qwen 14B ($d=1.6$) does provide a non-trivial signal-transfer data point, and the negative result for persona/false-beliefs is informative. We do not headline these findings.

**W4 (ADAGE-first structure).**
Fully restructured. Abstract paragraph 1 now leads with "a one-line label-free rule (refusal count $\geq 1$) achieves 80.1% average accuracy ... matching or exceeding a 5-feature LLM interrogation pipeline (ADAGE) on 6 of 7 models." §1.2 contributions are reordered: (1) regex rule, (2) instruction-following decomposition, (3) scale and adversarial findings. §3.2 explicitly frames ADAGE as "a standard behavioral-detection comparison baseline representing multi-turn behavioral detection, not as a proposed method."

**W5 (same-family confound).**
The abstract and §2.2 now consistently report the 7× figure as "variance" rather than "inflation" and explicitly note the capability-difference confound (reviewer 8 agreed this was the honest framing). The new Sonnet 4.5 data point uses Claude Haiku as extractor, i.e., same family but smaller --- "cross-family-from-below" --- which partially mitigates self-preference. A full non-Anthropic extractor of comparable capability is still out of reach (Q2) and is listed as the highest-priority future work.

**W6 (frontier scale).**
**Done.** Claude Sonnet 4.5, $n=100$, prompt-equalized, Bedrock. Reported in §4.5 as a one-paragraph "frontier-scale data point" with LOO accuracy, refusal-count accuracy, and interpretation relative to the $\geq 14$B pattern. Also referenced in the abstract and §1.2 bullet (3). The limitation of a single cross-family-from-below data point is stated explicitly.

**W7 (adversarial robustness).**
**Done.** Adversarial paraphrase system prompt on Llama 3B: target is instructed to avoid the lexical markers the rule keys on ("actually," "incorrect," "I cannot," etc.) and paraphrase disagreements neutrally. Both truth and lie conditions use the same adversarial+neutral prompt ($n=50$, equalized). Results in §sec:adversarial_paraphrase; the accuracy drop from the 64% baseline is reported as the rule's fragility estimate against a static, non-adaptive adversary. We note the limitation: "an adaptive adversary that tailors paraphrases to the detector's specific regex would likely drive accuracy further toward chance."

**W8 (writing density).**
Abstract compressed from 5 paragraphs to 4 tight paragraphs. §1.3 duplicate contribution list removed (replaced with a 1-sentence roadmap). Methodology §3.2 tightened. Appendix A.4 compressed to one paragraph (DC5).

---

## Detailed Comments (DC1--DC6)

**DC1 (both EXP-G ranges reported prominently).**
Addressed. Abstract paragraph 2 now reads: "instruction-following asymmetry accounts for +7.5--15 pp on knowledge-controlled subsets (14B/70B; clean decomposition) and +26--31 pp on smaller models (3B/8B/7B; upper bound that conflates instruction-following with knowledge-transfer effects)." §1.2 bullet (2) has the same balanced framing. Table 4 (EXP-G decomposition) explicitly annotates "Clean" vs "KT confound" per row.

**DC2 (not pre-registered).**
Added to §4.5: "This pooled comparison was not pre-registered; it was motivated by within-family patterns observed after data collection and should be interpreted as exploratory."

**DC3 (Claude Haiku 97.8% flag).**
The 97.8% result is flagged as driven by RLHF safety compliance (not deception detection) at every main-body reporting site: abstract paragraph 2, §5.2 discussion (full mechanism explanation), and §4 tables (noted as same-family with the limitation caveat). The 100%-refusal mechanism is quoted in the abstract.

**DC4 (EXP-K placement).**
EXP-K is now summarized in §2.2 related work (in the main body), with full detail in Appendix J. The main-body summary is one paragraph: "Our equalized replication (EXP-K, Appendix J) finds related and unrelated follow-ups within 1 pp (72% vs 71%, Mistral 7B, $n=100$), consistent with the detection signal residing primarily in the target's first response."

**DC5 (mock validation in appendix A.4 is too long).**
Compressed from 4 paragraphs + 1 table to 1 paragraph. Table 2 (consolidated mock results) is retained as the compact summary; the narrative paragraphs on feature separability, threshold sensitivity, baselines, and confidence trajectories were removed.

**DC6 (Claude Sonnet 4.5 on Bedrock).**
Done. We discovered Sonnet 4.5 is available via `anthropic.claude-sonnet-4-5-20250929-v1:0` on Bedrock in us-east-2 and used that.

---

## Questions (Q1--Q5)

**Q1 (adversarial robustness test).**
See W7. Result reported in §sec:adversarial_paraphrase.

**Q2 (GPT-4o/Gemini as cross-family extractor?).**
Not available to us as a structured feature extractor for this revision. The three-family comparison (Claude, Mistral Large, Qwen) established the phenomenon; a comparable-capability extractor from a non-Anthropic family (GPT-4, Gemini Pro) would sharpen the attribution of the 7× figure to self-preference vs capability. Retained as highest-priority future work.

**Q3 (Qwen 14B +7.5 pp).**
Added to §5.1: "The Qwen 14B +7.5 pp instruction-following contribution is the smallest of the five EXP-G models. Its equalized baseline (82.5%) is the highest of all sub-70B models, suggesting the small $\Delta$ reflects ceiling-effect compression rather than a family-specific difference in how much instruction-following adds: there is little headroom between 82.5% and the 90% instructed-matched ceiling. Llama 70B, by contrast, starts from 83.9% equalized and rises to 99% instructed-matched, giving a full +15 pp to span."

**Q4 (frontier scale).**
See W6. Sonnet 4.5 data point.

**Q5 (move EXP-K to main body).**
See DC4. Done.

---

## Candid Notes

**On ADAGE-first framing.**
The reviewer's diagnosis was correct: the pipeline earned too much prose given what it turned out to empirically add. Revision 9 restructures to lead with the regex finding. ADAGE is now introduced as a comparison baseline in the methodology, not a contribution. The correction-marker density ICC=0.114 finding further supports this reframing: the LLM feature is actually *less* reliable than the regex feature we ultimately recommend.

**On autonomous constraints.**
We agree $n=50$ per condition is thin for strong positive claims. The autonomous results are preliminary in revision 9. The sycophancy replication at Qwen 14B ($n=50$, $d=1.6$) is the strongest autonomous data point, but we present it as a transfer observation, not a frontier-deployment claim.

**On venue fit.**
We agree this is a methodological-hygiene paper rather than a technical advance. The reviewer's "methodological hygiene" framing is the one we now use internally. Our argument for NeurIPS fit rests on three concrete empirical phenomena that are not predictable from the prior literature: (1) the Qwen 32B RLHF collapse (RLHF agreeableness deleting surface-level detection signals entirely, despite 92% pre-check knowledge accuracy --- to our knowledge the first concrete demonstration on a current model); (2) the 30--41 pp accuracy collapse under prompt equalization, substantially larger than the prior sycophancy literature would predict; and (3) the frontier-scale data point (Sonnet 4.5) extending the methodology to current production models. We believe these findings are worth surfacing at NeurIPS given the community's growing investment in behavioral safety evaluations; if the reviewer's view is that the venue is still ill-fit, we would welcome a clearer pointer to an alternative venue (SafeAI workshop, ICML SafeTY track, TMLR) and would target that instead.

**On empirical-first framing.**
The contributions statement in both abstract and §1.2 has been reworded to be explicitly empirical --- "(i) a one-line label-free rule ... (ii) a decomposition of instruction-following vs knowledge-conflict signal via three reusable controls; and (iii) negative scaling and autonomy findings" --- rather than methodological. The methodological controls are the means by which the empirical findings are obtained, not the claim itself.
