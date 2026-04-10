from __future__ import annotations

import argparse
import json
from pathlib import Path

from algorithm_t import run_range


def save_results(data: dict, output_path: Path) -> None:
    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def save_results_js(data: dict, output_path: Path) -> None:
    js_payload = "window.__ALGO_T_RESULTS__ = " + json.dumps(data, indent=2) + ";\n"
    output_path.write_text(js_payload, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="T algorithm with separate Offline/Online phase measurements.")
    parser.add_argument("--start", type=int, default=3, help="start n value (default: 3)")
    parser.add_argument("--end", type=int, default=10, help="end n value (default: 10)")
    parser.add_argument("--sample", type=int, default=5, help="sample n used in the visual demo (default: 5)")
    parser.add_argument("--output", type=Path, default=Path("results.json"), help="output JSON file")
    args = parser.parse_args()

    if args.start < 1 or args.end < args.start:
        raise ValueError("Invalid n range.")

    data = run_range(args.start, args.end, args.sample)
    save_results(data, args.output)

    js_output = args.output.with_suffix(".js")
    save_results_js(data, js_output)

    print(f"Results saved to: {args.output}")
    print(f"JavaScript results saved to: {js_output}")


if __name__ == "__main__":
    main()
