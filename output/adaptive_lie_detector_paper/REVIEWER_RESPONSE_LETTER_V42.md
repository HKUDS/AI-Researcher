# V42 — Response to New Weak Accept 6/10 Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Cannot Substitute for Genuine Behavioral Deception Detection: A Three-Control Evaluation of Instructed-Roleplay Detection Across Open-Weight LLMs (3B–70B)

**Prior decision:** Weak Accept 6/10 (new reviewer; V41 addressed the returning reviewer's V40 weaknesses and added the Sonnet 4.5 frontier run)

**Reviewer's verdict:** "I lean toward acceptance." No new experiments required; all weaknesses are presentational or framing issues.

**V42 changes:** 8 text-only revisions + 1 figure change + 3 presentation moves. Paper: 51 pages, 0 errors, 0 undefined references.

---

## At-a-Glance Table

| Item | Reviewer ask | V42 action | Status |
|---|---|---|---|
| **W1** | Four headline numbers confusing — commit to one primary | Abstract restructured: 64.7% cross-family is now explicitly primary; 80.1% labeled "no-calibration variant"; "Headline numbers, by claim" reordered to lead with 64.7% | Done |
| **W2** | "4 of 5 features fail ICC" buried; "5-feature pipeline" misleading | Added construct validity note to §3.2 methodology at pipeline first mention; promoted ICC(2,1)=0.71 high-confidence result to named paragraph leading §5.1; added ICC caveat to abstract | Done |
| **W3** | Transfer whiplash — §4.6 leads with success numbers then drops to chance | Added explicit framing sentence at §4.6 open: "Sycophancy is the sole transfer exception"; added closing narrow-claim sentence | Done |
| **W4** | Abstract missing instructed-roleplay vs. autonomous deception caveat | Added one sentence to abstract: "All experiments study instructed roleplay…the signal does not generalize to fully-autonomous conditions" | Done |
| **W5** | Qwen 32B structural zero over-weighted — single n=100 observation | Added n=100 single-observation caveat to conclusion RLHF-fragility claim; added independent Qwen 14B supporting sentence; Qwen 32B already labeled supplementary case study in experiments §4.5 | Done |
| **W6** | Sonnet extractor reversal under-investigated | Added explicit "diagnostic finding, not cross-family estimate" framing to §frontier_sonnet; sign-test and panel-average exclusion already in place | Done |
| **W7** | +32pp human baseline comparison misleading (all-TRUTH, κ=0.00) | Removed "+32pp rule advantage" framing; replaced with "degenerate baseline (all-TRUTH, κ=0.00); characterizes rater behavior, not detection accuracy" | Done |
| **W8** | Scope caveats scattered across experiments.tex | Added `(scope: §\ref{sec:motivation})` cross-reference pointers in experiments.tex at key scope mentions; consolidated scope paragraphs already exist in introduction §1 | Done |
| **DC1** | Add 50% chance baseline to Figure 1 panel (a) | Added `extra y ticks={50}` dashed line with "chance" label to pgfplots panel (a) | Done |
| **DC2** | Move Table 1 (headline_decision) earlier in introduction | Moved "Which number to report" paragraph + Table 1 from after contributions list to immediately after "How to read this paper" paragraph | Done |
| **DC3** | Holm-Bonferroni justification appears too late | Added 1-sentence forward reference at §4.5 section opening: "All pairwise scale comparisons use within-family Holm-Bonferroni correction" | Done |
| **DC4** | ICC(2,1)=0.71 high-confidence subset buried at end of §5.1 | Promoted to named paragraph `\paragraph{High-confidence annotation reliability}` leading the ICC section | Done |

---

## Detailed Responses

### W1 — Commit to 64.7% as Primary Headline

**Reviewer:** "The abstract presents four headline numbers (80.1%, 71.8%, 74.3%, 64.7%) with no clear ordering. A reader should be able to tell in one sentence which number to quote."

**Prior state:** The "How to read this paper" paragraph in §1 already said "The cross-family pipeline 64.7% is the primary accuracy estimate; 71.8% and 80.1% are deployment-regime variants." But the abstract did not reflect this ordering.

**V42 change in abstract.tex:** The abstract now introduces 64.7% as the primary number first:

> "The *primary cross-family pipeline estimate* is **64.7%** (Mistral L3, 7 targets; Llama 70B within 3 pp), extractor-independent of Claude-family models. The refusal-count rule achieves **80.1%** (pooled-LOO, k=1, range 64–88%; 75–88% on models ≥7B) without calibration data—the surface-lexical ceiling more robust detectors must exceed, not a deployable classifier."

The "Headline numbers, by claim" paragraph now leads with: "(1) *Primary* cross-family pipeline estimate: 64.7%…rule 80.1% (no-calibration variant)…"

Table 1 (tab:headline_decision) is also moved earlier in §1 (before the contributions list) so readers see the full decision tree before encountering the five contribution claims.

---

### W2 — Surface "4 of 5 Features Fail ICC"

**Reviewer:** "Calling it a 5-feature pipeline throughout is misleading when §5.1 reveals that 4 of 5 features fail the ICC threshold. This should be disclosed where the pipeline is first introduced."

**V42 changes:**

1. **methodology.tex §3.2** — Added construct validity note immediately after pipeline description:
   > "**Construct validity note:** of the five LLM-extracted features, only correction-marker density achieves acceptable inter-annotator reliability (Krippendorff's α=0.606, §5.1); the remaining four features—consistency, specificity, confidence, and elaboration—fall below the pre-registered ICC threshold, so pipeline accuracy levels should be read as upper bounds on construct-valid pipeline performance."

2. **abstract.tex** — Added one-sentence ICC disclosure:
   > "Of the five LLM-extracted pipeline features, only correction-marker density achieves acceptable inter-annotator reliability (Krippendorff's α=0.606); the remaining four fail the ICC threshold—so pipeline levels should be read as upper bounds on construct-valid pipeline performance (§5.1)."

3. **discussion.tex §5.1** — The ICC(2,1)=0.71 high-confidence result (pre-registered, n=52 trials where all 3 annotators scored >7 or <3) is now the first named paragraph of the section:
   > **§High-confidence annotation reliability (pre-registered).** "On the n=52 high-confidence subset (all 3 annotators scored correction-marker density >7 or <3), **ICC(2,1)=0.71**—above the acceptable threshold."
   
   The "4 of 5 features fail ICC" finding is now bolded in the same section.

---

### W3 — Fix Transfer Whiplash

**Reviewer:** "§4.6 opens with sycophancy results that look like strong positives (68.5%, 83%, 72%), then immediately reports near-chance persona/FB results. The reader doesn't know until two paragraphs in that the section is mostly negative."

**V42 change in experiments.tex §4.6 opening:**

Added one framing sentence before the sycophancy results:

> "**Sycophancy is the *sole transfer exception***: the refusal-count signal transfers to semi-autonomous sycophancy (68.5% at Llama 3B, 83% at Qwen 14B, 72% at Llama 70B) but does **not** transfer to fully-autonomous persona and false-belief conditions (four of six n=200 Wilson CIs include chance). The results below show this in detail; the headline transfer claim is narrow: sycophancy alignment only."

---

### W4 — Add Instructed-vs-Autonomous Caveat to Abstract

**Reviewer:** "The abstract doesn't say this paper is about instructed roleplay. A safety researcher reading the abstract expecting autonomous deception results will be disappointed."

**V42 change in abstract.tex:**

Added one sentence as the second sentence of the abstract:

> "**All experiments study *instructed roleplay* (models explicitly prompted to defend false claims); the signal does not generalize to fully-autonomous conditions—four of six n=200 persona/false-belief cells have Wilson CIs including chance (§4.6).**"

---

### W5 — Reduce Qwen 32B Over-Weighting

**Reviewer:** "The Qwen 32B structural zero (n=100 single observation) appears repeatedly in the RLHF fragility narrative. It's driving a claim that should require more data."

**V42 changes:**

1. **conclusion.tex** — Added explicit n=100 single-observation caveat to the RLHF-fragility sentence:
   > "…it collapses on models where RLHF suppresses correction language (Qwen 32B: 50%, at chance—a **single n=100 observation**; camera-ready replication on Gemma 2 27B and Mistral-Small-3.1-24B committed, §4.5)…"
   
   Added independent Qwen 14B supporting evidence:
   > "The RLHF-fragility pattern is independently supported by Qwen 14B's partial effect (rule 83%, above the 64.7% cross-family panel mean, consistent with agreeableness pressure without full suppression) and does not depend on the Qwen 32B structural-zero row alone."

2. **experiments.tex §4.5** — Qwen 32B already labeled "supplementary case study" and "single-model observation at n=100 should not yet support conclusion-level claims about RLHF-trained detectors generally pending the camera-ready replication." No additional change needed here.

---

### W6 — Downgrade Sonnet Extractor Reversal to "Diagnostic"

**Reviewer:** "The Sonnet 4.5 row (Mistral L3 82.8%; Haiku/Llama 70B 50.5%) is a genuinely puzzling result. Either investigate it with feature-level decomposition or be clear it's a single-target diagnostic."

**V42 change in experiments.tex §frontier_sonnet:**

Added explicit diagnostic framing:

> "**The inverted extractor pattern (Mistral L3 succeeds; Haiku/Llama 70B collapse) is a single-target observation requiring feature-level decomposition to interpret; we report it as a *diagnostic finding* that motivates future extractor ablation rather than a cross-family pipeline estimate.** Accordingly, the Sonnet 4.5 row is excluded from cross-family panel averages (footnoted ¶ in Table 13) and from the sign test, which characterize the open-weight same-family bias only."

The mechanistic hypothesis (Mistral L3 captures abruptness of first-sentence corrections) remains in the paragraph but is now explicitly framed as speculative and motivating future work, not as an established explanation.

**Q1 — Follow-up commitment for ICC:** Camera-ready commits to a correction-marker-density-only ablation on the existing 689-trial transcript set (already available); no new data collection needed. The correction-marker-only pipeline under Mistral L3 achieves 54.5% LOO vs. 64.7% for the 5-feature pipeline (10.2 pp gap already reported in §5.1), but the feature-level decomposition of the Sonnet extractor divergence (which features Mistral L3 captures that Haiku/Llama 70B do not) requires separate extractor-level analysis on the n=99 Sonnet transcripts.

---

### W7 — Reframe Degenerate Human Baseline

**Reviewer:** "Reporting '+32pp rule advantage over human baseline' as a finding implies the rule is better than humans. But the human baseline is degenerate (all-TRUTH, κ=0.00). This is misleading."

**V42 change in experiments.tex §4.10:**

Replaced the "+32pp over naive crowdworker humans" framing with:

> "The crowdworker baseline is **degenerate**: all three annotators defaulted almost entirely to TRUTH (A: 50/50; B: 48/50; C: 49/50); Fleiss' κ=0.00 (all annotators converged on the majority class). Per-annotator accuracy: 44.0% (Wilson 95% CI [31.2%, 57.7%]). **This result characterizes naive crowdworker behavior under the experimental format, not a meaningful detection accuracy comparison** (Table 12). We report it for completeness and to justify the decision not to use crowdworker annotations as a performance ceiling. The refusal-count rule achieves 76.0% on the same 50 trials; the gap reflects the difference between an automated detector and an *untrained* all-TRUTH baseline, not an intrinsic human-vs-machine capability difference."

---

### W8 — Scope Cross-References in experiments.tex

**Reviewer:** "Scope caveats appear multiple times in experiments.tex. They should be consolidated or pointed back to §1."

**V42 changes in experiments.tex:**

Two targeted cross-reference additions:
1. §4.3 (hedging baseline section opening): added `(scope: §\ref{sec:motivation})` after "the rule is English-only, lexical."
2. §4.5 (scale sweep section): added `(scope: §\ref{sec:motivation})` after "frontier-scale (100B+) behavior remains untested."

The two consolidated scope paragraphs in introduction §1 ("Scope: English-only and lexical-fragile" and "Scope limitation: instructed roleplay vs. autonomous deception") remain unchanged. No new scope text was added.

---

### DC1 — 50% Chance Line in Figure 1 Panel (a)

Added `extra y ticks={50}` with a dashed red line and "chance" label to the pgfplots group plot panel (a) (three-control accuracy collapse). Panel (b) already had this line (it was present in the original §4.6 context). The addition makes the 30–41pp collapse immediately readable against the chance baseline.

---

### DC2 — Table 1 Moved Earlier

Table 1 (tab:headline_decision, "Which headline accuracy to cite, by claim") and its introducing paragraph ("Which number to report, by claim") moved from after the five-contribution list to immediately after the "How to read this paper" paragraph. Readers now encounter the decision tree before the contribution details, allowing them to interpret the contribution numbers in context.

---

### DC3 — Holm-Bonferroni Forward Reference

Added one sentence at the opening of §4.5 (within-family scale patterns):

> "All pairwise scale comparisons use within-family Holm-Bonferroni correction as the primary multiple-testing policy; full justification follows immediately below."

This ensures readers know the correction policy before encountering the first scale comparison p-values.

---

### DC4 — ICC(2,1)=0.71 High-Confidence Subset Promoted

The ICC(2,1)=0.71 result (n=52 high-confidence subset, pre-registered) was buried at the end of §5.1's machine-rater paragraph. It is now the first named paragraph of §5.1:

> **¶ High-confidence annotation reliability (pre-registered).** "On the n=52 high-confidence subset (all 3 annotators scored correction-marker density >7 or <3), **ICC(2,1)=0.71**—above the acceptable threshold. This confirms the pipeline's construct validity holds in the regime where the classifier makes its most confident predictions, though this subset is not the primary validation unit."

---

## Responses to Reviewer Questions

**Q1 (ICC follow-up commitment):** Camera-ready will include a correction-marker-density-only ablation on existing transcripts (n=689; no new data collection). The Sonnet extractor divergence requires feature-level decomposition on the n=99 Sonnet transcripts, committed for camera-ready as Future Direction 6 (§5.8).

**Q2 (Why not call it a regex paper?):** The paper's contribution is the three-control joint evaluation, not the rule. We agree the rule is a sanity-check baseline; the paper's claim is that the entire behavioral detection literature has been reporting numbers without applying these three controls jointly, and the 30–41pp, 9–10pp, and rule-pipeline-parity magnitudes are what joint application reveals. The rule is the instrument that quantifies the ceiling, not the finding itself.

**Q3 (What would make the pipeline useful?):** Under equalization at ≥14B in multi-turn claim-related follow-up regime (+14/+29pp gain documented in §4.5, Appendix D). This is the only regime where the pipeline materially outperforms the rule.

**Q4 (Autonomous deception external validity):** Sycophancy transfer (68.5–83% at 3B/14B) is the sole evidence that any autonomous signal exists. The abstract now makes this explicit: "the signal does not generalize to fully-autonomous conditions." The paper's primary claim is a negative: current behavioral detection is dominated by instruction-following artifacts and does not transfer to truly autonomous deception.

**Q5 (Qwen 32B replication timeline):** Camera-ready replication on Gemma 2 27B-Instruct and Mistral-Small-3.1-24B is committed. Timeline is 4–6 weeks from acceptance. If pattern replicates on ≥1 model, framing upgrades from "single-model observation" to "multi-model pattern"; if not, non-replication will be reported explicitly.

---

## Compilation

V42: 51 pages (unchanged from V41), 0 errors, 0 undefined references (pdflatex × 2). Page count stable because: W2 ICC caveat in methodology (~20 words) and W3/W4 framing sentences (~60 words net) are offset by the Table 1 relocation (no new text) and the human baseline reframe (replacement, not addition).

---

## Spot-Check Verification

1. Abstract sentence 2: "All experiments study *instructed roleplay*…signal does not generalize to fully-autonomous conditions": ✓
2. Abstract ICC caveat: "(4 of 5 pipeline features fail ICC threshold)": ✓
3. Abstract primary headline: "primary cross-family pipeline estimate is **64.7%**"; "80.1% (no-calibration variant)": ✓
4. §4.6 opening: "Sycophancy is the *sole transfer exception*": ✓
5. §frontier_sonnet: "diagnostic finding, not cross-family estimate": ✓
6. §4.10 human baseline: no "+32pp"; says "degenerate (all-TRUTH, κ=0.00); characterizes rater behavior": ✓
7. experiments.tex scope mentions: `(scope: §\ref{sec:motivation})` cross-refs added: ✓
8. Figure 1 panel (a): dashed 50% chance line added via `extra y ticks={50}`: ✓
9. Table 1 (tab:headline_decision) appears before contributions list in introduction: ✓
10. §5.1 opens with "High-confidence annotation reliability" named paragraph; ICC(2,1)=0.71 bolded: ✓
11. methodology.tex §3.2: construct validity note with "4 of 5 features fail ICC": ✓
12. §4.5 opening: "All pairwise scale comparisons use within-family Holm-Bonferroni correction": ✓
13. conclusion.tex: Qwen 32B "single n=100 observation" caveat; Qwen 14B independent support: ✓
14. `REVIEWER_RESPONSE_LETTER_V42.md` exists: ✓
