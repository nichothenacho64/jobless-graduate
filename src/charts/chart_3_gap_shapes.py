from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from src.preparation.series import is_missing_value
import src.charts.constants as ChartConstants
import src.charts.style as ChartStyle
from src.transform.chart_3_gap_shapes import build_chart_3_plot_table
from src.transform.constants import MEDIUM_TERM_TIME_WINDOW, SHORT_TERM_TIME_WINDOW


def create_chart_3(chart_table: pd.DataFrame) -> Figure:
    ChartStyle.apply_chart_style()
    plot_table = build_chart_3_plot_table(chart_table)
    row_positions = np.arange(len(plot_table))

    short_gaps = pd.to_numeric(plot_table[SHORT_TERM_TIME_WINDOW], errors="coerce")
    medium_gaps = pd.to_numeric(plot_table[MEDIUM_TERM_TIME_WINDOW], errors="coerce")
    available_mask = short_gaps.notna() & medium_gaps.notna()

    figure, axis = plt.subplots(figsize=(8.2, 5.2))
    axis.hlines(
        row_positions[available_mask],
        short_gaps[available_mask],
        medium_gaps[available_mask],
        color=ChartConstants.CONNECTOR_COLOR,
        linewidth=2.2,
        zorder=ChartConstants.DUMBBELL_CONNECTOR_ZORDER,
    )
    axis.scatter(
        short_gaps[available_mask],
        row_positions[available_mask],
        color=ChartConstants.SHORT_TERM_COLOR,
        s=44,
        label=ChartConstants.CATCH_UP_SHORT_TERM_LABEL,
        zorder=ChartConstants.DUMBBELL_LEFT_POINT_ZORDER,
    )
    axis.scatter(
        medium_gaps[available_mask],
        row_positions[available_mask],
        color=ChartConstants.MEDIUM_TERM_COLOR,
        edgecolors="white",
        linewidths=0.9,
        s=44,
        label=ChartConstants.CATCH_UP_MEDIUM_TERM_LABEL,
        zorder=ChartConstants.DUMBBELL_RIGHT_POINT_ZORDER,
    )

    _draw_behind_y_labels(axis, row_positions, plot_table)
    axis.set_title(
        ChartConstants.CHART_3_TITLE,
        loc="left",
        fontsize=ChartConstants.SUBGROUP_CHART_TITLE_FONT_SIZE,
        color=ChartConstants.TEXT_COLOR,
    )
    axis.set_xlabel("Full-time employment gap width (percentage points)")
    axis.set_xlim(*ChartConstants.CHART_3_X_AXIS.limits)
    axis.set_xticks(ChartConstants.CHART_3_X_AXIS.ticks)
    axis.grid(
        axis="x",
        color=ChartConstants.GRID_COLOR,
        linewidth=ChartConstants.AXIS_GRID_LINEWIDTH,
    )
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.tick_params(colors=ChartConstants.TEXT_COLOR)
    axis.invert_yaxis()

    ChartStyle.add_figure_legend(figure, axis, anchor=(0.98, 0.98))
    figure.tight_layout(rect=(0, 0, 1, 0.92))
    return ChartStyle.draw_figure(figure)


def _draw_behind_y_labels(
    axis: Axes,
    row_positions: np.ndarray,
    plot_table: pd.DataFrame,
) -> None:
    behind_labels = [
        _build_behind_label(short_group, medium_group)
        for short_group, medium_group in zip(
            plot_table[f"{SHORT_TERM_TIME_WINDOW}_lower_group"],
            plot_table[f"{MEDIUM_TERM_TIME_WINDOW}_lower_group"],
        )
    ]
    ChartStyle.draw_group_pair_y_labels(
        axis,
        row_positions,
        plot_table["subgroup_dimension"],
        behind_labels,
    )


def _build_behind_label(short_group: object, medium_group: object) -> str:
    short_group_label = _format_group_label(short_group)
    medium_group_label = _format_group_label(medium_group)

    if short_group_label == medium_group_label:
        return f"Behind: {short_group_label}"

    return (
        f"Behind: {short_group_label} (short); "
        f"{medium_group_label} (medium)"
    )


def _format_group_label(group_label: object) -> str:
    if is_missing_value(group_label):
        return "Unavailable"

    return str(group_label)
