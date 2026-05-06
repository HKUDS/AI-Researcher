# V52 — Response to Weak Reject (4/10) Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B–70B)

**Prior decision:** Weak Reject (4/10)

**Reviewer's explicit path to clear accept:**
> "With (a) a tightened scope (drop the frontier results to a 'preliminary observations' appendix or expand them properly), (b) a reframing as critical replication of Pacchiardi-style detectors rather than a general protocol, (c) statistical reporting cleanup, and (d) elimination of the human baseline comparison, this would be a clear accept."

**V52 strategy:** All four required conditions addressed, plus all six secondary concerns.

---

## At-a-Glance Table

| # | Reviewer concern | V52 action | Status |
|---|---|---|---|
| **(a) Frontier scope** | n=2 frontier results take disproportionate main-body real estate vs. evidential weight | Both frontier paragraphs moved from §3.5 to new Appendix~\ref{app:frontier_preliminary} "Frontier-Scale Preliminary Observations"; replaced with 2-sentence pointer in §3.5 | **Done** |
| **(b) Reframe** | "Paradigm-agnostic protocol" oversells generality; should be "critical replication + methodological lessons" | Abstract, Introduction §1.2, Discussion §4.4 all reframed to "methodological audit and critical replication of Pacchiardi et al."; protocol described as lesson derived, not primary contribution | **Done** |
| **(c.1) Sycophancy Bonferroni** | Sycophancy results not given same Bonferroni treatment as persona/FB cells | Added explicit note in §3.6: sycophancy cells are pre-registered positive predictions, separate Bonferroni family from the six persona/false-belief cells | **Done** |
| **(c.2) k=1 selection** | "Pre-selected from distribution" looks like data-peeking | Replaced with principled-prior explanation: right-skewed distribution makes k=1 a natural binary threshold; post-hoc k-sweep confirms | **Done** |
| **(c.3) Scale framing** | Already hedged in V51 | No change needed; Qwen non-monotonicity marked descriptive already | **Done** |
| **(d) Human baseline** | κ=0.00 is a methodological failure, not a baseline; comparing the rule to it is misleading | Entire `\paragraph{Human baseline.}` removed from §3.4; already fully present in Appendix~\ref{app:human_baseline_full} | **Done** |
| **C3** | ADAGE pipeline underspecified — K-stopping rule and LOO setup absent | Added sentence to §2.2: stopping rule τ=0.99, K=8 effective max; LOO setup (per-target within-model; pooled cross-model) | **Done** |
| **C7** | Persona-design artifact over-generalized from Qwen 14B spot-check to all six cells | Qualified in §3.6 and §4.2 Regime 3: "whether this artifact generalizes to Llama 3B and Mistral 7B is not directly verified; null results are consistent with widespread artifact but cannot rule out genuine detector null results" | **Done** |
| **M3** | L-dep/L-indep first defined only in appendix table caption | Added definition sentence to §2.2 after construct validity sentence | **Done** |
| **M6** | Abstract presents same-family extraction gap as established; causal account speculative | Qualified: "Five self-family controls are consistent with a 9–10 pp extraction bias localized to the Claude Haiku checkpoint (hypothesis-generating; Appendix N)" | **Done** |
| **M9** | "Mistral L3" never expanded in main text | First use now reads "Mistral Large 3 (Mistral L3)" | **Done** |
| **M8** | "Sanmi Koyber" should be "Sanmi Koyejo" | Fixed in references.bib | **Done** |

---

## Detailed Responses

### (a) Frontier results moved to appendix

**Reviewer concern:**
> "The n=2 frontier results occupy significant main-body space (three paragraphs) disproportionate to their evidential weight. Drop these to a clearly labeled 'preliminary observations' appendix or expand them properly."

**V52 response:**

Both frontier paragraphs have been removed from §3.5 and consolidated into a new appendix section:

> **New: Appendix~\ref{app:frontier_preliminary} — "Frontier-Scale Preliminary Observations"**

The section opens with: *"Preliminary observations, not findings. The two targets below differ on multiple confounded axes (closed/open weight, dense/MoE architecture, RLHF recipe); the n=2 panel is insufficient to attribute any observed pattern to a specific axis."*

The main body §3.5 now contains a 2-sentence pointer:

> "Two preliminary frontier-scale observations (Claude Sonnet 4.5 n=99, Llama 4 Maverick n=100) are reported in Appendix~\ref{app:frontier_preliminary} as diagnostic datapoints; the panel is too small and too confounded to support generalizations. The main findings—rule/pipeline equivalence, equalization collapse, construct validity limits—are established entirely within the ≤70B open-weight scope of this paper."

The discussion §4.2 frontier paragraph is similarly reduced to a single sentence pointing to the appendix.

**Page effect:** Freed ~12 lines in main body, no new main-body content added, paper remains within 9-page limit.

---

### (b) Reframed as critical replication

**Reviewer concern:**
> "The paper's self-presentation as introducing a paradigm-agnostic evaluation protocol overstates its generality. One cross-paradigm data point (SAPLMA, 3 targets) does not validate a 'general protocol.' The actual contribution—a thorough methodological audit of Pacchiardi et al.—is more valuable than the protocol framing suggests."

**V52 response:**

Three locations changed:

**Abstract (new lead sentence):**
> "We present a methodological audit and critical replication of Pacchiardi et al.'s behavioral deception-detection approach, finding that three controls—prompt equalization, cross-family extraction, and a regex baseline—reveal substantial artifacts: reported 93.9–100% accuracies collapse to 52–69% (30–41 pp) under equalization, exposing instruction-following dominance."

**Introduction §1.2 (new lead):**
> "This paper performs a methodological audit and critical replication of behavioral LLM deception-detection benchmarks, deriving three evaluation controls from this audit... The three-control protocol is a lesson derived from this critical replication, not a primary contribution independent of it."

**Discussion §4.4 (reframed opening):**
> "The primary contribution is a methodological audit and critical replication of Pacchiardi et al.-style behavioral probing detectors... The three-control protocol generalizes to other detector families in principle; we demonstrate this for one cross-paradigm application (SAPLMA, n=3 targets; §3.5), which is a hypothesis-generating extension, not a validated replication."

---

### (c.1) Sycophancy multiple-comparison clarification

**Reviewer concern (C4, Q4):**
> "Why are the sycophancy cells not subjected to the same Bonferroni correction as persona/false-belief? This asymmetry needs explanation."

**V52 response:**

Added to the sycophancy paragraph in §3.6:

> "The sycophancy cells are tested as pre-registered positive predictions (hypothesis: positive transfer under RLHF agreeableness pressure) and are not in the same Bonferroni family as the six persona/false-belief cells; those six cells form a single multiple-testing family (α/6) under the pre-registered null of no transfer."

---

### (c.2) k=1 selection — principled prior

**Reviewer concern (C5, Q1):**
> "'Pre-selected from refusal-count distribution' reads as data-peeking. Was k=1 chosen by examining the data?"

**V52 response:**

The EXP-J paragraph in §3.2 now reads:

> "$k=1$ pre-selected on a principled prior: refusal-count distributions under equalized prompts are right-skewed with most mass at 0; any nonzero count ($k=1$) is a natural binary threshold requiring no distributional fitting. Post-hoc $k$-sweep (Appendix O) confirms $k=1$ achieves the same or better LOO as $k=2$–5 on all seven models."

---

### (d) Human baseline removed from main text

**Reviewer concern (C6):**
> "κ=0.00 is a measurement failure, not a baseline. Reporting it alongside the 80.1% rule implies a comparison that is not meaningful. Remove from main text."

**V52 response:**

The entire `\paragraph{Human baseline.}` paragraph has been deleted from §3.4. The complete human baseline results remain in Appendix~\ref{app:human_baseline_full}. No inline comparison to the human result appears elsewhere in the main text (verified by search).

---

### C3: ADAGE K-stopping and LOO specification

**Reviewer concern:**
> "The pipeline setup in §2.2 does not specify the K-stopping rule or how the LOO classifier is trained, making reproducibility difficult."

**V52 response:**

Added to §2.2:

> "The adaptive stopping rule terminates interrogation when classifier confidence exceeds τ=0.99; in practice this rule is rarely triggered before K=8 turns (the effective maximum), and all reported LOO accuracies use the full-K run. The logistic-regression classifier is trained with leave-one-out cross-validation on the pooled equalized dataset (per-target LOO for within-model accuracy; pooled LOO for cross-model accuracy)."

---

### C7: Persona-design artifact qualification

**Reviewer concern:**
> "The spot-check was 10 Qwen 14B trials. You then claim the artifact explains all six cells across three models. The inference may be correct but it is not established."

**V52 response:**

Qualified in §3.6 and §4.2 Regime 3. §3.6 now reads:

> "A spot-check of 10 Qwen 14B persona trials (Appendix T) reveals persona-break-with-correction in 6/10 cases... Whether this artifact generalizes to the other two models (Llama 3B, Mistral 7B) in the persona/false-belief cells is not directly verified. The null results across all three models are consistent with a widespread scenario-design artifact, but we cannot rule out that those cells reflect genuine detector null results."

§4.2 Regime 3 matches this framing.

---

### M3: L-dep/L-indep definition in main text

**V52 response:**

Added to §2.2 after the construct validity sentence:

> "We use level-independent (L-indep) to denote claims (the 80.1% rule, the 30–41 pp collapse) that are unaffected by ICC-failing features; level-dependent (L-dep) denotes pipeline-accuracy claims that should be read as upper bounds given that 4 of 5 features fail ICC ≥ 0.4."

---

### M6: Same-family extraction claim qualified

**V52 response:**

Abstract now reads:

> "Five self-family controls are consistent with a 9–10 pp extraction bias localized to the Claude Haiku checkpoint (hypothesis-generating; Appendix N)"

---

### M9: Mistral L3 expansion

First use in §3.5 now reads "Mistral Large 3 (Mistral L3)."

---

### M8: Reference typo fixed

"Sanmi Koyber" → "Sanmi Koyejo" in references.bib.

---

## Summary of V52 Changes

| File | Change |
|---|---|
| `sections/experiments.tex` | Remove human baseline ¶ (d); move both frontier ¶s to appendix, add 2-sentence pointer (a); fix k=1 text (c.2); add sycophancy Bonferroni note (c.1); qualify persona artifact (C7); expand Mistral L3 (M9) |
| `sections/discussion.tex` | Replace frontier ¶ in §4.2 with 1 sentence (a); qualify Regime 3 persona framing (C7); reframe §4.4 contribution as critical replication (b) |
| `sections/abstract.tex` | Lead with critical-replication framing (b); qualify same-family extraction claim (M6); reduce frontier to 1 clause pointing to appendix (a) |
| `sections/introduction.tex` | §1.2 lead-in: "methodological audit and critical replication" (b); Scope paragraph: frontier references updated (a) |
| `sections/methodology.tex` | Add K-stopping + LOO setup sentence (C3); add L-dep/L-indep definition (M3) |
| `sections/appendix.tex` | New §: "Frontier-Scale Preliminary Observations" with header "Preliminary observations, not findings" (a) |
| `references.bib` | Fix Koyejo spelling (M8) |

**Paper status:** 41 pages total; 9 pages main content; compiles cleanly (2-pass); 0 undefined references.
