from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure

import src.charts.style as ChartStyle
import src.charts.constants as ChartConstants
from src.transform.constants import QILT_SHORT_MEDIUM_OUTCOME_SPECS

def create_unequal_distribution_chart(levels_table: pd.DataFrame) -> Figure:
    ChartStyle.apply_chart_style()
    ordered_table = levels_table.sort_values(
        ["row_group_order", "row_group"],
        kind="mergesort",
    ).reset_index(drop=True)
    row_positions = np.arange(len(ordered_table))

    figure, axes = plt.subplots(
        nrows=1,
        ncols=len(QILT_SHORT_MEDIUM_OUTCOME_SPECS),
        figsize=(12.4, 5.8),
        sharey=True,
        gridspec_kw={"width_ratios": ChartConstants.UNEQUAL_PANEL_WIDTH_RATIOS},
    )

    for axis, (outcome_key, _, _) in zip(axes, QILT_SHORT_MEDIUM_OUTCOME_SPECS):
        panel_style = ChartConstants.UNEQUAL_PANEL_STYLES[outcome_key]
        low_values = pd.to_numeric(
            ordered_table[f"{outcome_key}_low_value"],
            errors="coerce",
        ).to_numpy(dtype=float)
        high_values = pd.to_numeric(
            ordered_table[f"{outcome_key}_high_value"],
            errors="coerce",
        ).to_numpy(dtype=float)
        gap_values = pd.to_numeric(
            ordered_table[f"{outcome_key}_gap"],
            errors="coerce",
        ).to_numpy(dtype=float)
        available_mask = np.isfinite(low_values) & np.isfinite(high_values)

        axis.hlines(
            row_positions[available_mask],
            low_values[available_mask],
            high_values[available_mask],
            color=ChartConstants.CONNECTOR_COLOR,
            linewidth=panel_style["line_width"],
            alpha=panel_style["alpha"],
            zorder=ChartConstants.DUMBBELL_CONNECTOR_ZORDER,
        )
        axis.scatter(
            low_values[available_mask],
            row_positions[available_mask],
            color=ChartConstants.SHORT_TERM_COLOR,
            s=panel_style["marker_size"],
            label="Lower subgroup in pair",
            alpha=panel_style["alpha"],
            zorder=ChartConstants.DUMBBELL_LEFT_POINT_ZORDER,
        )
        axis.scatter(
            high_values[available_mask],
            row_positions[available_mask],
            facecolors="white",
            edgecolors=ChartConstants.SHORT_TERM_COLOR,
            linewidths=1.4,
            s=panel_style["marker_size"],
            label="Higher subgroup in pair",
            alpha=panel_style["alpha"],
            zorder=ChartConstants.DUMBBELL_RIGHT_POINT_ZORDER,
        )

        for row_index in np.flatnonzero(available_mask):
            gap_value = gap_values[row_index]
            axis.text(
                min(
                    max(low_values[row_index], high_values[row_index])
                    + ChartConstants.UNEQUAL_GAP_LABEL_OFFSET,
                    ChartConstants.SUBGROUP_LEVELS_X_AXIS.maximum - 0.4,
                ),
                row_positions[row_index],
                f"{gap_value:.1f} pp",
                fontsize=8,
                color=ChartConstants.TEXT_COLOR,
                ha="left",
                va="center",
                alpha=panel_style["alpha"],
            )

        for row_index in np.flatnonzero(~available_mask):
            availability_note = (
                ordered_table.iloc[row_index][f"{outcome_key}_availability_note"]
                or ordered_table.iloc[row_index]["availability_note"]
                or "Unavailable"
            )
            axis.text(
                ChartConstants.SUBGROUP_LEVELS_X_AXIS.minimum + 1.0,
                row_positions[row_index],
                str(availability_note),
                fontsize=8,
                color=ChartConstants.TEXT_COLOR,
                ha="left",
                va="center",
                alpha=0.8,
            )

        ChartStyle.style_outcome_axis(
            axis,
            title=ChartConstants.QILT_OUTCOME_TITLES[outcome_key],
            x_label="2024 short-term rate (percentage)",
        )
        axis.title.set_alpha(panel_style["title_alpha"])
        axis.set_xlim(*ChartConstants.SUBGROUP_LEVELS_X_AXIS.limits)
        axis.set_xticks(ChartConstants.SUBGROUP_LEVELS_X_AXIS.ticks)

    ChartStyle.draw_group_pair_y_labels(
        axes[0],
        row_positions,
        ordered_table["row_group"],
        ordered_table["pair_label"],
    )

    for axis in axes[1:]:
        axis.tick_params(axis="y", left=False, labelleft=False)

    ChartStyle.add_figure_legend(
        figure,
        axes[0],
        anchor=(0.98, 0.985),
    )

    figure.suptitle(
        ChartConstants.UNEQUAL_DISTRIBUTION_TITLE,
        fontsize=ChartConstants.SUBGROUP_CHART_TITLE_FONT_SIZE,
        color=ChartConstants.TEXT_COLOR,
        x=0.11,
        ha="left",
    )
    figure.tight_layout(rect=(0, 0, 1, 0.94))
    return ChartStyle.draw_figure(figure)
