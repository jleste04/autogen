"""
simulate.py
---------------

This script performs campaign simulations for different budget and duration scenarios
as outlined in the marketing presentation. It calculates key performance metrics
including the number of views, clicks, conversions, revenue, profit and ROI.

Four scenarios are simulated by default:

1. **Small** – budget $100 over 5 days.
2. **Baseline** – budget $200 over 10 days (the reference scenario).
3. **Large** – budget $500 over 30 days.
4. **Long** – budget $400 over 60 days.

Assumptions for cost per view (CPV), click‑through rate (CTR), conversion rate and
average order value can be adjusted via command‑line arguments. For larger
budgets/durations the model assumes improved performance as noted in the
presentation (lower CPV and higher CTR and conversion rate).  Results are
printed to the console and can optionally be written to a CSV file for further
analysis.

Usage:
    python simulate.py [--output results.csv] [--cpv_small 0.06] [--cpv_large 0.05]
                       [--ctr_small 0.05] [--ctr_large 0.06]
                       [--conv_small 0.04] [--conv_large 0.05]

Example:
    python simulate.py --output results.csv

This will generate a CSV file called `results.csv` containing the simulation
results. If no output file is provided, results are printed to stdout.
"""

import argparse
import csv

def run_scenarios(cpv_small: float, cpv_large: float,
                  ctr_small: float, ctr_large: float,
                  conv_small: float, conv_large: float,
                  revenue_per_sale: float = 100.0,
                  profit_per_sale: float = 50.0):
    """Compute simulation metrics for a set of predefined scenarios.

    Args:
        cpv_small: Cost per view for small/baseline scenarios (in dollars).
        cpv_large: Cost per view for large/long scenarios (in dollars).
        ctr_small: Click‑through rate for small/baseline scenarios (0–1).
        ctr_large: Click‑through rate for large/long scenarios (0–1).
        conv_small: Conversion rate for small/baseline scenarios (0–1).
        conv_large: Conversion rate for large/long scenarios (0–1).
        revenue_per_sale: Gross revenue per conversion.
        profit_per_sale: Profit per conversion (after costs).

    Returns:
        A list of dictionaries with metrics for each scenario.
    """
    # Define scenarios with budgets and durations
    scenarios = [
        ("Small", 100, 5, cpv_small, ctr_small, conv_small),
        ("Baseline", 200, 10, cpv_small, ctr_small, conv_small),
        ("Large", 500, 30, cpv_large, ctr_large, conv_large),
        ("Long", 400, 60, cpv_large, ctr_large, conv_large),
    ]
    results = []
    for name, budget, days, cpv, ctr, conv in scenarios:
        # views are total budget divided by cost per view
        views = budget / cpv
        # clicks come from applying click‑through rate to views
        clicks = views * ctr
        # conversions come from applying conversion rate to clicks
        conversions = clicks * conv
        # revenue and profit
        revenue = conversions * revenue_per_sale
        profit = conversions * profit_per_sale
        roi = revenue / budget if budget != 0 else 0.0
        results.append({
            "Scenario": name,
            "Budget": budget,
            "Days": days,
            "Views": views,
            "Clicks": clicks,
            "Conversions": conversions,
            "Revenue": revenue,
            "Profit": profit,
            "ROI": roi,
        })
    return results


def save_to_csv(results, output_path: str) -> None:
    """Save simulation results to a CSV file.

    Args:
        results: List of dictionaries returned by run_scenarios().
        output_path: Path to the CSV file to write.
    """
    with open(output_path, mode="w", newline="") as csvfile:
        fieldnames = ["Scenario", "Budget", "Days", "Views", "Clicks", "Conversions", "Revenue", "Profit", "ROI"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)


def parse_args():
    parser = argparse.ArgumentParser(description="Run campaign simulations for different scenarios.")
    parser.add_argument("--output", type=str, default=None, help="Optional path to save results as CSV.")
    parser.add_argument("--cpv_small", type=float, default=0.06, help="CPV for small/baseline scenarios (default: 0.06)")
    parser.add_argument("--cpv_large", type=float, default=0.05, help="CPV for large/long scenarios (default: 0.05)")
    parser.add_argument("--ctr_small", type=float, default=0.05, help="CTR for small/baseline scenarios (default: 0.05)")
    parser.add_argument("--ctr_large", type=float, default=0.06, help="CTR for large/long scenarios (default: 0.06)")
    parser.add_argument("--conv_small", type=float, default=0.04, help="Conversion rate for small/baseline scenarios (default: 0.04)")
    parser.add_argument("--conv_large", type=float, default=0.05, help="Conversion rate for large/long scenarios (default: 0.05)")
    parser.add_argument("--revenue_per_sale", type=float, default=100.0, help="Revenue per sale (default: 100)")
    parser.add_argument("--profit_per_sale", type=float, default=50.0, help="Profit per sale (default: 50)")
    return parser.parse_args()


def main():
    args = parse_args()
    results = run_scenarios(
        cpv_small=args.cpv_small,
        cpv_large=args.cpv_large,
        ctr_small=args.ctr_small,
        ctr_large=args.ctr_large,
        conv_small=args.conv_small,
        conv_large=args.conv_large,
        revenue_per_sale=args.revenue_per_sale,
        profit_per_sale=args.profit_per_sale,
    )
    # Output results
    if args.output:
        save_to_csv(results, args.output)
        print(f"Results saved to {args.output}")
    else:
        # Print results to stdout in a readable table
        print(f"{'Scenario':<10} {'Budget':>6} {'Days':>5} {'Views':>10} {'Clicks':>10} {'Conversions':>12} {'Revenue':>10} {'Profit':>10} {'ROI':>6}")
        for row in results:
            print(f"{row['Scenario']:<10} {row['Budget']:>6.0f} {row['Days']:>5} {row['Views']:>10.1f} {row['Clicks']:>10.1f} {row['Conversions']:>12.1f} {row['Revenue']:>10.1f} {row['Profit']:>10.1f} {row['ROI']:>6.2f}x")


if __name__ == "__main__":
    main()