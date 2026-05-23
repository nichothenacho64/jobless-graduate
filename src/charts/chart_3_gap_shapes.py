from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from src.charts.constants import (
    AXIS_GRID_LINEWIDTH,
    CATCH_UP_MEDIUM_TERM_LABEL,
    CATCH_UP_SHORT_TERM_LABEL,
    CHART_3_TITLE,
    CHART_3_X_AXIS,
    CONNECTOR_COLOR,
    DUMBBELL_CONNECTOR_ZORDER,
    DUMBBELL_LEFT_POINT_ZORDER,
    DUMBBELL_RIGHT_POINT_ZORDER,
    GRID_COLOR,
    MEDIUM_TERM_COLOR,
    SHORT_TERM_COLOR,
    SUBGROUP_CHART_TITLE_FONT_SIZE,
    TEXT_COLOR,
)
from src.charts.style import (
    add_figure_legend,
    apply_chart_style,
    draw_figure,
    draw_group_pair_y_labels,
)
from src.transform.chart_3_gap_shapes import build_chart_3_plot_table
from src.transform.constants import MEDIUM_TERM_TIME_WINDOW, SHORT_TERM_TIME_WINDOW


def create_chart_3(chart_table: pd.DataFrame) -> Figure:
    apply_chart_style()
    plot_table = build_chart_3_plot_table(chart_table)
    row_positions = np.arange(len(plot_table))

    short_gaps = pd.to_numeric(plot_table[SHORT_TERM_TIME_WINDOW], errors="coerce")
    medium_gaps = pd.to_numeric(plot_table[MEDIUM_TERM_TIME_WINDOW], errors="coerce")
    available_mask = short_gaps.notna() & medium_gaps.notna()

    figure, axis = plt.subplots(figsize=(8.2, 5.2))
    axis.axvline(0, color=TEXT_COLOR, linewidth=1.0, alpha=0.6, zorder=0)
    axis.hlines(
        row_positions[available_mask],
        short_gaps[available_mask],
        medium_gaps[available_mask],
        color=CONNECTOR_COLOR,
        linewidth=2.2,
        zorder=DUMBBELL_CONNECTOR_ZORDER,
    )
    axis.scatter(
        short_gaps[available_mask],
        row_positions[available_mask],
        color=SHORT_TERM_COLOR,
        s=44,
        label=CATCH_UP_SHORT_TERM_LABEL,
        zorder=DUMBBELL_LEFT_POINT_ZORDER,
    )
    axis.scatter(
        medium_gaps[available_mask],
        row_positions[available_mask],
        color=MEDIUM_TERM_COLOR,
        edgecolors="white",
        linewidths=0.9,
        s=44,
        label=CATCH_UP_MEDIUM_TERM_LABEL,
        zorder=DUMBBELL_RIGHT_POINT_ZORDER,
    )

    _draw_pair_y_labels(axis, row_positions, plot_table)
    axis.set_title(
        CHART_3_TITLE,
        loc="left",
        fontsize=SUBGROUP_CHART_TITLE_FONT_SIZE,
        color=TEXT_COLOR,
    )
    axis.set_xlabel("Signed full-time employment gap (percentage points)")
    axis.set_xlim(*CHART_3_X_AXIS.limits)
    axis.set_xticks(
        np.array(
            [
                CHART_3_X_AXIS.minimum,
                *np.arange(0, CHART_3_X_AXIS.maximum + 1, CHART_3_X_AXIS.tick_step),
            ]
        )
    )
    axis.grid(
        axis="x",
        color=GRID_COLOR,
        linewidth=AXIS_GRID_LINEWIDTH,
    )
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.tick_params(colors=TEXT_COLOR)
    axis.invert_yaxis()

    add_figure_legend(figure, axis, anchor=(0.98, 0.98))
    figure.tight_layout(rect=(0, 0, 1, 0.92))
    return draw_figure(figure)


def _draw_pair_y_labels(
    axis: Axes,
    row_positions: np.ndarray,
    plot_table: pd.DataFrame,
) -> None:
    pair_labels = [
        f"{reference_group} vs {comparison_group}"
        for reference_group, comparison_group in zip(
            plot_table["reference_group"],
            plot_table["comparison_group"],
        )
    ]
    draw_group_pair_y_labels(
        axis,
        row_positions,
        plot_table["subgroup_dimension"],
        pair_labels,
    )
