# Response to Reviewer #4

We thank the reviewer for their thorough and constructive evaluation. The explicit path to improvement was invaluable—we have addressed all ten weaknesses, five detailed comments, and five questions. Below we map each concern to specific changes.

---

## Weaknesses

### W1: Framing unclear (methods vs empirical vs negative-results)

**Response:** We have committed to the empirical framing throughout. The abstract opens with "We demonstrate that behavioral deception detection primarily detects instruction-following artifacts" (line 2). The methodology section (§3) explicitly states: "The primary methodological contribution is three evaluation controls... The ADAGE pipeline serves as the measurement apparatus" (§3.1). The discussion's §5.3 ("Technical Contribution and Novelty") directly addresses this: "The contribution of ADAGE is not an algorithmic advance... but a methodology for controlling instruction-following confounds" (§5.3, line 65). We believe the paper is now consistently framed as an empirical study that establishes what behavioral detection does and does not measure.

### W2: ICC=0.114 construct validity "near-zero"

**Response:** We agree this is a genuine limitation. Three changes address it:

1. The introduction now leads with the regex baseline (Finding #2: refusal count ≥1 at 80.1%) before the LLM pipeline, establishing that the positive finding does not depend on the weak-ICC feature.
2. Finding #3 explicitly states: "The LLM pipeline's primary feature (correction-marker density) has weak construct validity (ICC=0.114), but the regex baseline demonstrates the signal is robust and surface-level."
3. The discussion (§5.4) acknowledges the ICC reflects "a large scale discrepancy between annotators (means 1.10 vs. 3.95), not rank disagreement (ρ=0.62, p<0.01)," while noting that the LOO classifier operates on rank ordering.

The paper's central claims—both the negative finding (instruction-following dominates) and the positive finding (scale-dependent knowledge-conflict signal)—are supported by the regex baseline independently of any LLM-extracted feature.

### W3: Scaling claims weaker than prose (numerical inconsistency)

**Response:** The reviewer correctly identified that two different metrics were used interchangeably:
- **57%→57%→76%** = refusal-count-only LOO (from §4.8.1, Table 6)
- **61%→65%→84%** = 5-feature LLM pipeline LOO (from §4.8, line 269)

Every occurrence is now labeled with its metric. Specifically:
- Abstract line 9: "(refusal-count LOO)" with "the 5-feature LLM pipeline shows a parallel trend (61%→65%→84%)"
- Introduction Finding #6: "refusal-count LOO: 57%→57%→76%"
- Conclusion paragraph 3: Both metrics explicitly labeled with cross-reference
- Experiments §4.8 (line 269): "(5-feature LLM pipeline)" label added, with parenthetical cross-referencing the refusal-count numbers

The dangling white-box reference in the conclusion ("White-box probing comparison on Mistral 7B...") has been deleted—§4.9 was removed in the prior revision and this reference was inadvertently left behind. The orphaned files `whitebox_draft.tex` and `whitebox_section.tex` have also been deleted.

### W4: +7.5–31pp conflates instruction-following with knowledge transfer

**Response:** All occurrences now distinguish clean from confounded numbers:
- Abstract line 4: "+7.5–15pp on knowledge-controlled subsets (14B/70B), up to +31pp upper bound including knowledge-transfer effects on smaller models (3B/8B/7B)"
- Introduction Finding #1: Same decomposition
- Conclusion paragraph 1: "+7.5–15pp on knowledge-controlled subsets (14B/70B)"
- Discussion §5.1: Compressed to "instruction-following contributes +7.5–15pp on knowledge-controlled subsets (14B/70B), up to +31pp including knowledge-transfer effects on smaller models"
- Experiments §4.8 (line 389): "The 3B/8B numbers should be interpreted as upper bounds on pure instruction-following"

The knowledge-transfer confound paragraph (§5.1) remains in the discussion, and the knowledge pre-check stratification (§4.8, Table 8) provides the empirical control confirming instruction-following dominates even when knowledge is controlled.

### W5: Autonomous claims overclaimed (sycophancy = still instruction-following)

**Response:** We now explicitly position sycophancy as **semi-autonomous** throughout:
- Abstract line 11: "fails to generalize to fully autonomous deception: persona maintenance (66%) and ICL false beliefs (60%) barely exceed chance"
- Introduction line 17: "transfers to semi-autonomous settings (system-prompt-induced sycophancy at 82%) but fails to generalize to fully autonomous deception (persona 66%, false beliefs 60%, both near chance with wide CIs)"
- Discussion §5.1: "can transfer to semi-autonomous settings when the epistemic conflict is well-structured, though the 60–66% results on other designs indicate this transfer is not universal and fully autonomous deception remains out of reach for current behavioral methods"

We agree with the reviewer that sycophancy is system-prompt-induced rather than spontaneous strategic deception, and the text now reflects this.

### W6: Same-family bias claim rests on 1.5/3 evidence

**Response:** The claim has been softened in all locations:
- Introduction Finding #4: "same-family bias is observed only in Claude among three families tested, though whether this reflects Claude-specific RLHF self-preference or capability-masked bias remains open"
- Discussion §5.2: Changed from "Claude-specific phenomenon" to "observed only in Claude among the three families tested; whether this reflects Claude-specific RLHF self-preference or capability-masked bias in Mistral/Qwen remains open"

We acknowledge the Mistral result is ambiguous (bias may be masked by lower capability).

### W7: n≈100 gives wide CIs

**Response:** We report bootstrap 95% CIs for all equalized results (e.g., 70B: [76.3%, 91.4%]; 14B: [74.2%, 89.7%]). The paper's claims rest on the pooled group comparison (≤7B vs. ≥14B, p < 0.0001) and within-family trends validated across two families, not on individual pairwise comparisons. We explicitly note that "no individual adjacent increment is significant after Holm-Bonferroni correction" (§4.8, line 415). This is a fundamental limitation of the n≈100 design that we accept and report transparently.

### W8: No data beyond 70B

**Response:** Added explicit limitation in three locations:
- Abstract line 9: "all scaling claims are limited to ≤70B; frontier-scale behavior remains untested"
- Conclusion paragraph 3: "All scaling claims are limited to ≤70B; frontier-scale (100B+) behavior remains untested"
- Introduction Finding #6: "all scaling claims are limited to ≤70B"
- Discussion §5.5 (limitations): "Frontier-scale models (100B+) remain the gap"

### W9: Presentation too dense/repetitive

**Response:** Four compression changes:
1. **Introduction §1.3**: Compressed from 8 enumerated findings to 6, with forward section references instead of full numerical detail (~15 lines saved)
2. **Conclusion**: Fully rewritten from ~12 dense lines to 4 clean paragraphs, each with distinct focus (main finding → deployment rule → scale patterns → future work)
3. **Discussion §5.1**: Replaced full 5-model decomposition numbers with summary + section reference: "instruction-following contributes +7.5–15pp on knowledge-controlled subsets (14B/70B), up to +31pp including knowledge-transfer effects on smaller models. Full per-model decompositions are in Section 4.8"
4. **Discussion §5.5 (Future Direction 5)**: Compressed from ~12 lines to 4 lines with section cross-references

Total page reduction: 54 → 53 pages (1 page saved). Further compression is limited by the dense experimental content.

### W10: Mock validation takes too much space

**Response:** Mock validation (§4.2) is already compressed to ~5 lines. The detailed mock analyses are in the appendix (Appendix B–E). We have verified that the main text does not over-elaborate on mock results.

---

## Detailed Comments

### DC1: Abstract "93–100%" should clarify LOO-recalibrated

**Done.** Abstract line 4: "93–100% LOO-recalibrated accuracy"

### DC2: Pacchiardi claim "supports our hypothesis" too strong

**Done.** Changed to "raises the possibility that" in related_work.tex line 13.

### DC3: Figure 1 caption insufficient

**Done.** (Addressed in prior revision.) Figure 1 caption expanded from 1 to 4 sentences, describing all three components and the adaptive stopping mechanism.

### DC4: "Monotonically" contradicts non-monotonic findings

**Done.** Changed "improves monotonically across seven models" to "generally increases across seven models... though no individual adjacent increment is significant after Holm-Bonferroni correction" (experiments.tex line 269).

### DC5: Code availability not mentioned

**Done.** Added "All code and data are available in the supplementary material" in introduction.tex line 40.

---

## Questions

### Q1: Llama 57→76 vs 61→84 — which is correct?

Both are correct but measure different things. 57%→57%→76% is **refusal-count-only LOO** (a single regex feature); 61%→65%→84% is **5-feature LLM pipeline LOO** (logistic regression on all five behavioral features). Both are now clearly labeled at every occurrence with cross-references. See §4.8 line 269 and §4.8.1 Table 7.

### Q2: White-box in conclusion — where is the experiment?

The white-box comparison section (§4.9) was removed in a prior revision based on reviewer feedback, but a reference was inadvertently left in the conclusion. This dangling reference has now been deleted. The orphaned source files have also been removed.

### Q3: EXP-G on 3/5 models — why not all?

Knowledge pre-check stratification (EXP-G, Table 8) was initially run on 3 models (3B, 8B, Mistral 7B). Qwen 14B and Llama 70B were added later in the study; their near-perfect knowledge pre-check accuracy (>95% correct) already demonstrates that the +7.5–15pp instruction-following contributions at these scales are minimally contaminated by knowledge transfer, making the stratification confirmatory rather than revelatory. This is noted in §4.8 line 397.

### Q4: 100B+ model?

We acknowledge this limitation explicitly. All scaling claims are now qualified with "≤70B" in abstract, conclusion, and limitations. Frontier-scale behavior remains the most important open question.

### Q5: Qwen 32B transcripts — model knows but suppresses?

**Done.** Added to §4.8.1: "Manual inspection confirms that Qwen 32B knows the claims are false (a direct knowledge pre-check yields correct answers on 92% of claims) but suppresses correction language entirely." This confirms the RLHF agreeableness interpretation: the model retains factual knowledge but its training eliminates the surface-level behavioral signals that detection methods rely on.

---

## Summary of Changes

| Change | Files Modified | Reviewer Concern |
|--------|---------------|------------------|
| Label all Llama metric occurrences | abstract, intro, conclusion, experiments | W3, Q1 |
| Delete dangling white-box reference | conclusion | W3, Q2 |
| Decompose +7.5–31pp range | abstract, intro, conclusion, discussion | W4 |
| Position sycophancy as semi-autonomous | abstract, intro, discussion | W5 |
| Soften same-family bias claim | intro, discussion | W6 |
| Add ≤70B limitation | abstract, intro, conclusion | W8 |
| Compress §1.3, conclusion, discussion | intro, conclusion, discussion | W9 |
| Remove "monotonically" | experiments | DC4 |
| Soften Pacchiardi claim | related_work | DC2 |
| Add code availability | intro | DC5 |
| Add LOO-recalibrated qualifier | abstract | DC1 |
| EXP-G 3/5 explanation | experiments | Q3 |
| Qwen 32B transcript confirmation | experiments, qwen_scale_section | Q5 |
| Delete orphaned whitebox files | sections/ | W3 |
| Compress future direction (5) | discussion | W9 |
