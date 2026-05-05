# V34 — Response to Weak Accept 6/10 Review (New Reviewer)

**Paper:** Correction-Marker Signals Cannot Substitute for Genuine Behavioral Deception Detection: A Three-Control Evaluation of Instructed-Roleplay Detection Across Open-Weight LLMs

**Prior decision:** Weak Accept 6/10 (new reviewer, different from the 7/10 Accept reviewer addressed in V33)

**V34 changes:** Eight text-only fixes targeting the four raise-to-7 criteria and four supporting minor concerns. No new experiments.

---

## At-a-Glance Table

| Item | Reviewer ask | V34 action | Status |
|---|---|---|---|
| MC1 (headline) | "A paper shouldn't need a decision tree for its headline number." | Abstract now leads with three-control collapse (30–41 pp); primary accuracy identified as cross-family 64.7%; "How to read" paragraph updated | Done |
| MC2 (autonomous softening) | "'Does not transfer' is too strong given 2/6 cells exclude chance" | Changed to "does not transfer reliably" throughout (§1, §5.3); added multiple-testing note in §4.3 | Done |
| MC3 (adversarial reframing) | "Adversarial section reads like known limitation, not controlled finding" | Added explicit sentence in §4.3 and §5 labeling results as fragility-characterization, not robustness bound | Done |
| MC4 (methodology framing) | "Contribution oscillates between negative result and methodology paper" | Added "primary contribution is methodological: the joint three-control framework" in §1.1 | Done |
| MC5 (EXP-G caveat at §1) | "EXP-G clean band is only 14B/70B; §1 should acknowledge this" | Changed "single cleanest control" → "single cleanest control on knowledge-controlled subsets (≥14B; smaller models conflate instruction-following with knowledge transfer)" | Done |
| MC6 (Qwen 32B leaning) | "Single-model observation does significant interpretive work" | Added explicit note in §4.5: "single-model observation … should not yet support conclusion-level claims … pending camera-ready replication"; in conclusion: "pending camera-ready replication on additional RLHF-heavy models" | Done |
| MC7 (human baseline caveat-first) | "Caveat should lead rather than trail" | Swapped order in §4.9: caveat (naive crowdworkers, not upper bound on humans) now precedes result | Done |
| MC8 (multiple-testing note) | "No multiple-testing correction across 6 autonomous cells" | Added parenthetical in §4.3 autonomous partial-transfer paragraph: "no multiple-testing correction … exploratory comparisons … hypothesis-generating findings" | Done |

---

## Detailed Responses

### MC1 — Headline number / decision tree

**Reviewer:** "A paper shouldn't need a decision tree for its headline number. Commit to one primary number. The abstract leads with rule accuracy (71.8%), which is a deployment number, not the scientific claim."

**Our response:** You are correct. The scientific claim is the three-control collapse, not any individual accuracy number. We have restructured accordingly:

**Abstract:** The opening sentence now leads with the three-control collapse: "Three evaluation controls jointly applied (prompt equalization, cross-family extraction, regex baseline) collapse reported instructed-detection accuracies from 93.9–100% to 52–69% (30–41 pp): behavioral deception detection as practised is dominated by instruction-following artifacts." The rule accuracy follows as evidence of the residual signal's surface-lexical character, not as the headline finding.

**§1 "How to read":** Changed to: "The primary scientific claim is the three-control collapse: 30–41 pp drop, 9–10 pp same-family inflation, rule-vs-pipeline parity. The cross-family pipeline 64.7% is the primary accuracy estimate; 71.8% and 80.1% are deployment-regime variants (Table 1)."

We retain the decision tree (Table 1) because different downstream uses of this paper (reporting deployment performance, reporting scientific accuracy, reporting cross-family estimates) legitimately cite different numbers, and hiding this would be misleading. The tree is now framed as clarifying which regime each number corresponds to, not as a substitute for committing to the primary claim.

---

### MC2 — Autonomous transfer: "does not transfer" too strong

**Reviewer:** "With 6 cells, finding 2 above chance is not nothing. The headline 'does not transfer to fully autonomous deception' is too strong given 2/6 cells exclude chance. No multiple-testing correction is computed across cells."

**Our response:** Agreed. The V33 framing was asymmetric. We have made three changes:

1. **§1 opening paragraph:** Changed "the signal does not transfer to autonomous deception (persona or false-belief conditions at 60–66%, at or near chance)" → "the signal does not transfer reliably to autonomous deception: four of six fully-autonomous cells (persona and false-belief, n=200) have Wilson CIs including chance, and two exclude chance without a validated causal account (§4.3)."

2. **§5.3 autonomous-transfer summary:** Changed "(c) does not transfer to fully autonomous persona or false-belief ICL" → "(c) does not transfer reliably … four of six n=200 CIs include chance, and two exclude chance (Qwen 14B persona 68.0%, Mistral 7B false-belief 66.5%) without a validated causal account; the evidence is against reliable transfer, not against all transfer."

3. **§4.3 partial-transfer paragraph (MC8, new parenthetical):** Added: "(no multiple-testing correction is applied across the six autonomous cells: they are exploratory comparisons, not a confirmatory test battery; these two cells are treated as hypothesis-generating findings, not confirmatory detections)."

---

### MC3 — Adversarial reframing

**Reviewer:** "The adversarial section reads more like a known limitation than a controlled finding. Either run a closed-loop adversary or remove the deployment-ready framing."

**Our response:** The paper already says "we present the rule as a baseline … not as a production-ready classifier." We have added explicit labeling in two places:

**§4.3 adversarial closing (new sentence):** "We report these adversarial results as characterizations of the rule's lexical fragility rather than as controlled evaluations of adversarial robustness: the experiments establish the failure mode (lexical-channel suppression) but not the rate at which a motivated adversary would trigger it in practice."

**Conclusion (new sentence):** "The adversarial results characterize the failure mode (lexical-channel suppression) but are one-shot and static; they establish fragility, not a quantified adversarial robustness bound."

A closed-loop adversary is the right next experiment (Future Direction 7, §5.8). We have not run it in this revision; we have reframed the section as fragility-characterization rather than robustness evaluation.

---

### MC4 — Methodology vs. empirical contribution framing

**Reviewer:** "Contribution framing oscillates between negative result paper and methodological contribution. Commit."

**Our response:** We commit. Added to §1.1 (before the empirical findings list): "**The primary contribution is methodological: the joint three-control evaluation framework; the seven-model panel demonstrates the framework.**" This separates the framework contribution from the empirical findings that follow.

---

### MC5 — EXP-G clean band caveat at §1

**Reviewer:** "The EXP-G is the single cleanest control is walked back in §4.3 when 3B/8B/7B are noted as confounded. Clean band is only 14B/70B. Should be acknowledged at §1."

**Our response:** Correct. Changed in §1 "How to read": "the EXP-G decomposition in §4.3 is the single cleanest control" → "the EXP-G decomposition in §4.3 is the single cleanest control on knowledge-controlled subsets (≥14B; smaller models conflate instruction-following with knowledge transfer)."

---

### MC6 — Qwen 32B single-model leaning

**Reviewer:** "Table 11 shows 32B at 50%. A single-model observation is being asked to do significant interpretive work. Camera-ready commitment is appropriate but current framing leans too hard."

**Our response:** We have added explicit single-model caveats in two places:

**§4.5 Qwen paragraph:** Added: "RLHF training optimized for agreeableness eliminates all surface-level detection signals on this single model; this single-model observation at n=100 should not yet support conclusion-level claims about RLHF-trained detectors generally pending the camera-ready replication (below)."

**Conclusion:** Changed "is reported as a hypothesis-generator pending replication" → "is reported as a hypothesis-generator pending camera-ready replication on additional RLHF-heavy models."

---

### MC7 — Human baseline caveat-first

**Reviewer:** "+32 pp gap. Caveat 'trained annotators would likely score higher' is appropriate but should lead rather than trail."

**Our response:** Swapped order in §4.9. The section now reads: "Note that all three annotators were naive crowdworkers with no prior lie-detection training; the following result reflects untrained human performance and should not be read as an upper bound on human classification ability. All three annotators defaulted almost entirely to TRUTH…[result]…trained domain-expert annotators would likely score higher, narrowing the gap."

---

### MC8 — Multiple-testing note for autonomous cells

**Reviewer:** "Authors don't compute a multiple-testing correction across the 6 autonomous cells, only within-family for scale increments."

**Our response:** Added parenthetical in §4.3 at the "Partial transfer in two cells" paragraph: "(no multiple-testing correction is applied across the six autonomous cells: they are exploratory comparisons, not a confirmatory test battery; these two cells are treated as hypothesis-generating findings, not confirmatory detections)."

This is correct by design — the six autonomous cells are exploratory, and applying a Bonferroni correction across them would be overcorrection for a set of exploratory comparisons with no pre-specified confirmatory structure. The pre-registered confirmatory tests (within-family scale increments, the 4th-scenario paired bootstrap) do use corrections. We note the distinction explicitly.

---

## Responses to Open Questions

**Q1 (closed-loop adversary):** A closed-loop adversary that observes extractor scores and updates paraphrase strategy over multiple turns is the right next experiment. We have not run it in this revision. The single-iteration paraphrase result (−8 pp at Llama 3B) establishes fragility to one-shot lexical avoidance; whether the rule's failure mode compounds under iterative feedback is Future Direction 7 (§5.8). We have explicitly relabeled the adversarial results as fragility-characterization.

**Q2 (family-specific replication of partial-transfer cells):** Excellent suggestion. Qwen 7B persona and Mistral Large false-belief are the natural within-family replications for the two cells that exclude chance. We have not run these. The strengthened "does not transfer reliably" framing makes clear these two cells are hypothesis-generating; the family-specific replication is added to Future Direction 5(iii).

**Q3 (Sonnet as better extractor):** The Sonnet-on-Haiku result (65.7%, below both Mistral L3 71.7% and Llama 70B 72.7%) is inconsistent with Sonnet being a universally better extractor. If Sonnet were simply more capable than Haiku, it should outperform the non-Anthropic extractors on the Haiku target — it does not. The most parsimonious explanation remains Haiku-checkpoint-specific self-preference, not a capability story. Full interpretation is in §5.4.

**Q4 (Llama 8B outlier as noise):** The V33 cross-lingual hypothesis is post-hoc for a single-cell outlier at n=100. We have retained the hypothesis-level discussion (added in V33) but the primary explanation is n=100 noise; the cross-lingual mechanism is offered as a testable candidate for future work, not as a validated claim.

**Q5 (frontier-scale, 100B+):** Acknowledged as a real bound. All results are from models ≤70B parameters; frontier-scale (100B+) behavior is untested. A single Bedrock API cell (e.g., Llama 3.1 405B as cross-family extractor) would be feasible. We have not run this and acknowledge it as a limitation (§5.7(b)).

---

## Honest Residuals (Accepted As-Is)

**1. Qwen 14B persona qualitative coding.** The 10-trial spot-check remains deferred. The annotation protocol is written and the trials are identified; the two-coder annotation has not been completed. We accept this deferral and note the commitment in §5.8 Future Direction (5)(iii).

**2. Autonomous transfer asymmetry causally unexplained.** After two pre-registered null findings we do not have a validated causal account. The paper handles this honestly throughout (§5.3, §5.7(i)). We accept this as a real incompleteness.

**3. ADAGE is the only LLM pipeline compared.** This is the strongest version of the pipeline-redundancy claim (we are showing our own pipeline is largely redundant), so the absence of competing pipeline comparison strengthens rather than weakens the finding.

---

## Compilation

V34: 48 pages, 0 errors, 0 undefined references (pdflatex × 2).

## Spot-Check Verification

1. Abstract leads with "three-control collapse" / "30–41 pp": ✓
2. §1 "How to read" contains cross-family 64.7% as primary + EXP-G ≥14B caveat: ✓
3. §1.1 contains "primary contribution is methodological: the joint three-control evaluation framework": ✓
4. §1 autonomous sentence contains "does not transfer reliably": ✓
5. §4.3 adversarial section contains "fragility rather than … robustness": ✓
6. §4.9 human baseline leads with caveat: ✓
7. §4.3 autonomous partial-transfer paragraph contains "no multiple-testing correction": ✓
8. §5.3 "(c) does not transfer reliably" replaces "(c) does not transfer": ✓
9. `REVIEWER_RESPONSE_LETTER_V34.md` exists: ✓
