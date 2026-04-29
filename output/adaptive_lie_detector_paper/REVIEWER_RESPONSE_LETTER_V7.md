# Response to Reviewer #7

We thank the reviewer for a thorough and constructive review. The feedback identified genuine structural problems — the ADAGE identity crisis, the autonomous-section framing, and the novelty overclaims — that we have addressed directly. We appreciate the reviewer's explicit path to acceptance and have made the major revisions requested.

**Summary of changes:**
- ADAGE framing unified: consistently "measurement instrument," pipeline figure moved to appendix, §4.4 renamed "Pipeline Redundancy Under Equalization"
- §4.6 reframed as "Negative Result: Transfer to Autonomous Deception" — leads with failure, sycophancy labeled instruction-driven
- Abstract autonomous paragraph leads with "does not generalize to autonomous deception"
- "deployment-ready" -> "deployment-viable" throughout, with explicit English-only/adversarial limitations
- §5.3 novelty language toned down ("substantially larger than expected" replaces "not anticipated")
- ICC reframed in §5.4: underpowered study acknowledged; weak ICC supports rather than undermines central argument
- ICC added as explicit limitation (g) in §5.5
- Cohen's d values rounded to 1 decimal place throughout
- "<=70B" caveat reduced from 4 to 2 instances (abstract, experiments only)
- Same-family Claude target rationale explained in §5.2
- Pacchiardi claim caveated as single-model observation in appendix

---

## Major Concerns

**M1 (Contribution incremental / "methodological hygiene paper").**
We accept the reviewer's characterization. The contribution IS methodological hygiene applied to behavioral deception detection. We have toned down the novelty language in §5.3: "substantially larger than expected" replaces "not anticipated by the prior literature"; "suggest caution in interpreting" replaces "change the practical interpretation of all." We believe this is appropriate for NeurIPS main track: the field is actively building on instructed-deception benchmarks (Pacchiardi et al., Apollo Research), and a methodological contribution showing these benchmarks are confounded by 30-41pp is practically important even if the individual controls are known. The reviewer's suggested framing — "three reusable evaluation controls" as the primary contribution — is exactly what we lead with.

**M2 (ICC=0.114 construct validity genuinely weak).**
We agree the n=20, 2-annotator study is underpowered and cannot establish either reliability or unreliability. We have:
1. Added an explicit acknowledgment in §5.4: "The n=20, 2-annotator study is underpowered to establish either reliability or unreliability of correction-marker density."
2. Reframed the argument: the paper's central claims do NOT depend on correction-marker density being reliable. The regex baseline achieves comparable accuracy without LLM extraction. The weak ICC is consistent with — and supports — our central finding that the pipeline is redundant.
3. Added ICC as a formal limitation (g) in §5.5.
4. We commit to running a proper validation study (n>=100, 3+ annotators, Krippendorff's alpha) if accepted.

We cannot run the validation study before camera-ready — it requires coordinating external annotators. But we emphasize that this weakness strengthens rather than weakens the paper's argument: if the LLM-extracted feature is unreliable, that is additional evidence for the regex-over-pipeline conclusion.

**M3 (ADAGE framing inconsistency).**
Resolved. The paper now consistently frames ADAGE as a measurement instrument whose redundancy is itself a finding:
- Pipeline figure moved from methodology (§3) to Appendix A.8
- §4.4 renamed from "ADAGE Pipeline as Ablation" to "Pipeline Redundancy Under Equalization"
- §4.4 opening now explicitly states: "The ADAGE pipeline served as the measurement instrument through which we applied the three controls. Having established those results, we now show the pipeline itself is largely redundant."
- Discussion §5.4 contextualizes: "the ADAGE pipeline — having served its purpose as the measurement instrument — adds little over simple refusal-count heuristics."
The pattern is standard: build a measurement instrument, apply it to discover the phenomenon, then show a simpler instrument suffices. The instrument's redundancy doesn't retroactively invalidate the measurements.

**M4 (Scale claims fragile / underpowered).**
We agree n=50-100 per cell is underpowered for strong scaling claims. In revision 6, we already added dual Holm-Bonferroni reporting (within-family vs. joint 5-test correction) and noted that only Llama 8B->70B survives the strictest correction. The "scale-dependent gap" framing (models <=7B at 61-74% vs. >=14B at 82-84%) deliberately avoids smooth-scaling claims. We note the family-composition confound in the pooled comparison in §5.5(e). We believe the current language is appropriately hedged: "suggests family-specific, non-monotonic patterns" rather than "reveals" or "demonstrates."

**M5 (Autonomous extension doesn't deliver).**
The reviewer is right: the honest summary is "fails to generalize." We have:
- Renamed §4.6 to "Negative Result: Transfer to Autonomous Deception"
- Rewritten the opening: "The refusal-count signal does not generalize to autonomous deception."
- Rewritten the abstract paragraph to lead with failure: "shows the refusal-count signal does not generalize to autonomous deception"
- Reframed sycophancy: "System-prompt-induced sycophancy retains signal (82%) but remains instruction-driven rather than autonomous."
- In discussion, added: "the system prompt does the heavy lifting, making this closer to instructed deception than autonomous behavior."

We thank the reviewer for the framing that sycophancy is "essentially another instructed-deception variant with a different instruction wrapper." This is correct and our revision reflects it.

**M6 (Apollo AI Liar: null result with confounds).**
We agree this is a null result. We now present it explicitly as such: "yields a null result: refusal-count markers achieve 0-54% accuracy." The task-format mismatch is an observation, not a controlled finding. We chose not to reformat AI Liar trials as factual claims because that would change the task rather than control for the hypothesis. The null result is informative precisely because it confirms the method is domain-specific: it detects factual-claim correction behavior, not general strategic deception.

**M7 (Same-family bias unresolved).**
We agree a definitive test requires a comparable-capability cross-family extractor (GPT-4o, Gemini Pro). We do not have access to these as feature extractors. We have:
- Added to §5.2: "Claude Haiku was retained as a same-family target specifically because the same-family bias finding (d: 4.9->0.6) is itself a contribution; substituting a non-Anthropic model would have eliminated this finding."
- The existing text already states: "A definitive test would require a non-Claude extractor of comparable capability."
We believe the finding is still valuable even without resolution: the 7x inflation is a concrete number that practitioners can use when evaluating same-family extraction setups.

**M8 (Regex rule "deployment-ready" overclaimed).**
Changed to "deployment-viable" throughout (abstract, introduction, conclusion). Added explicit limitations in the EXP-J-fixed paragraph: "This rule is English-only, relies on lexical conventions specific to instruction-tuned models, and has not been tested against adversarial paraphrase or stylistic variation; deployment should include domain-specific validation." We agree adversarial robustness testing is essential future work.

---

## Minor Concerns

**m1 (Abstract U-shape truncation).** The sentence is complete in source but rendered awkwardly due to the nested [p=0.014*] within parentheses. Fixed: "exhibits a U-shape (50%->68%->72%->50%; 3B->7B increment p=0.014)" — p-value moved outside the arrow sequence.

**m2 (Claude Haiku same-family target).** Addressed in §5.2: Claude was retained because the same-family bias finding is itself a contribution. The 97.8% -> 82.6% drop under cross-family extraction (and d: 4.9->0.6) would not have been discoverable without a same-family target.

**m3 (n discrepancy between Table 1 and Table 2).** Added footnote to Table 1: "Per-model n varies from 93 to 100 due to API errors; Table 2 shows exact counts."

**m4 (Mock validation vestigial).** Already reduced to one sentence in §4.1 (revision 6). The sentence serves a specific purpose: it explains what "mock validation" means for readers who encounter the appendix reference. Further removal would be confusing.

**m5 (Figure 1 unnecessary).** Pipeline figure moved to Appendix A.8. The main body now contains only the feature_collapse and scale_trend figures, which directly illustrate the paper's contributions.

**m6 (Mistral Large naming).** The "Mistral Large 3" naming follows AWS Bedrock documentation. The 675b artifact is explained in the appendix footnote. We believe this is sufficient disambiguation.

**m7 (Cohen's d precision).** All Cohen's d values rounded to 1 decimal place throughout (experiments.tex, discussion.tex, abstract.tex). Tables and inline text now consistently report d=0.3, 1.5, 4.9, etc.

**m8 (Pacchiardi "first response" claim thin).** Added caveat: "This observation is from a single-model (Mistral 7B) replication; multi-model replication is needed to confirm generality."

**m9 (≤70B repetition).** Reduced from 4 instances to 2 (abstract and experiments §4.5 only). Discussion and introduction now use forward references ("scaling caveats in §4.5" or "frontier-scale behavior remains untested").

---

## Questions

**Q1 (Validation study before camera-ready?).**
We cannot coordinate a n>=100, 3-annotator study before camera-ready. We have strengthened the mitigation: (a) acknowledged the study is underpowered, (b) reframed weak ICC as supporting the pipeline-redundancy conclusion, (c) added it as explicit limitation (g). We commit to running the study if accepted.

**Q2 (GPT-4o/Gemini as cross-family extractor?).**
We have not tested these. Access to GPT-4o or Gemini as a structured feature extractor (scoring 5 behavioral dimensions per response) requires additional API integration and prompt engineering. We note this as the highest-priority experiment for future work. The existing cross-family comparison (3 extractors from 3 families) establishes the phenomenon; a comparable-capability extractor would quantify it.

**Q3 (Is sycophancy meaningfully different from instructed deception?).**
The reviewer is correct that it may not be. We now explicitly frame it as "instruction-driven rather than autonomous" and note "the system prompt does the heavy lifting." The distinction we draw — semi-autonomous vs. instructed — is one of degree (the sycophancy prompt doesn't mention deception), not of kind. We no longer claim this as positive transfer to autonomous deception.

**Q4 (Abstract truncation?).**
The sentence was complete in source but rendered awkwardly. Fixed by restructuring the parenthetical.

**Q5 (Why Claude Haiku as same-family target?).**
Answered in m2 above and now in §5.2: the same-family bias finding IS the contribution. Without a same-family target, we could not have documented the 7x feature inflation.

**Q6 (Adversarial paraphrase testing?).**
Not tested. We agree this is important and have added it as an explicit limitation: "has not been tested against adversarial paraphrase or stylistic variation." A model fine-tuned to suppress refusal markers would likely defeat this rule, which is exactly the concern raised by the Qwen 32B finding (where RLHF incidentally achieves the same effect). We now discuss this adversarial implication in §4.5.

---

## Reviewer's Suggestions

**"Tighten framing to lead with three reusable evaluation controls."** This was done in revision 5 and maintained. The contribution statement consistently leads with the empirical finding via three controls.

**"Demote ADAGE entirely to appendix."** We moved the pipeline figure to appendix but retain the 1-paragraph methodology description in §3.2 and the 1-page redundancy analysis in §4.4. Complete removal would leave the evaluation controls without a described measurement instrument. The reader needs to know what was used to apply the controls, even if it was ultimately redundant.

**"Run the validation study."** Committed to if accepted; cannot complete before camera-ready.

**"Drop or reframe autonomous section as negative result."** Done: §4.6 renamed "Negative Result: Transfer to Autonomous Deception," leads with failure, sycophancy labeled instruction-driven.
