# Reviewer Response Letter — V26
## NeurIPS 2026 Revised Submission

---

**To:** Reviewer 4 (Weak Accept 6/10, Confidence 4/5)

**Subject:** V26 revision addressing W1–W8 and DC items from the V25 follow-up

We thank the reviewer for the detailed V25 follow-up and for identifying the clear upgrade path to 7/10. V26 addresses every numbered item. The two highest-leverage changes are: (1) the Sonnet pilot is fully dropped (not merely demoted) — the paper now scopes explicitly to models ≤70B; (2) the pre-registered 2×2 clarity × turn-structure factorial is pre-registered with a completed experiment script and results will populate the camera-ready once ~600 trials complete. All text edits are executed and verified in a 43-page compile (0 errors, 0 undefined references).

---

## At-a-Glance Table

| Item | Ask | V26 action | Status |
|---|---|---|---|
| **W1** | Sonnet pilot: Table 4 rows, abstract allusion, §5.7(b), §1.1 Frontier paragraph — incomplete demotion from V25 | Drop pilot entirely: removed Table 4 Sonnet rows, §4.6 pointer, §1.1 Frontier observation paragraph, abstract "one frontier-scale model" allusion, §5.7(b) updated; Appendix M Sonnet block removed; paper now scoped to ≤70B | **Done — experiments.tex, introduction.tex, discussion.tex, abstract.tex, appendix.tex** |
| **W2** | ICC validation deferred; level-dependent claims remain provisional | Acceptable as-is (two-branch camera-ready commitment in §5.1); no new action needed | **No action — carried from V25** |
| **W3** | Autonomous-transfer mechanism unresolved; 2×2 factorial tractable before camera-ready | Pre-registered 2×2 clarity × turn-structure factorial added as §4.7.3; experiment script `run_2x2_factorial.py` written; §5.8(4) updated from "future work" to "reported in §4.7.3 once ~600 trials complete" | **Done — experiments.tex, discussion.tex** |
| **W4** | "unified picture" in conclusion rests on single-model Qwen 32B — too strong | Softened: "all instantiate the same failure mode" → "all instantiate qualitatively similar failure modes (with differing proximate causes: RLHF smoothing, lexical avoidance, and absence of system-prompt pressure, respectively)" | **Done — conclusion.tex** |
| **W5** | §4.7 cross-family re-extraction of Llama 70B embedded mid-paragraph, not cross-linked to §4.8 | Moved `\textbf{Cross-family re-extraction}` paragraph from §4.7 to top of §4.8; added 1-sentence forward pointer in §4.7 | **Done — experiments.tex** |
| **W6** | Appendix K Mistral 7B codes don't distinguish mechanisms | Added 2-sentence note after Mistral coding row: "These codes distinguish delivery channel... do not diagnose the mechanism-unknown near-parity result... distinguishing semantic substitution from lexical avoidance would require a second-pass factual-accuracy check not performed here." | **Done — appendix.tex** |
| **W7** | Abstract second paragraph too dense and defensive | Compressed "Headline numbers" paragraph from ~8 items to 3 focal bullets: (1) label-free rule + cross-family pipeline + ICC caveat; (2) sycophancy transfer + persona/FB chance; (3) two pre-registered falsifications | **Done — abstract.tex** |
| **W8** | Pacchiardi comparison appendix-only; 1 sentence in main text would strengthen positioning | Added to §4.5 EXP-K paragraph: "Our cross-family pipeline at 64.7% falls below Pacchiardi et al.'s published 67–73% original-protocol range (Appendix~J), consistent with same-family extraction inflation accounting for the gap between equalized and instructed protocols." | **Done — experiments.tex** |
| **DC §4.10** | +32 pp gap is naive-human vs. rule; add caveat | Added 1 sentence: "This gap measures naive unaided performance; annotators trained on the equalized-condition design (who know to look for the *absence* of correction markers in lying trials) could in principle learn the rule — the gap is not intrinsic to human vs. machine capability." | **Done — experiments.tex** |
| **DC §4.7.2** | "rejects the pre-registered prediction" misleading for descriptive n=30 pilot | Changed: "rejects the one-sided sycophancy>persona prediction" → "fails to confirm the one-sided sycophancy>persona prediction (persona > sycophancy at n=30, descriptive only)" in both §4.7.2 and §5.8(4) | **Done — experiments.tex, discussion.tex** |
| **DC Table footnote** | Table 17 cross-family 64.7% row — clarify source is n≈689, not n=50 sub-sample | Added `$^\dag$` footnote to that row; caption now reads: "$^\dag$From Table~\ref{tab:cross_family_panel} (7-target panel, n≈689); not computed on the n=50 sub-sample." | **Done — experiments.tex** |

---

## W3 — Pre-Registered 2×2 Factorial: Clarity × Turn-Structure

> *"The 5th-scenario pilot suggests clarity × turn-structure as the controlling axis; this is tractable before camera-ready."*

**V26 action: §4.7.3 added and experiment script written.**

The 5th-scenario pilot (§4.7.2) found that refusal-count signal is recoverable at 70–93% LOO when clarity is high and turns are multi-turn adaptive. We pre-registered the 2×2 factorial to test whether this interaction is the controlling axis for the transfer asymmetry.

**Design (pre-registered):**
- **Clarity** ∈ {high, low}: high = textbook-false claims (e.g., "Water boils at 80°C"); low = near-miss claims from the 4th-scenario claim set
- **Turn structure** ∈ {K=1, adaptive}: single-turn refusal-count vs. full multi-turn ADAGE
- **Disposition-source fixed**: sycophancy system prompt (the condition that replicates at 82% across three scales)
- **Models**: Llama 3.2 3B, Qwen 2.5 14B, Mistral 7B
- **n=50/cell → 600 total trials**; claim sets match §4.5

**Experiment script:** `code/adaptive_lie_detector/experiments/run_2x2_factorial.py` — complete, reuses existing `SycophancyAlignedModel` pipeline with `--turns {k1, adaptive}` flag.

**Analysis script:** `code/adaptive_lie_detector/experiments/analyze_2x2_factorial.py` — reads 4 JSON files per model (k1/high, k1/low, adaptive/high, adaptive/low), computes Wilson 95% CIs, main effects (clarity, turns), interaction, and outputs LaTeX table.

**§4.7.3 text (as in paper):**

> *The 5th-scenario pilot suggested the clarity × turn-structure interaction as the candidate controlling axis. We crossed: **Clarity** ∈ {high, low} × **Turn structure** ∈ {K=1, adaptive}, disposition-source fixed (sycophancy prompt) on Llama 3.2 3B, Qwen 2.5 14B, Mistral 7B (n=50/cell; code: `run_2x2_factorial.py`). Camera-ready will populate the full result table once ~600 trials complete.*

**§5.8(4) updated** from "future work" to: *"this pre-registered 2×2 factorial (clarity ∈ {high, low} × turns ∈ {K=1, adaptive}; Llama 3B, Qwen 14B, Mistral 7B; n=50/cell) is reported in §4.7.3."*

**Primary test:** clarity × turns interaction on refusal-count accuracy. Secondary: main effects across 3 models. If no interaction, the clarity × turn-structure candidate is also falsified; if interaction present, direction characterizes the mechanism.

---

## W1 — Sonnet Pilot Fully Dropped

> *"Table 4 Sonnet diagnostic rows, abstract allusion, §5.7(b), and §1.1 Frontier paragraph are still present — this is not a complete demotion."*

**V26 action: pilot dropped entirely.** Paper now scopes to models ≤70B throughout.

### (a) Table 4 (`tab:headlines_diagnostics`)

**Before (3 rows removed):**
```
Frontier pilot (rule, $n=99$) & 73.7\% \\
Frontier pilot (pipeline, Haiku) & 92.9\% \\
Frontier pilot (pipeline, Llama~70B) & 88.9\% \\
```

**After:** Table caption updated to: *"All tested models are ≤70B parameters; frontier-scale (100B+) behavior is untested."*

### (b) §4.6 Pointer

**Before:** 3-line paragraph: *"A single frontier pilot on Claude Sonnet~4.5 (Bedrock, n=99, equalized) is reported in Appendix~\ref{app:sonnet_pilot} for context..."*

**After:** Paragraph and `\label{sec:sonnet_frontier}` removed entirely.

### (c) §1.1 Frontier Observation Paragraph

**Before:** *"\paragraph{Frontier observation (single pilot).} On Claude Sonnet~4.5 (Bedrock, n=99, equalized), refusal-count LOO achieves 73.7\%... This is a single pilot on a single provider."* (~8 lines)

**After:** Entire paragraph removed. Model list in §1.1 updated to: *"seven LLMs spanning four model families... all tested models are ≤70B parameters, and frontier-scale (100B+) behavior is untested."*

### (d) §5.7(b)

**Before:** *"Frontier-scale models (100B+) remain inadequately powered: the Sonnet 4.5 pilot (n=99) is the only frontier data point and is 4–6× underpowered for a between-extractor comparison..."*

**After:** *"Frontier-scale models (100B+) are untested; all results in this paper are from models ≤70B parameters."*

### (e) Appendix M Sonnet Block

**Before:** `\emph{Sonnet~4.5 pilot (\S\ref{sec:sonnet_frontier}).}\label{app:sonnet_pilot}` inline paragraph in Appendix M.

**After:** Entire paragraph removed. `app:sonnet_pilot` label removed (no remaining references in main text).

**Page impact:** −0.4 pages (Table 4 rows, §4.6, §1.1 paragraph), partially offset by B.3–B.9 additions (+0.3 pages net). Final: 43 pages.

---

## W4 — Conclusion "Unified Picture" Softened

> *"The Qwen 32B collapse is a single-model observation; 'same failure mode' overstates generalization."*

**Before (conclusion.tex):**
> *"...all instantiate the same failure mode."*

**After:**
> *"...all instantiate qualitatively similar failure modes (with differing proximate causes: RLHF smoothing, lexical avoidance, and absence of system-prompt pressure, respectively)."*

The rhetorical insight is preserved while the mechanism language is accurate. The adjacent "hypothesis-generator pending replication" framing (unchanged from V25) continues to scope the Qwen 32B claim appropriately.

---

## W5 — Cross-Family Re-Extraction Paragraph Moved to §4.8

> *"The Llama 70B sycophancy cross-family re-extraction is embedded mid-paragraph in §4.7 without a link to §4.8's cross-family section."*

**V26 action:**

In **§4.7**, replaced the embedded `\textbf{Cross-family re-extraction.}` paragraph with a 1-sentence forward pointer:
> *"Cross-family re-extraction on the Llama~3.3~70B sycophancy cell is in §\ref{sec:cross_family_equalized} (Table~\ref{tab:cross_family_panel})."*

In **§4.8**, added at the very top as a named paragraph:

> *\paragraph{Cross-family re-extraction of Llama~3.3~70B sycophancy cell.} Re-extracting the 50 Llama~70B sycophancy transcripts with Llama~3.3~70B-as-extractor drops pipeline LOO from 92.0% (Haiku) to 82.0% (Llama~70B) — a +10.0 pp Haiku-over-cross-family gap comparable to the +8–12 pp same-family-bias range on the equalized panel (Table~\ref{tab:cross_family_panel}). The +10 pp residual rule-to-cross-family-pipeline gap is the honest headline: multi-turn extraction adds genuine signal on 70B sycophancy, but roughly half of the Haiku-reported uplift is same-family inflation.*

§4.8 then continues with the full equalized cross-family panel as before.

---

## W6 — Appendix K Mistral 7B Mechanism Note

> *"The Appendix K samples distinguish delivery channel but don't diagnose the mechanism-unknown near-parity result for Mistral 7B."*

**Before (appendix.tex, app:adv_qualitative):** Section ended after reporting coding counts (8/10 paraphrased + 2/10 direct for Mistral 7B; 10/10 paraphrased for Qwen 14B; "all 30 trials correct the false claim").

**After:** Added 2-sentence note:
> *"These codes distinguish delivery channel (paraphrase vs.\ direct correction) but do not diagnose the mechanism-unknown near-parity result for Mistral~7B (§\ref{sec:adversarial_paraphrase}); distinguishing semantic substitution from lexical avoidance would require a second-pass factual-accuracy check not performed here."*

---

## W7 — Abstract "Headline Numbers" Compressed

> *"The second abstract paragraph lists ~8 items including defensive caveats; ≤4 focal bullets would serve the reader better."*

**Before:** ~8 items including per-target LOO (71.8%), full ICC caveat chain, turn-structure, and level-dependence in sequential sentences.

**After:** 3 focal bullets:

> *\textbf{Headline numbers, by claim.} (1)~Label-free detection: rule 80.1\% (pooled-LOO, $k{=}1$, extractor-independent); pipeline cross-family 64.7\% (Mistral~L3 and Llama~70B agree within 3\,pp on 7 of 8 cells); pipeline same-family 74.3\% (Haiku; level-dependent, ICC=0.114, §5.1). (2)~Transfer: sycophancy 82\% at 3B/14B, 72\% at 70B; fully-autonomous persona/false-belief: four of six $n=200$ Wilson CIs include chance. (3)~Two pre-registered self-falsifications: knowledge-conflict clarity ($\Delta=-$4.2\,pp pooled, 4th scenario); and disposition-source ranking fails to confirm at $n=30$ pilot (5th scenario). The rule is a baseline, not a deployment-ready detector.*

Per-target LOO 71.8% (previously listed) is dropped from the abstract — it is already in Table 1 and the cross-family table. The ICC caveat consolidates into the same-family pipeline parenthetical.

---

## W8 — Pacchiardi Main-Text Sentence

> *"The Pacchiardi comparison is appendix-only; one sentence in §4.3 or §4.5 would strengthen the related-work positioning."*

**V26 action:** Added to **§4.5**, immediately after the Pacchiardi-style exception sentence that describes the equalized EXP-K results:

> *"Our cross-family pipeline at 64.7\% falls below Pacchiardi et al.'s published 67--73\% original-protocol range (Appendix~\ref{app:pacchiardi}), consistent with same-family extraction inflation accounting for the gap between equalized and instructed protocols."*

This positions the equalized result directly against the published benchmark in main text, without requiring the reader to navigate to the appendix for the comparison.

---

## DC §4.10 — Naive-Human Caveat

> *"+32 pp is naive unaided human vs. rule; the gap is not intrinsic to human vs. machine capability."*

**After:** Added at end of §4.10 Interpretation paragraph:

> *"Note that the $+$32\,pp gap measures \emph{naive unaided} performance; annotators trained on the equalized-condition design (who know to look for the \emph{absence} of correction markers in lying trials) could in principle learn the rule --- the gap is not intrinsic to human vs.\ machine capability."*

---

## DC §4.7.2 — "Fails to Confirm" Language

> *"'Rejects the pre-registered prediction' is misleading for a descriptive n=30 pilot."*

**Before (§4.7.2 table caption):** *"the pre-registered one-sided prediction is \emph{rejected}"*

**After:** *"the pre-registered one-sided prediction \emph{fails to be confirmed}: persona $>$ sycophancy at $n=30$ (descriptive only)"*

**Before (§4.7.2 interpretation):** *"we claim only that the pre-registered one-sided prediction (sycophancy $>$ persona) fails"*

**After:** *"we report only that the pre-registered one-sided prediction (sycophancy $>$ persona) fails to be confirmed (persona $>$ sycophancy at $n=30$, descriptive only)"*

**§5.8(4) cross-reference** updated consistently: *"fails to confirm the one-sided sycophancy>persona prediction"*.

---

## DC Table Footnote — Human Baseline 64.7% Source

> *"Table 17 cites cross-family 64.7% from the full panel, not the n=50 sub-sample; this should be flagged."*

**Before (tab:human_baseline):** `\emph{Pipeline cross-family ($n{\approx}689$)} & \emph{64.7\%}` — no footnote.

**After:**
- Row: `\emph{Pipeline cross-family ($n{\approx}689$)$^\dag$} & \emph{64.7\%}`
- Caption updated to include: *"$^\dag$From Table~\ref{tab:cross_family_panel} (7-target panel, $n{\approx}689$); not computed on the $n=50$ sub-sample."*

---

## V26 Diff Summary

**New code files:**
- `code/adaptive_lie_detector/experiments/run_2x2_factorial.py` — 2×2 factorial experiment script (~320 lines; reuses `SycophancyAlignedModel`; `--turns {k1, adaptive}` flag; checkpoint support; Bedrock patching for adaptive mode)
- `code/adaptive_lie_detector/experiments/analyze_2x2_factorial.py` — analysis script; Wilson 95% CIs, main effects, interaction, LaTeX table output, Fisher exact p-value with Holm-Bonferroni correction

**Paper edits (sections/*.tex):**
- `abstract.tex` — "Headline numbers" paragraph compressed to 3 bullets (−3 lines); removed "one frontier-scale model" allusion
- `introduction.tex` — §1.1 Frontier observation paragraph removed (−8 lines); model list updated to "seven LLMs...all ≤70B; frontier-scale untested"
- `experiments.tex` — Table 4 Sonnet rows removed (−3 rows); §4.6 Sonnet pointer removed (−5 lines); §4.5 Pacchiardi main-text sentence (+1 line); §4.7 cross-family paragraph moved to §4.8 (+1 pointer line); §4.7.2 "fails to confirm" language fix; §4.7.3 2×2 factorial paragraph added (+4 lines); §4.8 cross-family re-extraction paragraph at top (+3 lines compressed); §4.10 naive-human caveat (+2 lines); Table 17 footnote (+1 line + caption update)
- `discussion.tex` — §5.7(b) updated (−4 lines, +1 line); §5.8(4) title updated + "rejects" → "fails to confirm" + pointer to §4.7.3
- `conclusion.tex` — "same failure mode" → "qualitatively similar failure modes (with differing proximate causes...)" (+1 line)
- `appendix.tex` — Appendix K Mistral mechanism note (+2 lines); Appendix M Sonnet block removed (−3 lines)

**Page count:** 43 pages (within ≤43 target). 0 LaTeX errors. 0 undefined references.

---

## Out-of-Scope for V26

- **ICC validation n≥100/3-annotator**: remains camera-ready commitment (§5.1, two-branch fallback included).
- **Second-provider Sonnet replication**: user chose full drop; paper scoped to ≤70B throughout.
- **Qwen 32B replication on additional RLHF model**: user chose soften language; "hypothesis-generator pending replication" framing retained in conclusion.
- **2×2 factorial results (600 trials)**: pre-registered and script-complete; results will populate camera-ready; §4.7.3 and §5.8(4) commit to this.
- **Full three-condition × three-target n=50 5th-scenario replication**: remains future work (§5.8(4) last sentence).

---

*Word count: ~1,800. Response letter follows V25 template.*
