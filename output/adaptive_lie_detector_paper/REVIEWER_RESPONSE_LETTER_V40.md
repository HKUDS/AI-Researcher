# V40 — Response to Weak Accept 6/10 Review (New Reviewer)

**Paper:** Correction-Marker Signals Cannot Substitute for Genuine Behavioral Deception Detection: A Three-Control Evaluation of Instructed-Roleplay Detection Across Open-Weight LLMs (3B–70B)

**Prior decision:** Weak Accept 6/10 (new reviewer, first reading of this paper)

**V40 changes:** All nine weaknesses and four questions addressed by text-only revisions. No new experiments needed. Paper: 50 pages, 0 errors, 0 undefined references.

---

## At-a-Glance Table

| Item | Reviewer ask | V40 action | Status |
|---|---|---|---|
| W1 | Reframe as empirical characterization, not methodological framework | §1.1 contributions preamble rewritten to lead with "empirical characterization of confound magnitudes" | Done |
| W2 | Frontier-scale gap severe and not mitigated | §5.8(5)(ii) expanded with concrete priority targets (GPT-4o, Claude Sonnet) and honest external-validity caveat | Done |
| W3 | Two cells exclude chance — commit to Bonferroni null or explain | New named paragraph "Bonferroni across six autonomous cells" commits to hypothesis-generating framing with explicit p-values | Done |
| W4 | 80.1% rule: pick one framing | Abstract reordered: collapse leads, rule reframed as "measurement baseline…not a deployable classifier" | Done |
| W5 | Mistral 7B near-parity hand-waved — "two of three families" glass-half-full | Cross-target generalization claim now explicitly qualifies: "two of three families (Llama and Qwen)…Mistral 7B is an exception" | Done |
| W6 | ICC discrepancy deserves more than one sentence | New named paragraph "Implication of the unvalidated-feature gap" with two interpretations (noisy labeling vs. stylistic covariation) | Done |
| W7 | Human baseline +32 pp gap uninterpretable | Added two sentences: gap "not interpretable as the rule's advantage over trained human lie-detectors"; relevant comparison "left to future work" | Done |
| W8 | Multi-comparison boundary inconsistent | Added clarifying sentence to the multiple-comparison budget paragraph: cross-extractor gaps use "directional consistency, not p-value crossing, as the operative evidence" | Done |
| W9 | Writing density — §1.1 and §4.1 repeat same numbers | §4.1 "How to read" opener trimmed to remove redundant restatement of the collapse magnitude | Done |
| DC1 | Table `tab:autonomous_matched`: n=50 rows not visually distinguished | n=50 Llama 70B row italicized; footnote added: "$^\star$n=50 pilot; treat as preliminary" | Done |
| DC2 | §4.5 Qwen 32B replication commitment — name specific models | Now names Gemma 2 27B-Instruct and Mistral-Small-3.1-24B as specific replication targets | Done |
| DC3 | §4.7 sign test p-value over-interpreted | Inline qualifier added: "descriptive triangulation: targets share extractors and trial sets; the p-value quantifies direction consistency, not an independent inferential claim" | Done |
| DC4 | ADAGE acronym foregrounded unnecessarily | Approach paragraph in §1.3 reduced to two sentences pointing to §3; ADAGE in §1.1 kept as a parenthetical | Done |

---

## Detailed Responses

### W1 — Contribution Framing: Empirical Characterization, Not Methodological

**Reviewer:** "The empirical magnitudes are the real contribution, not the framework. I'd recommend reframing as 'an empirical characterization of confounds' rather than as a methodological contribution."

**Our response:** Agreed. We have rewritten the core contribution sentence in §1.1:

**Before:**
> "The primary contribution is methodological: the joint three-control evaluation framework; the seven-model panel demonstrates the framework."

**After:**
> "The primary contribution is an *empirical characterization* of confound magnitudes in behavioral deception detection: the joint three-control evaluation reveals that 30–41 pp of reported accuracy is attributable to instruction-following artifacts, 9–10 pp to same-family extraction bias, and the residual signal is surface-lexical. The three controls are individually standard; the contribution is documenting what joint application reveals at these magnitudes."

The controls are no longer claimed as the contribution — the magnitudes are.

---

### W2 — Frontier-Scale Gap

**Reviewer:** "At least one frontier-scale target would substantially strengthen the paper. The paper's central negative claim is tested on models 1–2 capability tiers below where autonomous deception is documented to robustly occur."

**Our response:** Honest. We cannot add a frontier-scale target within this revision. V39 adds Qwen 2.5 72B (pending, see below), which partially addresses the scale gap but remains below 100B. We have substantially expanded §5.8(5)(ii):

**Before:**
> "(ii) frontier-scale evaluation on models ≥100B parameters, which are completely untested in this paper"

**After:**
> "(ii) **frontier-scale evaluation** (≥100B Instruct-tuned models, including API-accessible models such as GPT-4o and Claude Sonnet) is the most pressing external-validity gap — the present 3B–70B results may not characterize behavior where autonomous deception phenomena are documented to robustly occur [Greenblatt et al., Scheurer et al., Hubinger et al.]"

We name the concrete priority targets (GPT-4o, Claude Sonnet), acknowledge the capability-tier gap explicitly, and cite the exact papers the reviewer references. We do not over-promise: this is a limitation with a concrete research direction, not a resolved concern.

---

### W3 — Two Cells Excluding Chance: Bonferroni Commitment

**Reviewer:** "A more disciplined either/or — either treat as confirmatory and explain, or treat as null under correction — would be cleaner."

**Our response:** We commit to the Bonferroni null. The existing parenthetical "(under Bonferroni correction, neither would survive)" has been promoted to a named paragraph preceding the "Partial transfer" paragraph:

> **Bonferroni across six autonomous cells.** Applying Bonferroni correction across the six fully-autonomous cells (α/6 = 0.008), neither Qwen 2.5 14B persona (uncorrected p ≈ 0.004) nor Mistral 7B false-belief (uncorrected p ≈ 0.009) survives. Both are treated as *hypothesis-generating* findings, not confirmatory detections. The "mixed result with negative predominance" framing reflects this: four of six cells are at chance under the uncorrected test and none survive correction; the two cells that exclude chance under the uncorrected test are directionally inconsistent (different target families, different scenario types) and lack a validated causal account.

The "Partial transfer" paragraph that follows retains the numbers for transparency ("neither survives the Bonferroni correction above") but no longer buries the correction in a parenthetical.

---

### W4 — 80.1% Rule: Sanity Baseline, Not Deployable

**Reviewer:** "The presentation oscillates between 'the rule is the deployable detector' and 'the rule is just a sanity baseline.' Pick one."

**Our response:** We pick sanity baseline. The abstract has been reordered so the 30–41 pp collapse leads, the 9–10 pp same-family bias follows, and the rule is introduced last as a *measurement baseline*:

**New abstract sentence:**
> "The most actionable finding is a *measurement baseline*: the same rule without calibration (pooled fixed threshold k=1) achieves 80.1% (range 64–88%; 75–88% on models ≥7B), characterizing the surface-lexical ceiling that more robust detectors must exceed — not a deployable classifier."

The "not a deployable classifier" language is now in the same sentence as the 80.1% number. The §1.1 closing sentence "We present the rule as a *baseline for more robust detectors*, not a deployment-ready detector" is retained.

---

### W5 — Mistral 7B Near-Parity: Qualify Cross-Target Generalization

**Reviewer:** "'Two of three families share a single failure mode' is a glass-half-full reading of three datapoints with one disagreeing."

**Our response:** Agreed. The cross-target claim in §4.8 now reads:

**Before:**
> "Two of three targets at n=200 therefore share a single failure mode (lying-channel suppression), while Mistral 7B remains near-parity."

**After:**
> "Two of three model families (Llama 3B and Qwen 14B) share a single failure mode (lying-channel suppression) at n=200; Mistral 7B is an exception (truth 56%, lie 73%, near-parity rather than channel suppression), discussed as a model-specific anomaly in the mechanistic note below."

The cross-target claim is now "two of three **model families** (Llama and Qwen)", and the exception is named inline rather than treated as a minor residual.

---

### W6 — ICC Discrepancy: Expanded Treatment

**Reviewer:** "It means the pipeline is extracting *something* discriminative beyond correction density, but that something isn't construct-validated. This deserves more than a one-sentence concession."

**Our response:** We have added a named paragraph in §5.1 immediately after the existing "methodological inconsistency" sentence:

> **Implication of the unvalidated-feature gap.** The 10.2 pp gap between 5-feature and defensiveness-only cross-family accuracy means the pipeline is extracting discriminative signal from four features that human annotators cannot reliably identify. Two interpretations are consistent with this finding: (a) the features are psychologically real but noisily labeled by LLMs on open-ended prompts (partial annotation agreement inflates variance without eliminating signal); or (b) the LLM extractor captures cross-model stylistic covariation — correlated with deceptive mode under equalized prompts — that human annotators do not recognize as a specific "feature." We cannot adjudicate between (a) and (b) without a pre-registered feature-specific ICC study at n≥200 with trained annotators. The practical consequence is that the 5-feature cross-family 64.7% should be treated as a *diagnostic upper bound* (what the pipeline extracts under equalization) rather than a construct-validated detection signal; the refusal-count rule (80.1%, extractor-independent, ICC-independent) remains the primary validated estimate.

This directly names the two mechanistic interpretations and states what would be needed to resolve them.

---

### W7 — Human Baseline: Caveat the +32 pp Framing

**Reviewer:** "Three naive crowdworkers all collapsing to TRUTH tells us almost nothing about whether the rule beats trained humans."

**Our response:** We have added two sentences immediately after the "+32 pp over naive crowdworker humans" statement:

> "This gap is not interpretable as the rule's advantage over trained human lie-detectors; it reflects the ceiling of naive crowdworker performance on equalized transcripts (all-TRUTH strategy, κ=0.00). The relevant comparison — rule vs. trained domain-expert annotators with knowledge of the equalized-condition design — is left to future work."

The data is retained; the framing is corrected. The existing sentence noting "trained domain-expert annotators would likely score higher" has been replaced by the stronger two-sentence caveat.

---

### W8 — Multi-Comparison Boundary: Clarify Confirmatory vs. Exploratory

**Reviewer:** "Cross-extractor accuracy gaps are doing real work in the same-family-bias argument…the boundary between confirmatory and exploratory is drawn in ways that conveniently favor the paper's central claims."

**Our response:** We have added one sentence to the multiple-comparison budget paragraph in §4.5:

> "Cross-extractor accuracy gaps are used as evidence for same-family bias not because they pass an inferential threshold, but because two independently-trained non-Anthropic extractors converge within 3 pp on 7 of 8 targets, making directional consistency — not p-value crossing — the operative evidence."

This makes the evidential logic explicit: the case for same-family bias rests on triangulation convergence, not on inferential test results. This is a defensible evidential standard and we now state it explicitly.

---

### W9 — Writing Density: Remove Redundant §4.1 Opener

**Reviewer:** "Sections 1.1 and 4.1 contain the same headline numbers stated three different ways."

**Our response:** The §4.1 "How to read this section" paragraph has been trimmed:

**Before:**
> "The seven-model panel in §4.2–§4.7 is a *demonstration* of the three controls, not a primary claim about any individual model. The paper's claims concern the magnitudes that emerge under joint application of equalization, cross-family extraction, and a regex baseline; the model-specific results instantiate those magnitudes. Headline numbers are consolidated in Tables 3 and 4."

**After:**
> "The seven-model panel is a *demonstration* of the three controls, not a primary claim about any individual model. Headline numbers are consolidated in Tables 3 and 4; scale breakdown is in §4.5–§4.6."

The redundant restatement of the framework's purpose (already said three times before §4) is removed. The cross-reference to scale breakdown is added for navigation.

---

### DC1 — Table: n=50 Rows Visually Distinguished

The single n=50 row (Llama 3.3 70B sycophancy) in Table `tab:autonomous_matched` is now italicized with a footnote marker:

> *Sycophancy defense* | *Llama 3.3 70B* | *50★* | *72.0%* | *[58–84%]* | *0.9*
>
> ★ *n=50 pilot; treat as preliminary (direction-reversal precedent at n=200 in §4.8).*

---

### DC2 — Qwen 32B Replication: Specific Model Names

**Before:** "at least two additional RLHF-heavy open-weight models at ≥14B scale"

**After:** "at least two additional RLHF-heavy open-weight models at ≥14B scale — specifically Gemma 2 27B-Instruct and Mistral-Small-3.1-24B, both of which have documented high-agreeableness post-training tuning that may produce analogous correction-marker suppression."

---

### DC3 — Sign Test Qualifier

The sign test sentence (§4.6) now contains an inline qualifier:

> "A sign test on the 8 per-target gaps confirms the directional result: all 8 are positive (sign test p=0.0078, two-sided; *descriptive triangulation: targets share extractors and trial sets; the p-value quantifies direction consistency, not an independent inferential claim*; …)"

---

### DC4 — ADAGE Acronym Reduced

The §1.3 Approach paragraph was:
> "We use an adaptive interrogation pipeline (ADAGE) as a measurement apparatus to extract behavioral features. The pipeline comprises an LLM-based question generator, a feature extractor that scores five behavioral dimensions per response, and a logistic regression classifier. Full architecture details, including an adaptive stopping mechanism (empirically near-vacuous; Section 3), are in Section 3."

Now:
> "We use the ADAGE adaptive interrogation pipeline (§3) as a measurement apparatus. Full architecture details are in §3."

The ADAGE acronym is now introduced once in §1.1 as a parenthetical pointing to §3, once in §1.3 as a pointer, and used as a label in §3. It is no longer re-introduced with "this is not a contribution" clarifications scattered through the intro.

---

## Questions for Authors (Our Responses)

**Q1 — Frontier-scale target (even n=100):**

We have not run a frontier-scale API target within this revision. V39 adds Qwen 2.5 72B (still pending hardware), which is the largest open-weight model we can run under Ollama. GPT-4o and Claude Sonnet evaluation would require API budget (estimated $50–100 for n=100 equalized trials) that we are arranging for camera-ready. We name these as the concrete priority targets in §5.8(5)(ii).

**Q2 — Two cells that exclude chance: are they driven by the same lexical markers?**

We have not analyzed which markers drive the two partial-transfer cells. This is a legitimate open question added to §5.8 future work. Our hypothesis (consistent with the mechanistic note in §4.9) is that the Qwen 14B persona cell may be driven by hedging residuals from the persona-prompt itself rather than by the same correction-marker channel. We flag this explicitly: "a 10-trial qualitative read…coded for persona-maintenance / direct-correction / other, to distinguish signal from persona-prompt leakage."

**Q3 — Pipeline +14/+29 pp: what is it keying on?**

This is addressed in §4.5 (Pacchiardi cross-pointer): multi-turn follow-ups accumulate weak per-question correction signals — each claim-related question re-asks whether the model will correct — so the signal compounds across turns. At ≥14B the model's knowledge capacity is sufficient to produce consistent correction-pressure signals per question; at 3B it is not. This is the pipeline's one genuine advantage over the rule: not a different detection mechanism, but aggregated re-exposure to the same correction-behavior channel.

**Q4 — Camera-ready replication models:**

Named in DC2 above: Gemma 2 27B-Instruct and Mistral-Small-3.1-24B.

---

## Compilation

V40: 50 pages, 0 errors, 0 undefined references (pdflatex × 2). One page above V39 (49 pages) due to the new Bonferroni paragraph (~60 words) and the ICC implication paragraph (~100 words), partially offset by §4.1 opener compression (~30 words removed).

## Spot-Check Verification

1. §1.1 says "empirical characterization" not "methodological contribution": ✓
2. Abstract leads with 30–41 pp collapse, not 80.1% rule: ✓
3. Abstract contains "measurement baseline…not a deployable classifier" in same sentence as 80.1%: ✓
4. Named paragraph "Bonferroni across six autonomous cells" commits to hypothesis-generating framing: ✓
5. "Two of three families (Llama and Qwen)…Mistral 7B is an exception" in §4.8: ✓
6. Named paragraph "Implication of the unvalidated-feature gap" in §5.1: ✓
7. Human baseline section contains "not interpretable as the rule's advantage over trained human lie-detectors": ✓
8. Multiple-comparison paragraph contains "directional consistency — not p-value crossing — the operative evidence": ✓
9. Sign test has "descriptive triangulation" qualifier: ✓
10. Table `tab:autonomous_matched` n=50 row italicized with ★ footnote: ✓
11. §4.5 names Gemma 2 27B-Instruct and Mistral-Small-3.1-24B: ✓
12. §5.8(5)(ii) names GPT-4o and Claude Sonnet as frontier priority targets: ✓
13. `REVIEWER_RESPONSE_LETTER_V40.md` exists: ✓
