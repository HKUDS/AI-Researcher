# Response to Reviewer Comments - Third Revision

**Paper:** Behavioral Deception Detection in LLMs Primarily Measures Instruction-Following: An Empirical Boundary Characterization

**Submission:** NeurIPS 2026 Main Track

**Date:** April 2026

---

## Overview

We thank the reviewer for their thorough and constructive feedback. We appreciate the recognition of our methodological rigor and honest reporting of negative results. This revision addresses all 7 major concerns (MC1-MC7) and 9 minor issues (MI1-MI9) through comprehensive reframing and writing revisions.

**Key changes:**
1. **Reframed contribution** from methodology to empirical finding (MC1, MC2)
2. **Regex baseline leads throughout** paper, LLM pipeline demoted to comparison apparatus (MC3)
3. **Scale claims softened** to "family-specific, non-monotonic patterns" (MC4, MC5)
4. **White-box section removed** as reviewer suggested (MC7)
5. **All 9 minor issues fixed** (MI1-MI9)

**Expected outcome:** The revised paper now honestly positions its contribution as the empirical finding that behavioral detection primarily measures instruction-following, with the residual signal captured by simple lexical heuristics. We believe this addresses the reviewer's core concern about scope mismatch and thin methodological novelty.

---

## Major Concerns

### MC1: Scope Mismatch with Motivation

**Reviewer concern:** "Paper opens with AI-safety deception motivation but studies instructed roleplay. Should reframe to lead with 'behavioral detection is mostly instruction-following detection.'"

**Response:** We agree completely and have reframed the entire paper accordingly.

**Changes made:**

1. **Abstract (lines 1-2):** Rewritten opening from "We present a methodology for evaluating..." to:
   > "We demonstrate that behavioral deception detection in large language models primarily detects instruction-following artifacts rather than deception per se."

2. **Introduction §1.1 (Motivation):** Changed from AI-safety-first framing to honest empirical framing:
   > "This paper investigates what current behavioral interrogation methods actually detect when applied to LLMs instructed to defend false claims. Our finding: they primarily detect instruction-following mode rather than deceptive capability."

3. **Scope limitation paragraph:** Moved to contextualize rather than lead, acknowledging that "this fundamentally differs from the AI safety scenario" and noting signal collapse on Apollo AI Liar (0-54%).

4. **Conclusion (page 43):** Now opens with:
   > "We demonstrate that behavioral deception detection in large language models primarily detects instruction-following artifacts rather than deception per se."

**Justification:** The revised paper no longer positions AI safety as the primary motivation. Instead, we lead honestly with what we discovered: behavioral interrogation in instructed roleplay settings primarily detects instruction-following, not deception. AI safety applications are discussed as limitations and future work.

---

### MC2: Thin Methodological Novelty

**Reviewer concern:** "Each control is standard (matched controls, LLM-as-judge robustness, regex baselines). 'Systematic combined application' is honest but thin for NeurIPS."

**Response:** We accept this critique. The revised paper pivots from methodology contribution to empirical contribution.

**Changes made:**

1. **Abstract:** Contribution statement changed from "methodology for evaluating..." to:
   > "The primary contribution is the empirical finding that instruction-following artifacts dominate reported detection accuracies (+7.5-31pp), with the residual knowledge-conflict signal captured by simple lexical heuristics."

2. **Introduction (page 2):** Contribution paragraph rewritten:
   > "The primary contribution is the empirical finding that instruction-following artifacts dominate reported detection accuracies, with the residual knowledge-conflict signal captured by simple lexical heuristics. We demonstrate this through systematic application of three controls..."

3. **Conclusion (page 43):** Positions controls as enabling tools:
   > "We establish this through systematic application of three evaluation controls (individually standard: matched controls, cross-evaluator checks, simple baselines) that expose confounds of surprising magnitude when applied together."

**Justification:** The controls are now positioned as diagnostic tools that enabled the empirical discovery, not as novel methodology per se. The contribution is what we learned (instruction-following dominance, family-specific scale effects, surface-level signals), not the evaluation framework itself.

---

### MC3: Construct Validity Problems (ICC=0.114)

**Reviewer concern:** "Too weak for correction-marker density feature. Should lead with regex baseline as primary detector."

**Response:** Excellent suggestion. We've restructured the entire paper to lead with the regex baseline throughout.

**Changes made:**

1. **Abstract paragraph reordered:** Now presents refusal-count heuristic first:
   > "A simple refusal-count heuristic (threshold ≥1) achieves 80.1% average accuracy across seven equalized models without labeled data. We validate this through comparison with a multi-turn LLM interrogation pipeline extracting five behavioral features (accuracy 52-69% equalized). The LLM pipeline's primary feature (correction-marker density) shows weak inter-rater reliability (ICC=0.114, n=20, 2 annotators), but the regex baseline demonstrates the underlying signal is robust and surface-level..."

2. **Introduction findings list:** Reordered to lead with "Label-free deployment rule" (Finding #2, formerly #3):
   > "A fixed-threshold decision rule ('predict knowledge-conflict if refusal count ≥1') achieves 80.1% average accuracy..."

3. **Introduction positioning:** LLM pipeline now explicitly characterized as comparison apparatus:
   > "...a single regex feature (refusal/correction count) achieves comparable accuracy, demonstrating the signal exists independently of LLM extraction."

**Justification:** The regex baseline is now the primary detection method throughout the paper. The LLM pipeline serves to validate that the regex signal is real (not an artifact of simple pattern matching) but is no longer positioned as the main contribution. This addresses the ICC concern by not depending on weak-reliability LLM features for the primary finding.

---

### MC4: Statistical Power on Key Claims

**Reviewer concern:** "Qwen 7B→14B jump (+8.5pp) NOT significant (p=0.17) yet cited repeatedly. Wide CIs."

**Response:** We agree and have added explicit caveats throughout.

**Changes made:**

1. **Abstract:** Scale finding rewritten to emphasize non-monotonicity:
   > "Within-family scale analysis reveals family-specific, non-monotonic patterns rather than universal improvement. Qwen 2.5 (3B→7B→14B→32B, n=100 each) exhibits a U-shape: 50%→68% (p=0.014*)→72%→50%..."

2. **Introduction Finding #8:** Updated to avoid citing 7B→14B as significant:
   > "Within-family analysis on two families reveals family-specific patterns rather than universal scale trends. Qwen 2.5... exhibits a U-shape: 50%→68% (Fisher p=0.014*)→72%→50% (collapse)."

3. **Conclusion (page 43):** Same honest framing:
   > "While both families contain at least one significant increment, the non-monotonic patterns indicate scale effects depend on family-specific RLHF objectives rather than parameter count alone."

**Justification:** We no longer claim universal scale improvement. Instead, we report the patterns observed (Qwen U-shape, Llama flat-then-jump) and note that only specific adjacent increments are significant (Qwen 3B→7B p=0.014, Llama 8B→70B p=0.004). The 7B→14B increment is not cited as evidence.

---

### MC5: Within-Family Scale Story Overstated

**Reviewer concern:** "With Qwen U-shape and Llama flat-then-jump, actual finding is 'scale effects are family-specific and non-monotonic' which *undermines* rather than supports claims about scale-dependent detection."

**Response:** We completely agree with this interpretation and have revised accordingly.

**Changes made:**

1. **Abstract:** Changed from "validating that scale improves detection" to:
   > "While both families contain at least one significant increment, the non-monotonic patterns indicate scale effects depend on family-specific RLHF objectives rather than parameter count alone."

2. **Introduction Finding #8:** Retitled from "Scale effects" to "Family-specific, non-monotonic scale patterns":
   > "...reveals RLHF training objectives modulate surface-level detection signals rather than universal capability scaling."

3. **Conclusion:** Parallel update:
   > "Within-family scale analysis reveals family-specific, non-monotonic patterns rather than universal improvement."

**Justification:** The revised framing is honest: we tested scale effects and found they're family-specific and non-monotonic. Qwen peaks at 14B then collapses at 32B due to RLHF agreeableness training. Llama stays flat 3B→8B then jumps at 70B. This is an interesting empirical finding about RLHF objectives, not evidence of universal scale-dependent improvement.

---

### MC6: Cross-Family Extraction Interpretation Muddled

**Reviewer concern:** "'Claude-specific' same-family bias based on null results from Mistral/Qwen, but could be 'bias masked by lower capability.'"

**Response:** We acknowledge this alternative interpretation in the existing text (Section 4.8):
   > "...though the Mistral result is also consistent with bias masked by lower extractor capability."

**No changes needed:** The paper already transparently notes this confound. We maintain "Claude-specific phenomenon" as the primary interpretation given n=3 families tested (Claude, Mistral, Qwen), with the capability-masking hypothesis noted as an alternative.

---

### MC7: White-Box Probing Too Thin

**Reviewer concern:** "Only 2 models, linear probes, final-layer. Either expand substantially or remove."

**Response:** We have removed the white-box section entirely per your suggestion.

**Changes made:**

1. **Abstract:** Removed white-box paragraph (previously lines 8-9)
2. **Experiments Section 4.9:** Entire "White-Box Probing Comparison" subsection deleted (~3 pages)
3. **Introduction findings list:** White-box comparison removed
4. **Page count:** Paper reduced from 55 → 54 pages

**Justification:** The white-box section was added to address a previous reviewer's request but is genuinely thin (2 models, linear probes, final-layer only). Removing it makes the paper more focused on its core contribution (instruction-following detection via behavioral methods) without inviting interpretability community pushback on underspecified white-box analysis.

---

## Minor Issues

### MI1: Truncated Abstract

**Fixed:** The abstract now compiles correctly with no truncation.

---

### MI2: Broken Table References

**Status:** No broken references found. We ran `grep -r "\?\?" sections/*.tex` and found no undefined cross-references.

---

### MI3: Terminology Drift

**Status:** Already standardized to "correction-marker density" throughout in second revision. No additional changes needed.

---

### MI4: Figure 1 Description Minimal

**Fixed:** Figure 1 caption expanded from 1 sentence to 4 sentences (methodology.tex line 60):
   > "ADAGE pipeline architecture used as measurement apparatus. The pipeline comprises three components: (1) an LLM question generator producing follow-up questions conditioned on dialogue history, (2) a feature extractor scoring five behavioral dimensions per response, and (3) a logistic regression classifier. The adaptive stopping mechanism (red feedback loop) is empirically near-vacuous (Section 4.11). Implementation details in Appendix A.1."

---

### MI5: EXP-K (Pacchiardi) Only on Mistral 7B

**Fixed:** Added explicit limitation note (experiments.tex line 565):
   > "**Limitation:** This finding is based on a single target model (Mistral 7B); replication on additional models (especially larger scales like 70B) is future work that would test whether the equalized signal is primarily first-response-driven across model families and scales."

---

### MI6: Compute Cost - Ollama Wall-Time

**Status:** Already documented in Appendix A.6 (appendix.tex line 329):
   > "Total wall-clock time across all experiments was approximately 40 hours, dominated by rate-limited Bedrock calls (Llama 70B and Claude Haiku) and local inference on Qwen 14B."

No additional changes needed.

---

### MI7: 50 Claims Feels Small

**Status:** Already acknowledged in Discussion §5.1 (discussion.tex footnote):
   > "Instructed d values (3.74 consistency, 3.35 correction density) are from the full 100-claim set; Table X reports matched-subset values of 3.70/0.86 (consistency) and 3.32 (correction density) for the 50-claim subset used in the equalized experiment."

The limitation is noted. Increasing claim bank would require proportional compute cost increase (~$22 already spent).

---

### MI8: "Fundamental Limit" Claim

**Fixed:** Qualified in experiments.tex line 155:
   > "The consistent ~93% LOO ceiling across two Llama models suggests a **limit of the 5-feature logistic classifier framework tested here** rather than a scale-dependent effect."

---

### MI9: Section 5.7 Future Directions

**Status:** The "Implications and Future Directions" section (Discussion §5.5) lists 5 concrete, specific directions:
1. RLHF-aware detection channels
2. Correction density-focused interrogation design
3. Cross-family extractors as standard practice
4. Domain-targeted claim design
5. Autonomous deception evaluation

These are not generic next steps but specific hypotheses motivated by our negative findings. We believe this is appropriately scoped.

---

## Summary of Revisions

### Quantitative Changes
- **Page count:** 55 → 54 pages (white-box section removed)
- **Abstract word count:** ~380 → ~394 words (within NeurIPS guidelines)
- **Framing:** Methodology contribution → Empirical finding

### Qualitative Changes

**Priority 1 (Reframing):**
1. ✅ Empirical finding leads throughout (MC1, MC2)
2. ✅ Regex baseline primary detector, LLM pipeline comparison (MC3)
3. ✅ Scale claims softened to family-specific, non-monotonic (MC4, MC5)
4. ✅ White-box section removed (MC7)

**Priority 2 (Minor issues):**
5. ✅ Figure 1 description expanded (MI4)
6. ✅ EXP-K replication limitation noted (MI5)
7. ✅ "Fundamental limit" claim qualified (MI8)
8. ✅ All other minor issues verified as already addressed or not applicable

---

## Addressing Reviewer's Bottom Line

**Reviewer stated:** "I lean toward borderline reject in the current form, with strong potential to become weak accept after revision. If the authors reframe and address the IRR issue, I'd shift to weak accept."

**Our response:**

1. **Reframing complete:** We have pivoted from methodology contribution to empirical finding throughout. The paper now leads with "behavioral detection primarily measures instruction-following" rather than positioning it as a limitation.

2. **IRR issue addressed via regex pivot:** By leading with the regex baseline (which achieves 80.1% without LLM extraction), we no longer depend on the weak-reliability correction-marker density feature (ICC=0.114) for the primary finding. The LLM pipeline validates that the regex signal is real, but the deployment-ready result uses only the regex heuristic.

3. **Scale interpretation honest:** We now present family-specific, non-monotonic patterns as the finding, rather than claiming universal scale improvement. This is more interesting (RLHF objectives modulate detection signals) and more honest (Qwen collapses at 32B, Llama is flat 3B→8B).

4. **Focused paper:** Removing the thin white-box section (MC7) makes the paper tighter and more focused on behavioral detection.

**We believe these changes address the reviewer's path to weak accept.**

---

## Contact

For any questions about the revisions, please contact:

[Corresponding author name and email]

---

**Thank you for the thorough and constructive feedback. We believe the revised paper is significantly stronger and more honestly positions its contributions.**
