# V36 — Response to New Weak Accept 6/10 Review

**Paper:** Correction-Marker Signals Cannot Substitute for Genuine Behavioral Deception Detection: A Three-Control Evaluation of Instructed-Roleplay Detection Across Open-Weight LLMs

**Prior decision:** New reviewer, Weak Accept 6/10 (different reviewer from V34/V35)

**V36 changes:** Eight text-only fixes addressing five raise-to-7 criteria (R1–R5) and three minor requests (M1–M3). No new experiments.

---

## At-a-Glance Table

| Item | Reviewer concern | V36 action | Status |
|---|---|---|---|
| R1 (C4) | §5.1 title "ICC=0.114 Caveat" contradicts validated α=0.606; reader "whiplashed" | Renamed §5.1 to "Construct Validity: Validated at α=0.606"; restructured opening to lead with validation, ICC=0.114 as historical context | Done |
| R2 (C6) | Qwen 32B adversarial-fine-tuning speculation unsupported at n=1 even with disclaimer | Removed the "Speculation, not evidence:" sentence entirely; RLHF-collapse finding stands on its own | Done |
| R3 (C7) | "+9–10 pp same-family gap" lacks a formal test | Added sign test sentence in §4.7: all 8 per-target Haiku-minus-cross-family gaps are positive; sign test p=0.0078 | Done |
| R4 (C2) | Multiple-testing admission for autonomous cells could be more direct | Extended §4.3 parenthetical: "under Bonferroni correction (α/6=0.008), neither of the two cells that exclude chance survives"; added parallel statement in §5.3 summary | Done |
| R5 (C5) | Semi-autonomous label for sycophancy contested; adversarial reading is coherent | Added explicit acknowledgment in §5.3 summary: "that reading is coherent, and we acknowledge it" with pointer to §4.8 detailed defense | Done |
| M1 (M2) | §4.7 re-explains Table 1 headline disambiguation | Replaced "The headline for behavioral-detection accuracy is therefore not a single number but several: [list]" with single pointer to Table 1 | Done |
| M2 (M9) | Apollo AI Liar pilot adds citation without scientific work | Removed the `\paragraph{Apollo AI Liar pilot}` paragraph entirely | Done |
| M3 (M7) | Footnote in §4.6 (K=1 inconsistency explanation) interrupts prose | Replaced ~50-word footnote with "mechanism detailed in §4.8" inline pointer | Done |

---

## Detailed Responses

### R1 (C4) — Construct Validity Narrative: No More Whiplash

**Reviewer:** "§5.1's subsection title is 'Construct Validity and the ICC=0.114 Caveat.' But §5.1 then reports α=0.606 clearing the threshold. The title front-loads the bad news even though the finding is good news. The reader is whiplashed."

**Our response:** Agreed. The section title was written when ICC=0.114 was the current state; it was never updated after the validation study completed. We have made two changes:

**Title:** `\subsection{Construct Validity and the ICC=0.114 Caveat}` → `\subsection{Construct Validity: Validated at $\alpha=0.606$}`  
(Labels `\label{sec:icc_caveat}` and `\label{sec:icc_owned}` unchanged for cross-references.)

**Opening paragraph restructured:** Now leads with the validated result: "The primary LLM-extracted feature (correction-marker density) **is validated**: the full n=100/3-annotator study yields Krippendorff's α=0.606, ICC(2,1)=0.647 (Appendix B), clearing the pre-registered α≥0.4 threshold; level-dependent claims are confirmed." The ICC=0.114 pilot is now framed as "a real weakness we committed to resolving; we report it as historical context that motivated the full study, not as the current validity status."

---

### R2 (C6) — Remove Adversarial Fine-Tuning Speculation

**Reviewer:** "The Qwen 32B n=1 observation is already appropriately caveated. But the additional speculation that 'adversarial fine-tuning could plausibly do so deliberately' is unsupported even with the 'Speculation, not evidence:' label. n=1 is not a sound basis for deployment threat reasoning."

**Our response:** Agreed. The speculation sentence is removed entirely:

**Removed:** "Speculation, not evidence: if standard RLHF can incidentally eliminate surface-level detection signals, adversarial fine-tuning could plausibly do so deliberately, and behavioral detection relying on surface markers would be vulnerable to that failure mode. Confirming or ruling out this speculation would require running equivalent evaluations on at least two additional RLHF-heavy models at ≥14B scale."

The RLHF-collapse finding (n=100 zero-marker result, 50% rule accuracy, 14B→32B collapse −22 pp) is the scientific contribution; it does not need the speculative implication. The camera-ready commitment to replicate on additional RLHF-heavy models remains.

---

### R3 (C7) — Formal Test for +9–10 pp Same-Family Gap

**Reviewer:** "The +9–10 pp Claude-on-Claude same-family inflation is a central numerical claim. The paper would benefit from at least one formal test — e.g., a permutation test on the per-target Haiku-minus-mean-of-non-Anthropic gap across 8 targets."

**Our response:** We added a sign test in §4.7, immediately after listing the 8 per-target gaps. The computation uses values already in Table 13 — no new data:

**Added sentence in §4.7:** "A sign test on the 8 per-target gaps confirms the directional result: all 8 are positive (sign test p=0.0078, two-sided; mean +9.4 pp, range +0.5 to +15.7 pp); Llama 8B is the only near-zero case and does not flip the direction."

**Computation:**
- Per-target Haiku-minus-cross-family (avg of Mistral L3 and Llama 70B) gaps from Table 13:
  +10.0 (Llama 3B), +0.5 (Llama 8B), +8.0 (Mistral 7B), +7.5 (Qwen 7B), +11.9 (Qwen 14B), +12.4 (Llama 70B), +10.6 (Haiku), +15.7 (Qwen 32B)
- All 8 positive → sign test p = 2 × (1/2)^8 = 2/256 = **0.0078**

The sign test is appropriate here: it is direction-only (makes no assumption about distribution of gap magnitudes) and controls for the Llama 8B near-zero case explicitly. The reviewer's suggestion of a permutation test would produce a similar conclusion but requires specifying a test statistic; the sign test is cleaner and makes the same directional argument.

---

### R4 (C2) — Strengthened Multiple-Testing Admission for Autonomous Cells

**Reviewer:** "The honest framing ('unexplained partial-transfer findings') is appreciated, but the paper's narrative would survive admitting more directly that under a multiple-testing correction, the two 'exclude chance' cells would not survive."

**Our response:** We have added the explicit Bonferroni statement in two places:

**§4.3 (extended existing parenthetical):** Added "; under Bonferroni correction (α/6=0.008), neither of the two cells that exclude chance under the uncorrected test would survive; these two cells are treated as hypothesis-generating findings, not confirmatory detections."

**§5.3 discussion summary:** Added after "the evidence is against reliable transfer, not against all transfer.": "Under a conservative Bonferroni correction across the six autonomous cells (α/6=0.008), neither of the two exclude-chance cells (Qwen 14B persona 68.0%, Mistral 7B false-belief 66.5%) survives; these cells are hypothesis-generating, not confirmatory."

The paper's negative-transfer claim is unaffected by this addition: the claim rests on four of six cells including chance at n=200 across three independent families, which is conservative on its own. The Bonferroni admission makes explicit that even the two cells that nominally exclude chance are not statistically privileged.

---

### R5 (C5) — Contested Semi-Autonomous Label Acknowledged

**Reviewer:** "The semi-autonomous label is contested. Adversarial readers will see sycophancy as 'instructed deception with one extra step.' The defense relies on (i) target behavior being agreement, not deception, and (ii) parallel to deceptive-alignment literature. The first is reasonable; the second is rhetorical. This deserves a sharper acknowledgment that the semi-autonomous label is contested."

**Our response:** We have added an explicit acknowledgment in §5.3, immediately after the passage about sycophancy transfer:

**Added sentence:** "The semi-autonomous label for sycophancy is acknowledged as contested: readers who treat it as instructed deception with one extra step will read the 68.5–83% results as an additional instructed-deception data point (detailed defense in §4.8)."

The §4.8 section already contains a full paragraph ("Sycophancy vs. instructed: qualitative difference in kind") that distinguishes the two mechanisms at the level of refusal-count signal direction and explains why the semi-autonomous framing is defensible. The §5.3 addition makes clear that we know this reading exists and do not dismiss it.

---

### Response to Open Questions

**Q1 (non-monotonic sycophancy scale: 68.5% / 83% / 72% at 3B/14B/70B).**

The apparent non-monotonicity has a straightforward explanation. The 70B result is n=50, not n=200: Wilson CI for 72% at n=50 is [58–84%], which overlaps the Qwen 14B 83% CI [77–88%]. The difference between 70B (72%) and 14B (83%) is not statistically distinguishable at these sample sizes. Only the 3B vs. 14B comparison is at n=200 with d=1.00 vs. d=1.52; that comparison is real and reflects the known pattern that Qwen 14B shows stronger behavioral separation than Llama 3B on most tasks. The 70B value is a preliminary single-family estimate; we have not scaled up to n=200 for 70B sycophancy.

**Q2 (within-family-different-checkpoint extractor).**

This is already done. The five self-family controls include:
- Llama 70B on Llama 3B/8B (within-family, different scale) — no self-boost
- Llama 8B on Llama 8B (same checkpoint) — no self-boost
- Qwen 14B on Qwen 7B (within-family) — no self-boost
- **Sonnet 4.5 on Haiku (within-Anthropic, different checkpoint)** — 65.7%, below both non-Anthropic extractors (71.7%/72.7%)

The Sonnet-on-Haiku control is exactly the "within-family-different-checkpoint" design the reviewer requests, and its result (Sonnet falls in the cross-family range rather than showing Haiku-like inflation) is the single cleanest piece of evidence that the +10 pp uplift is Haiku-checkpoint-specific rather than a Claude-family property.

**Q3 (closed-loop adversary pilot).**

V35 replaced the "almost certainly" speculation with a forward pointer to Future Direction 7. The current experiments bound only the one-shot informed case; a closed-loop pilot is the natural next experiment.

**Q4 (Is the +10 pp inflation symmetric — does Haiku show deflation as a target?).**

Yes. When Haiku is the *target*, Mistral L3 (71.7%) and Llama 70B (72.7%) both score well below Haiku-on-Haiku (82.8%); Sonnet-on-Haiku (65.7%) falls even below the non-Anthropic extractors. The +10 pp gap is unidirectional (Haiku-as-extractor inflates) rather than a general across-the-board elevation. The Sonnet result makes this especially clear: a more capable Claude model scoring *below* the non-Anthropic extractors on a Haiku target rules out capability as the explanation.

**Q5 (rule performance under instructed conditions).**

Under instructed asymmetric prompts, the refusal-count rule achieves 93.9–100% LOO accuracy on all seven models — essentially equivalent to the LLM pipeline. This confirms the equalization finding: both the rule and the pipeline primarily detect the instruction-following artifact (lying condition has no refusals; truth condition has normal corrections), and equalization is necessary to isolate whatever signal survives. The rule's ~18 pp drop from instructed (97.8%) to equalized (80.1%) on Claude Haiku is representative.

---

## Responses to Major Concerns (No Paper Change)

**C1 (NeurIPS venue / "high-quality audit" framing).**

We believe the joint three-control framework is a methodological contribution, not just an audit. Each control is individually non-novel; their joint application to behavioral deception detection, and the documentation of magnitudes that emerge (30–41 pp collapse, 9–10 pp family-bias, rule-vs-pipeline parity), establishes what controlled evaluation of this paradigm requires. The reviewer's characterization as a "high-quality measurement audit" is apt — and NeurIPS's Datasets and Benchmarks track was explicitly created for exactly this category of contribution, which changes how future work in the area is measured. We note this framing explicitly in the response but have not added text to the paper.

**C3 (More ≥14B models for EXP-G).**

The reviewer correctly notes that the "clean" instruction-following decomposition (EXP-G) rests on two data points (Qwen 14B, Llama 70B), giving the +7.5–15 pp range. A CI would require more models. This is acknowledged in §5.7(b) as a real limitation. The camera-ready RLHF-replication commitment (at least two additional ≥14B models) will provide additional data points, though not specifically designed to extend EXP-G.

---

## Honest Residuals (Accepted As-Is)

**1. EXP-G only two clean data points.** Adding more ≥14B models requires new API calls; deferred to camera-ready.

**2. Figure 1 label cramping (M3).** Requires figure regeneration; deferred to camera-ready.

**3. Regex list in main body (M4).** Adding 14 patterns would add ~0.5 pages; Appendix A.9 cross-reference is maintained as the primary pointer.

**4. Table 13 caption density (M8).** Table restructuring deferred to camera-ready.

---

## Compilation

V36: 48 pages, 0 errors, 0 undefined references (pdflatex × 2).

## Spot-Check Verification

1. §5.1 subsection heading does NOT contain "ICC=0.114 Caveat" — reads "Validated at α=0.606": ✓
2. §5.1 opening paragraph leads with α=0.606 validation result; ICC=0.114 is "historical context": ✓
3. §4.5 Qwen 32B paragraph does NOT contain "adversarial fine-tuning could plausibly": ✓
4. §4.7 triangulation paragraph contains "sign test p=0.0078": ✓
5. §4.3 autonomous partial-transfer parenthetical contains "Bonferroni correction (α/6=0.008)": ✓
6. §5.3 "(c) does not transfer reliably" sentence followed by Bonferroni sentence: ✓
7. §5.3 contains "semi-autonomous label for sycophancy is acknowledged as contested": ✓
8. §4.7 "headline for behavioral-detection accuracy" sentence is GONE, replaced with Table 1 pointer: ✓
9. Apollo AI Liar `\paragraph{Apollo AI Liar pilot}` is GONE: ✓
10. §4.6 K=1 footnote is GONE, replaced with inline pointer to §4.8: ✓
11. `REVIEWER_RESPONSE_LETTER_V36.md` exists: ✓
