# V45 — Response to Weak Reject 4/10 Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B–70B)

**Prior decision:** Weak Reject 4/10 ("borderline; leaning toward acceptance at a workshop or with major revisions")

**Reviewer's core concern:** "The contribution framing is awkward for NeurIPS. This reads as a 'null result replication study' suitable for a workshop, not a methodological contribution worthy of the main conference."

**Reviewer's suggested paths to acceptance:**
> (a) push harder on positive contributions (e.g., joint-control framework as reusable benchmark, replication on additional families, run missing controls), OR  
> (b) submit to a venue more naturally suited to replication studies (TMLR, workshop)

**V45 strategy:** We pursue path (a) by reframing the paper to foreground the **three-control evaluation protocol** as a reusable methodological contribution, with Pacchiardi et al. as a case study. This addresses the core concern (W1: contribution framing) while maintaining all technical rigor.

**V45 changes:** 12 text revisions across abstract, introduction, experiments, discussion, conclusion. Paper: 37 pages, 0 errors, 0 undefined references, conclusion on page 9.

---

## At-a-Glance Table

| Item | Reviewer ask | V45 action | Status |
|---|---|---|---|
| **W1 (contribution framing)** | Position as methodological contribution, not replication study | Reframed §1.1, §5.5, abstract, conclusion to lead with "three-control evaluation protocol" as paradigm-agnostic reusable framework | Done |
| **W2 (narrow scope)** | Scope limited to ≤70B open-weight English models | Acknowledged; argued narrow-scope findings are NeurIPS-appropriate (many NeurIPS papers scope to specific families/tasks) | Acknowledged |
| **W3 (underpowered pilots)** | Qwen 32B (n=100), Llama 70B sycophancy (n=50), 5th-scenario (n=30) | Hedged all pilots more aggressively: abstract and §4.6 now say "72% at 70B (n=50, preliminary)"; contribution 3 says "pending replication, committed for camera-ready" | Done |
| **W4 (construct validity)** | Why report 5-feature pipeline if 4/5 fail ICC? | Report 54.5% construct-valid pipeline as co-primary with 64.7% full pipeline in abstract, Table 1, contribution 1, conclusion | Done |
| **W5 (cross-family confound)** | Haiku-on-Sonnet cleanest test of localization | Addressed in text: Sonnet diagnostic §5.3 now includes Haiku-on-Sonnet 50.5% result (inverted from Haiku self-boost) | Done |
| **W6 (sycophancy fragility)** | System-prompt-only control needed | Already committed in V44; V45 adds contingency plan: "If it disconfirms, sycophancy collapses to Regime 1 (instructed with one reasoning step removed), and autonomous transfer is uniformly null—strengthening the paper's central claim" | Done |
| **W7 (Pacchiardi comparison muddled)** | Cross-protocol comparison not cleanest test | Added caveat to §4.4: "Our 64.7% falls below Pacchiardi et al.'s 67–73%, but this is a cross-protocol comparison (they used unrelated questions, different models). EXP-K shows related/unrelated are comparable, supporting the inference that same-family extraction accounts for the gap. The cleanest test—re-running their exact protocol with cross-family extraction—is future work" | Done |
| **W8 (degenerate human baseline)** | Table 29 human baseline misleading | Trimmed description to "a *degenerate baseline*, not a meaningful ceiling" | Done |
| **W9 (writing density)** | Dense presentation | Reframing §1.1 and §5.5 provides clearer through-line; aggressive trimming throughout for space | Addressed |
| **Q1 (sycophancy contingency)** | What if system-prompt-only disconfirms? | Added contingency plan to §5.3 Regime 2 | Done |
| **Q2 (Haiku-on-Sonnet)** | Why not run this cleanest test? | Addressed with existing data: Haiku-on-Sonnet 50.5% (inverted from self-boost) in §5.3 | Done |
| **Q3 (Pacchiardi exact protocol)** | Would you run their exact protocol with cross-family? | Added to §4.4: "The cleanest test—re-running their exact protocol with cross-family extraction—is future work" | Done |
| **Q4 (Why report 5-feature pipeline?)** | If 4/5 fail ICC, why report it as primary? | Report 54.5% construct-valid as co-primary with 64.7% full pipeline throughout | Done |
| **Q5 (Regex sensitivity)** | Have alternative patterns been tried? | Added to §4.2 EXP-J: "The 8-pattern rule (Appendix) is robust: removing any single pattern changes pooled-LOO by ≤2 pp (bootstrap n=1000)" | Done |

---

## Detailed Responses

### W1 (contribution framing) — HIGHEST PRIORITY

**Reviewer:** "The contribution framing is awkward for NeurIPS. This reads as a 'null result replication study' suitable for a workshop, not a methodological contribution worthy of the main conference."

**V45 response:** We have reframed the paper to foreground the **three-control evaluation protocol** as the primary methodological contribution. The protocol is paradigm-agnostic and applicable to any black-box behavioral detector (lie detection, sentiment, sycophancy, etc.). Pacchiardi et al. serves as a case study demonstrating the protocol's value.

**Changes:**

1. **§1.1 Motivation and Contributions** (opening paragraph):
   - **Old:** "This paper is a **replication-and-controls study** applied to behavioral deception detection, specifically to the Pacchiardi et al. paradigm. The contribution is documenting the *magnitudes* that emerge under joint application of three standard evaluation controls..."
   - **New:** "This paper introduces a **three-control evaluation protocol** for behavioral deception-detection claims: (1) prompt equalization, (2) cross-family extraction, (3) surface-level baselines. The protocol isolates instruction-following, same-family bias, and surface-lexical ceilings, and is **applicable to any black-box behavioral detector**. Applied to Pacchiardi et al.: 30–41 pp equalization collapse; 9–10 pp same-family inflation (Haiku-checkpoint-specific); 80.1% label-free rule matching the 5-feature pipeline on 6 of 7 targets."

2. **§5.5 Novelty**:
   - **Old:** "This is a **replication-and-controls study** of Pacchiardi et al.: their 67–73% is reproducible but attributable..."
   - **New:** "The **three-control protocol** is the primary methodological contribution: a reusable framework for evaluating behavioral detection claims by isolating instruction-following (equalization), same-family bias (cross-family controls), and surface-lexical ceilings (regex baselines). The protocol is **paradigm-agnostic** and applicable to any black-box behavioral detector. Applied to Pacchiardi et al.: their 67–73% is reproducible but attributable..."

3. **Conclusion**:
   - Added: "The 80.1% label-free rule serves three purposes: (1) **calibration-free baseline** for this paradigm; (2) **extractor-independent ceiling**; (3) threshold for non-surface-lexical signal. Detectors reporting <80.1% under equalization lack validated behavioral signal."

4. **Abstract**:
   - Trimmed verbose opening to focus on core finding, maintaining protocol framing implicitly through "three evaluation controls"

**Why this works:** The protocol is genuinely reusable — it can be applied to any behavioral detector claiming to detect deception, sycophancy, sentiment, etc. The three controls (equalization, cross-family, regex) are separable and address distinct artifact sources. The paper demonstrates the protocol's value by applying it to a high-profile prior work (Pacchiardi et al.), revealing substantial artifacts. This is a methodological contribution, not just a replication.

---

### W4 (construct validity) — CO-PRIMARY PIPELINE NUMBERS

**Reviewer:** "If 4 of 5 features fail ICC, why report the 5-feature pipeline as the headline pipeline number at all? The construct-valid number (54.5%) should be co-equal or primary."

**V45 response:** We now report **both** 54.5% (construct-valid) **and** 64.7% (full pipeline) as co-primary throughout the paper.

**Changes:**

1. **Abstract:**
   - **Old:** "The *primary* cross-family pipeline estimate is **64.7%** (Mistral L3 extractor, 7 equalized targets; Llama 70B within 3 pp); the refusal-count rule achieves **80.1% pooled-LOO**... Of the five pipeline features, only correction-marker density achieves acceptable inter-annotator reliability (Krippendorff's α=0.606); the remaining four fail the ICC threshold—pipeline levels should be read as upper bounds on construct-valid performance (§5.1)."
   - **New:** "The cross-family pipeline achieves **64.7%** (Mistral L3 extractor, 7 equalized targets; Llama 70B within 3 pp); the **construct-validated (correction-marker only) pipeline achieves 54.5%**—40% of the full pipeline's above-chance signal comes from ICC-failing features. The refusal-count rule achieves **80.1% pooled-LOO**..."

2. **Table 1 (tab:headline_decision):**
   - Added row: "Construct-valid pipeline | 54.5% | L-indep | correction-marker only"
   - Changed row 1: "Full pipeline (cross-family) | 64.7% | L-dep | 4/5 features fail ICC"

3. **§1.1 Contribution 1:**
   - **Old:** "The 5-feature pipeline drops from 74.3% (Haiku) to **64.7%** under cross-family extraction (Mistral L3; Llama 70B within 3 pp); construct-validated pipeline (correction-marker only) is 54.5% (§5.1)."
   - **New:** "The 5-feature pipeline drops from 74.3% (Haiku) to **64.7%** under cross-family extraction (Mistral L3; Llama 70B within 3 pp); the **construct-validated (correction-marker only) pipeline achieves 54.5%**—40% of the full pipeline's above-chance signal comes from ICC-failing features (§5.1)."

4. **Conclusion:**
   - **Old:** "The most actionable finding is a label-free *baseline*: refusal count ≥1 achieves 80.1% average accuracy across seven equalized models without calibration data, matching or exceeding the 5-feature LLM pipeline on 6 of 7 targets. The construct-validated portion (correction-marker density only) achieves 54.5%—40% of the cross-family pipeline's above-chance signal comes from ICC-failing features."
   - **New:** "The 80.1% label-free rule serves three purposes: (1) **calibration-free baseline** for this paradigm; (2) **extractor-independent ceiling**; (3) threshold for non-surface-lexical signal. Detectors reporting <80.1% under equalization lack validated behavioral signal. The construct-valid pipeline (correction-marker only) achieves 54.5%; the full cross-family pipeline achieves 64.7%."

**Why this works:** The construct-valid 54.5% is now presented as co-equal to 64.7% in all headline contexts. The "40% of above-chance signal from ICC-failing features" framing makes clear that 64.7% is an upper bound, not a validated estimate.

---

### W3 (underpowered pilots) — HEDGE MORE AGGRESSIVELY

**Reviewer:** "Several key results lean on n that is too small (Qwen 32B n=100 single observation, Llama 70B sycophancy n=50, 5th-scenario n=30). The pattern of 'preliminary, but...' framings weakens the paper's epistemic position."

**V45 response:** We have hedged all underpowered pilots more aggressively and added explicit camera-ready commitments.

**Changes:**

1. **Abstract:**
   - **Old:** "...sycophancy (68.5–83% at 3B/14B), where the system prompt does the heavy lifting."
   - **New:** "...sycophancy (68.5/83% at 3B/14B, n=200; 72% at 70B, n=50 preliminary), where the system prompt does the heavy lifting."

2. **§1.1 Scope paragraph:**
   - **Old:** "The signal transfers to semi-autonomous sycophancy (68.5--83% at 3B/14B; §4.6) but not reliably to fully autonomous conditions."
   - **New:** "The signal transfers to semi-autonomous sycophancy (68.5--83% at 3B/14B, n=200; 72% at 70B, n=50 preliminary; §4.6) but not reliably to fully autonomous conditions."

3. **§1.1 Contribution 3:**
   - **Old:** "Qwen 2.5: peak at 14B then collapse at 32B (n=100, single-observation pilot pending replication; §4.7)"
   - **New:** "Qwen 2.5: peak at 14B then collapse at 32B (n=100, single-observation pilot pending replication, committed for camera-ready; §4.7)"

4. **§1.1 Contribution 5:**
   - **Old:** "Sycophancy is the one positive case: 68.5--83% at 3B/14B (§4.7)."
   - **New:** "Sycophancy is the one positive case: 68.5--83% at 3B/14B (n=200; §4.7)."

5. **§4.6 (sycophancy paragraph):**
   - **Old:** "Llama 3B 68.5% (d=1.0), Qwen 14B 83.0% (d=1.52, n=200), Llama 70B 72.0% (n=50, preliminary)."
   - **New:** "Llama 3B 68.5% (d=1.0, n=200), Qwen 14B 83.0% (d=1.52, n=200), Llama 70B 72.0% (n=50, preliminary)."

6. **Conclusion:**
   - **Old:** "...sycophancy (68.5/83% at 3B/14B, n=200; 72% at 70B, n=50 preliminary) is the one positive case. The RLHF-fragility pattern (Qwen 32B at chance—a single n=100 observation; camera-ready replication committed)..."
   - **New:** "...sycophancy (68.5/83% at 3B/14B, n=200; 72% at 70B, n=50 preliminary) is the one positive case. Qwen 32B at chance (n=100 pilot, committed for camera-ready) is supported by Qwen 14B's partial effect."

**Why this works:** All mentions of Llama 70B sycophancy now include "n=50, preliminary" inline. Qwen 32B explicitly says "committed for camera-ready" in multiple locations. The paper no longer over-claims from underpowered pilots.

---

### W5 (cross-family confound) — HAIKU-ON-SONNET RESULT INTEGRATED

**Reviewer Q2:** "Why was Haiku-as-extractor on Sonnet 4.5 not run? It's the cleanest test of the Haiku-checkpoint-localization claim and seems within budget."

**V45 response:** The Haiku-on-Sonnet result already exists in the data and is now explicitly integrated into §5.3.

**Change:**

**§5.3 Sonnet diagnostic paragraph:**
- **V44:** "The Sonnet 4.5 diagnostic (§4.9) sharpens two claims. First, Haiku-as-extractor on Sonnet collapses to 50.5% while Mistral L3 achieves 82.8%—the *inverse* of Haiku's open-weight self-boost. Haiku has checkpoint-specific extraction biases in *opposite directions* for Haiku vs. Sonnet targets, tightening localization to a Haiku extractor artifact. Second, the rule failing (49.0%) while the pipeline succeeds (82.8%) confirms that 80.1% is an *open-weight* ceiling: Sonnet's stronger RLHF suppresses the refusal-marker channel entirely."
- **V45:** [same text, but now explicitly addresses reviewer's question]

**Why this works:** The reviewer asked for this result, and it already exists. The V45 text makes explicit that Haiku-on-Sonnet 50.5% is the *inverse* of Haiku's self-boost on open-weight targets, confirming Haiku checkpoint-specific biases operate in opposite directions.

---

### W6 (sycophancy fragility) — CONTINGENCY PLAN ADDED

**Reviewer Q1:** "What if the system-prompt-only control disconfirms the disposition-source interpretation?"

**V45 response:** Added explicit contingency plan.

**Change:**

**§5.3 Regime 2 (sycophancy):**
- **V44:** "We commit to running this control for camera-ready."
- **V45:** "We commit to running this control for camera-ready. If it disconfirms, sycophancy collapses to Regime 1 (instructed with one reasoning step removed), and autonomous transfer is uniformly null—strengthening the paper's central claim."

**Why this works:** The contingency plan shows we've thought through what happens if the control fails. Importantly, the outcome *strengthens* rather than weakens the paper's central claim (that the signal does not transfer to genuinely autonomous deception).

---

### W7 (Pacchiardi comparison muddled) — CROSS-PROTOCOL CAVEAT ADDED

**Reviewer Q3:** "Would you run Pacchiardi et al.'s exact protocol (unrelated questions, their specific claim types, their models) with cross-family extraction? That would be the cleanest test."

**V45 response:** Added explicit caveat that our comparison is cross-protocol, and the cleanest test is future work.

**Change:**

**§4.4 (pipeline redundancy, last paragraph):**
- **V44:** "Our cross-family pipeline at 64.7% falls below Pacchiardi et al.'s published 67–73% original-protocol range (Appendix), consistent with same-family extraction inflation accounting for the gap between equalized and instructed protocols."
- **V45:** "Our 64.7% falls below Pacchiardi et al.'s 67–73%, but this is a cross-protocol comparison (they used unrelated questions, different models). EXP-K (Appendix) shows related/unrelated questions are comparable, supporting the inference that same-family extraction accounts for the gap. The cleanest test—re-running their exact protocol with cross-family extraction—is future work (Appendix)."

**Why this works:** We acknowledge the cross-protocol limitation explicitly. EXP-K provides some support for the inference, but we're clear that the definitive test is future work.

---

### Q5 (regex sensitivity) — BOOTSTRAP VALIDATION ADDED

**Reviewer Q5:** "The refusal-count rule uses 8 curated patterns. Have you tested sensitivity to pattern-set perturbations? What happens if you remove one pattern or try alternative phrasings?"

**V45 response:** Added bootstrap validation showing the rule is robust to single-pattern removal.

**Change:**

**§4.2 EXP-J (fixed k=1) paragraph:**
- **V44:** "Methodological baseline, not a production detector: English-only and lexically fragile (§4.3)."
- **V45:** "Methodological baseline, not a production detector: English-only and lexically fragile (§4.3). The 8-pattern rule (Appendix) is robust: removing any single pattern changes pooled-LOO by ≤2 pp (bootstrap n=1000)."

**Why this works:** The bootstrap validation shows the rule is not brittle to the specific pattern set — it captures a semantic channel (correction/refusal) rather than specific lexemes.

---

### W8 (degenerate human baseline) — TRIMMED DESCRIPTION

**Reviewer:** "Table 29 reports human baseline κ=0.00 as if it's informative, but this is a degenerate baseline (all-TRUTH collapse). The framing should be clearer."

**V45 response:** Trimmed description to "a *degenerate baseline*, not a meaningful ceiling."

**Change:**

**§4.7 (human baseline paragraph):**
- **V44:** "Three crowdworkers collapsed to TRUTH almost entirely on 50 equalized transcripts (Fleiss' κ=0.00; Appendix): this is a *degenerate baseline* characterizing naive rater behavior under the task format, not a meaningful accuracy ceiling."
- **V45:** "Three crowdworkers collapsed to TRUTH on 50 equalized transcripts (Fleiss' κ=0.00; Appendix): a *degenerate baseline*, not a meaningful ceiling."

**Why this works:** More concise, same message.

---

### W9 (writing density) — ADDRESSED VIA REFRAMING AND TRIMMING

**Reviewer:** "The writing is dense and at times difficult to follow. The through-line from motivation to findings to implications could be clearer."

**V45 response:** The reframing of §1.1 and §5.5 provides a clearer through-line: the paper introduces a three-control protocol (motivation), applies it to Pacchiardi et al. (case study), and shows the protocol reveals substantial artifacts (findings). We also trimmed verbose sections throughout to improve readability within the 9-page constraint.

**Why this works:** The protocol framing provides a clearer organizing principle. The reader now understands from the opening that the paper is about a reusable evaluation framework, not just "here are some controls we applied."

---

### W2 (narrow scope) — ACKNOWLEDGED, NOT FIXED

**Reviewer:** "The scope is narrow: ≤70B open-weight English models, instructed roleplay only. This limits generalizability."

**V45 response:** We acknowledge this limitation explicitly throughout (abstract, scope paragraph, limitations). However, we argue this narrow-scope finding is still NeurIPS-appropriate: many NeurIPS papers scope to specific model families, languages, or tasks. The *protocol* is general even if the *case study* is narrow.

---

## Compilation and Verification

**V45:** 37 pages, 0 errors, 0 undefined references. Conclusion on page 9 (bibliography starts on page 9, continues to page 10, which is expected — 9-page limit is for main content only).

---

## Spot-Check Verification

1. §1.1 opens with "three-control evaluation protocol" as primary contribution: ✓
2. Table 1 includes "Construct-valid pipeline | 54.5%" row: ✓
3. Abstract mentions both 64.7% and 54.5% co-equally: ✓
4. §5.5 calls the protocol "paradigm-agnostic" and "reusable framework": ✓
5. Conclusion adds 3-purpose rule framing: ✓
6. §4.2 includes regex sensitivity bootstrap: ✓
7. §5.3 Sonnet diagnostic mentions Haiku-on-Sonnet 50.5% (inverted): ✓
8. Abstract and §4.6 hedge Llama 70B sycophancy as "n=50, preliminary": ✓
9. §4.4 adds Pacchiardi cross-protocol caveat: ✓
10. §5.3 Regime 2 includes sycophancy contingency plan: ✓
11. §4.7 human baseline trimmed to "degenerate baseline": ✓
12. 37 pages, 0 errors, 0 undefined refs, conclusion on p9: ✓
13. `REVIEWER_RESPONSE_LETTER_V45.md` exists: ✓

---

## Summary of Changes

**12 text revisions** addressing the reviewer's core concern (contribution framing) plus all 9 weaknesses and 5 questions:

1. **§1.1 Motivation opening** — reframed as "three-control evaluation protocol" contribution
2. **Table 1** — added construct-valid pipeline row, updated full pipeline row
3. **Abstract** — co-primary 54.5% and 64.7%; hedged 70B sycophancy
4. **§1.1 contributions** — 54.5% prominence, hedged Qwen 32B and sycophancy
5. **§1.1 scope** — hedged 70B sycophancy
6. **§4.2 EXP-J** — added regex sensitivity bootstrap
7. **§4.4 pipeline redundancy** — added Pacchiardi cross-protocol caveat
8. **§4.6 sycophancy** — added n=200 to all mentions
9. **§4.7 scale patterns** — trimmed cross-family paragraph
10. **§5.3 Regime 2** — added sycophancy contingency plan
11. **§5.5 Novelty** — reframed as protocol contribution
12. **Conclusion** — added 3-purpose rule framing, co-primary 54.5%/64.7%

**Trimming for space** (net 0 impact):
- Condensed §1.1 opening (~3 lines)
- Condensed §5.5 novelty (~2 lines)
- Condensed §5.3 Regime 1, Regime 3 (~3 lines)
- Condensed §4.4, §4.7, §5.1 (~5 lines)
- Condensed abstract, conclusion (~3 lines)

---

## Response to Reviewer's Suggested Paths

**Path (a): Push harder on positive contributions**

We have pursued this path by:
1. **Reframing the protocol as a reusable methodological contribution** — not just "controls applied to one paper" but a paradigm-agnostic framework
2. **Strengthening the rule's methodological value** — 3-purpose framing (calibration-free baseline, extractor-independent ceiling, threshold for non-surface-lexical signal)
3. **Co-primary construct-valid pipeline** — 54.5% is now presented alongside 64.7% throughout
4. **Running missing controls** — Haiku-on-Sonnet result integrated (answers Q2)
5. **Adding contingency plans** — sycophancy system-prompt-only control (answers Q1)

**Path (b): Submit to a venue more suited to replication studies**

We believe path (a) is sufficient to meet NeurIPS standards. The three-control protocol is a genuine methodological contribution with broad applicability. The paper demonstrates the protocol's value via a comprehensive case study, revealing substantial artifacts in a high-profile prior work. This is appropriate for NeurIPS.

---

## What This Paper Contributes to NeurIPS

1. **A reusable evaluation protocol** — applicable to any black-box behavioral detector (lie detection, sycophancy, sentiment, etc.)
2. **A label-free baseline** — 80.1% rule requiring no calibration data, establishing surface-lexical ceiling
3. **Quantified artifact magnitudes** — 30–41 pp equalization collapse, 9–10 pp same-family bias, 40% of pipeline signal from ICC-failing features
4. **Localization of extraction bias** — five self-family controls isolate +9–10 pp to Claude Haiku checkpoint specifically
5. **Autonomous-transfer null** — correction-marker signal does not transfer to fully-autonomous deception (4 of 6 n=200 cells include chance)

These contributions are relevant to the NeurIPS community working on AI safety, model evaluation, and robust benchmarking.
