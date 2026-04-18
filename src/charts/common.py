from __future__ import annotations

import numpy as np
import pandas as pd
from matplotlib.axes import Axes

import src.charts.style as ChartStyle
import src.constants.charts as ChartConstants


def build_group_boundaries(levels_table: pd.DataFrame) -> list[float]:
    group_sizes = levels_table.groupby("row_group", sort=False).size()
    boundaries: list[float] = []
    running_total = 0

    for group_size in group_sizes.iloc[:-1]:
        running_total += int(group_size)
        boundaries.append(running_total - ChartConstants.GROUP_BOUNDARY_POSITION_OFFSET)

    return boundaries

def plot_dumbbell_series(
    axis: Axes,
    row_positions: np.ndarray,
    left_values: np.ndarray,
    right_values: np.ndarray,
    *,
    left_label: str,
    right_label: str,
    marker_size: int,
) -> None:
    axis.hlines(
        row_positions,
        left_values,
        right_values,
        color=ChartStyle.CONNECTOR_COLOR,
        linewidth=ChartConstants.DUMBBELL_CONNECTOR_LINEWIDTH,
        zorder=ChartConstants.DUMBBELL_CONNECTOR_ZORDER,
    )
    axis.scatter(
        left_values,
        row_positions,
        color=ChartStyle.SHORT_TERM_COLOR,
        s=marker_size,
        label=left_label,
        zorder=ChartConstants.DUMBBELL_LEFT_POINT_ZORDER,
    )
    axis.scatter(
        right_values,
        row_positions,
        color=ChartStyle.MEDIUM_TERM_COLOR,
        s=marker_size,
        label=right_label,
        zorder=ChartConstants.DUMBBELL_RIGHT_POINT_ZORDER,
    )

def draw_group_boundaries(
    axis: Axes,
    boundaries: list[float],
    *,
    color: str = ChartStyle.GRID_COLOR,
    linewidth: float = ChartConstants.GROUP_BOUNDARY_LINEWIDTH,
) -> None:
    for boundary in boundaries:
        axis.axhline(boundary, color=color, linewidth=linewidth)

def style_outcome_axis(axis: Axes, *, title: str, x_label: str) -> None:
    axis.set_title(
        title,
        loc="left",
        fontsize=ChartConstants.AXIS_TITLE_FONT_SIZE,
        color=ChartStyle.TEXT_COLOR,
    )
    axis.set_xlabel(x_label)
    axis.grid(
        axis="x",
        color=ChartStyle.GRID_COLOR,
        linewidth=ChartConstants.AXIS_GRID_LINEWIDTH,
    )
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.tick_params(colors=ChartStyle.TEXT_COLOR)
    axis.invert_yaxis()

def set_axis_limits(
    axis: Axes,
    left_values: np.ndarray,
    right_values: np.ndarray,
    *,
    lower_padding: float,
    upper_padding: float,
) -> None:
    value_min = min(left_values.min(), right_values.min())
    value_max = max(left_values.max(), right_values.max())
    axis.set_xlim(max(0, value_min - lower_padding), value_max + upper_padding)
