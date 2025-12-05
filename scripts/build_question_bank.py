from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable, List, Optional

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "question_bank"
OUTPUT_PATH = OUTPUT_DIR / "index.json"
VALID_EXTENSIONS = {".pdf", ".doc", ".docx"}
YEAR_PATTERN = re.compile(r"(19|20)\d{2}")


def find_year(parts: Iterable[str]) -> tuple[Optional[str], Optional[int]]:
    for idx, part in enumerate(parts):
        match = YEAR_PATTERN.search(part)
        if match:
            return match.group(0), idx
    return None, None


def normalize_title(stem: str) -> str:
    cleaned = re.sub(r"[_\-]+", " ", stem)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def extract_stage(parts: List[str], year_index: Optional[int]) -> Optional[str]:
    if year_index is None:
        return None
    stage_parts = parts[year_index + 1 : -1]
    return "/".join(stage_parts) if stage_parts else None


def build_question_bank() -> list[dict]:
    entries: list[dict] = []
    for path in ROOT.rglob("*"):
        if path.is_dir():
            continue
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix.lower() not in VALID_EXTENSIONS:
            continue

        relative_parts = list(path.relative_to(ROOT).parts)
        competition = relative_parts[0] if len(relative_parts) > 1 else None
        year, year_index = find_year(relative_parts)
        title = normalize_title(path.stem)
        stage = extract_stage(relative_parts, year_index)

        entries.append(
            {
                "path": str(path.relative_to(ROOT)),
                "competition": competition,
                "year": int(year) if year else None,
                "stage": stage,
                "title": title,
                "format": path.suffix.lower().lstrip("."),
            }
        )

    entries.sort(
        key=lambda item: (
            item["competition"] or "~",  # ensure non-null competitions group together
            item["year"] or 0,
            item["stage"] or "",
            item["title"],
        )
    )
    return entries


def main() -> None:
    question_bank = build_question_bank()
    OUTPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(question_bank, ensure_ascii=False, indent=2))
    print(f"Saved {len(question_bank)} entries to {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
