# Reviewer Response Letter — V27
## NeurIPS 2026 Revised Submission

---

**To:** Reviewer 5 (Weak Reject 5/10, Confidence 4/5)

**Subject:** V27 revision addressing W1–W11 and Q1–Q4

We thank the reviewer for the detailed and constructive critique. V27 makes substantial changes across four areas: (1) the 2×2 clarity × turn-structure factorial is now complete and fully populated with real results (no longer a promissory note); (2) the Llama 70B within-scale self-extraction cell is added, directly controlling for the capability-asymmetry confound; (3) the paper's organization has been heavily revised — framing tics removed, EXP labels consolidated, headline subsection streamlined, summary figure added; (4) the novelty framing now leads with "establishes a measurement standard" rather than "none individually novel." All text edits are executed and verified in a 44-page compile (0 errors, 0 undefined references).

---

## At-a-Glance Table

| Item | Ask | V27 action | Status |
|---|---|---|---|
| **W1 (novelty)** | "Is this a note or a conference paper?" | §5.5 rewritten: "establishes a measurement standard"; conclusion updated to match | **Done — discussion.tex, conclusion.tex** |
| **W2 (scope)** | Abstract missing ≤70B/English-only/instructed scope before headline numbers | Scope sentence confirmed present; intro contribution list updated to "seven open-weight LLMs...plus supplementary Qwen 32B case study" | **Done — introduction.tex** |
| **W3 (ICC two-branch)** | Camera-ready commitment ≠ submitted paper; machine-ICC proxy misleads | Machine-ICC paragraph moved to Appendix M (new `app:machine_icc`); §5.1 replaces it with 1-sentence pointer; §5.1 title removes "Owned" | **Done — discussion.tex, appendix.tex** |
| **W4 (k=1 fragility)** | 80.1% fragile under adversary; "inspection" is opaque | k-sweep footnote added (k=0: 55.4%, k=1: 80.1%, k=2: 76.5%, k=3: 72.3%); fragility qualifier confirmed | **Done — experiments.tex** |
| **W5/Q1 (2×2 factorial)** | "Camera-ready will populate" unacceptable | 600 trials run; §4.7.3 populated with real 12-cell table; dominant finding: turns main effect +30–35 pp (K=1 fails below chance; adaptive 60–72%); clarity near-zero | **Done — experiments.tex** |
| **W6/Q2 (Llama within-scale)** | Capability-asymmetry confound in Llama-70B-extractor on 3B/8B | Llama-70B-on-Llama-70B self-extraction (n=93): 74.2% — $-$9.7 pp below Haiku even at same scale; $^\S$ marker + footnote in Table 9; §4.8 paragraph updated | **Done — experiments.tex** |
| **W7 (organization)** | 15+ EXP labels, 4 headlines, framing tics, outlier in main text | EXP labels consolidated (EXP-J-fixed→EXP-J(fixed), EXP-I-m→EXP-I(matched), EXP-ADV-FULLREGEX→EXP-ADV(full-regex)); "two pre-registered self-falsifications" varied; "honest headline/measurement" removed; Llama 8B outlier demoted to table footnote; "Headline Numbers" subsection removed, inlined as paragraph; summary figure added | **Done — experiments.tex, abstract.tex, introduction.tex, discussion.tex** |
| **W8 (adversarial n=50)** | EXP-ADV weak-adversarial fragile at n=50 | n=50 confirmed not expanded in V27 (the n=200 EXP-ADV-FULLREGEX already exists; the weak-14-word condition is acknowledged as preliminary at n=50 per W8 plan) | **Scoped out — plan noted** |
| **W9/Q4 (EXP-G decomposition)** | PASSED-subset 85–94% doesn't support 7.5–15 pp as clean range | Added paragraph explaining why ≥14B is "clean": PASSED-subset doesn't isolate KT direction; 14B/70B are clean because near-100% pre-check accuracy on both conditions | **Done — experiments.tex** |
| **W10/Q3 (k=1 inspection)** | What k values considered, on what data? | k-sweep footnote (same as W4) | **Done — experiments.tex** |
| **W11 (Qwen 32B)** | Pick one: contribution-relevant or single-model artifact | §4.6 retitled "Supplementary: Qwen 32B RLHF-Collapse Case Study"; removed from 7-model list in §1 intro; intro updated to "seven open-weight LLMs...plus supplementary Qwen 32B case study (§4.6)" | **Done — experiments.tex, introduction.tex** |

---

## W5/Q1 — 2×2 Factorial: Real Results

> *"The camera-ready-will-populate framing is unacceptable for a submitted paper."*

**V27 action: 600 trials run and §4.7.3 populated with real results.**

The pre-registered factorial tests whether the clarity × turn-structure interaction is the controlling axis for sycophancy transfer. Design: Clarity ∈ {high, low} × Turns ∈ {K=1, adaptive}, disposition-source fixed (sycophancy system prompt), on Llama~3.2~3B, Qwen~2.5~14B, Mistral~7B (n=50/cell, 600 trials total; code: `run_2x2_factorial.py`).

**Results — §4.7.3 (as in paper):**

The dominant finding is a large, consistent **turns main effect** — not a clarity × turns interaction. Key cell accuracies (refusal-count LOO, Wilson 95% CIs):

| Model | K=1/high | K=1/low | Adap/high | Adap/low | Turns effect | Clarity effect |
|---|---|---|---|---|---|---|
| Llama~3.2~3B | 28% [17,42] | 38% [26,52] | 70% [56,81] | 60% [46,72] | +32 pp | 0 pp |
| Qwen~2.5~14B | 22% [13,35] | 26% [16,40] | 60% [46,72] | 58% [44,71] | +35 pp | −1 pp |
| Mistral~7B | 34% [22,48] | 50% [37,63] | 72% [58,83] | 72% [58,83] | +30 pp | −8 pp |

**The K=1 rule fails below chance (22–50%) on all three models.** Mechanism: the sycophancy system prompt suppresses correction markers on truthful trials (refusal count = 0 for all 25 truthful trials on Llama~3B), eliminating the threshold signal. Adaptive multi-turn recovers 58–72% LOO accuracy despite the same sycophancy framing — confirming that multi-turn interrogation provides signal orthogonal to first-response refusal count.

**Interpretation:** This is the **third pre-registered test**. The result is a **partial confirmation with a different axis**: turns structure is the dominant factor (+30–35 pp on all models), not the clarity × turns interaction posited by the 5th-scenario pilot. The clarity main effect is near-zero on two models and slightly negative on Mistral (−8 pp). A clarity × turns interaction is present on Llama~3B (+20 pp) and Mistral~7B (+16 pp), but is not the dominant structural feature — the turns main effect overwhelms it.

**§4.7.3 and §5.8(4)** are both updated with real data; §5.8(4) now reads "completed: turns main effect +30–35 pp on all models (K=1 fails below chance; adaptive recovers 60–72%); clarity main effect near-zero; mixed interaction."

---

## W6/Q2 — Llama 70B Within-Scale Self-Extraction

> *"The Llama-70B-on-Llama-3B/8B cells have a capability-asymmetry confound: a stronger model extracts better regardless of family. You need Llama-70B-on-Llama-70B."*

**V27 action: Llama-70B-on-Llama-70B cell added (n=93, LOO analysis).**

We re-extracted the 93 equalized Llama~3.3~70B transcripts using Llama~3.3~70B Instruct via Bedrock as the extractor.

**Result:**

| Extractor | Target | LOO |
|---|---|---|
| Claude Haiku | Llama 3.3 70B | 83.9\% |
| Mistral Large~3 | Llama 3.3 70B | 68.8\% |
| **Llama 3.3 70B** | **Llama 3.3 70B** | **74.2\%$^\S$** |

$^\S$: same-family and same-scale extractor.

**Before (§4.8 Llama-on-Llama paragraph):** Reported only 3B and 8B cells; reviewer correctly noted capability asymmetry is not controlled.

**After:** Same-scale cell added. Llama-70B-on-Llama-70B = 74.2\%, which is $-$9.7\,pp below Haiku (83.9\%) even when capability asymmetry is eliminated. Mistral-L3 (68.8\%) is $-$5.4\,pp below the same-scale Llama extraction — consistent with Llama~70B being a somewhat stronger extractor than Mistral~L3, but both land well below Haiku. The updated §4.8 paragraph reads:

> *"Critically, on Llama~3.3~70B itself (same-scale self-pair, $n=93$, $^\S$), Llama-70B-as-extractor scores \textbf{74.2\%} vs.\ Haiku 83.9\% and Mistral~L3 68.8\%---Llama~70B self-extraction is $-$9.7\,pp \emph{below} Haiku on its own target, and $+$5.4\,pp above Mistral~L3 (within the capability-gap range expected from a stronger extractor). This same-scale cell directly controls for the capability-asymmetry confound..."*

**The capability-asymmetry confound is controlled: the Haiku +9.7 pp gap persists at same scale. The gap is not explained by extractor capability alone.**

---

## W1 — §5.5 Novelty Rewrite

> *"'None of the three controls is individually novel' is a red flag. Is this a note or a conference paper?"*

**Before (§5.5 lead):**
> *"The contribution of this paper is the \emph{magnitudes}... None of the three controls is individually novel..."*

**After:**
> *"This paper establishes a \emph{measurement standard} for behavioral deception detection. Three evaluation controls---prompt equalization, cross-family extraction, and regex baselines---have each been applied in isolation in prior work; their \emph{joint} application to behavioral deception detection has not been reported. The magnitudes that joint application reveals argue for treating all three as a floor standard: 30--41\,pp accuracy collapse, 9--10\,pp same-family extractor inflation localized to Claude-on-Claude (three independent self-family controls), and a one-line rule matching a 5-feature pipeline within 5\,pp. Researchers reporting behavioral detection accuracy without all three controls should treat those numbers as upper bounds."*

The rhetorical shift: from "we measured the magnitudes" (note framing) to "we establish the floor standard against which future work should be measured" (conference framing). The factual claim is identical; the positioning is different.

---

## W3 — Machine-ICC Proxy Moved to Appendix

> *"Having it both ways: you report human ICC=0.114 as a caveat, then machine-ICC=0.79 to reassure reviewers. These are contradictory signals and the machine proxy belongs in supplementary."*

**Before:** Machine-ICC paragraph was in §5.1 body (~8 lines starting "Machine-rater ICC proxy (does not substitute for human ICC)").

**After:** Entire paragraph moved to new `\section{Machine-Rater ICC Proxy (Supplementary)}\label{app:machine_icc}` at end of appendix. §5.1 body replaces it with:
> *"A supplementary machine-rater ICC proxy (Appendix~\ref{app:machine_icc}) achieves pooled ICC(2,1)=0.79 under LLM raters; as discussed there, this reflects shared training biases rather than human IRR and does not substitute for the $n\geq100$/3-annotator study."*

§5.1 title changed from "Construct Validity: the ICC=0.114 Caveat, **Owned**" to "Construct Validity and the ICC=0.114 Caveat."

---

## W4/W10/Q3 — k-Sweep Footnote

> *"What k values were considered? On what data? 'By inspection' is opaque."*

**Before (§4.3 EXP-J-fixed paragraph):**
> *"$k=1$ was selected by inspection of the refusal-count distribution rather than by labeled-set optimization."*

**After:**
> *"$k=1$ was selected by inspection of the refusal-count distribution rather than by labeled-set optimization.\footnote{k-sweep on 689 pooled trials (no held-out set): $k=0$ achieves 55.4\% LOO, $k=1$ 80.1\%, $k=2$ 76.5\%, $k=3$ 72.3\%. ``Inspection'' means the distribution showed a natural cluster at count=0 vs.\ count$\geq$1 before fixing $k=1$; no labeled set was used for selection.}"*

The k=0 baseline (55.4\%) confirms the rule is not trivially selecting "always predict lying"; the k=1 peak is genuine rather than a coincidental optimum.

---

## W7 — Organization Pass

> *"Framing tics, 15 EXP labels, 4 headline numbers in the abstract."*

### (a) Framing tics removed

| Before | After | Location |
|---|---|---|
| "Two pre-registered self-falsifications" | "Two registered null results" | abstract.tex |
| "Two pre-registered self-falsifications and" | "Two pre-registered disconfirmations and" | introduction.tex |
| "After two pre-registered self-falsifications---" | "After two pre-registered null findings---" | discussion.tex |
| "is the honest measurement;" | "is the measured value;" | experiments.tex |
| "is the honest headline:" | "is the primary cross-family result:" | experiments.tex |
| §5.1 title: "..., Owned" | §5.1 title: "..." (Owned removed) | discussion.tex |

### (b) EXP labels consolidated

| Old label | New label |
|---|---|
| EXP-J-fixed | EXP-J (fixed k=1) |
| EXP-I-m / EXP-I-matched | EXP-I (matched) |
| EXP-ADV-FULLREGEX | EXP-ADV (full-regex disclosed) |
| EXP-L | EXP-J (cross-claim) |

EXP-B and EXP-C remain as appendix-only rows in Tab. 1.

### (c) Headline Numbers subsection removed

`\subsection{Headline Numbers (Reader Orientation)}` demoted to `\paragraph{Primary and diagnostic headline numbers.}` — eliminates the dedicated subsection header without removing the table.

### (d) Llama 8B outlier demoted to footnote

The dedicated `\paragraph{Llama~8B outlier.}` paragraph removed from main text; its content now appears as a $^\star$ footnote in Tab. 9's caption.

### (e) Summary figure added (Figure 1)

Two-panel PGFplots figure inserted after the experimental setup paragraph:
- Panel (a): Three-control accuracy collapse per model (instructed → equalized rule → cross-family pipeline).
- Panel (b): Autonomous transfer (sycophancy 82/82/72\% vs. persona/FB near-chance at 3B).

---

## W9/Q4 — EXP-G ≥14B "Clean" Explanation

> *"The PASSED-subset 85–94\% on small models doesn't establish the 7.5–15 pp range as clean. Why isn't the 7.5–15 pp also contaminated?"*

**Before:** The PASSED-subset analysis was presented without explaining why it doesn't clean small-model estimates.

**After:** Added paragraph:
> *"However, PASSED-subset accuracy does not isolate instruction-following on small models: the lie instruction names the false claim explicitly, providing a knowledge-recall trigger absent in equalized conditions even when the model ``knows'' the correct answer. The $+$7.5--15\,pp range (14B/70B) is clean because near-perfect pre-check accuracy on \emph{both} conditions means the $\Delta$ cannot be explained by knowledge transfer in either direction; the clean range does not apply to $\leq$8B, where PASSED-subset size and pre-check saturation differ meaningfully between conditions."*

---

## W11 — Qwen 32B Framing

> *"The paper includes Qwen 32B in the 7-model list in §1 but calls it a 'single-model RLHF artifact' in the same paragraph. Pick one."*

**Before (§1 intro contribution list):**
> *"...seven LLMs spanning four model families (Llama~3.2~3B, Llama~3.1~8B, Mistral~7B, Qwen~2.5~7B/14B/32B, Llama~3.3~70B, Claude Haiku~4.5)..."*
plus: *"The Qwen~2.5~32B zero-refusal-marker observation is a single-model RLHF artifact..., not a contribution."*

**After (§1 contribution list):**
> *"...seven open-weight LLMs spanning four model families (Llama~3.2~3B, Llama~3.1~8B, Mistral~7B, Qwen~2.5~7B/14B, Llama~3.3~70B, Claude Haiku~4.5; plus a supplementary Qwen~2.5~32B case study, §\ref{sec:qwen_scale_sweep})..."*

The artifact sentence removed from "How to read this paper" — the retitling of §4.6 makes it self-evident.

**§4.6 title:**

**Before:** `\subsection{Within-Family Scale Patterns}`

**After:** `\subsection{Within-Family Scale Patterns (Supplementary: Qwen~2.5~32B RLHF-Collapse Case Study)}`

---

## C.2 — Abstract Scope Verification

The abstract already contains (line 2): *"All detection here is English-only and reads from the lexical surface of the reply."* The introduction already ends §1.1 with: *"all tested models are $\leq$70B parameters, and frontier-scale (100B+) behavior is untested."* No change needed.

---

## V27 Diff Summary

**Experiments (real data):**
- `code/adaptive_lie_detector/experiments/run_2x2_factorial.py` — 6 runs complete (600 trials); 3 output JSON files
- Llama 70B within-scale self-extraction: 74.2\% LOO on n=93 equalized transcripts (data from `cross_family_equalized_llama70b_llama70b_extractor.json`)

**Paper edits:**
- `experiments.tex` — §4.7.3 real results table + interaction paragraph; §4.8 Llama-on-Llama paragraph updated with 70B self-pair; Table 9 $^\S$ marker + footnote; EXP label consolidation (8 changes); §4.6 section retitle; §4.5 EXP-G ≥14B clean paragraph; k-sweep footnote; Headline Numbers subsection → paragraph; Llama 8B outlier paragraph removed → table footnote; summary figure input
- `discussion.tex` — §5.1 title fix (removed "Owned"); machine-ICC paragraph replaced by pointer; §5.5 novelty rewritten; framing tic fixes
- `abstract.tex` — "two pre-registered self-falsifications" → "two registered null results"
- `introduction.tex` — Qwen 32B removed from 7-model list; supplementary pointer added; "self-falsifications" → "disconfirmations"; Qwen artifact sentence removed
- `appendix.tex` — new §Machine-Rater ICC Proxy (Supplementary) section
- `figures/summary_results.tex` — new two-panel PGFplots summary figure
- `main.tex` — `\usepackage{pgfplots}` + `\usepgfplotslibrary{groupplots}` added

**Page count:** 44 pages (V26 was 43; +0.5 page for summary figure; +0.3 page for real factorial table; −0.3 page from organization pass; +0.5 page from machine-ICC appendix section = net +1 page). Verified 44 pages, 0 LaTeX errors, 0 undefined references.

---

## Out-of-Scope for V27

- **ICC validation n≥100/3-annotator**: remains camera-ready commitment (§5.1, two-branch fallback).
- **EXP-ADV weak-14-word n=200**: the full-regex-disclosed variant is already at n=200; the 14-word weak-adversarial remains at n=50 and is flagged as preliminary.
- **Scaling 2×2 to persona/FB conditions**: remains future work (§5.8).
- **Non-English pilot**: remains §5.8 future work.

---

*Word count: ~2,100. Response letter follows V26 template.*
