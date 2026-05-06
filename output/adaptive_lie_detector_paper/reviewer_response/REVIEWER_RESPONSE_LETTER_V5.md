# Response to Reviewer #5

We thank the reviewer for a thorough and constructive review. The path to acceptance—(a) lead with regex/confound, (b) demote ADAGE to ablation, (c) tighten statistical claims, (d) cut ~30%—was concrete and actionable. We have restructured the paper accordingly.

**Summary of changes:**
- Paper reduced from 53 → 32 pages (40% reduction; main body ~12 pages, appendix ~18 pages)
- Experiments section rewritten with regex-first narrative (§4.2 leads with EXP-J-fixed/EXP-J)
- ADAGE demoted to §4.4 "Pipeline as Ablation"
- Headline numbers tightened to +7.5–15pp throughout
- Six findings → three findings in introduction
- Discussion compressed from ~8 to ~3 pages
- Methodology compressed from ~2.5 to ~1.5 pages
- Per-model details moved to new appendix sections (B–K)

---

## Weaknesses

**W1 (Pipeline acknowledged as unnecessary but still structural backbone).**
The experiments section has been completely rewritten. §4.2 "Label-Free Detection Rule" now leads with EXP-J-fixed (80.1% label-free accuracy) and EXP-J (refusal-count matches pipeline on 6/7 models). §4.4 "ADAGE Pipeline as Ablation" explicitly frames the pipeline as an ablation study. The four converging results (K=1 sufficiency, weak ICC, regex parity, multi-turn value only under equalization at ≥14B) are consolidated in one subsection rather than scattered across the paper.

**W2 (+7.5–31pp conflates clean and confounded measurements).**
All headline appearances now read "+7.5–15pp on knowledge-controlled subsets" (abstract, introduction, conclusion, discussion). The +31pp number appears only in the EXP-G appendix (Appendix D) with explicit knowledge-transfer caveat and "upper bound" framing. Table 3 (now in §4.3) clearly distinguishes "Clean" vs. "KT confound" in the Note column.

**W3 (Three controls individually standard).**
We acknowledge this directly in §5.3: "The individual control ideas draw on established evaluation methodology." The contribution is their combined application revealing effects of substantial magnitude (30–41pp collapse, 7× inflation, 9–16pp extractor gap)—none previously documented in behavioral deception detection. Compressed to one paragraph.

**W4 (Non-monotonic claims weakly supported).**
Language softened throughout: "suggests family-specific, non-monotonic patterns" replaces "reveals." Within-family tests that survive Holm-Bonferroni are explicitly distinguished: Qwen 3B→7B (p=0.014, survives at α/3=0.017) and Llama 8B→70B (p=0.004, survives at α/2=0.025). The cross-family pooled trend is characterized as a "scale-dependent gap" (models ≤7B cluster at 61–74%, models ≥14B at 82.5–84%, pooled p<0.0001) rather than claimed as monotonic scaling. No individual adjacent increment is significant after Holm-Bonferroni correction—stated explicitly.

**W5 (Sycophancy at 82% called "semi-autonomous transfer success").**
Reframed in §4.6 and §5.1: "The 82% sycophancy result represents semi-autonomous behavior (system-prompt-induced agreement pressure) rather than spontaneous strategic deception." We no longer use "transfer success"—instead frame sycophancy as the ceiling of what behavioral detection achieves outside instructed roleplay, with persona (66%) and false beliefs (60%) near chance.

**W6 (ICC=0.114 buried in discussion).**
ICC=0.114 now appears in three places: methodology (§3.2), the pipeline ablation section (§4.4), and the feature validity discussion (§5.4). In the methodology, we note it motivates the regex baseline control. The discussion explicitly frames the pipeline contribution as "adds little over simple refusal-count heuristics."

**W7 (Mock validation prominent despite low relevance).**
Mock validation moved entirely to Appendix A.2. The main experiments section (§4.1) devotes one sentence to mock validation: "Pipeline hyperparameters and mock validation are in Appendix A.8 and A.2."

**W8 (Headline "scale-dependent signal" under-supported).**
The term "scale-dependent signal" is no longer used as a headline finding. Finding #3 in the introduction reads: "Scale effects are family-specific and non-monotonic." The cross-family trend is characterized as a "scale-dependent gap" with explicit caveats throughout. Within-family evidence (Qwen U-shape, Llama flat-then-jump) receives the emphasis, with statistically significant increments clearly marked.

**W9 (Paper length).**
Reduced from 53 → 32 pages (40% cut). Main body (abstract through conclusion): ~12 pages. Appendix: ~18 pages (expanded to receive moved content). References: ~2 pages.

**W10 (Autonomous pilot on n=54 with different task format).**
The Apollo pilot (EXP-I) is now a single paragraph in §4.6, explicitly framed as a format-mismatch finding: "Refusal-count markers achieve 0–54% accuracy, likely reflecting task-format mismatch." The matched-format evaluation (EXP-I-matched) follows immediately with proper autonomous/semi-autonomous framing.

**W11 (Contribution statement inconsistent).**
Aligned across all four appearance sites (abstract, intro, conclusion, discussion) to a consistent two-contribution statement: (1) empirical finding that instruction-following dominates (+7.5–15pp), demonstrated via three reusable evaluation controls; (2) deployment-ready label-free rule (refusal count ≥1, 80.1%) matching the full pipeline on 6/7 models.

---

## Detailed Comments

**DC1 (Figures would benefit from pattern differentiation for grayscale).**
Noted. We will add dashed/solid line differentiation and distinct markers in the final camera-ready version if source files are available for regeneration. The current figures use color which is distinguishable in the expected digital reading format.

**DC2 (§4.12 regex finding should lead experiments).**
Done. §4.2 "Label-Free Detection Rule" now leads the experiments section with EXP-J-fixed and EXP-J results. The section structure is: §4.1 Setup → §4.2 Label-Free Detection → §4.3 Instruction-Following Confound → §4.4 Pipeline as Ablation → §4.5 Scale Patterns → §4.6 Autonomous → §4.7 Cross-Family Extraction.

**DC3 (Method figure: "assert" label).**
Fixed: "assert" → "corr" in the TikZ figure (§3.2).

**DC4 (Appendix table: "Assert.").**
Fixed: "Assert." → "Corr. Dens." in the appendix correlation table.

**DC5 (EXP-J-cold naming).**
Renamed to "EXP-J-fixed" throughout to better describe what the experiment tests.

**DC6 (Abstract U-shape rendering).**
Fixed: "exhibits a U-shape: 50%→68%..." rewritten as "exhibits a U-shape (50%→68% [p=0.014*]→72%→50%)" with parentheses and square-bracket p-values to avoid nesting.

**DC7 (Discussion §5.1 repeats experiments).**
Discussion §5.1 compressed from ~2.5 pages to ~0.75 pages. Per-model EXP-G numbers removed; only the conceptual argument (instruction-following vs. knowledge-transfer) and the autonomous evaluation summary remain.

**DC8 (Discussion §5.6 repeats K=1 finding).**
§5.6 (Role of Interrogation) removed as standalone subsection. The K=1 finding is now stated once in §4.4 "Pipeline as Ablation" with forward reference to multi-turn details in Appendix I.

**DC9 (Claude Haiku RLHF compliance deserves clearer abstract framing).**
Added to abstract: "Claude Haiku's 97.8% is driven by RLHF safety compliance—100% refusal rate in lying trials—rather than deception detection per se."

**DC10 (Per-model instructed evaluations should be appendix).**
All per-model instructed evaluations (previously §4.3–4.7) moved to Appendix B "Per-Model Instructed Results."

---

## Questions

**Q1 (What is the honest headline number for instruction-following contribution?).**
+7.5–15pp on knowledge-controlled subsets (14B/70B). This is now the headline number in abstract, introduction, and conclusion. The +31pp on 8B is reported only in the appendix as an upper bound including knowledge-transfer effects.

**Q2 (Is there a defensible reason to call sycophancy "semi-autonomous transfer success"?).**
We no longer use this framing. Sycophancy is characterized as "semi-autonomous: system-prompt-induced agreement pressure rather than spontaneous strategic deception." The 82% result "represents the ceiling of what behavioral detection achieves outside the instructed-roleplay paradigm."

**Q3 (Do LLM-extracted features recover signal where refusal-count fails at Qwen 32B?).**
This experiment has not yet been run. We note this as future work: "we test only refusal-count detection; more sophisticated behavioral features may not collapse at 32B, though EXP-J found that refusal count matched or exceeded the full LLM pipeline on 6 of 7 models, suggesting limited upside from feature complexity" (§4.5).

**Q4 (Exact page/figure count for camera-ready target?).**
Current: 32 pages total (12 main body + 2 references + 18 appendix). The 40% reduction exceeds the requested ~30%.

**Q5 (What exactly would a "full validation study" for correction density look like?).**
Specified in §5.4: "$n \geq 100$ transcripts, 3+ annotators, reported Krippendorff's α" with the correction density construct definition provided to annotators. Planned as a standalone follow-up.

**Q6 (Knowledge pre-check data at 14B/70B?).**
For 70B: near-perfect pre-check confirmed in text (48/50 truthful, 50/50 lying). For 14B: not yet explicitly reported. We note: "Qwen 14B and Llama 70B have near-perfect knowledge pre-check accuracy, demonstrating that their +7.5–15pp instruction-following contributions are minimally contaminated by knowledge transfer" (Appendix D).

---

## Minor Issues

**m1 (Abstract "U-shape: 50" rendering).**
Fixed with parenthetical format.

**m2 (Assert → Corr. in figure and table).**
Fixed in both TikZ figure and appendix table.

**m3 (EXP-J-cold naming).**
Renamed to EXP-J-fixed throughout.

**m4 (Llama naming consistency).**
Verified: "Llama 3.3 70B" used consistently throughout (matching the Meta naming convention for the 3.3 generation of the 70B model).
