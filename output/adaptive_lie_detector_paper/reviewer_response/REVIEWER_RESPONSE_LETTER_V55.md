# V55 — Response to Accept (7/10) Reviewer (NeurIPS 2026)

**Paper:** Correction-Marker Signals Are Not Sufficient for Deception Detection in Instructed-Roleplay Evaluations: A Three-Control Study of English Open-Weight LLMs (3B-70B)

**Prior decision:** Accept (7/10) — "I'd vote to accept."

**Reviewer's path to strong accept:**
> "Camera-ready suggestions in priority order: (1) restructure contribution #1 so multi-turn is co-equal; (2) frame the two exclude-chance autonomous cells explicitly; (3) clarify small-model EXP-G decomposition; (4) fix lettering; (5) Table 24 canonical exclusion note; (6) Sonnet disambiguation sentence; (7) Pacchiardi reimplementation note."

**V55 strategy:** All seven text-only suggestions implemented.

---

## At-a-Glance Table

| # | Reviewer suggestion | V55 action | Status |
|---|---|---|---|
| **S2 — Multi-turn as co-equal finding** | "rule matches pipeline" + "pipeline value at >=14B multi-turn" should be two-part, not headline + exception | Contribution #1 bold title restructured: "Rule/pipeline equivalence in single-turn; pipeline value concentrated at >=14B multi-turn." Body ends with "this is where the pipeline's practical value lies." | **Done** |
| **S4 — Two exclude-chance cells as open question** | Qwen 14B persona (68%) and Mistral 7B false-belief (66.5%) are awkward loose ends | Added 2 sentences to end of persona/false-belief paragraph: "The two exclude-chance cells... are the one place the autonomous-deception story remains open" | **Done** |
| **S5 — EXP-G small-model decomposition** | PASSED-subset analysis from Table 23 can clarify the <=8B instruction-following vs knowledge-transfer split | Added: "On the PASSED subset (claims the model demonstrably knows), accuracy reaches 84-90%, yielding a conditional instruction-following estimate of +20-30 pp---comparable to the >=14B clean decomposition." | **Done** |
| **S6 — Limitation lettering** | (a, b, c, i) should be (a, b, c, d) | Fixed to (a), (b), (c), (d) in SS4.4 | **Done** |
| **S7 — Table 24 canonical exclusion note** | Explain why 7-target avg excluding Qwen 32B is canonical | Added paragraph after Table 24: "The 7-target average (excluding Qwen 2.5 32B) is the canonical headline number because Qwen 32B's zero-marker collapse is a qualitatively different failure mode..." | **Done** |
| **S8 — Sonnet disambiguation sentence** | "The open-weight self-family controls cannot disambiguate; only a Sonnet-target x third-extractor experiment can" | Appended to existing Appendix N Sonnet paragraph | **Done** |
| **S9 — Pacchiardi reimplementation note** | Whether original code was obtained or from-scratch | Added: "This is a from-scratch reimplementation of their core design feature; we did not obtain Pacchiardi et al.'s original code or data." | **Done** |

---

## Detailed Responses

### S2: Multi-turn as co-equal finding

**Reviewer suggestion:**
> "Consider restructuring as: 'in the single-turn regime the rule matches the pipeline; the pipeline's value is concentrated at >=14B multi-turn.' This is a more complete story than headline + exception."

**V55 response:**

SS1.1 contribution #1 now reads:

> **Rule/pipeline equivalence in single-turn; pipeline value concentrated at >=14B multi-turn.** In single-turn / pooled-LOO evaluation, refusal count >= 1 achieves **80.1%** (no calibration data), matching the 5-feature pipeline on 6 of 7 equalized models; construct-validated pipeline **54.5%**; full cross-family **64.7%**. At >=14B multi-turn, the pipeline outperforms the rule by +14-29 pp (Appendix R)---this is where the pipeline's practical value lies.

The bold title now contains both halves of the finding as co-equal statements rather than a headline with a trailing exception.

---

### S4: Two exclude-chance cells as "the one place the story remains open"

**Reviewer suggestion:**
> "The two exclude-chance cells (Qwen 14B persona 68%, Mistral 7B FB 66.5%) are genuine loose ends---frame them explicitly as 'the one place the autonomous-deception story remains open' rather than burying them in a statistical report."

**V55 response:**

SS3.6 persona/false-belief paragraph now ends with:

> "The two exclude-chance cells (Qwen 14B persona 68.0%, Mistral 7B false-belief 66.5%) are the one place the autonomous-deception story remains open: they could reflect sampling variation within a null regime, or genuine partial transfer the framework does not yet explain. We report them without interpretation pending higher-powered replication."

---

### S5: EXP-G small-model decomposition using PASSED subset

**Reviewer suggestion:**
> "The PASSED-subset numbers from Table 23 already give a conditional instruction-following estimate for <=8B models. Adding one sentence here would show readers you've thought through the decomposition even where it's confounded."

**V55 response:**

SS3.3 EXP-G paragraph now includes:

> "On the PASSED subset (claims the model demonstrably knows), accuracy reaches 84-90%, yielding a conditional instruction-following estimate of +20-30 pp---comparable to the >=14B clean decomposition."

This gives readers the conditional estimate that partially resolves the instruction-following vs. knowledge-transfer confound at <=8B.

---

### S6: Limitation lettering (i -> d)

**V55 response:** Fixed. SS4.4 now uses (a), (b), (c), (d) sequentially.

---

### S7: Table 24 canonical 7-target average note

**Reviewer suggestion:**
> "A reader might wonder why Qwen 32B is excluded from the headline average. One sentence after Table 24 would pre-empt the question."

**V55 response:**

Added after Table 24:

> **Canonical 7-target average.** The 7-target average (excluding Qwen 2.5 32B) is the canonical headline number because Qwen 32B's zero-marker collapse (mu_lie = mu_truth = 0.00) is a qualitatively different failure mode (complete marker suppression) rather than a gradation of detection difficulty. Including it would conflate a mechanistically distinct regime with the standard detection panel.

---

### S8: Sonnet disambiguation sentence

**Reviewer suggestion:**
> "Add: 'The open-weight self-family controls cannot disambiguate these two readings; only a Sonnet-target x third-extractor experiment can.'"

**V55 response:** Appended verbatim to the existing Appendix N Sonnet 4.5 inverted gap paragraph.

---

### S9: Pacchiardi reimplementation note

**Reviewer suggestion:**
> "Was the original code obtained? A sentence either way helps readers assess the comparison."

**V55 response:**

Added to Appendix (Pacchiardi-Style Replication section):

> "This is a from-scratch reimplementation of their core design feature (unrelated follow-up questions under equalized prompts); we did not obtain Pacchiardi et al.'s original code or data."

---

## On items not changed

**Third extractor (reviewer's preferred experimental addition):** Acknowledged as the decisive disambiguation test for the Haiku-checkpoint vs. extractor-quality question. Logged as future direction (10) in Appendix J. Requires API access to a third frontier-scale extractor of comparable capability---beyond text-only camera-ready scope.

**Persona spot-checks on Llama 3B / Mistral 7B:** Would clarify whether the scenario-design artifact generalizes beyond Qwen 14B. Requires additional API calls; logged as future direction (11).

**ADAGE naming:** V54 removed "ADAGE" from main text; appendix retains it as a code identifier (`\texttt{adage} in supplementary code`). The reviewer's concern was about introducing it as a contribution name, which is resolved. No further change needed.

---

## Summary of V55 Changes

| File | Change |
|---|---|
| `sections/introduction.tex` | Restructure contribution #1 (multi-turn as co-equal finding, not exception) |
| `sections/experiments.tex` | Add "open question" framing for 2 exclude-chance cells; add PASSED-subset conditional estimate to EXP-G |
| `sections/discussion.tex` | Fix limitation lettering (i -> d) |
| `sections/appendix.tex` | Table 24 canonical exclusion note; Sonnet disambiguation sentence; Pacchiardi reimplementation note |
| NEW: `REVIEWER_RESPONSE_LETTER_V55.md` | This document |

**Paper status:** 41 pages total; 9 pages main content; compiles cleanly (2-pass); 0 undefined references.
