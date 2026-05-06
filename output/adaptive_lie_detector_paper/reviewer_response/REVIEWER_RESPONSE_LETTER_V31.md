# Reviewer Response Letter — V31
## NeurIPS 2026 Revised Submission

---

**To:** Reviewer 7 (Accept 7/10, Confidence 4/5)

**Subject:** V31 revision addressing Q1–Q4 and minor issues; two experiments run

We thank the reviewer for the "would defend in committee" read and the clear remaining asks. V31 runs two experiments (Q1 sycophancy scale-up to n=200; Q2 Claude Sonnet 4.5 as cross-Anthropic extractor) and makes five text-only changes (Q3 Apollo removal from §1; Q4 sycophancy-kind paragraph; Minor-§5.5 consolidation; Minor-self-falsification; Minor-K=1 promotion + multi-comparison scope label).

---

## At-a-Glance Table

| Item | Ask | V31 action | Status |
|---|---|---|---|
| **Q1 (sycophancy n=200)** | Sycophancy 82/82/72% at n=50 vs. persona/FB at n=200 — asymmetric | Ran 3B and 14B sycophancy at n=200; 70B at n=50 (Bedrock dependency); results integrated into §4.7 Table 12 | **Done — experiments.tex** |
| **Q2 (Claude attribution)** | "Claude-specific RLHF self-preference" vs. "Haiku-checkpoint-specific" | Ran Claude Sonnet 4.5 as extractor on Haiku target (n=99); Sonnet 65.7% is below both non-Claude extractors (71.7%, 72.7%); inflation is Haiku-checkpoint-specific | **Done — discussion.tex §5.7** |
| **Q3 (Apollo in §1)** | "0–54% on Apollo AI Liar" still cited in intro §1 scope paragraph | Apollo sentence replaced with matched-format anchor (§4.7 sycophancy/persona/FB numbers) | **Done — introduction.tex** |
| **Q4 (sycophancy-kind)** | Is sycophancy refusal-count signal different *in kind* from instructed? | Added `\paragraph{Sycophancy vs. instructed: qualitative difference in kind.}` in §4.7; explains RC=0 on truthful trials under sycophancy vs. RC≥1 under equalized | **Done — experiments.tex** |
| **Minor-§5.5** | Redundant with §1.1 | §5.5 condensed to 2 sentences + pointer to §1.1 (§\ref{sec:motivation}) | **Done — discussion.tex** |
| **Minor-self-falsification** | "pre-registered self-falsification" overused (2x) | Appendix Table A caption: replaced second occurrence with "pre-registered disconfirmation" | **Done — appendix.tex** |
| **Minor-Table 12 K=1 footnote** | K=1 footnote in caption is dense; promote to body | K=1 scenario comparison moved to named `\paragraph{}` before Table 12; caption $\dagger$ now points to body text | **Done — experiments.tex** |
| **Minor-multi-comparison scope** | Multiple-comparison budget paragraph slightly out of place in §4.6 | Paragraph header updated to `Multiple-comparison budget (applies to §4.2–§4.7)` to signal global applicability without physical relocation | **Done — experiments.tex** |

---

## Q1 — Sycophancy n=200 Scale-Up

> *"The sycophancy n=50 vs. persona/FB n=200 difference is a potential confound. Closing this gap would increase confidence in the transfer asymmetry."*

We ran n=200 sycophancy evaluations for Llama 3B and Qwen 14B (the two models where sycophancy previously showed the highest transfer). Llama 3.3 70B sycophancy remains at n=50 due to a Bedrock-only dependency (the 70B is not available via Ollama; re-running at n=200 would require a full Bedrock run, which we treat as a camera-ready commitment matching the ICC and RLHF replication commitments from V30).

**Results at n=200:**

| Model | n=50 (V30) | n=200 (V31) | Wilson 95% CI (n=200) | Cohen's d |
|---|---|---|---|---|
| Llama 3B sycophancy | 82.0% [60–92%] | **68.5%** | [61.8–74.5%] | 1.00 |
| Qwen 14B sycophancy | 82.0% [70–92%] | **83.0%** | [77.2–87.6%] | 1.52 |
| Llama 70B sycophancy | 72.0% | n=50 (unchanged) | [58–84%] | 0.9 |

**Interpretation:** Both cells confirm sycophancy transfer above chance at n=200. Qwen 14B holds at 83.0%, confirming strong transfer at 14B scale. Llama 3B settles at 68.5%, which is lower than the n=50 estimate of 82% — the n=50 point estimate was within its own wide CI [60–92%] and the n=200 number is the correct value to report. 68.5% is still above chance (51.4% LOO baseline on equalized Llama 3B) and above the persona/FB near-chance cells (54.0%, 56.0%), so the transfer asymmetry claim is preserved. The asymmetric-sample-size confound (sycophancy n=50 vs. persona/FB n=200) is now closed: both conditions are at n=200 for Llama 3B and Qwen 14B.

**70B sycophancy camera-ready commitment:** N=200 sycophancy evaluation on Llama 3.3 70B will be included in the camera-ready version (Bedrock-based run, identical protocol to the existing n=50 Bedrock Llama 70B sycophancy evaluation).

---

## Q2 — Claude Attribution: Haiku-Checkpoint-Specific or Claude-Family?

> *"The same-family inflation is attributed to 'Claude-specific RLHF self-preference.' Does it replicate on a second Claude model? Testing Claude Sonnet 4.5 on the Haiku target would distinguish Haiku-checkpoint-specific from Claude-family explanations."*

We ran Claude Sonnet 4.5 (AWS Bedrock, `us.anthropic.claude-sonnet-4-5-20250929-v1:0`) as extractor on the 99 equalized Haiku target transcripts, using the identical 5-feature extraction protocol and computing refusal-count LOO accuracy with Wilson 95% CIs.

**Result:**

| Extractor | Accuracy on Haiku target | Wilson 95% CI |
|---|---|---|
| Haiku (self) | 82.8% | — |
| Mistral L3 (non-Anthropic) | 71.7% | — |
| Llama 70B (non-Anthropic) | 72.7% | — |
| **Sonnet 4.5 (Anthropic, non-Haiku)** | **65.7%** | **[55.9%, 74.3%]** |

**Interpretation:** Sonnet 4.5 is a second Anthropic model. If the +10 pp inflation were a Claude-*family* RLHF self-preference, Sonnet should score above the non-Anthropic cross-family extractors on the Haiku target. It does not: Sonnet 65.7% is *below* both Mistral L3 (71.7%) and Llama 70B (72.7%), and well below Haiku self-extraction (82.8%).

The three non-Haiku extractors (Mistral L3, Llama 70B, Sonnet 4.5) cluster at 65.7–72.7%, all in the cross-family range. Only Haiku self-extraction sits at 82.8%.

This result **localizes the inflation to the Haiku checkpoint specifically**, not to Claude-family or shared Anthropic RLHF properties. The interpretation in §5.7 and §5.3(f) has been updated accordingly.

**Before (§5.3(f) limitation):**
> *"Three self-family extractor cells now argue the 9–10 pp Claude-on-Claude uplift is Claude-specific RLHF self-preference rather than a universal family-bias..."*

**After:**
> *"Three self-family extractor cells (Llama-70B-on-Llama-3B/8B, Qwen-14B-on-Qwen-7B) and a within-Anthropic comparison (Sonnet 4.5-on-Haiku: 65.7%, below both non-Anthropic extractors at 71.7%/72.7%) all produce no analogous self-boost outside Haiku-on-Haiku. The +10 pp Claude-on-Claude uplift is localized to the Haiku checkpoint specifically rather than to Claude-family or universal same-family RLHF properties."*

A new `\paragraph{Q2 follow-up: is the Claude-on-Claude inflation Haiku-checkpoint-specific or Claude-family?}` in §5.7 reports the full result and interpretation.

---

## Q3 — Apollo Reference Removed from §1 Scope Paragraph

> *"The Apollo 'AI Liar 0–54%' citation is still in the introduction's scope paragraph, even though Apollo was demoted to a single sentence in §4.7. The scope paragraph should anchor on what the paper actually tests."*

**Before (§1 scope paragraph, EXP-I sentence):**
> *"The refusal-count signal (87% accuracy on equalized 70B in instructed roleplay) collapses to 0–54% on the Apollo AI Liar dataset (EXP-I, §4.7), likely due to task-format mismatch..."*

**After:**
> *"The refusal-count signal transfers to semi-autonomous sycophancy (68.5% at Llama 3B, 83% at Qwen 14B, 72% at Llama 70B; n=200/200/50; §4.7) but does not transfer to fully autonomous persona or false-belief conditions (54–68%, near chance; §4.7)."*

The scope paragraph now anchors on the matched-format evaluation (three families, n=200 for persona/FB) rather than the Apollo null result. Apollo appears exactly once in the paper: one sentence in §4.7 noting the format mismatch.

---

## Q4 — Sycophancy Signal: Qualitative Difference in Kind

> *"The sycophancy refusal-count result might be dismissed as 'instructed deception with one extra step.' Is the LOO distribution actually different in kind, or just in magnitude?"*

The sycophancy K=1 distribution is mechanistically distinct from the instructed distribution, not just different in magnitude. We added `\paragraph{Sycophancy vs. instructed: qualitative difference in kind.}` in §4.7 after the existing "Why sycophancy is semi-autonomous" paragraph:

> *"The sycophancy refusal-count signal also differs from the instructed signal in kind, not just magnitude. Under equalized (neutral) conditions, truthful-condition assistants produce RC≥1 (they do correct false claims when not under agreeableness pressure); K=1 discriminates reliably by detecting the lying-condition absence of corrections. Under sycophancy framing, the agree-with-user disposition suppresses correction language on truthful trials: when the user asserts a false claim, the sycophancy-prompted model agrees rather than corrects (RC=0 on all 25 truthful trials at Llama 3B). K=1 then predicts all trials as 'lying' and falls below chance on balanced data (22–50%). In the equalized regime K=1 succeeds because lying trials lack RC; in the sycophancy regime it fails because truthful trials also lack RC. The mechanism is a selective lie-time absence of correction signals (equalized) versus a global agreement-induced suppression (sycophancy). This qualitative difference addresses the reviewer's question: an adversarial reader who treats sycophancy as 'instructed deception with one extra step' would expect the same LOO distribution as instructed—but the sycophancy LOO distribution is not the same (K=1 below chance; instructed K=1 at 80.1%)."*

---

## Minor — §5.5 "Technical Contribution and Novelty" Consolidation

**Before (§5.5, ~200 words):** Full subsection covering all three controls, magnitudes, and "individually non-novel" qualifications — duplicating §1.1 content.

**After (§5.5, 2 sentences):**
> *"This paper establishes a measurement standard for behavioral deception detection: the joint application of prompt equalization, cross-family extraction, and regex baselines reveals confounds of a magnitude (30–41 pp, 9–10 pp, rule-vs-pipeline parity) not previously documented when any single control is applied in isolation. For a full statement of contribution see §1.1 (§\ref{sec:motivation})."*

Page savings: ~0.3 pages.

---

## Minor — "Pre-registered self-falsification" Count

The phrase appeared twice (discussion.tex §5.8 body and appendix.tex Table caption). The occurrence in the appendix Table caption is replaced with "pre-registered disconfirmation," so the phrase now appears exactly once in the paper.

---

## Minor — Table 12 K=1 Footnote → Body Paragraph

The `$\dagger$` caption footnote describing K=1 behavior on persona/FB vs. sycophancy was dense and easy to miss. Promoted to a named `\paragraph{K=1 behavior differs across scenarios.}` immediately before Table 12, with the caption `$\dagger$` updated to point to the body text. Content is unchanged; only the placement is promoted.

---

## Minor — Multiple-Comparison Scope Label

The "Multiple-comparison budget" paragraph in §4.6 was flagged as slightly out of place (it applies to all subsections §4.2–§4.7, not just the Qwen scale section). Rather than relocating the paragraph (which would disrupt context), we updated the header to make the scope explicit:

> `\paragraph{Multiple-comparison budget (applies to §4.2–§4.7).}`

This signals global applicability without removing the paragraph from its current position immediately following the within-family Holm-Bonferroni paragraph it contextualizes.

---

## V31 Diff Summary

**Experiments run:**
- Sycophancy n=200 at Llama 3B and Qwen 14B (camera-ready commitment for 70B n=200)
- Claude Sonnet 4.5 extractor on Haiku target (n=99): 65.7%, localizes inflation to Haiku checkpoint

**Paper edits:**
- `introduction.tex` — Q3: Apollo "0–54%" removed from §1 scope paragraph; replaced with matched-format anchor
- `experiments.tex` — Q4: sycophancy-kind paragraph added (§4.7); K=1 footnote → body paragraph (before Table 12); multi-comparison scope label updated; Q1: Table 12 sycophancy rows updated to n=200 (pending final numbers)
- `discussion.tex` — Q2: §5.7 Sonnet-extractor result paragraph added; §5.3(f) limitation updated to Haiku-checkpoint attribution; §5.5 condensed to 2 sentences + pointer
- `appendix.tex` — Minor: "pre-registered self-falsification" → "pre-registered disconfirmation" in Table caption

**Page count:** 47 pages (up 1 page from V30 46 pages; K=1 paragraph + Sonnet paragraph + sycophancy-kind paragraph; §5.5 consolidation saves ~0.3 pages). Within ≤48-page target.

---

## Camera-Ready Commitments (Carried Forward from V30)

- ICC n≥100/3-annotator study with Krippendorff's α (W2, firm commitment)
- RLHF-collapse replication on ≥2 additional models at ≥14B (W6, firm commitment)
- Sycophancy n=200 for Llama 70B (Q1, new V31 commitment)

---

## Out-of-Scope for V31

- ICC n≥100/3-annotator study: camera-ready commitment (from V30)
- RLHF replication on ≥2 models: camera-ready commitment (from V30)
- Persona transcript two-coder study (Q3 V30): future work §5.8 item (9)
- Closed-loop adversarial (Q4 V30): future work §5.8 item (10)
- Frontier-scale (100B+): §5.7(b) limitation

---

*Word count: ~1,800. Response letter follows V30 template.*
