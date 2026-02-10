#!/usr/bin/env python3
"""
Red Hen Bakery (25.048) — Retaining Wall Preliminary Design

Generates a wall schedule for retained heights 5–12 ft using the
design criteria in design_criteria.json.

Usage:
    python projects/red_hen_bakery/run_design.py
"""

import json
import sys
from pathlib import Path

# Ensure package is importable from project root
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from retaining_wall.schedule import (
    generate_schedule,
    format_schedule_table,
    format_detailed_report,
)

CRITERIA_FILE = Path(__file__).parent / "design_criteria.json"
OUTPUT_FILE = Path(__file__).parent / "wall_schedule_output.txt"


def main():
    print(f"Loading criteria from: {CRITERIA_FILE}")
    with open(CRITERIA_FILE) as f:
        project_data = json.load(f)

    print("Running designs for all scheduled heights...")
    entries, reports = generate_schedule(CRITERIA_FILE)

    # Summary table
    table = format_schedule_table(entries, project_data)

    # Detailed reports
    details = format_detailed_report(entries, reports)

    # Combine
    full_output = table + "\n" + details

    # Write to file
    with open(OUTPUT_FILE, "w") as f:
        f.write(full_output)

    # Also print to console
    print(full_output)
    print(f"\nOutput written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
