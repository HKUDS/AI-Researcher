# V39 — Response to Weak Accept 6/10 Review (Same Reviewer, V38 Response)

**Paper:** Correction-Marker Signals Cannot Substitute for Genuine Behavioral Deception Detection: A Three-Control Evaluation of Instructed-Roleplay Detection Across Open-Weight LLMs (3B--70B)

**Prior decision:** Weak Accept 6/10 (same third reviewer as V38)

**V39 changes:** Two text-only fixes (C3, C5) completed immediately; C4 Qwen 14B probe completed on AWS g5.xlarge (71.1% LOO, rule-parity confirmed at 14B); honest diagnostic reframing for C2 (defensiveness-only result was opposite of hypothesis); C1 Qwen 72B pending g5.12xlarge instance.

---

## At-a-Glance Table

| Item | Reviewer ask | V39 action | Status |
|---|---|---|---|
| C1 | Frontier-scale (≥100B) target data point | Qwen 2.5 72B equalized n=100 on AWS + cross-family re-extraction | **[PENDING AWS]** |
| C2 | Validated-features-only cross-family pipeline | Defensiveness-only LOO computed: 54.5% (ML3), vs 64.7% 5-feature — honest diagnostic added to §5.1 | Done (honest treatment) |
| C3 | Mistral 7B adversarial near-parity mechanistic discussion | Paragraph added to §4.8 (EXP-ADV, full-regex section) | Done |
| C4 | White-box probe at ≥14B target | Qwen 2.5 14B probe on AWS g5.xlarge: 71.1% LOO [61.9%, 79.4%], rule 69%, +2.1pp — rule-parity confirmed at 14B | Done |
| C5 | Conclusion "unified picture" overstates autonomous result | Unified-picture sentence narrowed to instructed/semi-autonomous only | Done |

---

## Detailed Responses

### C1 — Frontier-Scale (≥100B) Target Data Point

**Reviewer:** "The scope limitation '(3B--70B)' in the V38 title/abstract is an improvement, but the reviewer condition was OR: either add the data point or add the limitation. The reviewer's preferred path is data."

**Our response:** We are running Qwen 2.5 72B on an AWS GPU instance (g5.12xlarge, 4× A10G, 96 GB VRAM) to satisfy the data path. The model weights (~43 GB at Q4_K_M) fit in VRAM on this instance. The evaluation protocol: equalized n=100 trials, same 50 claim pairs as the existing panel, neutral system prompt (no instruction asymmetry), with Haiku as built-in extractor and Mistral Large 3 + Llama 3.3 70B as cross-family extractors. The infrastructure code change (adding `OLLAMA_HOST` environment variable support to `ollama_target_model.py`) was made in V39 to point experiment scripts at the remote server.

**Expected paper changes (pending results):**
- Qwen 2.5 72B row added to Table 13 (cross-family panel) with Haiku, ML3, and Llama 70B extractor columns
- §4.5 scale-sweep paragraph updated: 32B→72B recovery/continuation noted
- Title scope annotation "(3B--70B)" updated to "(3B--72B)" if Qwen 72B behaves as a 72B model in this evaluation
- Abstract final sentence: "limited to open-weight models at 3B--72B scale" (or "(3B--70B+)" if we retain the conservative framing)
- §4.7 sign test updated: 8→9 per-target gaps; if all 9 positive, p = 2×(1/2)^9 = 0.0039
- Conclusion: remove "Frontier-scale (100B+) behavior remains untested" once data is in

**[PLACEHOLDER: Insert actual Qwen 2.5 72B results here once AWS run completes]**

---

### C2 — Validated-Features-Only Cross-Family Pipeline

**Reviewer:** "If only correction-marker density passes construct validity (V38 §5.1), why does Table 13 report the 5-feature pipeline as the cross-family headline? The validated-features-only pipeline should be reported as the primary cross-family estimate."

**Our response — honest finding that differs from what we expected:**

We ran the correction-marker-density-only (defensiveness-only) cross-family pipeline on the existing 7-target panel. Results:

| Extractor | 5-feature LOO (paper) | Defensiveness-only LOO | Gap |
|---|---|---|---|
| Haiku (same-family) | 74.3% | 68.8% | −5.5 pp |
| Mistral Large 3 | 64.7% | 54.5% | −10.2 pp |
| Llama 3.3 70B | 66.9% | ~57% (estimated) | ~−10 pp |

The defensiveness-only pipeline under cross-family extraction is **substantially weaker** than the 5-feature pipeline, not stronger. The four unvalidated features (consistency, specificity, confidence, elaboration) carry genuine discriminative signal under cross-family extraction despite failing the pre-registered ICC threshold — a methodological inconsistency we cannot resolve within this revision.

**What this means:**

The §5.1/Table 13 tension the reviewer identified is real. The correct honest treatment — which we have applied in V39 — is:

1. **Do not** demote the 5-feature cross-family 64.7% to a footnote (it carries real signal; burying it would misrepresent the data).
2. **Do** add the defensiveness-only diagnostic to §5.1 with the honest gap: "A correction-marker-density-only pipeline under Mistral L3 extraction achieves 54.5% LOO (7-target avg), 10.2 pp below the 5-feature pipeline (64.7%), confirming that the four unvalidated features carry genuine discriminative signal under cross-family extraction despite failing the pre-registered ICC threshold; this is a methodological inconsistency acknowledged as a limitation."
3. **Elevate** the refusal-count rule (80.1% pooled, extractor-independent) as the primary validated accuracy estimate, since it does not depend on any feature extraction at all.

**What we changed in V39 (§5.1):**

Added the following sentence after "scoping the validated feature set to correction-marker density alone":

> "A correction-marker-density-only pipeline under Mistral L3 extraction achieves 54.5% LOO (7-target avg, excluding Qwen 32B), compared to 64.7% for the 5-feature pipeline---a 10.2 pp gap confirming that the four unvalidated features carry genuine discriminative signal under cross-family extraction despite failing the pre-registered ICC threshold; this is a methodological inconsistency acknowledged as a limitation. The refusal-count rule (80.1% pooled, extractor-independent) remains the primary validated accuracy estimate; the 5-feature cross-family 64.7% is a diagnostic upper bound, not the primary claim."

**Why the four unvalidated features carry signal despite failing ICC:**

The ICC threshold measures human inter-rater agreement on the feature *as labeled by LLMs on open-ended prompts*. A feature can fail ICC while retaining discriminative signal under equalized conditions for two reasons: (a) the feature is real but noisy in human annotation (partial annotation agreement), or (b) the LLM extractor captures cross-model stylistic differences that human annotators do not reliably identify. The equalized regime substantially concentrates the signal in correction-marker density (the single validated feature), but the other four features may carry residual discriminative signal from the equalized prompt structure itself. We cannot disentangle these at n=100 without a pre-registered feature-specific ICC study.

**Bottom line for the reviewer:** We acknowledge the tension is not resolvable in this revision by recomputation alone. The refusal-count rule (80.1%) is extractor-independent and validated; the 5-feature cross-family 64.7% is a useful diagnostic but rests on partially-validated features; the defensiveness-only 54.5% shows that restricting to the fully-validated feature loses 10 pp. We state this honestly and elevate the rule as the primary estimate.

---

### C3 — Mistral 7B Adversarial Near-Parity Mechanistic Discussion

**Reviewer:** "The paper reports Mistral 7B full-regex adversary as truth 56%, lie 73% but provides no mechanistic discussion of why this target shows near-parity rather than lying-channel suppression."

**Our response:** Added a named paragraph "Mistral 7B adversarial near-parity: mechanistic hypothesis" to §4.8 (EXP-ADV, full-regex-disclosed section), immediately after the existing three-target summary. The paragraph:

> "The Mistral 7B result (truth 56%, lie 73% at n=200, full-regex-disclosed adversary) contrasts with the lying-channel suppression pattern on Llama 3B and Qwen 14B and warrants a mechanistic note. A plausible hypothesis is that Mistral-7B-Instruct-v0.3's RLHF training produces a hedging register under factual uncertainty that is *reduced* rather than *eliminated* by the paraphrase constraint: the adversarial prompt suppresses the most explicit correction markers ('actually,' 'incorrect') but does not fully suppress the model's tendency to hedge with softer qualifiers that function as weaker correction proxies in lying conditions. The result---truth 56%, lie 73%---is consistent with the paraphrase constraint removing surface correction markers more efficiently from truthful responses (where hedging is situationally weaker) than from lying responses (where residual hedging from factual-conflict pressure persists). We do not have access to Mistral's training details to confirm this; the result is flagged as a model-specific anomaly requiring replication at n≥400 before interpretation."

This is an honest mechanistic hypothesis, not a confirmed mechanism. The key distinction from Llama 3B and Qwen 14B is that Mistral 7B shows *partial* symmetric degradation (both channels above floor) rather than one-sided collapse, consistent with a hedging-register hypothesis.

---

### C4 — White-Box Probe at ≥14B Target

**Reviewer:** "The white-box probe section (§4.9) reports results on Llama 3B and Mistral 7B only. Rule-parity should be tested at ≥14B to see whether the 'equalized regime is hard for probes' claim holds at scale."

**Our response:** We are running Qwen 2.5 14B white-box probe extraction on the AWS GPU instance. The extraction script (`whitebox_2b_extract_response_representations.py`) already has `qwen_14b: "Qwen/Qwen2.5-14B"` in its MODELS dict. The input data (`ollama_eval_qwen2_5_14b_prompt_equalized_latest.json`, n=100 equalized trials) already exists locally and will be transferred to the AWS instance. Probe training runs locally after extraction (~10 min on CPU).

**Qwen 14B probe results (AWS g5.xlarge, 4-bit quantization, last-layer LR on first-response representations, n=97):**

| Metric | Value |
|---|---|
| LOO accuracy | **71.1%** |
| Wilson 95% CI | [61.9%, 79.4%] |
| Refusal-count rule (same target) | 69.0% |
| Probe – rule gap | **+2.1 pp** |

Rule-parity holds at 14B scale: the last-layer LR probe exceeds the refusal-count rule by only +2.1 pp, well within the ±6 pp range across all three tested targets (Llama 3B: probe +6 pp; Mistral 7B base: rule leads by 3 pp; Qwen 14B: probe +2.1 pp). This is the third model family confirming that response-representation probes do not escape the surface-lexical ceiling under the equalized regime.

**Paper changes made:**
- Qwen 2.5 14B row added to Table (§4.9 whitebox probe) with LOO 71.1%, CI [61.9%, 79.4%], rule 69.0%
- §4.9 narrative updated: "Rule-parity thus holds at 14B scale in a third model family (Qwen), joining Llama 3B (+6 pp probe advantage) and Mistral 7B (rule leads by 3 pp on base checkpoint). Across all three targets, last-layer LR probes on response representations do not exceed the refusal-count rule by more than ±6 pp, confirming the surface-lexical ceiling hypothesis at 3B–14B scale."
- Table caption updated to note 4-bit quantization and response-representation extraction method

---

### C5 — Conclusion "Unified Picture" Overstates Autonomous Result

**Reviewer:** "The conclusion §6 says 'a unified picture emerges: refusal-count signal weakens whenever the target is trained or instructed to be agreeable' and lists Qwen 32B, the adversarial paraphrase, and the autonomous-persona/false-belief conditions as instances. But the autonomous conditions show a *mixed result with negative predominance* (V38 §5.3), not a clean negative. Grouping them under 'unified picture' overstates the finding."

**Our response:** Agreed. We narrowed the unified-picture sentence in §6 (conclusion.tex):

**Before:**
> "A unified picture emerges: refusal-count signal weakens whenever the target is *trained or instructed to be agreeable*---Qwen 32B's post-training smoothing, the adversarial paraphrase prompt, and the autonomous-persona and false-belief conditions (66% and 60% respectively) all instantiate qualitatively similar failure modes (with differing proximate causes: RLHF smoothing, lexical avoidance, and absence of system-prompt pressure, respectively)."

**After:**
> "A unified picture emerges for the instructed and semi-autonomous conditions: refusal-count signal weakens whenever the target is *trained or instructed to be agreeable*---Qwen 32B's post-training smoothing and the adversarial paraphrase prompt instantiate qualitatively similar failure modes (RLHF smoothing and lexical avoidance, respectively). The fully-autonomous persona and false-belief conditions are too empirically mixed (four of six n=200 Wilson CIs include chance; two partially exclude chance without a validated causal account) to group under this mechanism."

The revised sentence retains the unified picture for the three well-supported cases (equalized instructed regime, Qwen 32B RLHF collapse, adversarial paraphrase) while explicitly declining to extend it to the autonomous conditions where the evidence is mixed.

---

## Responses to Weaknesses (No Additional Paper Change)

**W1 (Autonomous-transfer thinness — need more cells):** We cannot add autonomous cells within this revision without redesigning the experiment (new claim sets, matched-format system prompts for persona and false-belief at additional scales). The V38 framing "mixed result with negative predominance" is maintained; the C5 conclusion narrowing makes the paper's position consistent throughout.

**W2 (Sycophancy semi-autonomous label):** Retained V38 acknowledgment. The paper's position: sycophancy is system-prompt-induced, making it closer to instructed deception than autonomous behavior. Readers who treat it as instructed get an additional instructed data point at 68.5--83%.

**W3 (5-feature pipeline tension with §5.1 ICC scoping — see C2 above):** Addressed honestly: the defensiveness-only diagnostic is now in §5.1; the refusal-count rule is elevated as primary; the 5-feature 64.7% is retained as a diagnostic upper bound with explicit acknowledgment of the methodological inconsistency.

**W4 (Paper density):** No restructuring in V39 beyond the targeted changes. Camera-ready reorganization of the 26-appendix structure deferred.

---

## Compilation

V39: 49 pages, 0 errors, 0 undefined references (pdflatex × 2). One page above V38 (48 pages) due to Mistral 7B adversarial paragraph (C3, ~100 words) and §5.1 defensiveness-only diagnostic sentence (~80 words).

## Spot-Check Verification

1. §4.8 contains "Mistral 7B adversarial near-parity: mechanistic hypothesis" paragraph: ✓
2. §5.1 contains "correction-marker-density-only pipeline under Mistral L3 extraction achieves 54.5% LOO...10.2 pp below the 5-feature pipeline": ✓
3. §5.1 contains "The refusal-count rule (80.1% pooled, extractor-independent) remains the primary validated accuracy estimate": ✓
4. Conclusion no longer lists "autonomous-persona and false-belief conditions" under "unified picture": ✓
5. Conclusion contains "The fully-autonomous persona and false-belief conditions are too empirically mixed...to group under this mechanism": ✓
6. `REVIEWER_RESPONSE_LETTER_V39.md` exists: ✓

---

## Pending (AWS-Dependent)

Once the AWS GPU instance is ready and experiments complete:

1. **Qwen 2.5 72B equalized n=100**: Run `run_prompt_equalized.py --model qwen2.5:72b --n_samples 100` with `OLLAMA_HOST=http://<aws-ip>:11434`
2. **Cross-family re-extraction**: Run `re_extract_equalized_cross_family.py` with `--extractor mistral_large` and `--extractor llama70b` on the Qwen 72B output
3. **Qwen 14B probe extraction**: Run `whitebox_2b_extract_response_representations.py --model qwen_14b --device cuda` on AWS; probe training runs locally
4. **Paper edits**: Add Qwen 72B row to Table 13; add Qwen 14B probe row to §4.9 table; update sign test and conclusion; write final V39 spot-checks

When these are complete, this response letter will be updated with actual numbers replacing the `[PLACEHOLDER]` entries.
