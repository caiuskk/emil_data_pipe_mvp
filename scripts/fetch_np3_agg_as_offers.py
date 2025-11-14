#!/usr/bin/env python
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from ercot_emil.api import get_np3_agg_as_offers_ecrsm


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Download NP3-911-ER 2d_agg_as_offers_ecrsm report as CSV"
    )
    p.add_argument(
        "--from-date",
        required=True,
        help="Delivery date from (YYYY-MM-DD)",
    )
    p.add_argument(
        "--to-date",
        help="Delivery date to (YYYY-MM-DD). Default = from-date",
    )
    p.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output CSV path. Default: stdout",
    )
    p.add_argument(
        "--size",
        type=int,
        default=1000,
        help="Page size (default: 1000)",
    )
    # 可以再加一些可选 filter，例如 hourEnding / MWOffered 等
    p.add_argument("--hour-from", type=int)
    p.add_argument("--hour-to", type=int)

    return p.parse_args()


def main() -> None:
    args = parse_args()

    d_from = date.fromisoformat(args.from_date)
    d_to = date.fromisoformat(args.to_date) if args.to_date else None

    df = get_np3_agg_as_offers_ecrsm(
        delivery_date_from=d_from,
        delivery_date_to=d_to,
        hour_ending_from=args.hour_from,
        hour_ending_to=args.hour_to,
        size=args.size,
    )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.output, index=False)
        print(f"Saved {len(df)} rows to {args.output}")
    else:
        # just print first few rows to show example
        print(df.head())
        print(f"Total rows: {len(df)}")


if __name__ == "__main__":
    main()
