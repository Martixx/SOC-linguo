#!/usr/bin/env python3
"""Normalize English SOC Lab battery metadata.

The script updates only top-level metadata fields:
  - name
  - category
  - version (when specified)

It never overwrites the source JSON files. Normalized copies are written to an
output directory, together with normalization_report.csv.

Usage:
    python normalize_english_soc_lab.py INPUT_DIR
    python normalize_english_soc_lab.py INPUT_DIR --output OUTPUT_DIR
    python normalize_english_soc_lab.py INPUT_DIR --dry-run

Matching strategy:
  1. Exact known filename aliases.
  2. Battery number detected in the filename.
  3. Battery number detected at the start of the top-level name.
  4. Conservative topic matching against the top-level name.

Unknown and ambiguous files are reported and left unchanged.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class BatterySpec:
    number: int
    topic: str
    category: str
    version: int = 1
    expected_questions: int | None = None
    aliases: tuple[str, ...] = ()

    @property
    def display_name(self) -> str:
        label = "Natural English" if self.category == "natural" else "Normal"
        return f"{self.number:02d} · {self.topic} · {label}"

    @property
    def output_filename(self) -> str:
        slug = re.sub(r"[^a-z0-9]+", "_", self.topic.lower()).strip("_")
        return f"{self.number:02d}_{slug}.json"


SPECS: dict[int, BatterySpec] = {
    1: BatterySpec(1, "Cybersecurity verb forms", "normal", expected_questions=30,
        aliases=("bateria_01_cybersecurity_verb_forms.json", "cybersecurity_verb_forms.json")),
    2: BatterySpec(2, "Present simple vs present continuous", "normal", expected_questions=30,
        aliases=("bateria_02_present_simple_vs_present_continuous.json",)),
    3: BatterySpec(3, "Past simple", "normal", expected_questions=30,
        aliases=("bateria_03_past_simple_soc_clientes.json", "bateria_03_past_simple_soc_communication.json")),
    4: BatterySpec(4, "Present perfect", "normal", expected_questions=30,
        aliases=("bateria_04_present_perfect_soc_clientes.json",)),
    5: BatterySpec(5, "Present perfect continuous", "normal", expected_questions=30,
        aliases=("bateria_05_present_perfect_continuous_soc_clientes.json",)),
    6: BatterySpec(6, "Past simple vs present perfect", "normal", expected_questions=30,
        aliases=("bateria_06_past_simple_vs_present_perfect_soc_clientes.json",)),
    7: BatterySpec(7, "Past perfect", "normal", expected_questions=30,
        aliases=("bateria_07_past_perfect_soc_clientes.json",)),
    8: BatterySpec(8, "Past perfect vs past simple", "normal", expected_questions=30,
        aliases=("bateria_08_past_perfect_vs_past_simple_soc_clientes.json",)),
    9: BatterySpec(9, "Past continuous", "normal", expected_questions=30,
        aliases=("bateria_09_past_continuous_soc_clientes.json",)),
    10: BatterySpec(10, "Past simple vs past continuous", "normal", expected_questions=30,
        aliases=("bateria_10_past_simple_vs_past_continuous_soc_clientes.json",)),
    11: BatterySpec(11, "Future simple with will", "normal", expected_questions=30,
        aliases=("bateria_11_future_simple_with_will.json",)),
    12: BatterySpec(12, "Will vs be going to vs present continuous", "normal", expected_questions=30,
        aliases=("bateria_12_will_vs_going_to_vs_present_continuous.json",)),
    13: BatterySpec(13, "Presenting an incident clearly", "natural", version=2, expected_questions=100,
        aliases=("bateria_13_v2_presenting_an_incident_clearly_soc_clientes_100.json",)),
    14: BatterySpec(14, "Explaining evidence and uncertainty", "natural", version=2, expected_questions=100,
        aliases=("bateria_14_v2_explaining_evidence_and_uncertainty_soc_clientes_100.json",)),
    15: BatterySpec(15, "Giving recommendations and explaining risk", "natural", version=2, expected_questions=100,
        aliases=("bateria_15_v2_recommendations_and_risk_soc_clientes_100.json",)),
    16: BatterySpec(16, "Explaining metrics and trends", "natural", version=2, expected_questions=100,
        aliases=("bateria_16_v2_metrics_and_trends_soc_clientes_100.json",)),
    17: BatterySpec(17, "Handling questions and disagreements", "natural", version=2, expected_questions=100,
        aliases=("bateria_17_v2_questions_and_disagreements_soc_clientes_100.json",)),
    18: BatterySpec(18, "Explaining detections and SOC processes", "natural", version=2, expected_questions=100,
        aliases=("explaining_detections_and_soc_processes_v2_natural_english_for_customer_briefings.json",)),
    19: BatterySpec(19, "Connectors and signposting for SOC presentations", "natural", version=2, expected_questions=100,
        aliases=("bateria_19_natural_connectors_and_signposting.json",)),
    20: BatterySpec(20, "Explaining processes and next steps", "natural", expected_questions=100,
        aliases=("bateria_20_explaining_processes_and_next_steps.json",)),
    21: BatterySpec(21, "Modal verbs", "normal", expected_questions=50, aliases=("21_modal_verbs.json",)),
    22: BatterySpec(22, "Infinitive, gerund or base form", "normal", expected_questions=50,
        aliases=("22_infinitive_gerund_or_base_form.json",)),
    23: BatterySpec(23, "Conditionals", "normal", expected_questions=50, aliases=("23_conditionals.json",)),
    24: BatterySpec(24, "Articles", "normal", expected_questions=40, aliases=("24_articles.json",)),
    25: BatterySpec(25, "Countable and uncountable nouns", "normal", expected_questions=40,
        aliases=("25_countable_and_uncountable_nouns.json",)),
    26: BatterySpec(26, "Prepositions and dependent prepositions", "normal", expected_questions=50,
        aliases=("26_prepositions_and_dependent_prepositions.json",)),
    27: BatterySpec(27, "Relative clauses", "normal", expected_questions=40, aliases=("27_relative_clauses.json",)),
    28: BatterySpec(28, "Passive voice", "normal", expected_questions=50, aliases=("28_passive_voice.json",)),
    29: BatterySpec(29, "Reported speech", "normal", expected_questions=40, aliases=("29_reported_speech.json",)),
    30: BatterySpec(30, "Common SOC collocations", "normal", expected_questions=60,
        aliases=("30_common_soc_collocations.json",)),
    31: BatterySpec(31, "Question forms", "normal", expected_questions=50, aliases=("31_question_forms.json",)),
    32: BatterySpec(32, "Mixed grammar review", "normal", expected_questions=100,
        aliases=("32_mixed_grammar_review.json",)),
}

# Exact aliases are safest and take priority.
EXACT_FILENAME_MAP: dict[str, int] = {
    alias.casefold(): number
    for number, spec in SPECS.items()
    for alias in spec.aliases
}

# Conservative phrases used only if neither filename nor current name contains a number.
TOPIC_HINTS: list[tuple[str, int]] = sorted(
    ((spec.topic.casefold(), number) for number, spec in SPECS.items()),
    key=lambda item: len(item[0]),
    reverse=True,
)


def normalize_text(value: str) -> str:
    value = value.casefold().replace("·", " ")
    value = re.sub(r"[_\-.]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def extract_number(value: str) -> int | None:
    # Prevent question counts such as 100 from being interpreted as a battery number.
    patterns = (
        r"^(?:bateria|battery)?\s*[_\-. ]*0*([1-9]|[12]\d|3[0-2])(?:\D|$)",
        r"\b(?:bateria|battery)\s*[_\-. ]*0*([1-9]|[12]\d|3[0-2])\b",
    )
    for pattern in patterns:
        match = re.search(pattern, value, flags=re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None


def identify_spec(path: Path, data: dict[str, Any]) -> tuple[BatterySpec | None, str]:
    exact = EXACT_FILENAME_MAP.get(path.name.casefold())
    if exact:
        return SPECS[exact], "exact filename"

    number = extract_number(path.stem)
    if number in SPECS:
        return SPECS[number], "number in filename"

    current_name = str(data.get("name", ""))
    number = extract_number(current_name)
    if number in SPECS:
        return SPECS[number], "number in JSON name"

    haystack = normalize_text(f"{path.stem} {current_name}")
    candidates = [number for hint, number in TOPIC_HINTS if normalize_text(hint) in haystack]
    candidates = list(dict.fromkeys(candidates))
    if len(candidates) == 1:
        return SPECS[candidates[0]], "topic match"
    if len(candidates) > 1:
        return None, f"ambiguous topic match: {candidates}"
    return None, "unknown file"


def get_questions(data: dict[str, Any]) -> list[Any] | None:
    questions = data.get("questions")
    return questions if isinstance(questions, list) else None


def validate_question_ids(questions: Iterable[Any]) -> tuple[int, int]:
    ids: list[str] = []
    missing = 0
    for question in questions:
        if not isinstance(question, dict) or question.get("id") in (None, ""):
            missing += 1
        else:
            ids.append(str(question["id"]))
    duplicates = len(ids) - len(set(ids))
    return missing, duplicates


def process_file(path: Path, output_dir: Path, dry_run: bool) -> dict[str, Any]:
    row: dict[str, Any] = {
        "source_file": path.name,
        "output_file": "",
        "match_method": "",
        "old_name": "",
        "new_name": "",
        "old_category": "",
        "new_category": "",
        "old_version": "",
        "new_version": "",
        "question_count": "",
        "expected_questions": "",
        "missing_question_ids": "",
        "duplicate_question_ids": "",
        "status": "",
        "notes": "",
    }

    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        row["status"] = "ERROR"
        row["notes"] = f"Invalid JSON: {exc}"
        return row

    if not isinstance(data, dict):
        row["status"] = "ERROR"
        row["notes"] = "Top-level JSON must be an object"
        return row

    row["old_name"] = data.get("name", "")
    row["old_category"] = data.get("category", "")
    row["old_version"] = data.get("version", "")

    questions = get_questions(data)
    if questions is None:
        row["status"] = "ERROR"
        row["notes"] = "Missing top-level questions array"
        return row

    row["question_count"] = len(questions)
    missing_ids, duplicate_ids = validate_question_ids(questions)
    row["missing_question_ids"] = missing_ids
    row["duplicate_question_ids"] = duplicate_ids

    spec, method = identify_spec(path, data)
    row["match_method"] = method
    if spec is None:
        row["status"] = "SKIPPED"
        row["notes"] = method
        return row

    row["new_name"] = spec.display_name
    row["new_category"] = spec.category
    row["new_version"] = spec.version
    row["expected_questions"] = spec.expected_questions or ""
    row["output_file"] = spec.output_filename

    notes: list[str] = []
    if spec.expected_questions is not None and len(questions) != spec.expected_questions:
        notes.append(f"question count {len(questions)}; expected {spec.expected_questions}")
    if missing_ids:
        notes.append(f"{missing_ids} questions without id")
    if duplicate_ids:
        notes.append(f"{duplicate_ids} duplicate question ids")

    data["name"] = spec.display_name
    data["category"] = spec.category
    data["version"] = spec.version

    destination = output_dir / spec.output_filename
    if destination.exists():
        # Do not silently overwrite two historical versions mapped to one canonical battery.
        row["status"] = "CONFLICT"
        notes.append(f"output already exists: {destination.name}")
        row["notes"] = "; ".join(notes)
        return row

    if not dry_run:
        destination.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    row["status"] = "OK" if not notes else "WARNING"
    row["notes"] = "; ".join(notes)
    return row


def write_report(rows: list[dict[str, Any]], report_path: Path) -> None:
    fieldnames = list(rows[0].keys()) if rows else ["status", "notes"]
    with report_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize English SOC Lab battery JSON files.")
    parser.add_argument("input_dir", type=Path, help="Folder containing battery JSON files")
    parser.add_argument("--output", type=Path, help="Output folder; default: INPUT_DIR_normalized")
    parser.add_argument("--dry-run", action="store_true", help="Generate only a report; write no JSON files")
    args = parser.parse_args()

    input_dir = args.input_dir.expanduser().resolve()
    if not input_dir.is_dir():
        parser.error(f"Input folder does not exist: {input_dir}")

    output_dir = (args.output or input_dir.with_name(f"{input_dir.name}_normalized")).expanduser().resolve()
    if output_dir == input_dir:
        parser.error("Output folder must be different from input folder; originals are never overwritten")

    output_dir.mkdir(parents=True, exist_ok=True)
    json_files = sorted(path for path in input_dir.glob("*.json") if path.is_file())
    if not json_files:
        print(f"No JSON files found in {input_dir}", file=sys.stderr)
        return 2

    rows: list[dict[str, Any]] = []
    for path in json_files:
        rows.append(process_file(path, output_dir, args.dry_run))

    report_path = output_dir / "normalization_report.csv"
    write_report(rows, report_path)

    totals: dict[str, int] = {}
    for row in rows:
        totals[row["status"]] = totals.get(row["status"], 0) + 1

    print(f"Input:  {input_dir}")
    print(f"Output: {output_dir}")
    print(f"Report: {report_path}")
    print("Summary: " + ", ".join(f"{key}={value}" for key, value in sorted(totals.items())))
    if args.dry_run:
        print("Dry run: no normalized JSON files were written.")

    return 1 if any(key in totals for key in ("ERROR", "CONFLICT")) else 0


if __name__ == "__main__":
    raise SystemExit(main())
