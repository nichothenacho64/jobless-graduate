from __future__ import annotations

from typing import cast

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

from src.charts.constants import (
    AXIS_GRID_LINEWIDTH,
    CHART_2_SERIES_COLORS,
    CHART_2_SERIES_LABELS,
    CHART_2_SERIES_MARKER_FACES,
    CHART_2_TITLE,
    CHART_2_Y_LIMITS,
    CHART_2_Y_TICKS,
    GRID_COLOR,
    SUBGROUP_CHART_TITLE_FONT_SIZE,
    TEXT_COLOR,
)
from src.charts.style import add_figure_legend, apply_chart_style, draw_figure
from src.transform.constants import CHART_2_CONSTANTS


def create_chart_2(chart_table: pd.DataFrame) -> Figure:
    apply_chart_style()
    ordered_table = chart_table.copy()
    if "series_order" not in ordered_table.columns:
        ordered_table["series_order"] = ordered_table["series_key"].map(
            CHART_2_CONSTANTS["series_order"]
        )
    x_column = "display_year" if "display_year" in ordered_table.columns else "year"
    ordered_table = ordered_table.sort_values(
        ["series_order", x_column],
        kind="mergesort",
    )

    figure, axis = plt.subplots(figsize=(8.8, 4.6))

    for raw_series_key, series_table in ordered_table.groupby("series_key", sort=False):
        series_key = cast(str, raw_series_key)

        axis.plot(
            series_table[x_column],
            series_table["value_pct"],
            color=CHART_2_SERIES_COLORS[series_key],
            linewidth=2.4,
            marker="o",
            markersize=6,
            markerfacecolor=CHART_2_SERIES_MARKER_FACES[series_key],
            markeredgecolor=CHART_2_SERIES_COLORS[series_key],
            markeredgewidth=1.2,
            label=CHART_2_SERIES_LABELS[series_key],
        )

    axis.set_title(
        CHART_2_TITLE,
        loc="left",
        fontsize=SUBGROUP_CHART_TITLE_FONT_SIZE,
        color=TEXT_COLOR,
    )
    axis.set_xlabel("Graduation year")
    axis.set_ylabel("Full-time employment (%)")
    axis.set_ylim(*CHART_2_Y_LIMITS)
    axis.set_yticks(CHART_2_Y_TICKS)
    axis.grid(
        axis="y",
        color=GRID_COLOR,
        linewidth=AXIS_GRID_LINEWIDTH,
    )
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.tick_params(colors=TEXT_COLOR)

    add_figure_legend(figure, axis, anchor=(0.98, 0.98))
    figure.tight_layout(rect=(0, 0, 1, 0.92))
    return draw_figure(figure)
