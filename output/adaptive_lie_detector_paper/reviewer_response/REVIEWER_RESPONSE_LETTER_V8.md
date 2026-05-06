# Response to Reviewer #8 (Re-review)

We thank the reviewer for the continued engagement and for raising the score to 5/10. We appreciate the explicit path to acceptance and have made targeted changes in response to M2, M3, and the minor concerns. We address each point below.

**Summary of changes:**
- Appendix cross-reference bug (m5) fixed: all `\ref{app:...}` now resolve to letter-based labels (A.1, B, C, ...) instead of "6"
- "7×" headline softened to "up to 7× feature variance across extractors (plausibly same-family self-preference, though extractor capability differences cannot be ruled out)" in §5.3 and §5.2
- Same softening in related work §2.3 ("vary by up to 7×" instead of "inflates by 7×")
- Abstract Llama scaling: consistent LaTeX escaping (57\%→57\%→76\%) and explicit framing: "the 8B→70B increment (p=0.004) is the only one surviving joint Holm-Bonferroni correction across all five within-family tests"
- Conclusion Llama scaling: "with a single statistically significant increment (8B→70B, p=0.004) under joint correction"
- Pacchiardi "confirming" → "consistent with" in §2.2
- Em-dash in §5.4 simplified: "having served its purpose as the measurement instrument through which the controls were applied" → "having served as the measurement instrument"
- Table 1 EXP-A n: "100" → "93--100"
- Deployment sentence: semicolon → period
- Adaptive controller removed from appendix TikZ figure; caption updated

---

## Major Concerns

**M1 (ICC validation study).**
We cannot coordinate a n≥100, 3-annotator study before camera-ready. We maintain the mitigations from revision 7: (a) the study is explicitly acknowledged as underpowered, (b) weak ICC is reframed as supporting the pipeline-redundancy conclusion, (c) it is listed as formal limitation (g). We commit to running the study if accepted. The paper's detection-accuracy claims (80.1% average for the refusal-count rule; 52–69% equalized range) do not depend on correction-density reliability — the regex baseline demonstrates the same signal without LLM extraction. The ICC issue is specific to the feature-level d claims in Appendix B, which are already caveated.

**M2 (7× headline tension).**
Addressed. The "7×" figure now reads "up to 7× feature variance across extractors (plausibly same-family self-preference, though extractor capability differences cannot be ruled out)" in §5.3 and §5.2, and "vary by up to 7×" in related work §2.3. The asymmetry explanation — that Claude achieves higher accuracy on all targets, not just Claude targets, suggesting extractor capability drives at least part of the gap — is preserved from revision 7. We agree the 7× number should be reported with the capability caveat; the revision does this consistently.

**M3 (Scale fragility).**
Addressed. The abstract now leads the Llama sentence with: "the 8B→70B increment (p=0.004) is the only one surviving joint Holm-Bonferroni correction across all five within-family tests." The conclusion adds: "with a single statistically significant increment (8B→70B, p=0.004) under joint correction." We agree the Llama scaling claim rests on a thin basis. The Qwen 32B collapse — complete elimination of surface-level detection signals despite 92% pre-check knowledge accuracy — remains the more practically significant and better-supported finding. We do not rely on the Llama increment as a primary contribution.

**M4 (Apollo null result under-investigated).**
We agree the format-mismatch explanation is post-hoc and a controlled experiment reformatting the AI Liar trials as factual claims would strengthen the claim. We have not run this experiment. It is noted in §4.6 as high-priority future work. The null result (0–54%) is reported as-is: "yields a null result: refusal-count markers achieve 0–54% accuracy," with the format-mismatch offered as an observation rather than a controlled finding.

**M5 (Venue fit).**
We accept the "methodological hygiene" characterization and have consistently framed it that way. We note, however, that the empirical magnitudes — 30–41 pp accuracy collapse, up to 7× extractor variance, complete signal elimination at Qwen 32B — are not predictable from the prior literature. NeurIPS has a strong tradition of accepting negative-result and measurement papers when the findings are surprising and practically significant. The Qwen 32B finding (RLHF optimization incidentally defeats surface-level detection) is, to our knowledge, the first concrete demonstration of this dynamic on a current model.

---

## Minor Concerns

**m1 (Abstract Llama rendering).** Fixed. The Llama line now uses consistent LaTeX escaping: `57\%$\to$57\%$\to$76\%` matching the Qwen line.

**m2 (≤70B repetition).** Confirmed at 2 instances (abstract and experiments §4.5 only). No further reduction needed per reviewer's acknowledgment that it is "better than previous."

**m3 (§3.2 no figure).** We have kept the lightweight methodology section without an inline controls diagram. The pipeline figure in Appendix A.10 now has the adaptive controller removed (Q6 addressed), making it a clean four-node linear diagram. Adding an inline §3.2 diagram would require additional space and is not essential for reader comprehension given the three controls are described in prose.

**m4 (Table 1 EXP-A n).** Changed from "100" to "93--100" to reflect per-model variation.

**m5 (Appendix "6" bug).** Fixed. All `\label{app:...}` commands now resolve to letter-based labels. The fix: converted `\subsection*{A.1\quad ...}` to numbered `\subsection{...}` under the `\appendix` command (already present in main.tex). B–K groups are now separate `\section{}` entries auto-lettered B through K. Verified in compiled aux file: `app:pipeline_details` → A.10, `app:instructed_results` → B, `app:validation_tests` → F, etc.

**m6 (Deployment sentence).** Fixed. Semicolon changed to period: "...has not been tested against adversarial paraphrase or stylistic variation. Deployment should include domain-specific validation."

**m7 (Em-dash in §5.4).** Simplified: "having served its purpose as the measurement instrument through which the controls were applied" → "having served as the measurement instrument."

**m8 (Pacchiardi "confirming").** Changed to "consistent with the detection signal residing primarily in the target's first response."

---

## Questions

**Q1 (Can you run the ICC study now?)**
No. External annotator coordination requires time we do not have before camera-ready. Commitment to run it if accepted stands.

**Q2 (GPT-4o/Gemini as cross-family extractor?)**
Not available to us as a structured feature extractor. The existing three-family comparison (Claude, Mistral Large, Qwen) establishes the phenomenon; a comparable-capability extractor would sharpen the attribution. Noted as highest-priority future work.

**Q3 (Is the 7× claim valid given the capability confound?)**
The 7× figure is now reported as "variance" rather than "inflation" and explicitly caveated with the capability-difference explanation in both §5.2 and §5.3. We believe the number remains informative: practitioners relying on same-family extraction should know the 7× variance bound regardless of whether it reflects self-preference or capability.

**Q4 (Is the Llama scaling claim worth reporting?)**
Yes, with appropriate hedging, which revision 8 provides. A single surviving increment (8B→70B, p=0.004 under joint correction) is weak but not uninformative — it is consistent with the non-monotonic, family-specific pattern we identify. The Qwen within-family results (U-shape, 32B collapse) are the more compelling scaling story.

**Q5 (Why not drop the autonomous section entirely?)**
The autonomous section, framed as a negative result, serves a methodological purpose: it answers the natural question of whether the equalized signal transfers. The answer (it does not, except for instruction-driven sycophancy) is informative for the community. We believe the section earns its space as a negative result rather than as a positive contribution.

**Q6 (Remove adaptive controller from figure?)**
Done. The appendix figure now shows the four-node linear pipeline (Target Model → Interrogator → Feature Extractor → Classifier) with the adaptive controller and red feedback loop removed. Caption updated accordingly.
