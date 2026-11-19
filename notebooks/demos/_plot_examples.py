"""Standalone, fictional visual examples for the EDA demo notebook."""

import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle


BLUE = "#699ac2"
INK = "#383838"
TEAL = "#15cdbf"


def _normal():
    x = np.linspace(54, 74, 1001)
    return x, np.exp(-0.5 * ((x - 64) / 2.2) ** 2) / (2.2 * np.sqrt(2 * np.pi))


def show_distributions():
    """Compare four probability models, without sampling noise."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 6.8), layout="constrained")
    x, density = _normal()
    axes[0, 0].plot(x, density, color=BLUE, lw=2)
    axes[0, 0].fill_between(x, density, color=BLUE, alpha=.25)
    axes[0, 0].set(xlabel="Height (inches)", ylabel="Probability density", xlim=(57, 71))
    k = np.arange(21)
    axes[0, 1].bar(k, [math.comb(20, int(i)) * .1**i * .9**(20-i) for i in k],
                   color=BLUE, edgecolor=INK, linewidth=.5, width=.7)
    axes[0, 1].set(xlabel="Clicks in 20 independent trials", ylabel="Probability", xlim=(-.5, 10.5))
    axes[0, 1].text(.98, .96, "p = 0.10 per trial\n11–20 omitted", transform=axes[0, 1].transAxes,
                    ha="right", va="top", fontsize=9)
    faces = np.arange(1, 7)
    axes[1, 0].bar(faces, np.full(6, 1/6), color=BLUE, edgecolor=INK, linewidth=.5, width=.7)
    axes[1, 0].set(xlabel="Face of a fair die", ylabel="Probability", xticks=faces, ylim=(0, .21))
    k = np.arange(11)
    axes[1, 1].bar(k, [math.exp(-2) * 2**int(i) / math.factorial(int(i)) for i in k],
                   color=BLUE, edgecolor=INK, linewidth=.5, width=.7)
    axes[1, 1].set(xlabel="Cancellations per day", ylabel="Probability", xticks=np.arange(0, 11, 2))
    axes[1, 1].text(.98, .96, "Mean = 2 per day\nAbove 10 omitted", transform=axes[1, 1].transAxes,
                    ha="right", va="top", fontsize=9)
    for ax, title in zip(axes.flat, ["Normal distribution", "Binomial distribution",
                                    "Uniform distribution", "Poisson distribution"]):
        ax.set_title(title, loc="left", fontweight="bold", color=INK)
        ax.tick_params(labelsize=9)
    fig.suptitle("Common distributions", fontsize=17, color=INK, fontweight="bold")
    plt.show()


def show_normal_intervals():
    """Show nested central intervals for a normal height model."""
    x, density = _normal()
    fig, ax = plt.subplots(figsize=(10, 4.5), layout="constrained")
    for spread, color, label in [(3, "#dcebf3", "±3 SD · 99.7%"),
                                 (2, "#a9cce1", "±2 SD · 95%"),
                                 (1, "#699ac2", "±1 SD · 68%")]:
        ax.fill_between(x, density, where=abs(x - 64) <= spread * 2.2, color=color, label=label)
    ax.plot(x, density, color="#406f92", lw=2)
    ax.axvline(64, color=TEAL, ls="--", lw=2)
    ax.annotate("", xy=(66.2, .11), xytext=(64, .11),
                arrowprops=dict(arrowstyle="<->", color=TEAL, lw=1.5))
    ax.text(65.1, .115, "1 SD = 2.2 in", color=INK, ha="center", va="bottom", fontsize=9)
    ax.set_xticks([64 + i * 2.2 for i in range(-3, 4)],
                  [f"{64 + i * 2.2:.1f}\n{'mean' if i == 0 else f'{i:+d} SD'}" for i in range(-3, 4)])
    ax.set(xlabel="Height (inches)", ylabel="Probability density", ylim=(0, .22),
           title="Normal distribution · centered intervals")
    ax.legend(title="Nested area within", frameon=False, loc="upper right")
    plt.show()


def show_correlations():
    """Show calculated Pearson r alongside four fictional point patterns."""
    x = np.arange(1, 10)
    examples = [
        (x, [91, 75, 85, 70, 77, 60, 69, 52, 58], "Negative", "Social media (hours/week)", "Test grade (points)"),
        (x, [67, 82, 74, 88, 65, 86, 77, 81, 69], "Near-zero linear trend", "Talking with friends (hours/week)", "Test grade (points)"),
        (x * 10, x * 10, "Perfect positive: a copy", "Original score (points)", "Copied score (points)"),
        (np.arange(-4, 5), np.arange(-4, 5) ** 2, "Curved relationship", "Input (units)", "Output (units)"),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(15, 3.8), layout="constrained")
    for ax, (xs, ys, title, xlabel, ylabel) in zip(axes, examples):
        r = np.corrcoef(xs, ys)[0, 1]
        ax.scatter(xs, ys, s=32, color="#4389bc")
        ax.set_title(f"{title}\nr = {r:+.2f}", fontweight="bold", fontsize=10, color=INK)
        ax.set(xlabel=xlabel, ylabel=ylabel)
        ax.tick_params(labelsize=8)
        ax.xaxis.label.set_size(9)
        ax.yaxis.label.set_size(9)
    fig.suptitle("Correlation · look at the points first", fontsize=16, fontweight="bold", color=INK)
    plt.show()


def show_correlation_matrix():
    """Highlight diagonal, near-zero, and strong values in a calculated matrix."""
    fictional = pd.DataFrame({
        "Study\n(hours)": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "Coffee\n(cups)": [3, 4, 1, 3, 5, 3, 1, 4, 2],
        "Test\n(points)": [52, 61, 57, 70, 66, 78, 74, 86, 82],
        "Class\n(points)": [55, 64, 59, 72, 65, 81, 74, 88, 79],
    })
    corr = fictional.corr()
    fig, ax = plt.subplots(figsize=(10, 5.4), layout="constrained")
    ax.axis("off")
    table = ax.table(cellText=[[f"{v:+.2f}" for v in row] for row in corr.to_numpy()],
                     rowLabels=corr.index, colLabels=corr.columns, cellLoc="center",
                     rowLoc="center", bbox=[.18, .30, .80, .55])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("white")
        cell.set_facecolor("#f1f1f1" if row > 0 and row % 2 else "white")
        if row == 0 or col == -1:
            cell.set_text_props(fontweight="bold", color=INK)
    # Borders and badges are added to table cells after layout resolves.
    fig.canvas.draw()
    for number, (row, col) in enumerate([(1, 0), (2, 0), (3, 3)], 1):
        cell = table[row, col]
        x, y = cell.get_xy()
        w, h = cell.get_width(), cell.get_height()
        ax.add_patch(Rectangle((x, y), w, h, fill=False, ec=TEAL, lw=1.8, transform=ax.transAxes))
        ax.text(x + w, y + h, str(number), transform=ax.transAxes, ha="center", va="center",
                color="white", fontsize=9, fontweight="bold",
                bbox=dict(boxstyle="circle,pad=.22", fc=TEAL, ec="none"))
    ax.text(.02, .13, "①  Diagonal: a variable\n     compared with itself.", transform=ax.transAxes, fontsize=9)
    ax.text(.37, .13, "②  Near zero: little\n     linear association.", transform=ax.transAxes, fontsize=9)
    ax.text(.70, .13, "③  Strong positive\n     test–class association.", transform=ax.transAxes, fontsize=9)
    ax.set_title("Fictional students  /  Pearson correlation matrix", loc="left",
                 fontsize=15, fontweight="bold", color=INK)
    plt.show()
