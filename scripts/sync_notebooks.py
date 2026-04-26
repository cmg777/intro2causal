#!/usr/bin/env python3
"""
Synchronize Colab (.ipynb) and Markdown (.md) notebooks from book source (.qmd).

The book versions in book/notebooks_quarto/ are the source of truth.
This script regenerates:
  - notebooks_colab/*.ipynb  (Jupyter/Colab format)
  - notebooks_md/*.md        (plain Markdown format)
  - notebooks_quarto/*.qmd   (standalone Quarto format)

Usage:
    python scripts/sync_notebooks.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK_DIR = ROOT / "book" / "notebooks_quarto"
COLAB_DIR = ROOT / "notebooks_colab"
MD_DIR = ROOT / "notebooks_md"
STANDALONE_DIR = ROOT / "notebooks_quarto"

# Chapter metadata
CHAPTERS = {
    "01-randomized-trials": "Chapter 1: Randomized Trials",
    "02-regression": "Chapter 2: Regression",
    "03-instrumental-variables": "Chapter 3: Instrumental Variables",
    "04-regression-discontinuity": "Chapter 4: Regression Discontinuity",
    "05-differences-in-differences": "Chapter 5: Differences in Differences",
    "06-wages-of-schooling": "Chapter 6: Wages of Schooling",
}

# Callout type → emoji mapping
CALLOUT_EMOJI = {
    "tip": "💡",
    "note": "📝",
    "important": "⭐",
    "warning": "⚠️",
    "caution": "🔶",
}


def read_qmd(path: Path) -> str:
    """Read a .qmd file and strip the YAML frontmatter."""
    text = path.read_text(encoding="utf-8")
    # Remove YAML frontmatter (between --- delimiters)
    match = re.match(r"^---\n.*?\n---\n", text, re.DOTALL)
    if match:
        text = text[match.end():]
    return text


def extract_title_from_yaml(path: Path) -> str:
    """Extract the title field from YAML frontmatter."""
    text = path.read_text(encoding="utf-8")
    match = re.search(r'^title:\s*"(.+?)"', text, re.MULTILINE)
    if match:
        return match.group(1)
    return ""


def strip_book_chrome(text: str) -> str:
    """Remove book-specific elements (SVG image, badges)."""
    lines = text.split("\n")
    filtered = []
    for line in lines:
        # Skip SVG image references
        if re.match(r"!\[.*\]\(\.\./images/.*\.svg\)", line.strip()):
            continue
        # Skip badge lines
        if "[![Open In Colab]" in line or "[![Return to Book Website]" in line:
            continue
        filtered.append(line)
    return "\n".join(filtered)


def convert_callouts_to_blockquotes(text: str) -> str:
    """Convert Quarto callout blocks to emoji blockquote format."""
    lines = text.split("\n")
    result = []
    in_callout = False
    callout_emoji = ""
    callout_depth = 0
    skip_closing = 0

    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect callout opening: ::: {.callout-TYPE ...}
        callout_match = re.match(
            r'^(:{3,})\s*\{\.callout-(\w+)(?:\s+collapse="[^"]*")?(?:\s+appearance="[^"]*")?(?:\s+title="([^"]*)")?\}',
            line,
        )
        if callout_match:
            colons = callout_match.group(1)
            ctype = callout_match.group(2)
            title = callout_match.group(3)
            emoji = CALLOUT_EMOJI.get(ctype, "📝")
            callout_depth += 1

            if not in_callout:
                in_callout = True
                callout_emoji = emoji

                # Look for title on next line (e.g., ### Title or ## Title)
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    heading_match = re.match(r"^#{1,4}\s+(.+)", next_line)
                    if heading_match:
                        heading_text = heading_match.group(1)
                        result.append(f"> {emoji} **{heading_text}**")
                        result.append(">")
                        i += 2
                        continue
                    elif title:
                        result.append(f"> {emoji} **{title}**")
                        result.append(">")
                        i += 1
                        continue

                if title:
                    result.append(f"> {emoji} **{title}**")
                    result.append(">")
                else:
                    result.append(f"> {emoji}")
                    result.append(">")
                i += 1
                continue
            else:
                # Nested callout - just use the title if present
                if title:
                    result.append(f"> **{title}**")
                    result.append(">")
                i += 1
                continue

        # Detect closing :::
        if re.match(r"^:{3,}\s*$", line.strip()) and in_callout:
            callout_depth -= 1
            if callout_depth <= 0:
                in_callout = False
                callout_depth = 0
                result.append("")
                i += 1
                continue
            i += 1
            continue

        # Skip column wrappers
        if re.match(r"^:{3,}\s*\{\.column", line.strip()):
            i += 1
            continue
        if re.match(r"^:{3,}\s*\{\.columns\}", line.strip()):
            i += 1
            continue

        # Inside callout: prefix lines with >
        if in_callout:
            # Skip heading lines that were already captured
            if re.match(r"^#{1,4}\s+", line.strip()):
                # Check if this is the heading right after callout open
                if i > 0 and re.match(r"^:{3,}\s*\{\.callout", lines[i - 1].strip()):
                    i += 1
                    continue
            if line.strip():
                result.append(f"> {line.strip()}")
            else:
                result.append(">")
        else:
            result.append(line)

        i += 1

    return "\n".join(result)


def convert_callouts_simple(text: str) -> str:
    """Simpler callout conversion that handles nested structures better."""
    lines = text.split("\n")
    result = []
    callout_stack = []  # Stack to track nested callouts/divs

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Detect callout opening
        callout_match = re.match(
            r'^(:{3,})\s*\{\.callout-(\w+)(?:\s+collapse="[^"]*")?(?:\s+appearance="[^"]*")?(?:\s+title="([^"]*)")?\}',
            stripped,
        )

        # Detect column/div opening (not callout)
        div_match = re.match(r"^:{4,}\s*\{", stripped)

        if callout_match:
            ctype = callout_match.group(2)
            title = callout_match.group(3)
            emoji = CALLOUT_EMOJI.get(ctype, "📝")
            callout_stack.append("callout")

            # Check next line for heading
            if i + 1 < len(lines):
                next_stripped = lines[i + 1].strip()
                heading_match = re.match(r"^#{1,4}\s+(.+)", next_stripped)
                if heading_match:
                    result.append(f"> {emoji} **{heading_match.group(1)}**")
                    result.append(">")
                    i += 2
                    continue

            if title:
                result.append(f"> {emoji} **{title}**")
                result.append(">")
            else:
                result.append(f"> {emoji}")
                result.append(">")
            i += 1
            continue

        elif div_match or re.match(r"^:{4,}\s*$", stripped):
            # Column or multi-colon div wrapper
            callout_stack.append("div")
            i += 1
            continue

        elif re.match(r"^:{3,}\s*$", stripped):
            if callout_stack:
                popped = callout_stack.pop()
                if popped == "callout" and not any(
                    c == "callout" for c in callout_stack
                ):
                    result.append("")
            i += 1
            continue

        # Content lines
        if any(c == "callout" for c in callout_stack):
            if stripped:
                result.append(f"> {stripped}")
            else:
                result.append(">")
        else:
            result.append(line)

        i += 1

    return "\n".join(result)


def convert_mermaid_for_md(text: str) -> str:
    """Convert Quarto mermaid blocks to plain mermaid code blocks for markdown."""
    # Replace ```{mermaid} with ```mermaid and strip %%| directives
    def replace_mermaid(match):
        content = match.group(1)
        # Remove %%| directives
        content_lines = []
        for line in content.split("\n"):
            if line.strip().startswith("%%|"):
                continue
            # Change stroke color for better visibility in plain markdown
            line = line.replace("stroke:#64748b", "stroke:#fff")
            content_lines.append(line)
        return "```mermaid\n" + "\n".join(content_lines) + "\n```"

    text = re.sub(r"```\{mermaid\}\n(.*?)\n```", replace_mermaid, text, flags=re.DOTALL)
    return text


def convert_mermaid_for_colab(text: str) -> str:
    """Replace mermaid blocks with placeholder text for Colab."""

    def replace_mermaid(match):
        content = match.group(1)
        # Try to extract fig-cap
        cap_match = re.search(r'%%\|\s*fig-cap:\s*"(.+?)"', content)
        if cap_match:
            caption = cap_match.group(1)
        else:
            # Try to extract a meaningful title from node labels
            label_match = re.search(r'\["(.+?)"\]', content)
            caption = label_match.group(1) if label_match else "Diagram"
        return f'> 📊 **{caption}** *(diagram — view in the [online book](https://cmg777.github.io/intro2causal/))*'

    text = re.sub(
        r"```\{mermaid\}\n(.*?)\n```", replace_mermaid, text, flags=re.DOTALL
    )
    return text


def convert_python_blocks_for_md(text: str) -> str:
    """Convert Quarto Python blocks to plain markdown code blocks."""
    # Replace ```{python} with ```python and strip #| directives
    def replace_python(match):
        content = match.group(1)
        content_lines = []
        for line in content.split("\n"):
            if line.strip().startswith("#|"):
                continue
            content_lines.append(line)
        # Remove leading blank lines
        while content_lines and not content_lines[0].strip():
            content_lines.pop(0)
        return "```python\n" + "\n".join(content_lines) + "\n```"

    text = re.sub(
        r"```\{python\}\n(.*?)\n```", replace_python, text, flags=re.DOTALL
    )
    return text


def convert_tables(text: str) -> str:
    """Clean up Quarto table attributes."""
    # Remove {.striped} and {#tbl-xxx .striped} etc from table captions
    text = re.sub(r"\s*\{[#.][\w\s.-]*\}\s*$", "", text, flags=re.MULTILINE)
    return text


def remove_columns_layout(text: str) -> str:
    """Remove Quarto column layout divs, keeping content."""
    # Remove ::::: {.columns} and :::: {.column ...} wrappers
    text = re.sub(r"^:{3,}\s*\{\.columns\}\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r'^:{3,}\s*\{\.column\s+width="[^"]*"\}\s*$', "", text, flags=re.MULTILINE)
    # Remove standalone closing divs (:::, ::::, :::::) that are just layout closers
    # This is handled by the callout converter
    return text


def qmd_to_markdown(qmd_path: Path, chapter_slug: str) -> str:
    """Convert a book .qmd file to plain markdown format."""
    title = CHAPTERS[chapter_slug]
    content = read_qmd(qmd_path)
    content = strip_book_chrome(content)

    # Convert mermaid blocks
    content = convert_mermaid_for_md(content)

    # Convert Python code blocks
    content = convert_python_blocks_for_md(content)

    # Convert callouts to blockquotes
    content = convert_callouts_simple(content)

    # Clean up tables
    content = convert_tables(content)

    # Adjust heading levels: ## → ## (keep same since title is #)
    # Actually in the book version, ## is the top level (under the YAML title)
    # For standalone md, we want # for the title, ## for main sections
    # The book uses ##, which maps correctly since we add # title separately

    # Build the header
    header = f"""# {title}

**Mastering Causal Metrics: An AI-Powered Study Guide**

*A companion to Mastering 'Metrics by Angrist & Pischke*

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/intro2causal/blob/main/notebooks_colab/{chapter_slug}.ipynb)

---
"""

    # Clean up excessive blank lines
    content = re.sub(r"\n{4,}", "\n\n\n", content)

    return header + content


def split_into_cells(content: str):
    """Split markdown+code content into a list of (type, content) cells."""
    cells = []
    lines = content.split("\n")
    current_type = "markdown"
    current_lines = []
    in_code_block = False
    code_lang = None

    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect Python code block start
        if not in_code_block and re.match(r"^```\{python\}", line.strip()):
            # Flush current markdown
            md_text = "\n".join(current_lines).strip()
            if md_text:
                cells.append(("markdown", md_text))
            current_lines = []
            in_code_block = True
            code_lang = "python"
            i += 1
            continue

        # Detect code block end
        if in_code_block and re.match(r"^```\s*$", line.strip()):
            code_text = "\n".join(current_lines)
            # Strip #| directives
            code_lines = []
            for cl in code_text.split("\n"):
                if cl.strip().startswith("#|"):
                    continue
                code_lines.append(cl)
            # Remove leading blank lines
            while code_lines and not code_lines[0].strip():
                code_lines.pop(0)
            code_text = "\n".join(code_lines).rstrip()
            if code_text:
                cells.append(("code", code_text))
            current_lines = []
            in_code_block = False
            code_lang = None
            i += 1
            continue

        current_lines.append(line)
        i += 1

    # Flush remaining
    remaining = "\n".join(current_lines).strip()
    if remaining:
        cells.append((current_type, remaining))

    return cells


def convert_callouts_in_cells(raw_cells):
    """Convert callout syntax in markdown cells, tracking state across code cell boundaries.

    Code blocks that were inside callouts in the source become standalone code cells,
    making them executable in Jupyter/Colab.
    """
    processed = []
    in_callout = False
    callout_stack_depth = 0

    for cell_type, cell_content in raw_cells:
        if cell_type == "code":
            processed.append(("code", cell_content))
            continue

        lines = cell_content.split("\n")
        result_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Detect callout opening
            callout_match = re.match(
                r'^:{3,}\s*\{\.callout-(\w+)(?:\s+collapse="[^"]*")?(?:\s+appearance="[^"]*")?(?:\s+title="([^"]*)")?\}',
                stripped,
            )

            # Detect column/div opening (not callout)
            div_match = re.match(r"^:{4,}\s*\{", stripped) and not callout_match

            if callout_match:
                ctype = callout_match.group(1)
                title = callout_match.group(2)
                emoji = CALLOUT_EMOJI.get(ctype, "📝")
                in_callout = True
                callout_stack_depth += 1

                # Check next line for heading
                if i + 1 < len(lines):
                    next_stripped = lines[i + 1].strip()
                    heading_match = re.match(r"^#{1,4}\s+(.+)", next_stripped)
                    if heading_match:
                        result_lines.append(f"> {emoji} **{heading_match.group(1)}**")
                        result_lines.append(">")
                        i += 2
                        continue

                if title:
                    result_lines.append(f"> {emoji} **{title}**")
                    result_lines.append(">")
                else:
                    result_lines.append(f"> {emoji}")
                    result_lines.append(">")
                i += 1
                continue

            elif div_match or re.match(r"^:{4,}\s*$", stripped):
                # Column/div wrapper - skip silently
                i += 1
                continue

            elif re.match(r"^:{3,}\s*$", stripped):
                if callout_stack_depth > 0:
                    callout_stack_depth -= 1
                    if callout_stack_depth == 0:
                        in_callout = False
                        result_lines.append("")
                i += 1
                continue

            # Content lines
            if in_callout:
                if stripped:
                    result_lines.append(f"> {stripped}")
                else:
                    result_lines.append(">")
            else:
                result_lines.append(line)

            i += 1

        md_text = "\n".join(result_lines).strip()
        if md_text:
            processed.append(("markdown", md_text))

    return processed


def qmd_to_ipynb(qmd_path: Path, chapter_slug: str) -> dict:
    """Convert a book .qmd file to Jupyter notebook (ipynb) format."""
    title = CHAPTERS[chapter_slug]
    content = read_qmd(qmd_path)
    content = strip_book_chrome(content)

    # Convert mermaid to placeholders BEFORE splitting cells
    content = convert_mermaid_for_colab(content)

    # Clean up tables
    content = convert_tables(content)

    # Remove column layout wrappers
    content = remove_columns_layout(content)

    # Clean up excessive blank lines
    content = re.sub(r"\n{4,}", "\n\n\n", content)

    # Split into cells FIRST (extracts {python} blocks even inside callouts)
    raw_cells = split_into_cells(content)

    # THEN convert callouts in markdown cells (preserving code cells as executable)
    processed_cells = convert_callouts_in_cells(raw_cells)

    # Build header markdown
    header = f"""# {title}

**Mastering Causal Metrics: An AI-Powered Study Guide**

*A companion to Mastering 'Metrics by Angrist & Pischke*

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/intro2causal/blob/main/notebooks_colab/{chapter_slug}.ipynb)

---"""

    # Build notebook cells
    nb_cells = []

    # Add header cell
    nb_cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": header.split("\n"),
        }
    )

    for cell_type, cell_content in processed_cells:
        if cell_type == "markdown":
            # Split into lines for notebook format
            content_lines = cell_content.split("\n")
            source_lines = []
            for j, line in enumerate(content_lines):
                if j < len(content_lines) - 1:
                    source_lines.append(line + "\n")
                else:
                    source_lines.append(line)
            nb_cells.append(
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": source_lines,
                }
            )
        else:
            content_lines = cell_content.split("\n")
            source_lines = []
            for j, line in enumerate(content_lines):
                if j < len(content_lines) - 1:
                    source_lines.append(line + "\n")
                else:
                    source_lines.append(line)
            nb_cells.append(
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": source_lines,
                }
            )

    # Build notebook structure
    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.12.0",
                "mimetype": "text/x-python",
                "file_extension": ".py",
            },
            "colab": {
                "provenance": [],
                "toc_visible": True,
            },
        },
        "cells": nb_cells,
    }

    return notebook


STANDALONE_YAML = """\
---
title: "{title}"
subtitle: "A Study Guide for *Mastering 'Metrics* by Angrist & Pischke"
format:
  html:
    toc: true
    toc-depth: 3
    code-tools: true
    code-fold: true
    number-sections: true
    theme: cosmo
    self-contained: true
execute:
  warning: false
  message: false
---
"""


def qmd_to_standalone(qmd_path: Path, chapter_slug: str) -> str:
    """Convert a book .qmd file to standalone .qmd format.

    Replaces the minimal book YAML with a full standalone header
    and removes book-specific elements (SVG image, badges).
    Content (including heading levels) is preserved as-is.
    """
    title = CHAPTERS[chapter_slug]
    content = read_qmd(qmd_path)
    content = strip_book_chrome(content)

    # Build standalone YAML header
    yaml = STANDALONE_YAML.format(title=title)

    # Clean up excessive blank lines
    content = re.sub(r"\n{4,}", "\n\n\n", content)

    return yaml + content


def main():
    """Regenerate all Colab, Markdown, and standalone Quarto notebooks from book sources."""
    COLAB_DIR.mkdir(exist_ok=True)
    MD_DIR.mkdir(exist_ok=True)
    STANDALONE_DIR.mkdir(exist_ok=True)

    for slug, title in CHAPTERS.items():
        qmd_path = BOOK_DIR / f"{slug}.qmd"
        if not qmd_path.exists():
            print(f"  SKIP {slug} — source not found")
            continue

        print(f"  Processing {slug}...")

        # Generate standalone Quarto version
        standalone_content = qmd_to_standalone(qmd_path, slug)
        standalone_path = STANDALONE_DIR / f"{slug}.qmd"
        standalone_path.write_text(standalone_content, encoding="utf-8")
        print(f"    ✓ {standalone_path.relative_to(ROOT)}")

        # Generate Markdown version
        md_content = qmd_to_markdown(qmd_path, slug)
        md_path = MD_DIR / f"{slug}.md"
        md_path.write_text(md_content, encoding="utf-8")
        print(f"    ✓ {md_path.relative_to(ROOT)}")

        # Generate Colab version
        notebook = qmd_to_ipynb(qmd_path, slug)
        ipynb_path = COLAB_DIR / f"{slug}.ipynb"
        ipynb_path.write_text(
            json.dumps(notebook, indent=1, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"    ✓ {ipynb_path.relative_to(ROOT)}")

    print("\n  Done! All notebooks synchronized.")


if __name__ == "__main__":
    main()
