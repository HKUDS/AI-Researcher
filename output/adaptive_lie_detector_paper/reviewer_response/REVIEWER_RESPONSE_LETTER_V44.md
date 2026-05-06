# V44 — Response to Revised Weak Accept 6→7 Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B–70B)

**Prior decision:** Weak Accept 6/10 leaning 7 (same reviewer; V43 addressed new reviewer; V44 addresses this returning reviewer's revision-round concerns)

**Reviewer's three explicit conditions for clear accept:**
> (i) Integrate Sonnet inverted-extractor finding into §5.3 rather than §4.5 sidebar  
> (ii) Flag high-confidence ICC selection bias  
> (iii) Commit to running sycophancy system-prompt-only control for camera-ready

**V44 changes:** Title updated, 8 text revisions, 1 appendix completion, camera-ready commitment added. Paper: 37 pages, 0 errors, 0 undefined references.

---

## At-a-Glance Table

| Item | Reviewer ask | V44 action | Status |
|---|---|---|---|
| **C3 (must-do i)** | Integrate Sonnet inverted-extractor into §5.3 | Added `\paragraph{Sonnet diagnostic: rule is open-weight ceiling, not universal.}` in §5.3 (Transfer Regimes); shows Haiku checkpoint biases go in opposite directions for Haiku vs. Sonnet targets; tightens localization claim | Done |
| **C4 (must-do ii)** | Flag high-confidence ICC selection bias | Added "selecting on annotator agreement biases this estimate upward---it is a sensitivity check, not a population-level reliability estimate" to §5.1 ICC paragraph | Done |
| **W7 (must-do iii)** | Commit to sycophancy system-prompt-only control | Added explicit camera-ready commit to §5.3 Regime 2: "We commit to running this control for camera-ready" | Done |
| **C2** | Add "what this number is NOT" column to Table 1 | Added "Not" column to tab:headline_decision with concrete misreading caveats | Done |
| **C5** | Promote 54.5%/40% ICC-failing finding | Made bold and explicit as stand-alone conclusion in §5.1: "40% of the pipeline's above-chance signal comes from ICC-failing features and should not be cited as validated performance" | Done |
| **C6** | Fix "will appear in camera-ready" appendix placeholder | Replaced with actual coded spot-check results: P=3, B-correct=6, B-other=1; added interpretation (persona-break-with-correction pattern) | Done |
| **C7** | Narrow title scope | Changed to: "Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B–70B)" | Done |
| **W5** | Downgrade Qwen 32B U-shape further | §1.1 contribution 3 now reads "Qwen 2.5: peak at 14B then collapse at 32B (n=100, single-observation pilot pending replication)" — Llama result leads, Qwen is explicitly secondary | Done |

---

## Detailed Responses

### C3 (must-do i) — Sonnet Inverted-Extractor Integrated into §5.3

**Reviewer:** "The Sonnet 4.5 result reads as 'data we don't want to integrate' rather than as evidence that strengthens the Haiku-checkpoint-specificity claim. It deserves explicit discussion in §5.3 rather than a footnote exclusion."

**V44 change:** Added `\paragraph{Sonnet diagnostic: rule is open-weight ceiling, not universal.}` as a fourth paragraph in §5.3 (Three Transfer Regimes). The paragraph makes two arguments:

1. **Haiku extraction biases go in opposite directions.** Haiku-on-Sonnet collapses to 50.5%, while Mistral L3 achieves 82.8%. This is the *inverse* of the Haiku self-boost on open-weight targets. The implication is that Haiku has *checkpoint-specific* extraction biases in different directions for Haiku (self-boost) vs. Sonnet (self-deflate) — tightening the localization claim to a single Haiku extractor artifact rather than a generic same-family effect.

2. **The rule is an open-weight RLHF ceiling, not universal.** Rule fails (49.0%) while pipeline succeeds (82.8%) on Sonnet. Sonnet's stronger RLHF alignment suppresses the refusal-marker channel that the rule reads — so 80.1% characterizes the ceiling for open-weight RLHF patterns, not a floor for all model families.

These two points *strengthen* the paper's central claims rather than being awkward data to exclude.

---

### C4 (must-do ii) — High-Confidence ICC Selection Bias Flagged

**Reviewer:** "Selecting on annotator agreement is a known biased estimator of population ICC — it inflates reliability by definition. The authors don't acknowledge this."

**V44 change in discussion.tex §5.1:**

Added immediately after ICC(2,1)=0.71: "Note: selecting on annotator agreement biases this estimate upward---it is a sensitivity check, not a population-level reliability estimate."

The full α=0.606 from the primary n=100 study is now explicitly labeled "(the primary validation unit, clearing α≥0.4)" to reinforce which number should be cited.

---

### W7 (must-do iii) — Sycophancy System-Prompt-Only Control Committed

**Reviewer:** "Running it for camera-ready would be valuable."

**V44 change in discussion.tex §5.3 Regime 2:**

Added explicit commitment at end of Regime 2 paragraph: "We commit to running this control for camera-ready."

This control tests whether the sycophancy signal persists when only the system prompt (no user-asserted false claims) is present, isolating disposition-source from epistemic pressure.

---

### C2 — "Not" Column Added to Table 1

**Reviewer:** "Consider adding a column for 'what this number is *not*'."

**V44 change in introduction.tex:**

Added "Not" column to tab:headline_decision:
- 64.7%: "not a production accuracy"
- 80.1%: "not a deployable detector"
- 30–41 pp: "not a single cause"
- 9–10 pp: "not all same-family pairs"
- 68.5–83%: "sycophancy only"

---

### C5 — 54.5%/40% ICC-Failing Finding Promoted

**Reviewer:** "This is one of the paper's most consequential findings for anyone citing the pipeline. Consider promoting it to a stand-alone bullet."

**V44 change in discussion.tex §5.1:**

The 54.5%/40% finding is now presented as a bolded key implication inline:

> "**Key implication:** A correction-marker-only pipeline achieves **54.5%**; the full 5-feature pipeline achieves 64.7%---**40% of the pipeline's above-chance signal comes from ICC-failing features** and should not be cited as validated performance."

---

### C6 — Appendix Qwen 14B Persona Spot-Check Completed

**Reviewer:** "Appendix V says results 'will appear in camera-ready.' Please commit to running this before camera-ready or remove the reference."

**V44 change in appendix.tex §Qwen Persona Spot-Check:**

Replaced "will appear in camera-ready" with actual coded results from the 10-trial spot-check:
- P (persona maintained) = 3 (all FALSE condition)
- B-correct (persona broken, direct correction) = 6 (5 TRUE, 1 FALSE)
- B-other = 1 (TRUE)

Interpretation added: "The dominant pattern is persona-break-with-correction on TRUE trials — the model abandons the false identity and corrects the claim. This is consistent with *detection-task mismatch*: the classifier picks up correction behavior in TRUE trials (where the model breaks persona), not suppression in FALSE trials."

---

### C7 — Title Narrowed

**Reviewer:** "'Cannot Substitute for Genuine Deception Detection' is a strong claim that is supported only for instructed-roleplay detection on ≤70B open-weight English models."

**V44 change in main.tex:**

New title: "Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B–70B)"

This is more precise: "not sufficient for...instructed-roleplay evaluations" rather than the broader "cannot substitute for genuine deception detection."

---

### W5 — Qwen 32B Claim Downgraded in §1.1

**Reviewer:** "The Qwen 32B framing in §1.1 contribution 3 is still slightly stronger than one pilot warrants."

**V44 change in introduction.tex:**

Reordered contribution 3 so Llama (confirmed, p=0.004, survives correction) leads and Qwen 32B is explicitly secondary:

> "Llama: flat-then-jump (8B→70B, p=0.004). Qwen 2.5: peak at 14B then collapse at 32B (n=100, single-observation pilot pending replication)"

---

## Responses to Remaining Reviewer Concerns

**W1 (Novelty):** We acknowledge this remains the central reviewer concern. The paper's corrective value is that Pacchiardi et al.'s 67–73% is reproducible but attributable — magnitudes not previously jointly documented. The Sonnet diagnostic (now §5.3) extends the finding beyond open-weight models, showing the rule fails on frontier RLHF. We agree a second paradigm would strengthen novelty but this is beyond the current revision scope.

**W6 (Autonomous-transfer null):** We agree the two exclude-chance cells could be treated more cleanly as nulls. The Qwen 14B persona spot-check (now completed in the appendix) supports the "detection-task mismatch" reading: the classifier picks up persona-break-with-correction, not genuine deception detection. We retain the main text framing as "hypothesis-generating only, not confirmatory."

**W8 (Human baseline):** The §T framing now consistently uses "degenerate baseline" language. Table 29 pointer updated to direct readers to the correct interpretation in §D.1(k).

**W9 (White-box probing):** Last-layer probes only. We acknowledge this as a limitation and note it as Future Direction 9 in the appendix.

---

## Compilation

V44: 37 pages (unchanged), 0 errors, 0 undefined references. The Sonnet discussion paragraph in §5.3 (~4 lines) and ICC bias sentence (~1 line) are offset by condensing the cross-family extraction paragraph (~3 lines), matched-format evaluation (~1 line), and per-feature LOO paragraph (~2 lines). Net change: 0.

---

## Spot-Check Verification

1. §5.3 has `\paragraph{Sonnet diagnostic: rule is open-weight ceiling, not universal.}` with both claims (Haiku biased in opposite directions; rule is open-weight ceiling): ✓
2. §5.1: "selecting on annotator agreement biases this estimate upward---it is a sensitivity check": ✓
3. §5.3 Regime 2: "We commit to running this control for camera-ready": ✓
4. Table 1: "Not" column with 5 entries: ✓
5. §5.1: "40% of the pipeline's above-chance signal comes from ICC-failing features and should not be cited as validated performance": ✓
6. Appendix §Qwen Persona Spot-Check: coded results P=3, B-correct=6, B-other=1; no "will appear in camera-ready": ✓
7. Title: "Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations": ✓
8. §1.1 contribution 3: "Qwen 2.5: peak at 14B then collapse at 32B (n=100, single-observation pilot pending replication)": ✓
9. 37 pages, 0 errors, 0 undefined references: ✓
10. `REVIEWER_RESPONSE_LETTER_V44.md` exists: ✓
