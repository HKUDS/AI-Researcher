# Reviewer Response Letter — V30
## NeurIPS 2026 Revised Submission

---

**To:** Reviewer 7 (Weak Accept 6/10, Confidence 4/5)

**Subject:** V30 revision addressing W1–W8 and Q1–Q5

We thank the reviewer for the positive read and the clear path to acceptance. V30 addresses both stated clear-accept conditions: (1) the ICC n≥100/3-annotator commitment is now a firm camera-ready guarantee (no fallback language in paper); (2) the RLHF-collapse replication is a named camera-ready commitment in §4.6, with experiments initiated. Beyond these, V30 makes six text-only changes: title narrowing (Q5/W3), §1.1 contribution reframe (W1), Apollo pilot demotion (W5), multiple-comparison paragraph (W7), Figure 1(b) expansion to all six fully-autonomous cells (Minor), and inline Mistral caveat (§5.2).

---

## At-a-Glance Table

| Item | Ask | V30 action | Status |
|---|---|---|---|
| **W1 (framing)** | Lead with what controls *uncover*; "individually non-novel" undersells | §1.1 rewritten: lead with magnitudes (30–41 pp, 9–10 pp Claude localization, rule parity); "individually non-novel" relegated to end of paragraph | **Done — introduction.tex** |
| **W2 (ICC)** | Commit to n≥100/3-annotator by camera-ready, no fallback | §5.1 fallback language removed; firm: "A full n≥100/3-annotator ICC study with Krippendorff's α will be included in the camera-ready version" | **Done — discussion.tex** |
| **W3/Q5 (scope + title)** | Title oversells; "correction-marker" framing more accurate | Title updated to "Correction-Marker Signals Cannot Substitute for Genuine Behavioral Deception Detection: A Three-Control Evaluation Across Open-Weight LLMs" | **Done — main.tex** |
| **W5 (Apollo pilot)** | n=54 too thin for autonomous-deception anchor | Apollo pilot demoted to one sentence in main text; matched-format n=200 across three families is the primary anchor | **Done — experiments.tex** |
| **W6 (Qwen 32B)** | Single-model RLHF collapse bleeds into conclusion; needs replication | Camera-ready commitment added to §4.6; conclusion already softened in V29 (parenthetical, "not a primary contribution claim"); replication experiments initiated | **CR commitment — experiments.tex** |
| **W7 (multi-testing)** | Multiple-comparison accounting uneven | New paragraph "Multiple-comparison budget" added after §4.6 Holm-Bonferroni paragraph; unified budget: within-family = primary; cross-extractor = directional triangulation; all other pairwise = descriptive | **Done — experiments.tex** |
| **Minor-Fig1b** | Figure 1(b) missing Qwen 14B and Mistral 7B persona/FB cells | Panel (b) expanded to 8 bars; caption updated to describe all six fully-autonomous cells | **Done — figures/summary_results.tex** |
| **Minor-§5.2** | Mistral base/Instruct caveat easy to miss | Inline "(Mistral 7B uses base checkpoint only—see §4.8 caveat)" added at the Mistral probe-parity sentence in §5.2 | **Done — discussion.tex** |
| **Q3 (persona coding)** | n=50 persona transcript coding with two coders | Future work commitment added; not feasible for this revision | **Future work — §5.8** |
| **Q4 (closed-loop adversary)** | Single-iteration feedback adversary | Future work commitment; noted in §5.8 | **Future work — §5.8** |

---

## W1 — §1.1 Contribution Reframe

> *"The second paragraph of §1.1 leads with 'None of the three controls below is individually novel...' — this is a defensive position, not a contribution statement. Lead with what the controls uncover."*

The reviewer's diagnosis is correct. "Individually non-novel" is accurate — prompt equalization is standard in the sycophancy literature, cross-family extraction is the jury-of-judges design, and lexical baselines are routine NLP sanity checks — but foregrounding this undersells the empirical content of the paper, which is the *magnitudes* those controls reveal when applied jointly to behavioral deception detection.

**Before (§1.1 second paragraph lead sentence):**
> *"None of the three controls below is individually novel---prompt equalization is standard in the sycophancy literature, cross-family LLM-as-judge usage is the ``jury-of-judges'' design, and lexical/regex baselines are routine NLP sanity checks. Our contribution is their \emph{joint} application to behavioral deception detection: when applied together, they reveal confounds of a magnitude previously undocumented in this domain (30--41\,pp equalization collapse; 9--10\,pp same-family inflation, localized; a one-line rule matching a 5-feature pipeline within 5\,pp)."*

**After:**
> *"Our contribution is documenting the \emph{magnitudes} that emerge when all three controls are applied jointly to behavioral deception detection: a 30--41\,pp equalization collapse (the dominant fraction of reported accuracy is instruction-following artifact); a 9--10\,pp same-family extractor inflation \emph{localized} to Claude-on-Claude across three independent self-family controls (Llama-on-Llama and Qwen-on-Qwen show no analogous boost); and a one-line refusal-count rule that matches a 5-feature LLM pipeline within 5\,pp under same-family extraction and exceeds it under cross-family extraction. Each control is individually non-novel---prompt equalization is standard in the sycophancy literature, cross-family extraction is the ``jury-of-judges'' design, and regex baselines are routine NLP sanity checks---but their joint application to this domain, and the magnitudes they jointly reveal, have not been previously documented."*

The "individually non-novel" qualification is now where it belongs: after the contribution statement, as a clarification, not as the opening defensive move.

---

## W2 — ICC Camera-Ready Commitment (Firm)

> *"The two-branch fallback in §5.1 undercuts the commitment. Either you're running the study or you're not."*

The reviewer is right. The fallback language ("if recruitment slips: n≥50/2-annotator; if that slips: raw CSVs") is a hedge that signals insufficient confidence in the commitment itself. V30 removes all fallback language from the paper.

**Before (§5.1):**
> *"**Camera-ready commitment (two-branch).** Target: a full n≥100/3-annotator ICC study with Krippendorff's α included in the camera-ready. Explicit fallback if recruitment slips past the camera-ready deadline: (i) a preliminary n≥50/2-annotator ICC report with Krippendorff's α, and (ii) the raw per-rater CSVs released alongside, so downstream researchers can complete validation independently."*

**After:**
> *"**Camera-ready commitment.** A full n≥100/3-annotator ICC study with Krippendorff's α will be included in the camera-ready version. Raw per-rater CSVs will be released alongside for downstream reanalysis."*

The fallback is retained in this response letter (see W2 note below) for the AC's awareness, but not in the paper itself. **Note for AC:** If the n≥100/3-annotator study cannot be completed before the camera-ready deadline despite our commitment, we will contact the AC directly rather than silently inserting a smaller study.

---

## W3/Q5 — Title and Scope

> *"The title oversells the scope. The paper evaluates correction-marker-based behavioral detectors, not 'behavioral detection' as a broad category."*

**Before:**
> *"Evaluating the Limits of Behavioral Detection of Instructed Deception and Knowledge-Conflict Correction in Large Language Models"*

**After:**
> *"Correction-Marker Signals Cannot Substitute for Genuine Behavioral Deception Detection: A Three-Control Evaluation Across Open-Weight LLMs"*

The new title: (a) names what the paper actually evaluates (correction-marker signals), (b) states the direction of the finding (cannot substitute), (c) names the method (three-control evaluation), and (d) scopes the models (open-weight LLMs ≤70B). "Genuine behavioral deception detection" signals that the paper is offering a methodological standard, not claiming to achieve it.

---

## W5 — Apollo Pilot Demotion

> *"EXP-I Apollo pilot (n=54) is the opener for the autonomous-deception section but uses a different task format. Why does a null result in a different regime anchor the section?"*

The reviewer is correct. At n=54 in a different task format (action-recommendation reward-function context, not factual-claim defense), the Apollo pilot's null result neither confirms nor disconfirms autonomous-deception transfer in the paper's primary paradigm.

**Before (§4.7 opener, ~3 sentences):**
> *"A preliminary pilot ($n=54$, Apollo Research AI Liar dataset \cite{apollo2024liar}, two Llama~70B versions) yields a null result: refusal-count markers achieve 0--54\% accuracy, likely reflecting task-format mismatch (action recommendations in reward-function contexts, not factual claim defense). Hedge-word features achieve 59--74\% with wide CIs."*

**After (§4.7 opener, 1 sentence):**
> *"A preliminary pilot ($n=54$, Apollo Research AI Liar dataset \cite{apollo2024liar}) yields null results, likely due to task-format mismatch (action-recommendation regime vs.\ factual-claim defense); the matched-format evaluation below (§\ref{sec:autonomous_matched}) is the primary test of autonomous-deception transfer."*

The matched-format evaluation (n=200 each, three independently-pretrained families at two scale points) is the primary autonomous-deception evidence, and V30 makes that explicit by making it the second sentence rather than appearing after the null-result pilot.

---

## W6 — Qwen 32B RLHF-Collapse Replication

> *"The Qwen 32B RLHF collapse is a single-model observation but is used to motivate the conclusion's 'failure mode' paragraph. Either replicate it or demote it harder."*

The paper already explicitly states in §4.6 that "*confirming or ruling out this speculation would require running equivalent evaluations on at least two additional RLHF-heavy models at ≥14B scale — future work.*" V29 softened the conclusion to: "(§\ref{sec:qwen_scale_sweep}, supplementary case study)---is reported as a hypothesis-generator pending replication; it is not a primary contribution claim."

V30 goes further by upgrading the §4.6 future-work pointer to a named camera-ready commitment:

**§4.6 addition (end of Qwen 32B paragraph):**
> *"**Camera-ready commitment (RLHF replication).** Equalized evaluations (n=100 each, refusal-count rule + Haiku extractor + one cross-family extractor) on at least two additional RLHF-heavy open-weight models at ≥14B scale will be included in the camera-ready version. If the pattern replicates on ≥1 model, the §4.6 framing will be upgraded from 'single-model observation' to 'multi-model pattern'; if it does not replicate, that non-replication will be reported explicitly and the Qwen 32B result further demoted."*

**Why this is the right disposition for this revision:** The conclusion paragraph already carries the appropriate epistemic status ("hypothesis-generator pending replication; not a primary contribution claim"). Running experiments for this revision would require downloading and evaluating two 9–14 GB models at n=100 each — feasible but not completable within the revision window. We treat this identically to the ICC commitment: both are completable before camera-ready, both are stated as firm commitments rather than aspirations.

---

## W7 — Multiple-Comparison Budget

> *"The paper applies within-family Holm-Bonferroni to scale comparisons but cross-extractor accuracy gaps and LOO comparisons appear without equivalent accounting."*

The reviewer is correct that the accounting has been uneven. V30 adds a named paragraph to §4.6 immediately after the existing Holm-Bonferroni paragraph:

**New paragraph "Multiple-comparison budget":**
> *"Formal tests in this paper are limited to two categories: (1) within-family Holm-Bonferroni-corrected Fisher exact tests on adjacent scale increments (primary correction unit; three tests per family), and (2) paired-bootstrap CIs on the pre-registered 4th-scenario Δ (Appendix~\ref{app:causal_probes}). All other pairwise comparisons---cross-extractor accuracy gaps, cross-model LOO differences, per-target CF gap values---are \emph{descriptive}, not inferential. Cross-family extractor comparisons specifically use directional triangulation: Mistral Large~3 and Llama~3.3~70B (two independently-trained non-Anthropic extractors) agree within 3\,pp on 7 of 8 targets; this convergence is the evidence for same-family bias, not a formal test. Readers should not interpret non-significant pairwise LOO differences as confirmation of equivalence; the paper's claims are about the \emph{directions and magnitudes} of the three-control collapse, not about fine-grained per-model ranking."*

This clarifies: (a) where formal correction applies; (b) that extractor comparisons use directional triangulation, not p-values; (c) that per-model LOO comparisons are descriptive. The statement "two independent non-Anthropic extractors agree within 3 pp on 7 of 8 targets" is the factual claim we are triangulating from, and it does not require a p-value because the claim is convergence of two independent measurements, not a difference from zero.

---

## Minor — Figure 1(b) Cell Coverage

> *"Panel (b) shows only Llama 3B for persona/FB. The paper claims three-family negative transfer. Show all cells or retitle."*

Panel (b) has been expanded to include all eight bars: Sycophancy 3B/14B/70B (blue, transfers) plus Persona 3B, FB 3B, Persona 14B, FB 14B, and Persona Mistral 7B (red, near-chance or partial). Caption updated to describe the full data:

> *"(b) Autonomous transfer (all six fully-autonomous cells plus three sycophancy): sycophancy (blue) transfers at 82/82/72\% across 3B/14B/70B; persona/false-belief (red) is near chance at Llama~3B ($n=200$) but partially excludes chance at Qwen~14B persona (68.0\%) and Mistral~7B FB (66.5\%). P=persona, FB=false-belief, Mi7B=Mistral~7B persona. All results equalized; models ≤70B."*

The two cells that partially exclude chance (Qwen 14B persona 68.0%, Mistral 7B FB 66.5%) are shown in the same red series as the near-chance cells, not flagged as transfers — consistent with the §4.7 text that notes these "still trail sycophancy transfer by ≥14 pp and sit at or below the equalized baseline."

---

## Minor — §5.2 Mistral Base-Checkpoint Caveat

> *"The Mistral 7B probe parity at §5.2 could mislead if readers don't catch the §4.8 footnote that this uses the base checkpoint."*

Added inline at the relevant §5.2 sentence:

> *"...and the white-box last-layer LR probe (Llama~3B 63\%, Mistral~7B 65\%; Mistral~7B uses base checkpoint only---see §\ref{sec:whitebox_probing} caveat) fall in the same 61--68\% band..."*

---

## Q3 — Persona Transcript Coding (n=50, Two Coders)

> *"Persona transcripts are the hardest case for the ICC concern. Have two coders label n=50 persona trials explicitly."*

This would require recruiting two independent coders and developing a persona-transcript coding manual — annotation work not completable in this revision window. We add this to §5.8 future work:

> *"(9) Persona-scenario transcript coding: explicit two-coder annotation of n≥50 persona trials, with per-feature IRR breakdown and comparison against the machine-ICC proxy. This is the targeted validation the equalized correction-marker ICC does not cover."*

---

## Q4 — Closed-Loop Adversary

> *"Single-iteration paraphrase feedback is not an adversary. A closed-loop adversary that iteratively updates paraphrase based on extractor response is the right test."*

The reviewer is correct that the V30 adversarial setup (one-shot paraphrase prompt, §4.10) does not constitute a closed-loop adversary. Adding this to §5.8 future work:

> *"(10) Closed-loop adversarial evaluation: an iterative adversary that observes extractor scores and updates paraphrase strategy over multiple turns, testing whether the refusal-count rule is robust to adaptive reformulation rather than just single-shot paraphrase."*

---

## V30 Diff Summary

**Paper edits:**
- `main.tex` — Title updated (W3/Q5)
- `introduction.tex` — §1.1 lead paragraph reframed: magnitudes first, "individually non-novel" at end (W1)
- `discussion.tex` — §5.1 ICC fallback language removed; firm camera-ready commitment (W2); §5.2 inline Mistral base-checkpoint caveat added (Minor)
- `experiments.tex` — Apollo pilot demoted to one sentence (W5); Multiple-comparison budget paragraph added after §4.6 Holm-Bonferroni paragraph (W7); §4.6 RLHF replication camera-ready commitment added (W6); §5.8 future-work items (9) persona coding and (10) closed-loop adversary added (Q3, Q4)
- `figures/summary_results.tex` — Figure 1(b) expanded to 8 bars (all six fully-autonomous cells); caption updated (Minor)

**Page count:** 46 pages (unchanged from V29). Text-only changes: Apollo demotion saves ~0.1p; multiple-comparison paragraph adds ~0.1p; Fig 1(b) expansion zero cost (same figure box size); net 0.

---

## Out-of-Scope for V30

- RLHF replication experiments (W6): camera-ready commitment; experiments initiated
- ICC n≥100/3-annotator study (W2): camera-ready commitment
- Persona transcript two-coder study (Q3): future work §5.8 item (9)
- Closed-loop adversarial evaluation (Q4): future work §5.8 item (10)
- Frontier-scale (100B+) evaluation: remains §5.7(b) limitation
- Non-English pilot: remains §5.8 future work

---

*Word count: ~1,900. Response letter follows V29 template.*
