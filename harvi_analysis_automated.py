"""HARVI project: paired before/after security awareness training analysis."""
from pathlib import Path

import matplotlib.pyplot as plt
from scipy import stats
import csv

# Find the data files beside this script, regardless of terminal working directory.
PROJECT_DIR = Path(__file__).resolve().parent
PILOT_BEFORE = [40, 62, 74, 22, 64, 65, 49, 49, 49]
PILOT_AFTER = [68, 61, 64, 76, 90, 75, 66, 60, 63]


def analyze_scores(group, before_scores, after_scores):
    """Calculate paired statistics and return values usable by charts."""
    if not before_scores or len(before_scores) != len(after_scores):
        raise ValueError(f"{group}: before/after scores must be nonempty and paired")

    count = len(before_scores)
    average_before = sum(before_scores) / count
    average_after = sum(after_scores) / count
    score_change = average_after - average_before
    percent_change = (score_change / average_before * 100) if average_before else None

    improved = sum(a < b for b, a in zip(before_scores, after_scores))
    worsened = sum(a > b for b, a in zip(before_scores, after_scores))
    unchanged = count - improved - worsened
    t_stat, p_value = stats.ttest_rel(after_scores, before_scores)

    if p_value < 0.05:
        conclusion = ("Significant improvement" if score_change < 0 else
                      "Significant worsening" if score_change > 0 else
                      "Statistically significant difference")
    else:
        conclusion = "No statistically significant change"

    return {
        "group": group,
        "participants": count,
        "average_before": average_before,
        "average_after": average_after,
        "score_change": score_change,
        "percent_change": percent_change,
        "improved": improved,
        "worsened": worsened,
        "unchanged": unchanged,
        "t_stat": t_stat,
        "p_value": p_value,
        "conclusion": conclusion,
    }

def analyze_department(filename):
    """Read a department file and analyze its paired scores."""
    path = PROJECT_DIR / filename
    with path.open("r", encoding="utf-8-sig") as file:
        department = file.readline().strip()
        before_scores, after_scores = [], []
        for line_number, line in enumerate(file, start=2):
            if not line.strip():
                continue
            fields = line.split()
            if len(fields) != 2:
                raise ValueError(f"{filename}, line {line_number}: expected two scores")
            before, after = map(int, fields)
            before_scores.append(before)
            after_scores.append(after)
    return analyze_scores(department, before_scores, after_scores)


def print_results(result):
    """Print the same report format for all three groups."""
    print(f"\n--- {result['group']} ---")
    print(f"Participants: {result['participants']}")
    print(f"Average Before: {result['average_before']:.2f}")
    print(f"Average After: {result['average_after']:.2f}")
    print(f"Score Change: {result['score_change']:+.2f}")
    if result['percent_change'] is None:
        print("Percentage Change: Undefined (baseline average is zero)")
    else:
        print(f"Percentage Change: {result['percent_change']:+.2f}%")
    print("\nIndividual Results")
    for key in ("improved", "worsened", "unchanged"):
        print(f"{key.capitalize()}: {result[key]}")
    print("\nPaired-Samples T-Test")
    print(f"T-statistic: {result['t_stat']:.4f}")
    p = result["p_value"]
    print("P-value: < 0.001" if p < 0.001 else f"P-value: {p:.4f}")
    print(f"Conclusion: {result['conclusion']}.")


def plot_average_scores(results):
    groups = [r["group"] for r in results]
    before = [r["average_before"] for r in results]
    after = [r["average_after"] for r in results]
    x = list(range(len(groups)))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars_before = ax.bar([i - width / 2 for i in x], before, width,
                         label="Before Training", color="steelblue")
    bars_after = ax.bar([i + width / 2 for i in x], after, width,
                        label="After Training", color="coral")
    ax.bar_label(bars_before, fmt="%.2f", padding=3)
    ax.bar_label(bars_after, fmt="%.2f", padding=3)
    ax.set_xticks(x, groups)
    ax.set_xlabel("Study Group")
    ax.set_ylabel("Average HARVI Score")
    ax.set_title("HARVI Scores Before and After Security Training")
    ax.set_ylim(0, max(100, max(before + after) * 1.15))
    ax.legend()
    ax.grid(axis="y", alpha=0.2)
    fig.text(
        0.5, 0.01,
        "Note: Lower HARVI scores indicate lower phishing susceptibility.",
        ha="center",
        fontsize=9,
        style="italic"
    )
    fig.tight_layout(rect=[0, 0.05, 1, 1])

    output = PROJECT_DIR / "harvi_average_comparison.png"
    fig.savefig(output, dpi=300)
    print(f"Saved: {output.name}")
    return fig


def plot_participant_outcomes(results):
    groups = [r["group"] for r in results]
    improved = [r["improved"] / r["participants"] * 100 for r in results]
    worsened = [r["worsened"] / r["participants"] * 100 for r in results]
    unchanged = [r["unchanged"] / r["participants"] * 100 for r in results]
    bottom_unchanged = [i + w for i, w in zip(improved, worsened)]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(groups, improved, label="Improved", color="seagreen")
    ax.bar(groups, worsened, bottom=improved, label="Worsened", color="coral")
    ax.bar(groups, unchanged, bottom=bottom_unchanged,
           label="Unchanged", color="gray")
    for index in range(len(groups)):
        ax.text(index, improved[index] / 2, f"{improved[index]:.1f}%",
                ha="center", va="center", color="white")
        ax.text(index, improved[index] + worsened[index] / 2,
                f"{worsened[index]:.1f}%", ha="center", va="center", color="white")
    ax.set_title("HARVI Participant Outcomes After Security Training")
    ax.set_xlabel("Study Group")
    ax.set_ylabel("Percentage of Participants (%)")
    ax.set_ylim(0, 100)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1))
    ax.grid(axis="y", alpha=0.2)

    # Add explanatory note below Figure 2
    fig.text(
        0.5, 0.01,
        "Note: Lower HARVI scores indicate lower phishing susceptibility.",
        ha="center",
        fontsize=9,
        style="italic"
    )

    # Adjust layout to make room for the note
    fig.tight_layout(rect=[0, 0.05, 0.85, 1])

    output = PROJECT_DIR / "harvi_participant_outcomes.png"
    fig.savefig(output, dpi=300)
    print(f"Saved: {output.name}")
    return fig

def export_csv_report(results):
    """Export HARVI analysis results to a CSV file."""

    output = PROJECT_DIR / "harvi_summary_report.csv"

    columns = [
        "Group",
        "Participants",
        "Average Before",
        "Average After",
        "Score Change",
        "Percentage Change (%)",
        "Improved",
        "Worsened",
        "Unchanged",
        "T-Statistic",
        "P-Value",
        "Statistically Significant",
        "Conclusion"
    ]

    with output.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(columns)

        for result in results:
            p_value = result["p_value"]

            writer.writerow([
                result["group"],
                result["participants"],
                round(result["average_before"], 2),
                round(result["average_after"], 2),
                round(result["score_change"], 2),
                round(result["percent_change"], 2)
                if result["percent_change"] is not None else "",
                result["improved"],
                result["worsened"],
                result["unchanged"],
                round(result["t_stat"], 4),
                f"{p_value:.8g}",
                "Yes" if p_value < 0.05 else "No",
                result["conclusion"]
            ])

    print(f"Saved: {output.name}")


def main():
    results = [
        analyze_scores("Pilot", PILOT_BEFORE, PILOT_AFTER),
        analyze_department("technology.txt"),
        analyze_department("marketing.txt"),
    ]

    print("========== AUTOMATED HARVI ANALYSIS ==========")

    for result in results:
        print_results(result)

    export_csv_report(results)
    plot_average_scores(results)
    plot_participant_outcomes(results)

    plt.show()


if __name__ == "__main__":
    main()
