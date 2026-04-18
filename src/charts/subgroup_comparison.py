from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.colors import TwoSlopeNorm
from matplotlib.figure import Figure

import src.charts.style as ChartStyle
from src.charts.common import (
    build_group_boundaries,
    draw_group_boundaries,
    plot_dumbbell_series,
    style_outcome_axis,
)
from src.constants.qilt import (
    QILT_OUTCOME_SHORT_TITLES,
    QILT_OUTCOME_TITLES,
    SUBGROUP_LONG_OUTCOME_SPECS,
)

SUBGROUP_CHART_TITLE_FONT_SIZE = 13
SUBGROUP_Y_TICK_FONT_SIZE = 9

LEVELS_CHART_FIGSIZE = (9.0, 10.5)
LEVELS_CHART_MARKER_SIZE = 30
LEVELS_CHART_X_LIMITS = (50, 100)
LEVELS_CHART_X_TICKS = np.arange(50, 101, 10)
LEVELS_CHART_SUPTITLE_X = 0.12
LEVELS_CHART_TIGHT_LAYOUT_RECT = (0, 0, 1, 0.91)
LEVELS_CHART_LEGEND_ANCHOR = (0.98, 0.965)

CHANGE_HEATMAP_FIGSIZE = (6.4, 8.0)
CHANGE_HEATMAP_MIN_ABS_CHANGE = 1.0
CHANGE_HEATMAP_GROUP_BOUNDARY_LINEWIDTH = 2.0
CHANGE_HEATMAP_TEXT_COLOR_THRESHOLD = 0.55
CHANGE_HEATMAP_TEXT_FONT_SIZE = 7
CHANGE_HEATMAP_COLORBAR_SHRINK = 0.84
CHANGE_HEATMAP_COLORBAR_PAD = 0.03

GAP_WIDTH_CHART_FIGSIZE = (11.0, 4.4)
GAP_WIDTH_CHART_MARKER_SIZE = 32
GAP_WIDTH_CHART_X_LIMITS = (0, 18)
GAP_WIDTH_CHART_X_TICKS = np.arange(0, 19, 6)
GAP_WIDTH_CHART_SUPTITLE_X = 0.06
GAP_WIDTH_CHART_TIGHT_LAYOUT_RECT = (0, 0, 1, 0.86)
GAP_WIDTH_CHART_LEGEND_ANCHOR = (0.98, 0.965)


def _build_group_header_mask(row_groups: pd.Series) -> list[bool]:
    header_mask: list[bool] = []
    previous_group: str | None = None

    for row_group in row_groups.astype(str):
        header_mask.append(row_group != previous_group)
        previous_group = row_group

    return header_mask


def _style_group_header_ticks(axis: Axes, header_mask: list[bool]) -> None:
    for tick_label, is_group_header in zip(axis.get_yticklabels(), header_mask):
        tick_label.set_fontweight("bold" if is_group_header else "normal")
        tick_label.set_fontsize(
            SUBGROUP_Y_TICK_FONT_SIZE + (1 if is_group_header else 0)
        )
        tick_label.set_alpha(1.0 if is_group_header else 0.9)
        tick_label.set_color(ChartStyle.TEXT_COLOR)


def _add_figure_legend(
    figure: Figure,
    source_axis: Axes,
    *,
    anchor: tuple[float, float],
) -> None:
    handles, labels = source_axis.get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        loc="upper right",
        bbox_to_anchor=anchor,
        frameon=False,
        ncols=2,
        columnspacing=1.4,
        handletextpad=0.6,
    )


def create_subgroup_levels_chart(levels_table: pd.DataFrame) -> Figure:
    row_positions = np.arange(len(levels_table))
    chart_labels = levels_table["chart_label"].tolist()
    group_boundaries = build_group_boundaries(levels_table)
    group_header_mask = _build_group_header_mask(levels_table["row_group"])

    figure, axes = plt.subplots(
        nrows=len(SUBGROUP_LONG_OUTCOME_SPECS),
        ncols=1,
        figsize=LEVELS_CHART_FIGSIZE,
        sharey=True,
    )

    for axis, (outcome_key, short_column, medium_column, _) in zip(
        axes, SUBGROUP_LONG_OUTCOME_SPECS
    ):
        short_values = levels_table[short_column].to_numpy(dtype=float)
        medium_values = levels_table[medium_column].to_numpy(dtype=float)

        plot_dumbbell_series(
            axis,
            row_positions,
            short_values,
            medium_values,
            left_label="Short-term",
            right_label="Medium-term",
            marker_size=LEVELS_CHART_MARKER_SIZE,
        )
        draw_group_boundaries(axis, group_boundaries)
        style_outcome_axis(axis, title=QILT_OUTCOME_TITLES[outcome_key], x_label="Per cent")
        axis.set_xlim(*LEVELS_CHART_X_LIMITS)
        axis.set_xticks(LEVELS_CHART_X_TICKS)
        axis.set_yticks(row_positions, chart_labels)
        axis.tick_params(axis="y", left=False, labelleft=True, pad=4)
        _style_group_header_ticks(axis, group_header_mask)

    _add_figure_legend(
        figure,
        axes[0],
        anchor=LEVELS_CHART_LEGEND_ANCHOR,
    )

    figure.suptitle(
        "Short-term and medium-term subgroup levels",
        fontsize=SUBGROUP_CHART_TITLE_FONT_SIZE,
        color=ChartStyle.TEXT_COLOR,
        x=LEVELS_CHART_SUPTITLE_X,
        ha="left",
    )
    figure.tight_layout(rect=LEVELS_CHART_TIGHT_LAYOUT_RECT)
    return figure


def create_subgroup_change_heatmap(levels_table: pd.DataFrame) -> Figure:
    change_columns = [
        change_column for _, _, _, change_column in SUBGROUP_LONG_OUTCOME_SPECS
    ]
    outcome_keys = [outcome_key for outcome_key, _, _, _ in SUBGROUP_LONG_OUTCOME_SPECS]
    change_matrix = levels_table[change_columns].to_numpy(dtype=float)
    max_change = max(
        float(np.abs(change_matrix).max()),
        CHANGE_HEATMAP_MIN_ABS_CHANGE,
    )
    group_boundaries = build_group_boundaries(levels_table)
    group_header_mask = _build_group_header_mask(levels_table["row_group"])

    figure, axis = plt.subplots(figsize=CHANGE_HEATMAP_FIGSIZE)

    heatmap = axis.imshow(
        change_matrix,
        cmap="RdBu_r",
        norm=TwoSlopeNorm(vmin=-max_change, vcenter=0.0, vmax=max_change),
        aspect="auto",
    )

    axis.set_xticks(np.arange(len(outcome_keys)))
    axis.set_xticklabels(
        [QILT_OUTCOME_SHORT_TITLES[outcome_key] for outcome_key in outcome_keys]
    )
    axis.set_yticks(np.arange(len(levels_table)))
    axis.set_yticklabels(levels_table["chart_label"].tolist())
    axis.set_title(
        "Change from short-term to medium-term",
        loc="left",
        fontsize=SUBGROUP_CHART_TITLE_FONT_SIZE,
        color=ChartStyle.TEXT_COLOR,
    )
    axis.tick_params(colors=ChartStyle.TEXT_COLOR)

    for boundary in group_boundaries:
        axis.axhline(
            boundary,
            color="white",
            linewidth=CHANGE_HEATMAP_GROUP_BOUNDARY_LINEWIDTH,
        )

    for row_index in range(change_matrix.shape[0]):
        for column_index in range(change_matrix.shape[1]):
            value = change_matrix[row_index, column_index]
            text_color = (
                "white"
                if abs(value) >= max_change * CHANGE_HEATMAP_TEXT_COLOR_THRESHOLD
                else ChartStyle.TEXT_COLOR
            )
            axis.text(
                column_index,
                row_index,
                f"{value:.1f}",
                ha="center",
                va="center",
                fontsize=CHANGE_HEATMAP_TEXT_FONT_SIZE,
                color=text_color,
            )

    _style_group_header_ticks(axis, group_header_mask)

    colorbar = figure.colorbar(
        heatmap,
        ax=axis,
        shrink=CHANGE_HEATMAP_COLORBAR_SHRINK,
        pad=CHANGE_HEATMAP_COLORBAR_PAD,
    )
    colorbar.set_label("Change (percentage points)", color=ChartStyle.TEXT_COLOR)
    colorbar.ax.yaxis.set_tick_params(color=ChartStyle.TEXT_COLOR)
    plt.setp(colorbar.ax.get_yticklabels(), color=ChartStyle.TEXT_COLOR)

    figure.tight_layout()
    return figure


def create_subgroup_gap_width_chart(gap_width_table: pd.DataFrame) -> Figure:
    row_group_order = gap_width_table["row_group"].drop_duplicates().tolist()
    row_positions = np.arange(len(row_group_order))

    figure, axes = plt.subplots(
        nrows=1,
        ncols=len(SUBGROUP_LONG_OUTCOME_SPECS),
        figsize=GAP_WIDTH_CHART_FIGSIZE,
        sharey=True,
    )

    for axis, (outcome_key, _, _, _) in zip(axes, SUBGROUP_LONG_OUTCOME_SPECS):
        outcome_table = gap_width_table.loc[
            gap_width_table["outcome_key"] == outcome_key
        ].copy()
        outcome_table["row_group"] = pd.Categorical(
            outcome_table["row_group"],
            categories=row_group_order,
            ordered=True,
        )
        outcome_table = outcome_table.sort_values("row_group")

        short_gaps = outcome_table["short_term_gap"].to_numpy(dtype=float)
        medium_gaps = outcome_table["medium_term_gap"].to_numpy(dtype=float)

        plot_dumbbell_series(
            axis,
            row_positions,
            short_gaps,
            medium_gaps,
            left_label="Short-term gap",
            right_label="Medium-term gap",
            marker_size=GAP_WIDTH_CHART_MARKER_SIZE,
        )
        style_outcome_axis(
            axis,
            title=QILT_OUTCOME_TITLES[outcome_key],
            x_label="Gap width (percentage points)",
        )
        axis.set_xlim(*GAP_WIDTH_CHART_X_LIMITS)
        axis.set_xticks(GAP_WIDTH_CHART_X_TICKS)

    axes[0].set_yticks(row_positions, row_group_order)
    axes[0].tick_params(axis="y", left=False, labelleft=True, pad=4)
    _style_group_header_ticks(axes[0], [True] * len(row_group_order))

    for axis in axes[1:]:
        axis.tick_params(axis="y", left=False, labelleft=False)

    _add_figure_legend(
        figure,
        axes[0],
        anchor=GAP_WIDTH_CHART_LEGEND_ANCHOR,
    )

    figure.suptitle(
        "Within-group inequality gap widths",
        fontsize=SUBGROUP_CHART_TITLE_FONT_SIZE,
        color=ChartStyle.TEXT_COLOR,
        x=GAP_WIDTH_CHART_SUPTITLE_X,
        ha="left",
    )
    figure.tight_layout(rect=GAP_WIDTH_CHART_TIGHT_LAYOUT_RECT)
    return figure
