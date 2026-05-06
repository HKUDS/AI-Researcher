# Reviewer Response Letter — V29
## NeurIPS 2026 Revised Submission

---

**To:** Reviewer 6 (Weak Reject 5/10, Confidence 4/5)

**Subject:** V29 revision addressing M1–M6 and Q1–Q4

We thank the reviewer for the detailed structural critique. V29 makes no new experiments — all changes are structural repositioning and text edits. The most substantive changes are: (1) §3.2 ADAGE pipeline description moved to Appendix N, replaced with a 3-sentence pointer; (2) §4.7 causal-probe subsections (4th/5th scenario, 2×2 factorial) moved to Appendix O (new `app:causal_probes`), replaced with 1-sentence summaries + cross-refs; (3) §5.1 ICC machine–human gap strengthened as evidence of same-family bias, not two contradictory signals; (4) §1 stale numbers fixed (92.9% Sonnet-Haiku removed; 74.5% → 74.3%); (5) conclusion Qwen 32B use softened to parenthetical; (6) §4.9 human baseline +32 pp claim qualified as "naive crowdworkers."

---

## At-a-Glance Table

| Item | Ask | V29 action | Status |
|---|---|---|---|
| **M1 (scope gap)** | Frontier-scale and internals-methods comparison missing | §5.5 already has "measurement standard" framing (V27); §5.7(b) already notes frontier-scale untested; no new claim needed — noted in response | **Verified — already addressed** |
| **M2 (ADAGE prominence)** | §3.2 detailed pipeline description contradicts §5.5 "not a contribution" | §3.2 moved to `app:adage_details` (Appendix N); main text §3.2 replaced with 3-sentence pointer: what ADAGE does, 5 features, why it's the measurement vehicle | **Done — methodology.tex, appendix.tex** |
| **M3 (§4.7 space)** | 3 pages for causal probes with no validated causal account | 4th-scenario, 5th-scenario, 2×2 factorial blocks moved to `app:causal_probes` (Appendix O); each replaced by 1-sentence summary + cross-ref in §4.7 | **Done — experiments.tex, appendix.tex** |
| **M4 (construct validity)** | Machine-ICC 0.79 and human ICC 0.114 are contradictory | §5.1 pointer sentence strengthened: gap between machine-ICC and human-ICC is itself evidence of same-family scoring bias | **Done — discussion.tex** |
| **M5 (Qwen 32B rhetoric)** | Conclusion uses Qwen RLHF-collapse structurally when demoted to supplementary | Conclusion paragraph softened: Qwen 32B claim now parenthetical with §4.6 pointer | **Done — conclusion.tex** |
| **M6 (human baseline caveat)** | "+32 pp rule-beats-human" misleading without "naive annotators" qualifier | Added caveat at §4.9: "naive crowdworker annotators; trained domain-expert annotators would likely score higher" | **Done — experiments.tex** |
| **Q4 (K=1 consistency)** | K=1 fails below chance in §4.7.3 but best rule in §4.3 — apparent contradiction | Added footnote in §4.7 (2×2 cross-ref paragraph): K=1 below-chance is sycophancy-specific mechanism (RC=0 on truthful trials under sycophancy framing), not contradictory with K=1's 80.1% in equalized regime where truthful trials do produce RC≥1 | **Done — experiments.tex** |
| **Minor (stale numbers)** | 74.5%/92.9% Sonnet-Haiku in introduction.tex §1 "How to read" | Fixed: `74.5%` → `74.3%`; `92.9% Sonnet-Haiku` removed from level-dependent list; `\ref{sec:icc_owned}` → `\ref{sec:icc_caveat}` | **Done — introduction.tex** |

---

## M1 — Scope Gap (Frontier-Scale + Internals Methods)

> *"The paper lacks comparison to model-internals methods (representation probing, activation analysis). Frontier-scale behavior is untested."*

These limitations are already explicitly stated in the paper:
- §5.7(b): "Frontier-scale models (100B+) are untested; all results are from models ≤70B parameters."
- §5.2: white-box probing comparison is included and lands in the same 61–68% band as the refusal-count rule (no white-box probe exceeds the rule by more than ±4 pp; §4.8).
- §5.5 already reads: "This paper establishes a *measurement standard* for behavioral deception detection" — the framing is methodological commentary, not a competitive system claim.

The reviewer's concern is that the paper reads as a systems paper claiming state-of-the-art. V29 does not change the scope (which is intentionally ≤70B, English, instructed), but the §3.2 ADAGE move (M2 below) and §4.7 consolidation (M3) directly reduce the systems-paper feel by removing the detailed pipeline description from the front matter.

**No text change beyond M2/M3** — the scope statement is already present; the structural changes address the perception issue.

---

## M2 — §3.2 ADAGE Pipeline Description Moved to Appendix N

> *"§3.2 gives a detailed pipeline description for a method the paper says in §5.5 is not a contribution. This is structurally contradictory."*

**Before (§3.2 main text, ~5 lines):**
> *"The ADAGE pipeline produces, for each trial, five LLM-extracted features on a 0--10 scale: consistency, specificity, correction-marker density, confidence, and elaboration. These feature names are the ones referenced by the experiments and probe sections; the extractor LLM scores each assistant response across up to 8 interrogator turns and trial-level means feed a logistic-regression classifier. The pipeline is the measurement vehicle, not the contribution..."*

**After (§3.2 main text, 3 sentences):**
> *"The ADAGE adaptive interrogation pipeline (detailed in Appendix~\ref{app:adage_details}) produces five LLM-extracted features per trial---consistency, specificity, correction-marker density, confidence, and elaboration---which feed a logistic-regression classifier. The pipeline is the \emph{measurement vehicle} through which the three evaluation controls are applied, not a proposed contribution; a one-line refusal-count regex matches or exceeds it on 6 of 7 equalized models (§\ref{sec:hedging_baseline}). Feature extraction uses an LLM from a specified model family; the extractor choice is the locus of the cross-family extraction control."*

The full pipeline description (feature definitions, stopping rule, classifier, turn structure, construct validity note, target-model pointer) is now in **Appendix N (§app:adage_details)**. Readers who need implementation details can find them; readers who only care about the evaluation controls see a three-sentence summary that foregrounds the pipeline's role as measurement apparatus.

---

## M3 — §4.7 Causal Probe Details Moved to Appendix O

> *"Three pages of causal probes (4th/5th scenario, 2×2 factorial) with no validated causal account. If neither axis is confirmed, why does this take so much space in the main text?"*

The reviewer is correct that the negative results from two pre-registered probes and a third mixed-confirmation test do not justify 3 main-text pages when neither yields a validated causal account. V29 moves all three probe blocks to **Appendix O (`app:causal_probes`)** and replaces each with a one-sentence summary in §4.7.

**Before:** §4.7 contained three subsections:
- `\subsubsection{Pre-Registered 4th Scenario: Knowledge-Conflict Clarity}` — full design, table, interpretation (~0.8 pages)
- `\subsubsection{Pre-Registered 5th Scenario: Disposition-Source (Pilot)}` — full design, table, interpretation (~0.8 pages)
- `\paragraph{Pre-Registered 2×2 Factorial...}` — full design, table, interpretation, full 12-cell table (~1.0 page)

**After:** §4.7 contains three paragraph-level summaries:

> *"\paragraph{Pre-registered 4th scenario (knowledge-conflict clarity).} Full design, Table~\ref{tab:exp_i_4th_scenario}, and interpretation are in Appendix~\ref{app:causal_probes}. Summary: holding disposition-source (sycophancy) and turn-count fixed, varying only claim clarity on n=50/condition rejects the pre-registered Δ>0 prediction (pooled Δ=−4.2 pp, bootstrap CI [−14.9, +5.9], includes zero)."*

> *"\paragraph{Pre-registered 5th scenario (disposition-source pilot).} Full design, Table~\ref{tab:exp_i_5th_scenario}, and interpretation are in Appendix~\ref{app:causal_probes}. Summary: on Qwen 2.5 14B (n=30/condition), persona > sycophancy at n=30 rejects the pre-registered one-sided prediction."*

> *"\paragraph{Pre-registered 2×2 clarity×turns factorial.} Full design, all 12 cells (Table~\ref{tab:factorial_2x2}), and interpretation are in Appendix~\ref{app:causal_probes}. Summary: dominant finding is a turns main effect (+30–35 pp on all three models); clarity main effect near-zero."*

All tables and full interpretations remain available in Appendix O; a reader wanting the details has them. The net saving is ~2.5 main-text pages.

---

## M4 — §5.1 ICC Machine–Human Gap as Same-Family Bias Evidence

> *"You report machine-ICC=0.79 to reassure the reader, then ICC=0.114 as a caveat. These are contradictory signals, not additive evidence."*

The reviewer's reading was correct under the V28 framing. V29 makes the relationship explicit:

**Before (§5.1 pointer sentence):**
> *"A supplementary machine-rater ICC proxy (Appendix~\ref{app:machine_icc}) achieves pooled ICC(2,1)=0.79 under LLM raters; as discussed there, this reflects shared training biases rather than human IRR and does not substitute for the n≥100/3-annotator study."*

**After:**
> *"A supplementary machine-rater ICC proxy (Appendix~\ref{app:machine_icc}) achieves pooled ICC(2,1)=0.79 under LLM raters. The gap between machine ICC (0.79) and human ICC (0.114) is itself evidence of same-family scoring bias: LLM raters share systematic training biases with the target models---the same phenomenon that produces the 9--10 pp same-family extractor inflation documented in §\ref{sec:cross_family_equalized}---and these shared biases inflate agreement on the correction-marker feature in a way that naive human annotators do not. The machine proxy therefore does not substitute for the n≥100/3-annotator study; its informative content is subtractive (Appendix~\ref{app:machine_icc})."*

The gap between 0.79 and 0.114 is not two contradictory measurements of the same thing — it is a demonstration that LLM raters systematically inflate ICC in the same direction as same-family extractor bias, which is itself supporting evidence for the cross-family extraction control.

---

## M5 — Conclusion Qwen 32B Softened

> *"The conclusion uses Qwen 32B structurally even though it was demoted to a supplementary case study. Pick one."*

**Before (conclusion, paragraph 2):**
> *"The Qwen~32B collapse---where RLHF optimization entirely eliminates surface-level detection signals despite the model retaining factual knowledge---is a striking single-model observation that we report as a hypothesis-generator pending replication on additional RLHF-tuned models."*

**After:**
> *"The Qwen~32B collapse (§\ref{sec:qwen_scale_sweep}, supplementary case study)---where RLHF optimization entirely eliminates surface-level detection signals despite the model retaining factual knowledge---is reported as a hypothesis-generator pending replication; it is not a primary contribution claim."*

The parenthetical `(supplementary case study)` signals to the reader that this is not a primary result, consistent with its demotion to §4.6 supplementary.

---

## M6 — Human Baseline +32 pp Caveat Added

> *"'+32 pp rule-beats-human' is misleading without noting these are naive annotators, not trained lie-detection experts."*

**Before (§4.9 result paragraph):**
> *"The refusal-count rule achieves 76.0% (Wilson CI [62.6%, 85.7%]) on the same 50 trials---+32 pp over humans (Table~\ref{tab:human_baseline})."*

**After:**
> *"The refusal-count rule achieves 76.0% (Wilson CI [62.6%, 85.7%]) on the same 50 trials---+32 pp over humans (Table~\ref{tab:human_baseline}). Note these are naive crowdworker annotators with no prior lie-detection training; trained domain-expert annotators would likely score higher, narrowing the gap."*

This is consistent with the §4.9 interpretation paragraph (which already notes "annotators trained on the equalized-condition design could in principle learn the rule") but makes the caveat more prominent at the result statement itself.

---

## Q4 — K=1 Consistency (Equalized vs. Sycophancy)

> *"K=1 fails below chance in §4.7.3 but K=1 is your best rule at 80.1% in §4.3. These findings appear contradictory."*

They are not contradictory — the failure mode is sycophancy-specific. V29 adds a footnote to the §4.7 2×2 cross-reference paragraph:

> *"This K=1 inconsistency is mechanism-specific, not contradictory: in equalized conditions (no sycophancy framing) truthful trials produce correction markers and K=1 works as intended; under sycophancy framing the agree-with-user disposition eliminates correction markers on truthful trials only, breaking the threshold's assumption."*

**Mechanism:**
- **Equalized regime (§4.3):** Truthful-condition assistants respond to neutral prompts and do correct false claims, producing RC≥1 on truthful trials. The K=1 threshold discriminates correctly (lie: low RC; truth: high RC).
- **Sycophancy regime (§4.7.3):** The agree-with-user system prompt suppresses correction language *on truthful trials* — when the user asserts a false claim, the sycophancy-prompted model goes along with it rather than correcting. Result: RC=0 for all 25 truthful trials on Llama 3B. K=1 now predicts all trials as "lying" → below-chance on balanced data (22–50%).

The K=1 rule works exactly as designed in equalized conditions. It fails in sycophancy conditions not because of design fragility but because sycophancy-induced suppression violates the assumption that truthful trials produce correction markers.

---

## Minor — Stale Numbers in introduction.tex §1

> *"'How to read this paper' paragraph still lists '74.5% Haiku pipeline, 92.9% Sonnet-Haiku' as level-dependent claims."*

**Before (introduction.tex, §1 "How to read" paragraph):**
> *"...level-dependent claims (74.5% Haiku pipeline, 92.9% Sonnet-Haiku, EXP-G, probe band) read under the ICC caveat..."*

**After:**
> *"...level-dependent claims (74.3% Haiku pipeline, EXP-G, probe band) read under the ICC caveat (§\ref{sec:icc_caveat})..."*

Changes: `74.5%` corrected to `74.3%` (7-target average from Table~\ref{tab:refusal_only}); `92.9% Sonnet-Haiku` removed (was already removed from §5.7(g) in V28; introduction.tex was missed); stale `\ref{sec:icc_owned}` replaced with `\ref{sec:icc_caveat}` (2 occurrences).

---

## V29 Diff Summary

**Paper edits:**
- `methodology.tex` — §3.2 full ADAGE description replaced with 3-sentence pointer to Appendix N
- `experiments.tex` — §4.7 three causal-probe blocks replaced with paragraph-level summaries + `app:causal_probes` cross-refs; K=1 consistency footnote added; §4.9 +32 pp caveat added
- `discussion.tex` — §5.1 ICC gap sentence strengthened as same-family bias evidence
- `introduction.tex` — stale 74.5%/92.9%/sec:icc_owned fixed in "How to read" paragraph
- `conclusion.tex` — Qwen 32B structural claim → parenthetical
- `appendix.tex` — Appendix N (ADAGE Pipeline Details, `app:adage_details`) added; Appendix O (Causal Probe Details, `app:causal_probes`) added with full 4th/5th scenario + 2×2 factorial content

**Page count:** 46 pages (V28 was 45; net: main text −3.0 pages from §3.2 + §4.7 moves; appendix +4.0 pages from Appendix N + O; minor adds +0.3 pages; net +1 page). All additions address specific reviewer gaps; the structural moves address the reviewer's primary concern about the paper reading as a systems paper.

---

## Out-of-Scope for V29

- New experiments (frontier-scale, internals-comparison, n=200 sycophancy replication)
- ICC validation n≥100/3-annotator: remains camera-ready commitment
- Non-English pilot: remains §5.8 future work
- EXP-ADV weak-14-word n=200: remains preliminary at n=50

---

*Word count: ~1,700. Response letter follows V28 template.*
