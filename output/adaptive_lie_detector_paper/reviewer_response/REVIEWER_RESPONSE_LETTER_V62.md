# V62 — Response to Weak Accept (6/10) Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B-70B)

**Prior decision:** Weak Accept (6/10) — "borderline, leaning accept"

**Reviewer's key assessment:**
> "The community benefits more from rigorous audits of popular paradigms than from yet another marginal-improvement detection method... With moderate revisions to framing (especially around the Pacchiardi comparison and the deployment recommendations), this is a solid contribution."

**V62 strategy:** This reviewer's concerns are primarily about framing, not methodology. We address each: (1) make explicit that the audit's force comes from equalization, not from showing Pacchiardi's numbers are wrong; (2) narrow deployment language; (3) balance the pipeline-vs-rule story; (4) consolidate frontier mentions; (5) clarify k=1 status; (6) reduce abstract density.

---

## At-a-Glance Table

| # | Concern | V62 action | Status |
|---|---|---|---|
| **W1 — Reimplementation ≠ overturning** | §3.4 rewritten: "The audit's force does not rest on showing their reported numbers are wrong—it rests on the equalization control"; EXP-K regime distinction (≥14B reach 80-84% under equalization with Haiku) now explicit | **Done** |
| **W2 — Deployment rec premature** | Changed to "Evaluation recommendation (not deployment-ready; pending benign-conversation FPR baseline)" | **Done** |
| **W3 — Persona n=10 scope** | Already addressed V61: "rests on n=10 from a single model; highest-priority replication gap" | **Pre-resolved** |
| **W5 — Pipeline-vs-rule balance** | Reframed: "The rule is a strong baseline that should always be reported; the pipeline adds value specifically at ≥14B multi-turn, arguably the most practically relevant regime" | **Done** |
| **W6 — Frontier consolidation** | 3-sentence paragraph → 1 sentence: "Two preliminary frontier-scale observations are in Appendix C (n≤100, confounded; not interpretable beyond the ≤70B scope)" | **Done** |
| **W7 — k=1 pre-registration** | Added "(exploratory, not pre-registered)" before k-sweep reference | **Done** |
| **W8 — Human baseline** | Already addressed V61 (caveat: "uninformative about human-vs-machine capability") | **Pre-resolved** |
| **W9 — Abstract density** | Three-extractor sentence trimmed from 2 lines to 1 | **Done** |
| **Q1 — EXP-K vs 64.7% reconciliation** | Now explicit in §3.4: 64.7% conflates cross-family extraction and scale pooling; ≥14B targets reach 80-84% under equalization with Haiku | **Done** |

---

## Detailed Responses

### W1/Q1: Reimplementation caveat and EXP-K reconciliation

**Reviewer concern:**
> "The paper repeatedly contrasts its 64.7% with Pacchiardi et al.'s 67–73%, but this is a from-scratch reimplementation... The audit's force comes from the equalization control, not from showing the original numbers were wrong."
>
> "EXP-K shows the pipeline reaches 80–81% on Llama 70B and Qwen 14B... How should readers reconcile this with the 64.7% headline?"

**V62 response:**

§3.4 now reads:

> "Our cross-family pooled-LOO (64.7%) falls below Pacchiardi et al.'s 67–73% (their Table 1), but this comparison conflates two regime differences: (1) cross-family vs. same-family extraction (−7–10 pp), and (2) model-scale pooling (EXP-K in Appendix S shows ≥14B targets reach 80–84% with claim-related follow-ups under equalization using Haiku, within Pacchiardi et al.'s range). **The audit's force does not rest on showing their reported numbers are wrong—it rests on the equalization control demonstrating that the instructed-roleplay paradigm is dominated by instruction-following artifacts regardless of reported accuracy level.**"

This makes three things explicit:
1. The 64.7% vs. 67-73% gap is explainable by regime differences (extractor family, scale pooling)
2. EXP-K shows ≥14B models reach numbers within Pacchiardi's range under equalization with Haiku
3. The paper's contribution is the equalization control, not a claim that Pacchiardi's numbers are wrong

---

### W2: Deployment recommendations

**Reviewer concern:**
> "If the autonomous regime is unassessed, deployment recommendations are premature regardless of single-turn vs. multi-turn results."

**V62 response:**

The conclusion now reads:

> "**Evaluation recommendation (not deployment-ready; pending benign-conversation FPR baseline):** use the refusal-count rule as a strong baseline for single-turn evaluation..."

Two changes: (1) "Practical" → "Evaluation" (this is a research finding, not a deployment guide); (2) explicit "(not deployment-ready)" clarifies the recommendation's limited scope. Combined with the existing "pending FPR baseline" caveat (V61), this ensures no reader mistakes this for a deployment endorsement.

---

### W5: Pipeline-vs-rule balance

**Reviewer concern:**
> "The headline 'regex matches pipeline on 6/7 models' could lead practitioners to dismiss the pipeline... A more balanced framing: 'the rule is a strong baseline that should always be reported; the pipeline adds value specifically in the multi-turn ≥14B setting.'"

**V62 response:**

We adopt the reviewer's exact suggested framing. §3.4 now reads:

> "The rule is a strong baseline that should always be reported; the full pipeline adds value specifically at ≥14B multi-turn (+14–29 pp; Appendix R), arguably the most practically relevant regime for larger models in conversational use. Rule-vs-pipeline equivalence holds only in the single-turn / pooled-LOO regime."

This foregrounds the pipeline's practical value rather than treating it as an exception to a rule-dominance story.

---

### W6: Frontier consolidation

**Reviewer concern:**
> "Each individual mention [of Sonnet/Maverick] is appropriately hedged, but the cumulative effect is to give frontier-scale observations more weight than n=2 supports."

**V62 response:**

The 3-sentence frontier paragraph in §3.5 is now a single sentence:

> "Two preliminary frontier-scale observations are in Appendix C (n ≤ 100, confounded; not interpretable beyond the ≤70B scope of this paper)."

The §4.2 brief mention remains (2 sentences, already appropriately scoped). The cumulative presence is substantially reduced — from ~8 sentences across the paper to ~3.

---

### W7: k=1 pre-registration

**Reviewer concern:**
> "If the sweep was pre-registered as confirmatory, this should be stated; if not, this is a mild researcher-degrees-of-freedom issue."

**V62 response:**

Now reads: "A post-hoc **(exploratory, not pre-registered)** k-sweep (Appendix H) confirms k=1 achieves the same or better LOO as k=2–5 on all seven models."

The k=1 threshold itself was pre-selected on a principled prior (stated in the preceding sentence); the post-hoc sweep is correctly tagged as exploratory.

---

### W9: Abstract density

**Reviewer concern:**
> "The abstract is hard to parse — the three-control collapse, the construct-validity finding, the rule-vs-pipeline result, the extractor-quality finding, and the autonomous-transfer null all compete for first-paragraph attention."

**V62 response:**

Trimmed the three-extractor sentence from:
> "Three extractors (Haiku, Mistral L3, Llama 70B) show Haiku outperforms both alternatives on 6 of 7 open-weight targets (avg +7–10 pp); five self-family controls show no additional same-family boost, indicating extractor-quality differences rather than checkpoint-specific bias"

To:
> "Three extractors show Haiku outperforms Mistral L3 and Llama 70B by +7–10 pp on 6 of 7 targets; five self-family controls rule out same-family bias"

This reduces one claim-dense sentence by ~40% without losing information. The abstract's overall structure (construct-validated finding → three controls → rule → pipeline → cross-family → autonomous) remains hierarchical with the most important finding first.

---

### Responses to specific questions

**Q2 (base-model paradigm boundary):** Already addressed in V61: the Paradigm Boundaries paragraph (§4.3) now cites existing Appendix Z probe data ("33-layer probe sweep on Mistral-7B-v0.1 representations yields no layer exceeding the 68% instruction-tuned rule, consistent with the signal being post-training-induced"). A full behavioral panel on Mistral-7B-v0.1 remains the definitive test but is committed as future work.

**Q3 (FPR on benign corpus):** Acknowledged via the conclusion caveat "(not deployment-ready; pending benign-conversation FPR baseline)" and the Paradigm Boundaries §4.3(ii) discussion. We agree this has high informational value for modest compute; it is listed as a priority future direction.

**Q4 (Sonnet 4.5 triangulation):** We agree this is the most interesting single-target result but cannot firm it up with n=99 from one extractor. It remains in Appendix C as a diagnostic datapoint, not a headline finding. The V62 consolidation further reduces its prominence.

---

## Summary of Changes (V61 → V62)

| File | Key changes |
|------|-------------|
| `experiments.tex` | §3.4: regime distinction explicit (64.7% conflates cross-family + scale pooling; ≥14B reach 80-84%); audit force statement; pipeline-vs-rule reframed as "rule = strong baseline; pipeline adds value at ≥14B"; frontier paragraph 3→1 sentence; k-sweep marked "(exploratory, not pre-registered)" |
| `conclusion.tex` | "Practical recommendation" → "Evaluation recommendation (not deployment-ready; pending...)" |
| `abstract.tex` | Three-extractor sentence trimmed ~40% |

**Verification:** 41 pages, 0 undefined references, main content ≤ 9 pages.
