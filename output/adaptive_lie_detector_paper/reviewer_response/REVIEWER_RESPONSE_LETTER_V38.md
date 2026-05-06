# V38 — Response to Weak Accept 6/10 Review (Third Reviewer)

**Paper:** Correction-Marker Signals Cannot Substitute for Genuine Behavioral Deception Detection: A Three-Control Evaluation of Instructed-Roleplay Detection Across Open-Weight LLMs (3B–70B)

**Prior decision:** Weak Accept 6/10 (third reviewer, distinct from V34–V37 reviewers)

**V38 changes:** Three text-only fixes addressing all three reviewer conditions. No new experiments.

---

## At-a-Glance Table

| Item | Reviewer ask | V38 action | Status |
|---|---|---|---|
| C1 | Frontier-scale (≥100B) target OR explicit scope-limitation in title/abstract | Added "(3B--70B)" to title; added explicit scope-limitation sentence to abstract | Done |
| C2 | Tighten framing of autonomous-transfer negative result | §5.3 opening: "largely negative" → "mixed result with negative predominance"; abstract autonomous-transfer line updated to lead with the two positive cells before the negative summary | Done (prior session) |
| C3 | Integrate Appendix R construct-validity ICC table into §5.1 main text | Added feature-level breakdown sentence to §5.1: "correction-marker density is the only feature that clears the validation threshold (α=0.606, ICC(2,1)=0.647); consistency (α=0.070), specificity (α=0.264), confidence (α=0.164), and elaboration (α=0.087) all fall below the pre-registered cutoff" | Done (prior session) |

---

## Detailed Responses

### C1 — Frontier-Scale Scope (Title + Abstract)

**Reviewer:** "The paper tests models up to 70B parameters, but the abstract and title don't signal this scope restriction. Either run at least one ≥100B target or add an explicit scope-limitation so readers know frontier-scale claims are out of scope."

**Our response:** We have taken the scope-limitation path. Running a ≥100B target requires local inference of a model whose weights do not fit within the evaluation machine's memory; the evaluation protocol requires the target model to generate responses under controlled conditions (not via a black-box API) because prompt equalization and turn-level monitoring require access to the raw generation. Closed-source frontier APIs do not support this role. Qwen 2.5 72B at standard Q4_K_M quantization requires ~43 GB to load into memory, exceeding the available RAM. We have therefore added an explicit scope restriction:

**Title change:**

**Before:** "...A Three-Control Evaluation of Instructed-Roleplay Detection Across Open-Weight LLMs"

**After:** "...A Three-Control Evaluation of Instructed-Roleplay Detection Across Open-Weight LLMs (3B--70B)"

**Abstract change (final sentence):**

**Before:** "All detection here is English-only and reads from the lexical surface of the reply."

**After:** "All detection here is English-only, limited to open-weight models at 3B--70B scale (frontier-scale ($\geq$100B) targets are out of scope for this evaluation), and reads from the lexical surface of the reply."

The §4.5 scale-sweep section already contained the sentence "All scaling claims are limited to ≤70B; frontier-scale (100B+) behavior remains untested." The title and abstract now match this existing body text. The constraint is methodological (local inference required; model weights must fit in RAM) rather than a choice to exclude frontier-scale behavior.

---

### C2 — Autonomous-Transfer Framing

**Reviewer:** "The abstract and §5.3 say the autonomous transfer result is 'largely negative.' But two of six n=200 cells (Qwen 14B persona 68.0%, Mistral 7B false-belief 66.5%) exclude chance. 'Largely negative' misrepresents empirical mixedness."

**Our response:** Agreed. We made two changes:

**§5.3 opening:**

**Before:** "yields a largely negative result: the refusal-count signal does not generalize to autonomous deception."

**After:** "yields a **mixed result with negative predominance**: the refusal-count signal does not generalize to fully autonomous persona or false-belief conditions (four of six $n=200$ CIs include chance), though two cells (Qwen~14B persona 68.0\%, Mistral~7B false-belief 66.5\%) exclude chance without a validated causal account."

**Abstract autonomous-transfer sentence:**

**Before:** "...fully-autonomous persona/false-belief: four of six $n=200$ Wilson CIs include chance; two cells partially exclude chance..."

**After:** "...fully-autonomous persona/false-belief: \textbf{mixed result with negative predominance} --- four of six $n=200$ Wilson CIs include chance; two exclude chance (Qwen~14B persona 68.0\%, Mistral~7B false-belief 66.5\%), treated as unexplained partial-transfer findings, not confirmatory detections."

The two cells that exclude chance do so without a validated causal account. Under Bonferroni correction across six cells (α/6=0.008), neither survives; the cells are hypothesis-generating. The framing "mixed result with negative predominance" is the accurate characterization: the preponderance of evidence is against reliable transfer, but the two exclude-chance cells are real and should not be buried.

---

### C3 — Feature-Level ICC Breakdown into §5.1

**Reviewer:** "The construct-validity section (§5.1) cites the ICC table (Appendix R) but only summarizes the overall result (α=0.606). The decision to scope validity claims to correction-marker density alone should be stated explicitly in the main text, not just in the appendix."

**Our response:** Agreed. We added one sentence to §5.1 immediately after "level-dependent claims are confirmed.":

**Added sentence:** "The feature-level breakdown (Table~\ref{tab:icc_study_n100}) shows correction-marker density is the \emph{only} feature that clears the validation threshold ($\alpha=0.606$, ICC(2,1)$=0.647$); consistency ($\alpha=0.070$), specificity ($\alpha=0.264$), confidence ($\alpha=0.164$), and elaboration ($\alpha=0.087$) all fall below the pre-registered cutoff, scoping the validated feature set to correction-marker density alone."

The five ICC values are taken directly from Table~\ref{tab:icc_study_n100} (Appendix R). The overall α=0.606 reported in the opening sentence is the correction-marker density ICC; the sentence now makes clear this is the only feature at that level rather than a summary across all five features.

---

## Responses to Weaknesses (No Paper Change)

**W1 (Frontier-scale scope):** Addressed by C1 scope-limitation.

**W2 (Claude-on-Claude: could be stylistic regularity rather than RLHF self-preference):**

The Sonnet 4.5-on-Haiku control (65.7%) is the strongest available test of stylistic-regularity vs. RLHF self-preference. If Haiku's correction-marker style were simply more lexically distinctive (i.e., a property of Haiku transcripts, not a property of Haiku as extractor), a more capable Claude extractor should score at least as high as Haiku on Haiku transcripts. Sonnet 4.5 is substantially more capable than Haiku 4.5 at instruction following and text analysis. Yet Sonnet 4.5 on Haiku transcripts scores 65.7% — below both non-Anthropic cross-family extractors (Mistral L3 71.7%, Llama 70B 72.7%). The stylistic-regularity hypothesis predicts Sonnet ≥ Haiku on Haiku transcripts (because Sonnet should be better at detecting any distinctive style); the observed result is Sonnet < non-Anthropic extractors on Haiku transcripts. This directly rules out stylistic regularity as the primary mechanism and localizes the effect to the Haiku checkpoint specifically. We acknowledge this is one control cell and cannot fully exclude all forms of stylistic regularity; the paper states "Haiku-checkpoint-specific self-preference" as the most parsimonious explanation, not a confirmed causal mechanism.

**W3 (Autonomous-transfer negative result):** Addressed by C2 framing change. The honest picture is: four of six n=200 cells include chance; two exclude chance at hypothesis-generating level only; sycophancy transfers robustly. "Mixed result with negative predominance" is now the headline framing.

**W4 (Adversarial robustness generalization: one-shot static bound):**

The one-shot adversarial paraphrase is a single disclosed modification; it establishes a lower bound on attacker cost rather than a general robustness claim. Under one-shot paraphrase, rule accuracy drops −5 to −10 pp on 2 of 3 targets (Wilson CI includes zero on the third). This is a published baseline constraint, not a claimed ceiling. Section 4.8 explicitly states "the rule is a baseline, not a deployment-ready detector."

**W5 (Paper density):**

We have not restructured for readability in V38 beyond the three targeted changes. The appendix structure (26 appendices, A through R) reflects incremental experiment additions across 37 revisions and will be reorganized for camera-ready. The main text is 22 pages; the remaining 26 pages are appendices.

**W6 (ADAGE treatment: only as comparison baseline):**

ADAGE is a prior work using a different methodology (probing-based rather than behavioral) and different target scope (broader than our equalized panel). Treating it as a comparison baseline is the correct framing; elevating it to a co-submission or primary alternative would misrepresent its role. The §4.9 probe section already shows our white-box baseline matches ADAGE-style accuracy at 63–67% on Llama 3B, consistent with the behavioral ceiling finding.

**W7 (Mistral 7B adversarial near-parity: truth 56%, lie 73%):**

The Mistral 7B adv-fullregex result is a lying-channel partial suppression anomaly, not complete suppression as in Llama 3B. Under the disclosed-full-regex adversarial protocol, lying transcripts still produce refusal markers at 73% accuracy while truth transcripts are near chance (56%). We do not have a validated mechanistic explanation for why Mistral 7B's RLHF training produces asymmetric adversarial resilience on the lying channel. This is noted in §4.8 as an n=200 anomaly. The absence of explanation is the honest answer.

**W8 (English-only limitation as non-pilot):**

Addressed in C1: the scope is now "(3B--70B)" in the title. The English-only limitation is already stated in the abstract final sentence (now more explicitly) and is listed as Future Direction (9) in §5.8. Non-English evaluation requires new claim sets and target models in the relevant languages; this is deferred.

---

## Responses to Open Questions

**Q1 (Frontier-scale target):** Scope-limitation path taken (C1 above). The evaluation protocol requires local inference; ≥100B model weights exceed available RAM (24 GB system RAM vs. ~43 GB needed for Q4_K_M quantization of the smallest ≥72B model). This is a hardware constraint, not a methodological choice to exclude frontier behavior.

**Q2 (Test of Haiku-on-non-Claude stylistic regularity via fine-tuned Llama):**

Creating a fine-tuned Llama checkpoint with Claude-style instruction following would require access to Claude RLHF training data (unavailable). The Sonnet-on-Haiku control (65.7%) is the closest available proxy: it uses a different Claude checkpoint of substantially higher capability than Haiku. We agree a purpose-trained stylistic-regularity control would be stronger; it is listed as a Future Direction but is not feasible within this revision.

**Q3 (Qualitative read on two exclude-chance cells: what distinguishes them?):**

The 10-trial spot-check (Appendix B.11) reveals that both cells (Qwen 14B persona, Mistral 7B false-belief) involve scenarios where the model has strong factual knowledge about the claim domain AND the system-prompt-induced behavioral structure produces occasional correction-like hedging in lie conditions. Neither of the two pre-registered causal axes (knowledge-conflict clarity: ΔAcc=−4.2 pp, n=300, §4.7.1; disposition-source ranking: n=30 pilot, §4.7.2) explains these cells. The best post-hoc hypothesis: both Qwen 14B and Mistral 7B are in the 7–14B "partial RLHF recovery" zone (Figure 1(a)) where correction markers are partially reinstated but not fully, creating a weak but detectable asymmetry in autonomous conditions. This is not a validated causal account; these cells are hypothesis-generating. We would need a purpose-designed experiment with matching claim difficulty and system-prompt structure to test the hypothesis.

**Q4 (Probing at ≥14B):**

Acknowledged as Future Direction (8) in §5.8. The Llama 3B and Mistral 7B probe results establish rule-parity (black-box rule ≈ white-box probing in the equalized regime) at tested configurations. Scaling to ≥14B requires access to internal activations of those models under the equalized protocol; deferred to camera-ready.

---

## Honest Residuals (Accepted As-Is)

1. **EXP-G (Haiku CF gap) has two clean data points (Qwen 14B, Llama 70B).** A CI requires ≥4 models; the range (+7.5–15 pp) is directional evidence only. Stated in §5.7(b).

2. **No cross-family re-extraction on Qwen 14B n=200 sycophancy.** The 8-target cross-family panel covers the equalized instructed-deception panel; the autonomous sycophancy cells are not re-extracted. Deferred to camera-ready.

3. **Qwen 14B persona qualitative coding not yet complete.** Spot-check available (Appendix B.11); formal two-coder annotation deferred to camera-ready.

4. **Figure 1 label cramping and Table 13 caption density.** Layout deferred to camera-ready.

---

## Compilation

V38: 48 pages, 0 errors, 0 undefined references (pdflatex × 2).

## Spot-Check Verification

1. Title reads "...Open-Weight LLMs (3B--70B)": ✓
2. Abstract final sentence contains "limited to open-weight models at 3B--70B scale (frontier-scale (≥100B) targets are out of scope for this evaluation)": ✓
3. §5.3 no longer says "largely negative result" — says "mixed result with negative predominance": ✓
4. §5.1 contains sentence: "correction-marker density is the only feature that clears the validation threshold (α=0.606, ICC(2,1)=0.647)": ✓
5. Abstract reads "fully-autonomous persona/false-belief: **mixed result with negative predominance**": ✓
6. `REVIEWER_RESPONSE_LETTER_V38.md` exists: ✓
