#!/usr/bin/env python3
"""
generate_conference_paper.py

Generates a NeurIPS 2024 conference paper from RESEARCH_DOCUMENTATION.md
using Claude API (claude-opus-4-6) for each section, then compiles to PDF.

Usage:
    python generate_conference_paper.py
    python generate_conference_paper.py --skip-compile   # generate LaTeX only
    python generate_conference_paper.py --section intro  # regenerate one section
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

# ---------------------------------------------------------------------------
# Section prompts
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are an expert academic writer helping produce a NeurIPS 2024 conference paper.
Write ONLY the LaTeX body content for the requested section — no \\documentclass, no \\begin{{document}},
no preamble, and no markdown code fences. Use proper LaTeX commands throughout.
Write in third-person academic style. Be precise, formal, and technically rigorous.
Where you introduce citations use \\cite{{key}} with reasonable BibTeX keys (e.g. \\cite{{vaswani2017attention}}).
"""

SECTION_PROMPTS = {
    "abstract": """Write the LaTeX content for the Abstract section of a NeurIPS paper.
Use the \\begin{{abstract}} ... \\end{{abstract}} environment.
Target 150-200 words. Highlight:
- The problem: detecting deception in LLMs through behavioral analysis
- The method: adaptive interrogation with confidence-based early stopping
- Key result: 70% reduction in questions with 100% accuracy on controlled tests
- Honest limitation: results are on mock models, real-model validation is future work

Research documentation:
{doc}
""",

    "introduction": """Write the LaTeX content for the Introduction section.
Use \\section{{Introduction}} and 3-4 subsections covering:
1. Motivation — why AI deception detection matters (safety, alignment, interpretability)
2. The challenge — why LLM lies are hard to detect compared to human lies
3. Our approach — the 4-part adaptive interrogation strategy
4. Contributions — bullet list with \\begin{{itemize}}

Target ~800 words. End with a roadmap sentence ("The remainder of this paper is structured as follows...").

Research documentation:
{doc}
""",

    "related_work": """Write the LaTeX content for the Related Work section.
Use \\section{{Related Work}} and organise into 3-4 subsections:
1. Human deception detection (polygraphs, micro-expressions — not directly applicable)
2. Adversarial examples and prompt injection (different from intentional model deception)
3. AI interpretability and alignment (complementary internal-state approaches)
4. LLM evaluation and red-teaming (closest prior work, highlight the gap)

For each area, write 2-4 sentences, use \\cite{{}} with plausible BibTeX keys, and end with
a paragraph explaining the gap this work fills. Target ~600 words.

Research documentation:
{doc}
""",

    "methodology": """Write the LaTeX content for the Methodology section.
Use \\section{{Methodology}} with subsections for each component:
1. System Overview — describe the 5-component pipeline with a \\begin{{figure}} placeholder
   (use \\fbox{{\\parbox{{...}}{{System diagram placeholder}}}} as a placeholder figure)
2. Target Model Setup — truth mode vs lie mode, include the system prompts verbatim
   in \\begin{{lstlisting}} or \\begin{{verbatim}} blocks
3. Interrogation Strategy — LLM-based question generation, question type taxonomy
4. Feature Extraction — table of the 5 features (consistency, specificity, defensiveness,
   confidence, elaboration) using \\begin{{table}} with booktabs
5. Classification — logistic regression with L2, training procedure, hyperparameters
6. Adaptive Stopping — formal definition of stopping criteria with math notation

Target ~1000 words. Use \\begin{{equation}} for any mathematical expressions.

Research documentation:
{doc}
""",

    "experiments": """Write the LaTeX content for the Experiments section.
Use \\section{{Experiments}} with subsections for each of the 6 experiments:
1. Experimental Setup — mock models, claims used (truth/lie examples), hyperparameters table
2. Core Detection Accuracy — confusion matrix as a table, precision/recall/F1
3. Adaptive vs Fixed-Question Baseline — comparison table with accuracy + avg questions,
   include t-test result (t=-28.24, p<0.001) and Cohen's d=12.63
4. Feature Importance Analysis — table of question types with avg confidence change,
   statistical significance (t=2.14, p=0.045, Cohen's d=0.91)
5. Confidence Trajectory Analysis — table of confidence by question number, discuss
   diminishing returns after Q2
6. Failure Analysis — false negative characteristics, calibration discussion
7. Topic Inference (Ablation) — automatic vs manual topic specification

Use \\begin{{table}}[h] \\centering \\caption{{...}} \\begin{{tabular}}{{...}} with booktabs
(\\toprule, \\midrule, \\bottomrule) for all tables. Target ~1200 words.

Research documentation:
{doc}
""",

    "discussion": """Write the LaTeX content for the Discussion section.
Use \\section{{Discussion}} with subsections:
1. Key Findings — brief summary (not repetition) of the 3 main takeaways
2. Limitations — thorough treatment of all 6 limitations identified in the research:
   mock models, roleplay vs real deception, small sample sizes, overfitting risk,
   confidence calibration, limited claim diversity
3. Implications for AI Safety — how adaptive interrogation complements interpretability,
   relevance to alignment evaluation and red-teaming
4. Future Work — immediate priorities (real model validation, larger datasets,
   calibration, cross-model testing) and longer-term directions

Be honest about the preliminary nature of results. Target ~500 words.

Research documentation:
{doc}
""",

    "conclusion": """Write the LaTeX content for the Conclusion section.
Use \\section{{Conclusion}}.
Summarise: (1) what the system does, (2) what was shown (efficiency gains in controlled setting),
(3) what was NOT shown (real-model generalization), and (4) the broader implication for AI safety research.
Be concise (150-200 words). Do not introduce new information.

Research documentation:
{doc}
""",
}

REFERENCES_PROMPT = """Generate a BibTeX references file for a NeurIPS paper on adaptive AI lie detection.
Include entries for:
1. Key human deception detection papers (polygraph, micro-expressions)
2. Adversarial examples in deep learning (e.g. Goodfellow et al. FGSM)
3. Prompt injection / jailbreaking papers
4. LLM alignment and RLHF papers (Ouyang et al. InstructGPT, Bai et al. Constitutional AI)
5. AI interpretability (Anthropic, mechanistic interpretability)
6. Red-teaming LLMs (Perez et al., Ganguli et al.)
7. Logistic regression / calibration (Platt scaling, temperature scaling)
8. Transformer / GPT architecture references (Vaswani et al., Brown et al. GPT-3)

Output ONLY valid BibTeX entries, nothing else. Use realistic author names, venues, and years.
"""


# ---------------------------------------------------------------------------
# Core generation
# ---------------------------------------------------------------------------

def generate_section(client: anthropic.Anthropic, section: str, doc: str) -> str:
    prompt_template = SECTION_PROMPTS[section]
    user_prompt = prompt_template.format(doc=doc)

    print(f"  Generating {section}...", end="", flush=True)
    response = client.messages.create(
        model="claude-opus-4-6",
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


def generate_references(client: anthropic.Anthropic) -> str:
    print("  Generating references.bib...", end="", flush=True)
    response = client.messages.create(
        model="claude-opus-4-6",
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

MAIN_TEX_TEMPLATE = r"""\documentclass[10pt,letterpaper]{{article}}
\usepackage[final]{{neurips_2024}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage{{booktabs}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{graphicx}}
\usepackage{{hyperref}}
\usepackage{{url}}
\usepackage{{microtype}}
\usepackage{{verbatim}}
\usepackage{{listings}}
\usepackage{{xcolor}}
\lstset{{
  basicstyle=\small\ttfamily,
  breaklines=true,
  frame=single,
  backgroundcolor=\color{{gray!10}},
}}

\title{{Adaptive Lie Detection Through Strategic Interrogation of Large Language Models}}

\author{{
  Anonymous Author(s) \\\\
  NeurIPS 2024 Submission
}}

\begin{{document}}

\maketitle

\input{{sections/abstract}}
\input{{sections/introduction}}
\input{{sections/related_work}}
\input{{sections/methodology}}
\input{{sections/experiments}}
\input{{sections/discussion}}
\input{{sections/conclusion}}

\bibliographystyle{{plain}}
\bibliography{{references}}

\end{{document}}
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

def main():
    parser = argparse.ArgumentParser(description="Generate NeurIPS paper from RESEARCH_DOCUMENTATION.md")
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

    # Init Claude client
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print(
            "\nError: ANTHROPIC_API_KEY is not set.\n"
            "Set it in your environment:\n"
            "  export ANTHROPIC_API_KEY=sk-ant-...\n"
            "Or create a .env file in the repo root with:\n"
            "  ANTHROPIC_API_KEY=sk-ant-...\n"
        )
        sys.exit(1)
    client = anthropic.Anthropic(api_key=api_key)

    # Generate sections
    if args.section:
        print(f"\nRegenerating section: {args.section}")
        content = generate_section(client, args.section, doc)
        (SECTIONS_DIR / f"{args.section}.tex").write_text(content)
    else:
        print("\nGenerating paper sections:")
        for section in SECTIONS:
            content = generate_section(client, section, doc)
            (SECTIONS_DIR / f"{section}.tex").write_text(content)

        print("\nGenerating bibliography:")
        bib_content = generate_references(client)
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
