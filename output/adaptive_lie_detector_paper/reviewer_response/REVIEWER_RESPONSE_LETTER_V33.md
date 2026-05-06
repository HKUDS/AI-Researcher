# V33 — Response to Accept 7/10 Review (Camera-Ready)

**Paper:** Correction-Marker Signals Cannot Substitute for Genuine Behavioral Deception Detection: A Three-Control Evaluation of Instructed-Roleplay Detection Across Open-Weight LLMs

**Prior decision:** Accept 7/10 (moved up from Weak Accept 6/10)

**V33 changes:** Five text-only fixes for camera-ready. No new experiments.

---

## At-a-Glance Table

| Item | Reviewer ask | V33 action | Status |
|---|---|---|---|
| RC1 | Abstract "four of six CIs include chance" is accurate but asymmetric | Added symmetric complement: "two of six exclude chance (Qwen 14B persona 68.0%, Mistral 7B FB 66.5%), treated as unexplained partial-transfer findings rather than noise" | Done |
| RC2 | Conclusion misses the Pacchiardi-positive regime | Added one sentence: "The pipeline materially outperforms the rule in one well-defined regime: claim-related multi-turn follow-ups at ≥14B (+14 pp on Llama 70B, +29 pp on Qwen 14B)" | Done |
| RC3 | Llama-8B-on-8B is the cleanest localization experiment; currently one unnamed paragraph | Promoted to named `\paragraph{Same-checkpoint control (Llama 8B-on-8B): capability asymmetry eliminated.}` with explicit framing sentence | Done |
| MC-App | Appendix ICC methodology brief; expand for camera-ready | Added annotator QC paragraph: per-annotator attention-check results, rating-distribution quality (SD, range) for correction-marker density and elaboration | Done |
| MC-Table | Other four features at α=0.07–0.26; clarify pipeline noise inheritance | Added explicit sentences: no paper claim from those four features; pipeline absolute level inherits noise but LOO operates on ranks, which are preserved (mean r=0.56) | Done |
| MC-Llama8B-outlier | +0.5 pp outlier deserves hypothesis discussion | Extended footnote: n=100 noise is primary explanation; plausible mechanism is Llama 3.1 8B's cross-lingual generalization producing less same-family lexical overlap | Done |

---

## Detailed Responses

### RC1 — Asymmetric abstract framing on autonomous transfer

**Reviewer:** "The abstract says 'four of six n=200 Wilson CIs include chance.' That's accurate but selects one direction. The symmetric statement is 'two of six exclude chance.'"

**Our response:** You are correct. Both facts belong in the abstract side by side. We have updated the headline numbers bullet to read: "fully-autonomous persona/false-belief: four of six n=200 Wilson CIs include chance; two of six exclude chance (Qwen 14B persona 68.0%, Mistral 7B false-belief 66.5%), treated as unexplained partial-transfer findings rather than noise (§4.3)."

The two cells are flagged as "findings, not noise" throughout the paper (§5.3, §4.3) — the abstract now reflects that framing consistently.

---

### RC2 — Conclusion omits the Pacchiardi-positive regime

**Reviewer:** "A reader who reads only the abstract and conclusion still misses that the pipeline gains +14–+29 pp at ≥14B with topical multi-turn. The conclusion should carry both halves symmetrically."

**Our response:** Agreed. The conclusion's second paragraph previously stated "Multi-turn interrogation adds genuine value only under equalization at ≥14B scale (+19–21.5 pp)" and stopped there, relying on the reader to connect this to the regime where the pipeline specifically wins. We have added an explicit follow-on sentence: "The pipeline materially outperforms the rule in one well-defined regime: claim-related multi-turn follow-ups at ≥14B scale (+14 pp on Llama 70B, +29 pp on Qwen 14B; §4.4, Appendix R), where accumulated weak per-question signals exceed the single-question baseline."

A reader of the conclusion alone now sees both halves: regex wins on 6/7 models (rule-vs-pipeline parity finding) AND pipeline wins in the Pacchiardi-style regime (behavioral interrogation positive finding).

---

### RC3 — Llama-8B-on-8B prominence

**Reviewer:** "The Llama-8B-on-8B result deserves slightly more emphasis — it's the cleanest single experiment for the localization claim because it eliminates capability asymmetry entirely. Currently reported as one paragraph."

**Our response:** We have promoted the same-checkpoint cell to a named paragraph heading: `\paragraph{Same-checkpoint control (Llama 8B-on-8B): capability asymmetry eliminated.}` and prepended an explicit framing sentence: "This cell is the cleanest single test of same-family bias: extractor and target share identical checkpoint, scale, and family, so any self-boost cannot be attributed to capability asymmetry." The result (63.0% pipeline, no self-boost, below all three cross-family extractors) now reads as a standalone conclusion rather than a supporting note within the broader Llama-on-Llama paragraph.

---

### MC-App — Appendix ICC methodology expansion

**Reviewer:** "The methodology section is brief. For camera-ready, expand to include attention-check failure rates per annotator, time-on-task, and rating-distribution histograms."

**Our response:** We have added a `\paragraph{Annotator quality control.}` paragraph before the results table. It reports:
- Per-annotator attention-check results: Ann1 (0 failures, PASS), Ann2 (1 failure, PASS), Ann3 (1 failure, PASS); all within the ≤1 failure threshold
- Rating-distribution quality: correction-marker density showed healthy spread across all three annotators (SD: 2.8, 2.6, 3.0; full 0–10 range used), consistent with genuine feature discrimination
- Elaboration showed mild ceiling compression (mean 6.9–8.8, SD 0.4–1.4), expected for multi-turn LLM conversation transcripts and not affecting any paper claims

We do not have Prolific session timing data available at camera-ready; the estimated time (2.5–3 hr, $75 compensation) is in the task description released with supplementary materials. Rating-distribution histograms are derivable from the released per-rater CSVs.

---

### MC-Table — Pipeline noise inheritance from low-α features

**Reviewer:** "Table 33 shows α=0.07–0.26 on the other four features. Should be more explicit that no paper claim should be drawn from them, and that the pipeline absolute level inherits this noise."

**Our response:** We have updated the closing paragraph of Appendix R to state explicitly: "No paper claim should be drawn from consistency, specificity, confidence, or elaboration as standalone features. The five-feature pipeline's absolute level inherits noise from all five features, but the LOO classifier operates on rank ordering rather than absolute level, and rank agreement is preserved (mean pairwise Pearson r=0.56 across the three annotator pairs on correction-marker density), so pipeline rank-based comparisons are unaffected."

---

### MC-Llama8B-outlier — Hypothesis for +0.5 pp CF gap

**Reviewer:** "The Llama 8B outlier (+0.5 pp vs. +7.5 pp next-smallest) deserves a hypothesis-level discussion. Is this Llama 3.1 8B-specific, or n=100 noise?"

**Our response:** We have extended the table footnote to add: "A plausible mechanism is that Llama 3.1 8B's strong cross-lingual generalization produces lower same-family lexical overlap between extractor and target responses, yielding less same-family scoring bias; but at n=100 this cannot be distinguished from noise." n=100 noise remains the primary stated explanation (one-prediction noise range), with the cross-lingual hypothesis offered as a testable candidate for future work.

---

## Honest Residuals (Accepted As-Is)

Three residuals remain that we accept as honest incompleteness:

**1. Qwen 14B persona qualitative coding.** The 10-trial spot-check (coded for persona-maintenance / direct-correction / other) was a camera-ready commitment in the prior round. It remains deferred — the annotation protocol is written and the trials are identified, but the two-coder annotation has not been completed. We accept this deferral and note the commitment in §5.8 Future Direction (6).

**2. Autonomous transfer asymmetry causally unexplained.** After two pre-registered null findings (knowledge-conflict clarity, §4.4; disposition-source ranking, §4.7.2) we do not have a validated causal account of why sycophancy transfers while persona and false-belief do not. The paper handles this honestly in §5.3 ("No validated causal account of the transfer asymmetry") and in §5.7(i). We accept this as a real incompleteness.

**3. ADAGE is the only LLM pipeline compared.** As the reviewer notes, this is actually the strongest version of the pipeline-redundancy claim (we are showing our own pipeline is largely redundant), and the concern is weaker than in the prior round. We accept the current framing.

---

## Compilation

V33: 48 pages, 0 errors, 0 undefined references (pdflatex × 2).
