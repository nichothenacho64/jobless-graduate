from __future__ import annotations

from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import TwoSlopeNorm
from matplotlib.figure import Figure

import src.charts.style as ChartStyle
import src.charts.constants as ChartConstants
from src.transform.constants import QILT_SHORT_MEDIUM_OUTCOME_SPECS

def create_catch_up_levels_chart(
    levels_table: pd.DataFrame,
    *,
    row_group_order: Optional[list[str]] = None,
) -> Figure:
    ChartStyle.apply_chart_style()
    ordered_table = _order_levels_table(
        levels_table,
        row_group_order=row_group_order,
    )
    row_positions = np.arange(len(ordered_table))
    chart_labels = ChartStyle.build_group_chart_labels(
        ordered_table["row_group"],
        ordered_table["row_label"],
    )
    group_boundaries = ChartStyle.build_group_boundaries(ordered_table)
    group_header_mask = ChartStyle.build_group_header_mask(ordered_table["row_group"])

    figure, axes = plt.subplots(
        nrows=len(QILT_SHORT_MEDIUM_OUTCOME_SPECS),
        ncols=1,
        figsize=(9.0, 10.5),
        sharey=True,
    )

    for axis, (outcome_key, short_column, medium_column) in zip(
        axes, QILT_SHORT_MEDIUM_OUTCOME_SPECS
    ):
        short_values = ordered_table[short_column].to_numpy(dtype=float)
        medium_values = ordered_table[medium_column].to_numpy(dtype=float)

        ChartStyle.plot_dumbbell_series(
            axis,
            row_positions,
            short_values,
            medium_values,
            left_label="Short-term",
            right_label="Medium-term",
            marker_size=30,
        )
        ChartStyle.draw_group_boundaries(axis, group_boundaries)
        ChartStyle.style_outcome_axis(
            axis,
            title=ChartConstants.QILT_OUTCOME_TITLES[outcome_key],
            x_label="Percentage",
        )
        axis.set_xlim(*ChartConstants.SUBGROUP_LEVELS_X_AXIS.limits)
        axis.set_xticks(ChartConstants.SUBGROUP_LEVELS_X_AXIS.ticks)
        axis.set_yticks(row_positions, chart_labels)
        axis.tick_params(axis="y", left=False, labelleft=True, pad=4)
        ChartStyle.style_group_header_ticks(axis, group_header_mask)

    ChartStyle.add_figure_legend(
        figure,
        axes[0],
        anchor=(0.98, 0.965),
    )

    figure.suptitle(
        ChartConstants.CATCH_UP_LEVELS_TITLE,
        fontsize=ChartConstants.SUBGROUP_CHART_TITLE_FONT_SIZE,
        color=ChartConstants.TEXT_COLOR,
        x=0.12,
        ha="left",
    )
    figure.tight_layout(rect=(0, 0, 1, 0.93))
    return ChartStyle.draw_figure(figure)

def create_catch_up_change_heatmap(
    levels_table: pd.DataFrame,
    *,
    row_group_order: Optional[list[str]] = None,
) -> Figure:
    ChartStyle.apply_chart_style()
    ordered_table = _order_levels_table(
        levels_table,
        row_group_order=row_group_order,
    )
    outcome_keys = [outcome_key for outcome_key, _, _ in QILT_SHORT_MEDIUM_OUTCOME_SPECS]
    change_columns = [f"{outcome_key}_change" for outcome_key in outcome_keys]
    change_matrix = ordered_table[change_columns].to_numpy(dtype=float)
    max_change = max(
        float(np.abs(change_matrix).max()),
        ChartConstants.SUBGROUP_CHANGE_HEATMAP_MIN_ABS_CHANGE,
    )
    group_boundaries = ChartStyle.build_group_boundaries(ordered_table)
    group_header_mask = ChartStyle.build_group_header_mask(ordered_table["row_group"])

    figure, axis = plt.subplots(figsize=(6.4, 8.0))

    heatmap = axis.imshow(
        change_matrix,
        cmap="RdBu_r",
        norm=TwoSlopeNorm(vmin=-max_change, vcenter=0.0, vmax=max_change),
        aspect="auto",
    )

    axis.set_xticks(np.arange(len(outcome_keys)))
    axis.set_xticklabels(
        [ChartConstants.QILT_OUTCOME_SHORT_TITLES[outcome_key] for outcome_key in outcome_keys]
    )
    axis.set_yticks(np.arange(len(ordered_table)))
    axis.set_yticklabels(
        ChartStyle.build_group_chart_labels(
            ordered_table["row_group"],
            ordered_table["row_label"],
        )
    )
    axis.set_title(
        ChartConstants.CATCH_UP_CHANGE_HEATMAP_TITLE,
        loc="left",
        fontsize=ChartConstants.SUBGROUP_CHART_TITLE_FONT_SIZE,
        color=ChartConstants.TEXT_COLOR,
    )
    axis.tick_params(colors=ChartConstants.TEXT_COLOR)

    for boundary in group_boundaries:
        axis.axhline(
            boundary,
            color="white",
            linewidth=2.0,
        )

    for row_index in range(change_matrix.shape[0]):
        for column_index in range(change_matrix.shape[1]):
            value = change_matrix[row_index, column_index]
            text_color = (
                "white"
                if abs(value) >= max_change * 0.55
                else ChartConstants.TEXT_COLOR
            )
            axis.text(
                column_index,
                row_index,
                f"{value:.1f}",
                ha="center",
                va="center",
                fontsize=7,
                color=text_color,
            )

    ChartStyle.style_group_header_ticks(axis, group_header_mask)

    colorbar = figure.colorbar(
        heatmap,
        ax=axis,
        shrink=0.84,
        pad=0.03,
    )
    colorbar.set_label("Change (percentage points)", color=ChartConstants.TEXT_COLOR)
    colorbar.ax.yaxis.set_tick_params(color=ChartConstants.TEXT_COLOR)
    plt.setp(colorbar.ax.get_yticklabels(), color=ChartConstants.TEXT_COLOR)

    figure.tight_layout()
    return ChartStyle.draw_figure(figure)

def create_catch_up_gap_width_chart(gap_width_table: pd.DataFrame) -> Figure:
    ChartStyle.apply_chart_style()
    ordered_table = gap_width_table.sort_values(
        ["row_group_order", "row_group"],
        kind="mergesort",
    ).reset_index(drop=True)
    reference_rows = (
        ordered_table.loc[ordered_table["outcome_key"] == "full_time_employment"]
        .sort_values(["row_group_order", "row_group"], kind="mergesort")
        .reset_index(drop=True)
    )
    row_positions = np.arange(len(reference_rows))

    figure, axes = plt.subplots(
        nrows=1,
        ncols=len(QILT_SHORT_MEDIUM_OUTCOME_SPECS),
        figsize=(11.9, 5.6),
        sharey=True,
        gridspec_kw={"width_ratios": ChartConstants.GAP_WIDTH_PANEL_WIDTH_RATIOS},
    )

    for axis, (outcome_key, _, _) in zip(axes, QILT_SHORT_MEDIUM_OUTCOME_SPECS):
        panel_style = ChartConstants.GAP_WIDTH_PANEL_STYLES[outcome_key]
        outcome_table = (
            ordered_table.loc[ordered_table["outcome_key"] == outcome_key]
            .sort_values(["row_group_order", "row_group"], kind="mergesort")
            .reset_index(drop=True)
        )
        short_gaps = pd.to_numeric(
            outcome_table["short_term_gap"],
            errors="coerce",
        ).to_numpy(dtype=float)
        medium_gaps = pd.to_numeric(
            outcome_table["medium_term_gap"],
            errors="coerce",
        ).to_numpy(dtype=float)
        available_mask = np.isfinite(short_gaps) & np.isfinite(medium_gaps)

        axis.hlines(
            row_positions[available_mask],
            short_gaps[available_mask],
            medium_gaps[available_mask],
            color=ChartConstants.CONNECTOR_COLOR,
            linewidth=panel_style["line_width"],
            alpha=panel_style["alpha"],
            zorder=ChartConstants.DUMBBELL_CONNECTOR_ZORDER,
        )
        axis.scatter(
            short_gaps[available_mask],
            row_positions[available_mask],
            color=ChartConstants.SHORT_TERM_COLOR,
            s=panel_style["marker_size"],
            label=ChartConstants.CATCH_UP_SHORT_TERM_LABEL,
            alpha=panel_style["alpha"],
            zorder=ChartConstants.DUMBBELL_LEFT_POINT_ZORDER,
        )
        axis.scatter(
            medium_gaps[available_mask],
            row_positions[available_mask],
            color=ChartConstants.MEDIUM_TERM_COLOR,
            edgecolors="white",
            linewidths=0.9,
            s=panel_style["marker_size"],
            label=ChartConstants.CATCH_UP_MEDIUM_TERM_LABEL,
            alpha=panel_style["alpha"],
            zorder=ChartConstants.DUMBBELL_RIGHT_POINT_ZORDER,
        )
        ChartStyle.style_outcome_axis(
            axis,
            title=ChartConstants.QILT_OUTCOME_TITLES[outcome_key],
            x_label="Gap width (percentage points)",
        )
        axis.title.set_alpha(panel_style["title_alpha"])
        axis.set_xlim(*ChartConstants.SUBGROUP_GAP_WIDTH_X_AXIS.limits)
        axis.set_xticks(ChartConstants.SUBGROUP_GAP_WIDTH_X_AXIS.ticks)

    ChartStyle.draw_group_pair_y_labels(
        axes[0],
        row_positions,
        reference_rows["row_group"],
        reference_rows["pair_label"],
    )
    axes[0].axvline(
        0,
        color=ChartConstants.GRID_COLOR,
        linewidth=1.0,
        zorder=0,
    )

    for axis in axes[1:]:
        axis.tick_params(axis="y", left=False, labelleft=False)

    ChartStyle.add_figure_legend(
        figure,
        axes[0],
        anchor=(0.98, 0.985),
    )

    figure.suptitle(
        ChartConstants.CATCH_UP_GAP_WIDTH_TITLE,
        fontsize=ChartConstants.SUBGROUP_CHART_TITLE_FONT_SIZE,
        color=ChartConstants.TEXT_COLOR,
        x=0.08,
        ha="left",
    )
    figure.tight_layout(rect=(0, 0, 1, 0.94))
    return ChartStyle.draw_figure(figure)

def _order_levels_table(
    levels_table: pd.DataFrame,
    *,
    row_group_order: Optional[list[str]],
) -> pd.DataFrame:
    ordered_table = levels_table.copy()
    ordered_row_groups = row_group_order or ordered_table["row_group"].drop_duplicates().tolist()
    ordered_table["row_group_sort"] = pd.Categorical(
        ordered_table["row_group"],
        categories=ordered_row_groups,
        ordered=True,
    )
    ordered_table = ordered_table.sort_values(
        ["row_group_sort", "short_term_full_time_employment", "row_label"],
        kind="mergesort",
    ).reset_index(drop=True)
    return ordered_table.drop(columns="row_group_sort")
