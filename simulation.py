"""
Simulation script for Extreme Zipliner campaign scenarios.

This script evaluates four advertising budget scenarios (small, baseline,
large and long) defined in the accompanying presentation. It computes
key metrics such as views, clicks, conversions, revenue, profit and
return on investment (ROI) based on assumed CPV, CTR and conversion
rates for each scenario. The results are written to a CSV file and a
simple bar chart is saved to disk.

Usage:
    python simulation.py

The output files `simulation_results.csv` and `simulation_chart.png`
will be created in the working directory. These artefacts can be used
in the slide deck and as part of the GitHub Actions workflow.
"""

import pandas as pd
import matplotlib.pyplot as plt

def run_simulation():
    scenarios = [
        {
            "Scenario": "Small",
            "Budget": 100,
            "Days": 5,
            "CPV": 0.06,
            "CTR": 0.05,
            "ConvRate": 0.04,
            "RevenuePerSale": 100,
            "ProfitPerSale": 50,
        },
        {
            "Scenario": "Baseline",
            "Budget": 200,
            "Days": 10,
            "CPV": 0.06,
            "CTR": 0.05,
            "ConvRate": 0.04,
            "RevenuePerSale": 100,
            "ProfitPerSale": 50,
        },
        {
            "Scenario": "Large",
            "Budget": 500,
            "Days": 30,
            "CPV": 0.05,
            "CTR": 0.06,
            "ConvRate": 0.05,
            "RevenuePerSale": 100,
            "ProfitPerSale": 50,
        },
        {
            "Scenario": "Long",
            "Budget": 400,
            "Days": 60,
            "CPV": 0.05,
            "CTR": 0.06,
            "ConvRate": 0.05,
            "RevenuePerSale": 100,
            "ProfitPerSale": 50,
        },
    ]

    rows = []
    for s in scenarios:
        budget = s["Budget"]
        views = budget / s["CPV"]
        clicks = views * s["CTR"]
        conversions = clicks * s["ConvRate"]
        revenue = conversions * s["RevenuePerSale"]
        profit = conversions * s["ProfitPerSale"]
        roi = profit / budget
        rows.append(
            {
                "Scenario": s["Scenario"],
                "Budget": budget,
                "Days": s["Days"],
                "Views": views,
                "Clicks": clicks,
                "Conversions": conversions,
                "Revenue": revenue,
                "Profit": profit,
                "ROI": roi,
            }
        )

    df = pd.DataFrame(rows)
    # Save to CSV
    df.to_csv("simulation_results.csv", index=False)

    # Create bar chart of profit and ROI (% multiplied by 100)
    fig, ax1 = plt.subplots()
    scenarios = df["Scenario"]
    profit_vals = df["Profit"]
    roi_vals = df["ROI"] * 100  # convert to percentage

    bar_width = 0.35
    x = range(len(scenarios))

    ax1.bar(x, profit_vals, width=bar_width, label="Profit ($)")
    ax1.set_xlabel("Scenario")
    ax1.set_ylabel("Profit ($)")
    ax1.set_title("Simulation Results: Profit and ROI")
    ax1.set_xticks(x)
    ax1.set_xticklabels(scenarios)

    ax2 = ax1.twinx()
    ax2.bar([i + bar_width for i in x], roi_vals, width=bar_width, label="ROI (%)")
    ax2.set_ylabel("ROI (%)")

    # Add legend
    lines, labels = [], []
    for ax in [ax1, ax2]:
        line, label = ax.get_legend_handles_labels()
        lines += line
        labels += label
    ax1.legend(lines, labels, loc="upper left")

    plt.tight_layout()
    plt.savefig("simulation_chart.png")
    plt.close()

    return df

if __name__ == "__main__":
    results = run_simulation()
    print(results)