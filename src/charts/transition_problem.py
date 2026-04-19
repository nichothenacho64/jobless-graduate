from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

import src.charts.style as ChartStyle
import src.constants.charts as ChartConstants
from src.constants.qilt import QILT_OUTCOME_TITLES, QILT_SHORT_MEDIUM_OUTCOME_SPECS

TRANSITION_SUPTITLE_Y = 0.975
TRANSITION_LEGEND_ANCHOR = (0.98, 0.945)  # 0.985 is lower
TRANSITION_TIGHT_LAYOUT_RECT = (0, 0, 1, 0.90)
TRANSITION_Y_LIMITS = (65, 95)
TRANSITION_Y_TICKS = np.arange(65, 96, 5)
SHORT_TERM_LABEL = "Short-term (4 months after graduation)"
MEDIUM_TERM_LABEL = "Medium-term (3 years after graduation)"
TRANSITION_CHART_TITLE = "Short-term and medium-term graduate outcomes by graduation year"
TRANSITION_PANEL_HEIGHT_RATIOS = (1.3, 1.0, 0.82)
TRANSITION_PANEL_STYLES = {
    "full_time_employment": {
        "alpha": 1.0,
        "short_linewidth": 2.8,
        "medium_linewidth": 2.2,
        "marker_size": 6.4,
        "title_alpha": 1.0,
    },
    "overall_employment": {
        "alpha": 0.88,
        "short_linewidth": 2.2,
        "medium_linewidth": 1.8,
        "marker_size": 5.6,
        "title_alpha": 0.95,
    },
    "labour_force_participation": {
        "alpha": 0.58,
        "short_linewidth": 1.5,
        "medium_linewidth": 1.3,
        "marker_size": 4.8,
        "title_alpha": 0.78,
    },
}

def create_transition_problem_chart(transition_table: pd.DataFrame) -> Figure:
    ChartStyle.apply_chart_style()
    x_positions = np.arange(len(transition_table))
    period_labels = transition_table["period_label"].tolist()

    figure, axes = plt.subplots(
        nrows=len(QILT_SHORT_MEDIUM_OUTCOME_SPECS),
        ncols=1,
        figsize=(8.8, 7.9),
        sharex=True,
        gridspec_kw={"height_ratios": TRANSITION_PANEL_HEIGHT_RATIOS},
    )

    for axis, (outcome_key, short_column, medium_column) in zip(
        axes, QILT_SHORT_MEDIUM_OUTCOME_SPECS
    ):
        panel_style = TRANSITION_PANEL_STYLES[outcome_key]
        short_values = transition_table[short_column].to_numpy(dtype=float)
        medium_values = transition_table[medium_column].to_numpy(dtype=float)

        axis.plot(
            x_positions,
            short_values,
            color=ChartConstants.SHORT_TERM_COLOR,
            linewidth=panel_style["short_linewidth"],
            marker="o",
            markersize=panel_style["marker_size"],
            markeredgecolor="white",
            markeredgewidth=0.9,
            alpha=panel_style["alpha"],
            label=SHORT_TERM_LABEL,
        )
        axis.plot(
            x_positions,
            medium_values,
            color=ChartConstants.MEDIUM_TERM_COLOR,
            linewidth=panel_style["medium_linewidth"],
            marker="o",
            markersize=max(panel_style["marker_size"] - 0.5, 4.0),
            markerfacecolor="white",
            markeredgecolor=ChartConstants.MEDIUM_TERM_COLOR,
            markeredgewidth=1.0,
            alpha=max(panel_style["alpha"] - 0.08, 0.45),
            label=MEDIUM_TERM_LABEL,
        )
        _style_transition_axis(
            axis,
            title=QILT_OUTCOME_TITLES[outcome_key],
            title_alpha=panel_style["title_alpha"],
        )
        axis.set_ylim(*TRANSITION_Y_LIMITS)
        axis.set_yticks(TRANSITION_Y_TICKS)

    axes[-1].set_xticks(x_positions, period_labels)
    axes[-1].set_xlabel("Graduation year")

    ChartStyle.add_figure_legend(
        figure,
        axes[0],
        anchor=TRANSITION_LEGEND_ANCHOR,
    )

    figure.suptitle(
        TRANSITION_CHART_TITLE,
        fontsize=ChartConstants.SUBGROUP_CHART_TITLE_FONT_SIZE,
        color=ChartConstants.TEXT_COLOR,
        x=0.08,
        y=TRANSITION_SUPTITLE_Y,
        ha="left",
    )

    figure.tight_layout(rect=TRANSITION_TIGHT_LAYOUT_RECT)
    return ChartStyle.draw_figure(figure)

def _style_transition_axis(
    axis: Axes,
    *,
    title: str,
    title_alpha: float,
) -> None:
    axis.set_title(
        title,
        loc="left",
        fontsize=ChartConstants.AXIS_TITLE_FONT_SIZE,
        color=ChartConstants.TEXT_COLOR,
        alpha=title_alpha,
    )
    axis.set_ylabel("Percentage")
    axis.grid(
        axis="y",
        color=ChartConstants.GRID_COLOR,
        linewidth=ChartConstants.AXIS_GRID_LINEWIDTH,
    )
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.tick_params(colors=ChartConstants.TEXT_COLOR)
