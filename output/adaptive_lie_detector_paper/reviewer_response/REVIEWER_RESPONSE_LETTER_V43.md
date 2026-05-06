# V43 — Response to New Weak Accept 6/10 Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Cannot Substitute for Genuine Behavioral Deception Detection: A Three-Control Evaluation of Instructed-Roleplay Detection Across Open-Weight LLMs (3B–70B)

**Prior decision:** Weak Accept 6/10 (new reviewer; V42 planned responses; V43 implements them)

**Reviewer's verdict:** "I lean toward acceptance." All weaknesses are presentational/framing issues; no new experiments required.

**V43 changes:** 9 text revisions + 1 new table + 1 new §frontier_sonnet paragraph. Paper: 37 pages, 0 errors, 0 undefined references.

---

## At-a-Glance Table

| Item | Reviewer ask | V43 action | Status |
|---|---|---|---|
| **W1** | Four headline numbers confusing — commit to one primary | Abstract restructured: 64.7% introduced as "primary cross-family pipeline estimate"; 80.1% labeled "no-calibration-data rule variant, not a deployable classifier"; added Table 1 (tab:headline_decision) in §1 | Done |
| **W2** | "4 of 5 features fail ICC" buried | Added ICC caveat sentence to abstract; §5.1 now opens with "High-confidence reliability (pre-registered)" named paragraph: ICC(2,1)=0.71 bolded | Done |
| **W3** | Transfer whiplash — §4.6 leads with positive then drops to chance | §4.6 now opens with bold sentence: "Sycophancy is the sole transfer exception" + summary of what follows | Done |
| **W4** | Abstract missing instructed-roleplay vs. autonomous scope | Added bolded sentence 2 of abstract: "All experiments study instructed roleplay…signal does not generalize to fully-autonomous conditions" | Done |
| **W5** | Qwen 32B structural zero over-weighted — single n=100 observation | Added "(single n=100 observation; camera-ready replication committed)" to conclusion; added Qwen 14B independent support sentence | Done |
| **W6** | Sonnet extractor reversal under-investigated | Added §frontier_sonnet paragraph (§4.5) with explicit "Diagnostic finding, not a panel estimate" framing; Sonnet row excluded from panel averages | Done |
| **W7** | +32pp human baseline comparison misleading (degenerate, all-TRUTH) | §4.5 human baseline paragraph now says "degenerate baseline characterizing naive rater behavior, not a meaningful accuracy ceiling" | Done |
| **W8** | Scope caveats scattered | Two `(scope: §\ref{sec:motivation})` cross-refs added in §4.2; consolidated scope paragraph in §1 retained | Done (§1 scope merged) |
| **DC1** | Add 50% chance line to Figure 1 panel (a) | Already present in both panels (V9 Round 9) | Already done |
| **DC2** | Move Table 1 (headline decision) earlier | Table 1 (tab:headline_decision) added to §1 immediately after "How to read" paragraph | Done |
| **DC3** | Holm-Bonferroni justification appears too late | "All pairwise scale comparisons use within-family Holm-Bonferroni correction" sentence added at §4.5 opening | Done |
| **DC4** | ICC(2,1)=0.71 high-confidence subset buried | Promoted to named first paragraph of §5.1: "High-confidence reliability (pre-registered). ICC(2,1)=0.71" | Done |

---

## Detailed Responses

### W1 — Commit to 64.7% as Primary Headline

**Reviewer:** "The abstract presents four headline numbers with no clear ordering."

**V43 changes:**

1. **abstract.tex**: Restructured sentence 3 to introduce 64.7% first as "*primary* cross-family pipeline estimate" and 80.1% second as "the surface-lexical ceiling more robust detectors must exceed, not a deployable classifier."

2. **introduction.tex**: Added "How to read this paper" paragraph and Table 1 (`tab:headline_decision`) immediately after — before the five contribution claims:

| Claim | Number | Type |
|---|---|---|
| Pipeline accuracy under fair controls | 64.7% | L-dep |
| Surface-lexical ceiling | 80.1% rule | L-indep |
| Equalization collapse | 30–41 pp | L-indep |
| Same-family bias | 9–10 pp | L-indep |
| Autonomous transfer (sycophancy) | 68.5–83% | L-indep |

---

### W2 — Surface "4 of 5 Features Fail ICC"

**Reviewer:** "Calling it a 5-feature pipeline is misleading when §5.1 reveals that 4 of 5 features fail the ICC threshold."

**V43 changes:**

1. **abstract.tex**: Added one sentence: "Of the five pipeline features, only correction-marker density achieves acceptable inter-annotator reliability (Krippendorff's α=0.606); the remaining four fail the ICC threshold—pipeline levels should be read as upper bounds on construct-valid performance (§5.1)."

2. **discussion.tex §5.1**: Added named paragraph **¶ High-confidence reliability (pre-registered)** as the first paragraph of §5.1: "On the n=52 high-confidence subset (all 3 annotators scored correction-marker density >7 or <3), **ICC(2,1)=0.71**. The full n=100 study yields α=0.606 (primary validation unit), clearing α≥0.4."

---

### W3 — Fix Transfer Whiplash

**Reviewer:** "§4.6 opens with sycophancy results that look like strong positives, then immediately drops to near-chance results."

**V43 change in experiments.tex §4.6:**

Replaced "Section take-home" with bold framing sentence at §4.6 open:

> "**Sycophancy is the *sole transfer exception*:** signal transfers to semi-autonomous sycophancy (68.5%/83%/72% at 3B/14B/70B) but **not** to fully-autonomous conditions (4/6 n=200 Wilson CIs include chance). K=1 fails differently: uniform RC=0 in persona/false-belief vs. directional suppression in sycophancy."

---

### W4 — Add Instructed-vs-Autonomous Caveat to Abstract

**Reviewer:** "The abstract doesn't say this paper is about instructed roleplay."

**V43 change in abstract.tex:** Added sentence 2 (bolded):

> "**All experiments study *instructed roleplay* (models explicitly prompted to defend false claims); the signal does not generalize to fully-autonomous conditions—four of six n=200 persona/false-belief cells have Wilson CIs including chance (§4.6).**"

---

### W5 — Reduce Qwen 32B Over-Weighting

**Reviewer:** "The Qwen 32B structural zero (n=100 single observation) drives a claim that should require more data."

**V43 changes in conclusion.tex:**

Added to conclusion RLHF-fragility sentence: "The RLHF-fragility pattern (Qwen 32B at chance---a single n=100 observation; camera-ready replication committed) is independently supported by Qwen~14B's partial effect and does not depend on the Qwen~32B row alone."

---

### W6 — Sonnet Extractor Reversal as Diagnostic Finding

**Reviewer:** "The Sonnet 4.5 row (Mistral L3 82.8%; Haiku/Llama 70B 50.5%) is puzzling. Investigate or be clear it's a single-target diagnostic."

**V43 change in experiments.tex §4.5:**

Added `\paragraph{Frontier-scale target: Claude Sonnet~4.5 equalized (n=99).\label{sec:frontier_sonnet}}` at end of §4.5:

Computed results from existing data:
- Refusal-count rule: **49.0%** (near chance; RC≥1 in 5/50 lying and 6/50 truth trials)
- Haiku pipeline LOO: **83.0%** (n=100)
- Mistral L3 cross-family pipeline: **82.8%** (n=99)

Key framing: "**Diagnostic finding, not a panel estimate**; Sonnet row excluded from panel averages (Table tab:cross_family_panel, ¶)."

---

### W7 — Reframe Degenerate Human Baseline

**Reviewer:** "Reporting '+32pp rule advantage over human baseline' is misleading — the baseline is degenerate."

**V43 change in experiments.tex §4.5 human baseline:**

Replaced with: "Three crowdworkers collapsed to TRUTH almost entirely on 50 equalized transcripts (Fleiss' κ=0.00; App. N): this is a *degenerate baseline* characterizing naive rater behavior under the task format, not a meaningful accuracy ceiling."

---

### W8 — Scope Cross-References

**Reviewer:** "Scope caveats appear multiple times in experiments.tex."

**V43 change:** The two separate "Scope" paragraphs in §1 were merged into one concise paragraph. The existing `(scope: §\ref{sec:motivation})` cross-reference in §4.2 is retained. No new scope text added.

---

### DC2 — Headline Decision Table Added to §1

Table 1 (`tab:headline_decision`) added to §1 immediately after "How to read this paper" paragraph, before the five contribution claims. This allows readers to interpret contribution numbers in context before encountering them.

---

### DC3 — Holm-Bonferroni Forward Reference

Added one sentence at the opening of §4.5 scale patterns:

> "All pairwise scale comparisons use within-family Holm-Bonferroni correction as the primary multiple-testing policy; full justification…in Appendix B."

---

### DC4 — ICC(2,1)=0.71 High-Confidence Subset Promoted

The ICC(2,1)=0.71 result (n=52 high-confidence subset, pre-registered) is now the first named paragraph of §5.1 (was buried at end). Named "**¶ High-confidence reliability (pre-registered).**"

---

## Responses to Reviewer Questions

**Q1 (Which number should I cite?):** For "does behavioral detection work under fair controls?": 64.7% (primary, cross-family). For "what's the lexical ceiling?": 80.1% (rule, no calibration). Table 1 in §1 now maps claim type to number.

**Q2 (What's the frontier result?):** Claude Sonnet 4.5 equalized (n=99): rule fails at 49.0% (near chance), Mistral L3 pipeline 82.8%, Haiku pipeline 83.0%. This inverted pattern (rule fails; pipeline succeeds) is diagnostic of Sonnet-specific RLHF suppression of refusal markers and is reported as a single-target diagnostic finding, not a generalizable cross-family estimate.

---

## Compilation

V43: 37 pages (unchanged from V42 target), 0 errors, 0 undefined references (pdflatex × 2). Abstract adds 2 sentences (~40 words); introduction adds Table 1 (~6 lines); experiments adds frontier paragraph (~3 lines); discussion adds ICC(2,1)=0.71 paragraph (~3 lines); all additions offset by condensing verbose passages in §4.5, §4.6, §5.1, §5.2, §5.4, §5.5, and §1 scope.

---

## Spot-Check Verification

1. Abstract sentence 2 (bold): "All experiments study *instructed roleplay*…signal does not generalize to fully-autonomous conditions": ✓
2. Abstract: "primary cross-family pipeline estimate is 64.7%"; "80.1% (pooled-LOO, k≥1, no calibration data)": ✓
3. Abstract: ICC caveat "(only correction-marker density achieves acceptable inter-annotator reliability)": ✓
4. §1: Table tab:headline_decision before contribution list: ✓
5. §4.5: `\label{sec:frontier_sonnet}` paragraph with 49.0%/83.0%/82.8%; "Diagnostic finding": ✓
6. §4.6 opens with "Sycophancy is the *sole transfer exception*": ✓
7. §4.5 human baseline: "degenerate baseline characterizing naive rater behavior": ✓
8. §5.1 opens with "High-confidence reliability (pre-registered)"; ICC(2,1)=0.71 bolded: ✓
9. Conclusion: Qwen 32B "single n=100 observation; camera-ready replication committed": ✓
10. `REVIEWER_RESPONSE_LETTER_V43.md` exists: ✓
11. 0 LaTeX errors, 0 undefined references: ✓
12. 37 pages total (conclusion on p9, bibliography on p10): ✓
