from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

import src.charts.style as ChartStyle
import src.charts.constants as ChartConstants
from src.transform.constants import QILT_SHORT_MEDIUM_OUTCOME_SPECS

def create_transition_problem_chart(transition_table: pd.DataFrame) -> Figure:
    ChartStyle.apply_chart_style()
    x_positions = np.arange(len(transition_table))
    period_labels = transition_table["period_label"].tolist()

    figure, axes = plt.subplots(
        nrows=len(QILT_SHORT_MEDIUM_OUTCOME_SPECS),
        ncols=1,
        figsize=(8.8, 7.9),
        sharex=True,
        gridspec_kw={"height_ratios": ChartConstants.TRANSITION_PANEL_HEIGHT_RATIOS},
    )

    for axis, (outcome_key, short_column, medium_column) in zip(
        axes, QILT_SHORT_MEDIUM_OUTCOME_SPECS
    ):
        panel_style = ChartConstants.TRANSITION_PANEL_STYLES[outcome_key]
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
            label=ChartConstants.TRANSITION_SHORT_TERM_LABEL,
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
            label=ChartConstants.TRANSITION_MEDIUM_TERM_LABEL,
        )
        _style_transition_axis(
            axis,
            title=ChartConstants.QILT_OUTCOME_TITLES[outcome_key],
            title_alpha=panel_style["title_alpha"],
        )
        axis.set_ylim(*ChartConstants.TRANSITION_Y_LIMITS)
        axis.set_yticks(ChartConstants.TRANSITION_Y_TICKS)

    axes[-1].set_xticks(x_positions, period_labels)
    axes[-1].set_xlabel("Graduation year")

    ChartStyle.add_figure_legend(
        figure,
        axes[0],
        anchor=ChartConstants.TRANSITION_LEGEND_ANCHOR,
    )

    figure.suptitle(
        ChartConstants.TRANSITION_CHART_TITLE,
        fontsize=ChartConstants.SUBGROUP_CHART_TITLE_FONT_SIZE,
        color=ChartConstants.TEXT_COLOR,
        x=0.08,
        y=ChartConstants.TRANSITION_SUPTITLE_Y,
        ha="left",
    )

    figure.tight_layout(rect=ChartConstants.TRANSITION_TIGHT_LAYOUT_RECT)
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
