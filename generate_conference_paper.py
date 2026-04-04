#!/usr/bin/env python3
"""
generate_conference_paper.py

Generates a NeurIPS 2024 conference paper from RESEARCH_DOCUMENTATION.md
using Claude API for each section, then compiles to PDF.

Supports two backends:
  - Direct Anthropic API (default): set ANTHROPIC_API_KEY
  - AWS Bedrock:                    set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
                                    AWS_REGION (default: us-east-1), and pass --bedrock

Usage:
    python generate_conference_paper.py
    python generate_conference_paper.py --bedrock              # use AWS Bedrock
    python generate_conference_paper.py --skip-compile        # LaTeX only, no PDF
    python generate_conference_paper.py --section methodology # regenerate one section
    python generate_conference_paper.py --model <model-id>    # override model
"""

import argparse
import os
import sys
import re
import subprocess
from pathlib import Path

import anthropic

# ---------------------------------------------------------------------------
# Load .env if present (simple parser, no extra deps required)
# ---------------------------------------------------------------------------
def _load_dotenv(path: str = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value

_load_dotenv()

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent
RESEARCH_DOC = REPO_ROOT / "RESEARCH_DOCUMENTATION.md"
OUTPUT_DIR = REPO_ROOT / "output" / "adaptive_lie_detector_paper"
SECTIONS_DIR = OUTPUT_DIR / "sections"
TEMPLATE_DIR = REPO_ROOT / "paper_templates" / "neurips"
STY_FILE = TEMPLATE_DIR / "neurips_2024.sty"

SECTIONS = [
    "abstract",
    "introduction",
    "related_work",
    "methodology",
    "experiments",
    "discussion",
    "conclusion",
]

# Default model IDs per backend
DEFAULT_MODEL_DIRECT = "claude-opus-4-6"
DEFAULT_MODEL_BEDROCK = "us.anthropic.claude-opus-4-6-v1"

# ---------------------------------------------------------------------------
# Real LLM pilot results — injected into section prompts
# ---------------------------------------------------------------------------
REAL_LLM_RESULTS = """
REAL LLM PILOT RESULTS (Claude Haiku 4.5 via AWS Bedrock — use these in the paper):
- Target model: Claude Haiku 4.5-20251001 (a production LLM, not a mock)
- Completed trials: 9 (7 truthful claims, 2 lying claims)
- Overall accuracy: 88.9% (8/9 correct)
- Truthful claim accuracy: 100% (7/7)
- Lying claim accuracy: 50% (1/2) — harder than mock; classifier partially transfers
- Average questions asked (adaptive): 3.0 per interrogation
- Key observation: the single lying misclassification had very high confidence (0.92),
  confirming the calibration problem noted in the mock study
- Limitation: small pilot (n=9 completed); 17 additional trials failed due to API rate limits
- Interpretation: framework transfers to real LLMs with reduced lying detection accuracy
  compared to mock (50% vs 82%), suggesting mock patterns are simpler than real LLM behaviour
"""

# ---------------------------------------------------------------------------
# Section prompts (Revision 2 — addressing NeurIPS reviewer feedback)
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are an expert academic writer helping produce a NeurIPS 2024 conference paper.
Write ONLY the LaTeX body content for the requested section — no \\documentclass, no \\begin{{document}},
no preamble, and no markdown code fences. Use proper LaTeX commands throughout.
Write in third-person academic style. Be precise, formal, and technically rigorous.
Where you introduce citations use \\cite{{key}} with reasonable BibTeX keys (e.g. \\cite{{vaswani2017attention}}).
"""

SECTION_PROMPTS = {
    "abstract": """Write the LaTeX content for the Abstract section (REVISED per reviewer feedback).
Use the \\begin{{abstract}} ... \\end{{abstract}} environment. Target 160-200 words.

Requirements (address reviewer feedback directly):
1. Scope the claim precisely: this is "behavioral deception detection in constrained roleplay settings",
   NOT a general-purpose LLM lie detector. Use this exact framing.
2. Report the mock study results honestly: n=100 trials, 91% accuracy with adaptive method vs 100%
   with fixed 8-question baseline. Do NOT claim perfect 100% accuracy.
3. Report the real LLM pilot: 88.9% overall accuracy on Claude Haiku 4.5, but only 50% lying
   detection, showing the gap between mock and real LLM performance.
4. Mention the efficiency finding: adaptive stopping achieves 75% fewer questions than fixed baseline.
5. Be explicit that this is a proof-of-concept requiring validation at scale.

{real_llm}

Research documentation:
{{doc}}
""",

    "introduction": """Write the LaTeX content for the Introduction section (REVISED).
Use \\section{{Introduction}} with 4 subsections. Target ~800 words.

Requirements (address reviewer feedback):
1. §1.1 Motivation: AI safety, alignment, interpretability — cite \\cite{{hubinger2019risks}} for
   deceptive alignment, \\cite{{ouyang2022training}} for RLHF alignment.
2. §1.2 The Challenge: explain why LLM deception detection differs from human lie detection.
   Explicitly distinguish between (a) instructed roleplay deception (this paper's setting) and
   (b) autonomous strategic deception (the harder alignment problem) — be clear this paper
   addresses (a) as a tractable proxy for studying behavioral detection methods.
3. §1.3 Our Approach: the 4-component adaptive interrogation system.
4. §1.4 Contributions: use \\begin{{itemize}} listing:
   - Adaptive interrogation framework with confidence-based early stopping
   - Behavioral feature extraction and classification pipeline
   - Empirical study on mock models (n=100) and real LLM pilot (n=9, Claude Haiku)
   - Demonstration that lying detection is harder on real LLMs than mock models
5. End with paper structure roadmap.

{real_llm}

Research documentation:
{{doc}}
""",

    "related_work": """Write the LaTeX content for the Related Work section (REVISED — add missing work).
Use \\section{{Related Work}} with 5 subsections. Target ~700 words.

CRITICAL: The reviewer specifically called out missing these areas — you MUST include them:
1. §2.1 Human Deception Detection: polygraph (\\cite{{raskin1988polygraph}}), micro-expressions
   (\\cite{{ekman2003emotions}}). Explain why physical tells don't apply to LLMs.
2. §2.2 Adversarial Examples and Prompt Injection: \\cite{{goodfellow2014explaining}},
   \\cite{{perez2022ignore}}. These differ from intentional model deception (different threat model).
3. §2.3 Representation Engineering and Probing Classifiers (REQUIRED — reviewer called this out):
   - \\cite{{zou2023representation}}: representation engineering finds deception-related directions
     in activation space (white-box, requires model internals)
   - \\cite{{burns2022discovering}}: probing classifiers for model honesty (white-box)
   - Contrast with our black-box behavioral approach: no model internals needed
4. §2.4 Sycophancy, Sandbagging, and AI Safety Risks (REQUIRED — reviewer called this out):
   - \\cite{{hubinger2019risks}}: deceptive alignment in advanced AI systems
   - \\cite{{perez2022discovering}}: sycophancy in LLMs
   - Note this paper addresses instructed roleplay, not autonomous strategic deception
5. §2.5 LLM Red-Teaming and Evaluation:
   - \\cite{{ganguli2022red}}: red-teaming language models at scale
   - \\cite{{perez2022red}}: red teaming with LMs
   - Gap: prior red-teaming focuses on eliciting harmful outputs, not detecting deception

End with a clear paragraph stating the gap: "No prior work combines adaptive multi-turn behavioral
interrogation with confidence-based early stopping for black-box deception detection."

{real_llm}

Research documentation:
{{doc}}
""",

    "methodology": """Write the LaTeX content for the Methodology section (REVISED).
Use \\section{{Methodology}} with subsections. Target ~1000 words.

CRITICAL CHANGES required by reviewer:
1. §3.1 System Overview: Use a REAL TikZ diagram (not a placeholder fbox). Write the full
   LaTeX TikZ code for a horizontal pipeline diagram:
   \\usepackage{{tikz}} is already in preamble.
   Draw five boxes connected by arrows:
   [Target Model] → [Interrogator] → [Feature Extractor] → [Classifier] → [Adaptive Controller]
   with a feedback arrow from [Adaptive Controller] back to [Interrogator].
   Use \\begin{{figure}}[t] \\centering \\begin{{tikzpicture}}...\\end{{tikzpicture}} \\caption{{...}}
   \\label{{fig:architecture}} \\end{{figure}}

2. §3.2 Target Model: truth/lie mode system prompts (verbatim in \\begin{{verbatim}}).
   IMPORTANT: Add a subsection "§3.2.3 Scope Note" explicitly stating: "The target operates
   in cooperative roleplay mode — it is instructed to defend a false claim. This is distinct
   from autonomous deceptive behaviour where a model strategically misleads without instruction.
   We study the former as a tractable experimental proxy."

3. §3.3 Interrogation Strategy: question generation with LLM, question taxonomy.

4. §3.4 Feature Extraction: table with \\label{{tab:behavioral_features}} (NOT tab:features —
   this avoids duplicate label conflict). Include 5 features with descriptions and why-it-matters.
   ALSO add a paragraph: "Feature validity note: scores are assigned by an LLM judge, introducing
   circularity — the extractor may capture stylistic artifacts of the prompts rather than genuine
   deception signals. No ground-truth validation of feature scores was performed."

5. §3.5 Classification: logistic regression. Add: "We choose logistic regression for
   interpretability; feature coefficients reveal which behavioral signals drive predictions."

6. §3.6 Adaptive Stopping: formal equation. Use \\begin{{equation}} for the stopping rule.

{real_llm}

Research documentation:
{{doc}}
""",

    "experiments": """Write the LaTeX content for the Experiments section (MAJOR REVISION).
Use \\section{{Experiments}}. Target ~1300 words.

CRITICAL CHANGES required by reviewer:

§4.1 Experimental Setup:
- Clearly state: "All mock experiments use deterministic pattern-matching models (MockTargetModel).
  Statistics are descriptive — p-values are not meaningful for deterministic processes and are
  omitted from this revision."
- Table of hyperparameters.
- Claims used (truth/lie examples).

§4.2 Core Detection Accuracy (n=100, NOT n=10):
Use the n=100 mock results: Adaptive: 91% accuracy (truthful: 100%, lying: 82%), avg 2.0 questions.
Do NOT report 100% perfect accuracy — that was the flawed n=10 result. Use:
\\begin{{table}}[h] \\centering \\caption{{Adaptive system accuracy on n=100 mock interrogations}}
Show: overall acc=91%, truthful acc=100%, lying acc=82%, precision=1.00, recall=0.82, F1=0.901.

§4.3 Adaptive vs. Fixed Baseline (n=100):
Adaptive: 91% accuracy, 2.0 avg questions. Fixed (8Q): 100% accuracy, 8.0 avg questions.
Efficiency gain: 75% fewer questions. IMPORTANT: add caveat — "The fixed baseline always asks
8 questions; this number is arbitrary. On the deterministic mock setup, even 1 question may
suffice. The efficiency result demonstrates that early stopping works on mock patterns, but
the absolute question counts should not be interpreted as evidence for real-world efficiency."
Remove p-values and Cohen's d from this comparison (mock is deterministic, statistics misleading).

§4.4 Feature Importance:
Open-ended questions 58% more diagnostic than detail probes (0.280 vs 0.177 avg confidence change).
Effect size d=0.91 is meaningful here (this compares question types, not systems). Keep this result.

§4.5 Confidence Trajectory:
Table showing confidence by question number. Discussion of diminishing returns.

§4.6 Failure Analysis:
Only 0.04 confidence gap between correct (0.88) and incorrect (0.84) predictions.
Interpret this clearly as a calibration failure, not a subtle distinction.

§4.7 Real LLM Pilot (NEW — directly addresses reviewer concern #1):
"To assess whether the framework transfers beyond mock models, we conducted a pilot evaluation
using Claude Haiku 4.5 (\\cite{{anthropic2024claude}}) via AWS Bedrock as the target model —
a production-grade LLM, not a pattern-matching mock."
Results table: n=9 completed, 88.9% overall, 100% truthful, 50% lying, avg 3.0 questions.
Discuss: (1) truthful detection transfers well, (2) lying detection harder on real LLMs (50% vs 82%),
(3) the misclassification had 0.92 confidence (calibration failure confirmed on real model),
(4) pilot is underpowered (n=9) but provides directional signal.
End with: "Full validation on real LLMs at scale remains as future work."

All tables must use \\begin{{table}}[h] \\centering \\caption{{...}} \\label{{tab:...}}
\\begin{{tabular}} with \\toprule \\midrule \\bottomrule (booktabs).

{real_llm}

Research documentation:
{{doc}}
""",

    "discussion": """Write the LaTeX content for the Discussion section (REVISED).
Use \\section{{Discussion}} with structured subsections. Target ~600 words.

CRITICAL restructuring required by reviewer:

§5.1 Key Findings: 3 bullet paragraphs — adaptive efficiency, confidence convergence, question type.

§5.2 Instructed Roleplay vs. Genuine Deception (REQUIRED — reviewer said this was inadequate):
Write a DEDICATED subsection (not buried in limitations) making this explicit:
"The experimental setting in this paper involves instructed cooperative roleplay: the target model
is given an explicit system prompt instructing it to defend a specific false claim. This is
fundamentally different from the AI safety scenario of autonomous strategic deception
\\cite{{hubinger2019risks}}, where a model independently chooses to mislead. Our setting is closer
to testing whether a verifier can distinguish \\emph{{prompted lying}} from \\emph{{prompted truth-telling}}.
This is a tractable experimental proxy for studying behavioral detection methods, but findings
may not generalise to models that deceive without instruction."

§5.3 Feature Extraction Validity (REQUIRED — reviewer raised circularity issue):
"The five behavioral features are scored by an LLM judge (Claude Haiku). This introduces
circularity: the extractor may be sensitive to surface-level stylistic differences between
truth and lie prompts rather than genuine deception signals. There is no ground-truth annotation
of feature scores, and no human inter-rater reliability study was conducted. Future work
should validate features against human judgments or interpretability methods
\\cite{{zou2023representation}}."

§5.4 Limitations: cover remaining issues —
(a) Mock model testing (all confirmed by real LLM pilot)
(b) Small sample sizes and need for scale
(c) Classifier overfitting risk (trained on same mock distribution tested on)
(d) Confidence calibration failure (narrow 0.04 gap; 0.92 confidence on wrong prediction in pilot)
(e) Limited claim diversity (subjective claims untested)
(f) Efficiency claims: "the 75% question reduction is an artifact of early information gain on
    deterministic mock patterns; this number should not be taken as an estimate for real deployments"

§5.5 Implications: AI safety red-teaming, black-box complement to probing, future directions.

{real_llm}

Research documentation:
{{doc}}
""",

    "conclusion": """Write the LaTeX content for the Conclusion section (REVISED).
Use \\section{{Conclusion}}. Target 180-220 words.

Requirements:
1. Accurately state what was shown: adaptive interrogation works in constrained roleplay settings
   (mock: 91% accuracy at 2.0 questions; real LLM pilot: 88.9% but only 50% lying accuracy).
2. Accurately state what was NOT shown: generalisation to real LLMs at scale, robustness to
   sophisticated adversarial lying, applicability to non-cooperative deception settings.
3. The real LLM pilot shows partial transfer — truthful detection works, lying detection degrades.
4. Broader implication: behavioral black-box interrogation is a complementary approach to
   white-box probing \\cite{{zou2023representation}} \\cite{{burns2022discovering}}.
5. Future work: real-model validation at scale, calibration, cross-model generalization,
   naturalistic (non-instructed) deception scenarios.

{real_llm}

Research documentation:
{{doc}}
""",
}

REFERENCES_PROMPT = """Generate a BibTeX references file for a NeurIPS paper on adaptive AI lie detection.
Include complete, accurate entries (realistic authors, venues, years) for ALL of the following:

REQUIRED (reviewer noted missing entries):
1. Zou et al. 2023 — Representation Engineering: A Top-Down Approach to AI Transparency (arxiv)
2. Burns et al. 2022 — Discovering Latent Knowledge in Language Models Without Supervision (arxiv/ICLR)
3. Hubinger et al. 2019 — Risks from Learned Optimization in Advanced ML Systems (arxiv)
4. Perez et al. 2022 — Discovering Language Model Behaviors with Model-Written Evaluations (sycophancy)
5. Ganguli et al. 2022 — Red Teaming Language Models to Reduce Harms (Anthropic, arxiv)
   Include journal/booktitle field so bibtex does not warn about empty journal.
6. Perez et al. 2022 — Ignore Previous Prompt: Attack Techniques For Language Models (prompt injection)
   Include venue field.

ALSO INCLUDE:
7. Ekman 2003 — Emotions Revealed (human micro-expressions)
8. Raskin & Kircher — polygraph / concealed information test
9. Goodfellow et al. 2014 — Explaining and Harnessing Adversarial Examples (ICLR)
10. Ouyang et al. 2022 — Training language models to follow instructions with human feedback (InstructGPT, NeurIPS)
11. Bai et al. 2022 — Constitutional AI (Anthropic, arxiv)
12. Brown et al. 2020 — Language Models are Few-Shot Learners (GPT-3, NeurIPS)
13. Anthropic 2024 — Claude (model card / technical report)
14. Platt 1999 — Probabilistic outputs for SVMs (temperature/confidence calibration)
15. Guo et al. 2017 — On Calibration of Modern Neural Networks (ICML)
16. Shevlane et al. 2023 — Model evaluation for extreme risks (DeepMind, arxiv)

Output ONLY valid BibTeX entries, nothing else.
"""


# ---------------------------------------------------------------------------
# Core generation
# ---------------------------------------------------------------------------

def generate_section(client, model: str, section: str, doc: str) -> str:
    prompt_template = SECTION_PROMPTS[section]
    # New prompts use {real_llm} and {{doc}} (double-brace escapes the inner format call)
    # First inject real_llm, then inject doc
    user_prompt = prompt_template.format(real_llm=REAL_LLM_RESULTS, doc=doc)

    print(f"  Generating {section}...", end="", flush=True)
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    content = response.content[0].text
    # Strip any accidental markdown fences
    content = re.sub(r"^```(?:latex)?\n?", "", content, flags=re.MULTILINE)
    content = re.sub(r"\n?```$", "", content, flags=re.MULTILINE)
    print(" done.")
    return content


def generate_references(client, model: str) -> str:
    print("  Generating references.bib...", end="", flush=True)
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": REFERENCES_PROMPT}],
    )
    content = response.content[0].text
    content = re.sub(r"^```(?:bibtex)?\n?", "", content, flags=re.MULTILINE)
    content = re.sub(r"\n?```$", "", content, flags=re.MULTILINE)
    print(" done.")
    return content


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

MAIN_TEX_TEMPLATE = r"""\documentclass[10pt,letterpaper]{article}
\usepackage[final]{neurips_2024}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{url}
\usepackage{microtype}
\usepackage{verbatim}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{shapes.geometric,arrows.meta,positioning}
\lstset{
  basicstyle=\small\ttfamily,
  breaklines=true,
  frame=single,
  backgroundcolor=\color{gray!10},
}

\title{Adaptive Lie Detection Through Strategic Interrogation of Large Language Models}

\author{
  Anonymous Author(s) \\
  NeurIPS 2024 Submission
}

\begin{document}

\maketitle

\input{sections/abstract}
\input{sections/introduction}
\input{sections/related_work}
\input{sections/methodology}
\input{sections/experiments}
\input{sections/discussion}
\input{sections/conclusion}

\bibliographystyle{plain}
\bibliography{references}

\end{document}
"""


def assemble_main_tex(output_dir: Path) -> None:
    main_tex = output_dir / "main.tex"
    main_tex.write_text(MAIN_TEX_TEMPLATE)
    print(f"  Assembled {main_tex}")


# ---------------------------------------------------------------------------
# PDF compilation (reusing pattern from paper_agent/tex_writer.py)
# ---------------------------------------------------------------------------

def compile_pdf(output_dir: Path) -> bool:
    original_dir = os.getcwd()
    try:
        os.chdir(output_dir)
        print("  Running pdflatex (pass 1)...")
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "main.tex"],
            capture_output=True, text=True,
        )
        if (output_dir / "main.aux").exists():
            print("  Running bibtex...")
            subprocess.run(["bibtex", "main"], capture_output=True, text=True)
        print("  Running pdflatex (pass 2)...")
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "main.tex"],
            capture_output=True, text=True,
        )
        print("  Running pdflatex (pass 3)...")
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "main.tex"],
            capture_output=True, text=True,
        )
        pdf = output_dir / "main.pdf"
        if pdf.exists():
            print(f"\n  PDF generated: {pdf}")
            return True
        else:
            print("\n  PDF generation failed. Check main.log for errors.")
            if result.stdout:
                # Print last 30 lines of stdout for diagnostics
                lines = result.stdout.splitlines()
                print("\n  --- pdflatex output (last 30 lines) ---")
                print("\n".join(lines[-30:]))
            return False
    finally:
        os.chdir(original_dir)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_client(use_bedrock: bool):
    """Build and return the appropriate Anthropic client."""
    if use_bedrock:
        # Prefer explicit env vars; otherwise fall back to the boto3 credential
        # chain (~/.aws/credentials from `aws configure`, IAM role, etc.)
        aws_key = os.environ.get("AWS_ACCESS_KEY_ID")
        aws_secret = os.environ.get("AWS_SECRET_ACCESS_KEY")
        aws_region = (
            os.environ.get("AWS_REGION")
            or os.environ.get("AWS_DEFAULT_REGION")
        )
        kwargs = {}
        if aws_key and aws_secret:
            kwargs["aws_access_key"] = aws_key
            kwargs["aws_secret_key"] = aws_secret
        if aws_region:
            kwargs["aws_region"] = aws_region

        region_label = aws_region or "from ~/.aws/config"
        print(f"  Using AWS Bedrock (region: {region_label})")
        return anthropic.AnthropicBedrock(**kwargs)
    else:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print(
                "\nError: ANTHROPIC_API_KEY is not set.\n"
                "Set it in your environment:\n"
                "  export ANTHROPIC_API_KEY=sk-ant-...\n"
                "Or create a .env file in the repo root:\n"
                "  ANTHROPIC_API_KEY=sk-ant-...\n"
                "\nAlternatively, use --bedrock for AWS Bedrock.\n"
            )
            sys.exit(1)
        print("  Using Anthropic direct API")
        return anthropic.Anthropic(api_key=api_key)


def main():
    parser = argparse.ArgumentParser(description="Generate NeurIPS paper from RESEARCH_DOCUMENTATION.md")
    parser.add_argument("--bedrock", action="store_true",
                        help="Use AWS Bedrock instead of direct Anthropic API")
    parser.add_argument("--model", default=None,
                        help="Override model ID (default: claude-opus-4-6 or Bedrock equivalent)")
    parser.add_argument("--skip-compile", action="store_true", help="Generate LaTeX only, skip PDF compilation")
    parser.add_argument("--section", choices=SECTIONS, help="Regenerate a single section only")
    args = parser.parse_args()

    # Check source doc
    if not RESEARCH_DOC.exists():
        print(f"Error: {RESEARCH_DOC} not found.")
        sys.exit(1)

    doc = RESEARCH_DOC.read_text()
    print(f"Loaded research doc: {len(doc)} chars")

    # Ensure directories
    SECTIONS_DIR.mkdir(parents=True, exist_ok=True)

    # Copy .sty to output dir so pdflatex can find it
    import shutil
    shutil.copy(STY_FILE, OUTPUT_DIR / "neurips_2024.sty")

    # Init client and resolve model
    print("\nInitialising Claude client:")
    client = build_client(args.bedrock)
    if args.model:
        model = args.model
    else:
        model = DEFAULT_MODEL_BEDROCK if args.bedrock else DEFAULT_MODEL_DIRECT
    print(f"  Model: {model}")

    # Generate sections
    if args.section:
        print(f"\nRegenerating section: {args.section}")
        content = generate_section(client, model, args.section, doc)
        (SECTIONS_DIR / f"{args.section}.tex").write_text(content)
    else:
        print("\nGenerating paper sections:")
        for section in SECTIONS:
            content = generate_section(client, model, section, doc)
            (SECTIONS_DIR / f"{section}.tex").write_text(content)

        print("\nGenerating bibliography:")
        bib_content = generate_references(client, model)
        (OUTPUT_DIR / "references.bib").write_text(bib_content)

        print("\nAssembling main.tex:")
        assemble_main_tex(OUTPUT_DIR)

    if not args.skip_compile:
        print("\nCompiling PDF:")
        compile_pdf(OUTPUT_DIR)
    else:
        print("\nSkipping PDF compilation (--skip-compile).")
        print(f"Run manually: cd {OUTPUT_DIR} && pdflatex main.tex")


if __name__ == "__main__":
    main()
