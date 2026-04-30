from __future__ import annotations

from collections.abc import Sequence
from functools import lru_cache
from pathlib import Path
from typing import Optional

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.text import Text
from matplotlib.transforms import blended_transform_factory

from src.preparation.series import is_missing_value
import src.charts.constants as ChartConstants
from src.transform.constants import QILT_SUBGROUP_TEXT_EQUIVALENTS


@lru_cache(maxsize=1)
def _load_source_sans_3_font_variants() -> dict[str, Path]:
    font_paths = {
        path.name: path
        for path in ChartConstants.SOURCE_SANS_3_DIRECTORY.iterdir()
        if path.suffix.lower() in {".ttf", ".otf"}
    }

    if not font_paths:
        raise FileNotFoundError(
            f"No font files found in {ChartConstants.SOURCE_SANS_3_DIRECTORY}"
        )

    missing_variants = sorted(
        file_name
        for file_name in ChartConstants.SOURCE_SANS_3_VARIANTS.values()
        if file_name not in font_paths
    )
    if missing_variants:
        missing_display = ", ".join(missing_variants)
        raise FileNotFoundError(
            f"Missing Source Sans 3 font variants in {ChartConstants.SOURCE_SANS_3_DIRECTORY}: "
            f"{missing_display}"
        )

    for font_path in font_paths.values():
        font_manager.fontManager.addfont(str(font_path))

    return {
        variant_name: font_paths[file_name]
        for variant_name, file_name in ChartConstants.SOURCE_SANS_3_VARIANTS.items()
    }


def _is_bold_weight(weight: str | int | float) -> bool:
    if isinstance(weight, (int, float)):
        return weight >= 600

    normalized_weight = str(weight).lower()
    if normalized_weight in {"normal", "regular", "book", "roman", "medium"}:
        return False

    return font_manager.weight_dict.get(normalized_weight, 400) >= 600


def _resolve_text_font_variant(text: Text) -> Path:
    font_variants = _load_source_sans_3_font_variants()
    is_italic = str(text.get_fontstyle()).lower() == "italic"
    is_bold = _is_bold_weight(text.get_fontweight())

    if is_bold and is_italic:
        variant_name = "bold_italic"
    elif is_bold:
        variant_name = "bold"
    elif is_italic:
        variant_name = "italic"
    else:
        variant_name = "regular"

    return font_variants[variant_name]


def _build_font_properties(text: Text) -> font_manager.FontProperties:
    return font_manager.FontProperties(
        fname=str(_resolve_text_font_variant(text)),
        size=text.get_fontsize(),
    )


def _apply_source_sans_3_to_figure(figure: Figure) -> None:
    for text in figure.findobj(match=Text):
        text.set_fontproperties(_build_font_properties(text))


def apply_chart_style() -> None:
    _load_source_sans_3_font_variants()

    sans_serif_fonts = [
        ChartConstants.SOURCE_SANS_3_FONT_FAMILY,
        *[
            font_name
            for font_name in mpl.rcParams.get("font.sans-serif", [])
            if font_name != ChartConstants.SOURCE_SANS_3_FONT_FAMILY
        ],
    ]

    mpl.rcParams["font.family"] = [ChartConstants.SOURCE_SANS_3_FONT_FAMILY]
    mpl.rcParams["font.sans-serif"] = sans_serif_fonts
    mpl.rcParams["pdf.fonttype"] = 42
    mpl.rcParams["ps.fonttype"] = 42
    mpl.rcParams["svg.fonttype"] = "none"


def build_group_boundaries(levels_table: pd.DataFrame) -> list[float]:
    group_sizes = levels_table.groupby("row_group", sort=False).size()
    boundaries: list[float] = []
    running_total = 0

    for group_size in group_sizes.iloc[:-1]:
        running_total += int(group_size)
        boundaries.append(
            running_total - ChartConstants.GROUP_BOUNDARY_POSITION_OFFSET
        )

    return boundaries


def build_group_chart_labels(
    row_groups: Sequence[object] | pd.Series,
    row_labels: Sequence[object] | pd.Series,
) -> list[str]:
    labels: list[str] = []
    previous_group: Optional[str] = None

    for row_group, row_label in zip(row_groups, row_labels):
        row_group_text = str(row_group)
        row_label_text = _format_chart_label_text(row_label)

        if row_group_text != previous_group:
            labels.append(f"{row_group_text}: {row_label_text}")
            previous_group = row_group_text
        else:
            labels.append(f"  {row_label_text}")

    return labels

def _format_chart_label_text(value: object) -> str:
    text = str(value)
    return QILT_SUBGROUP_TEXT_EQUIVALENTS.get(text, text)


def build_group_header_mask(
    row_groups: Sequence[object] | pd.Series,
) -> list[bool]:
    header_mask: list[bool] = []
    previous_group: Optional[str] = None

    for row_group in row_groups:
        row_group_text = str(row_group)
        header_mask.append(row_group_text != previous_group)
        previous_group = row_group_text

    return header_mask


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
        color=ChartConstants.CONNECTOR_COLOR,
        linewidth=ChartConstants.DUMBBELL_CONNECTOR_LINEWIDTH,
        zorder=ChartConstants.DUMBBELL_CONNECTOR_ZORDER,
    )
    axis.scatter(
        left_values,
        row_positions,
        color=ChartConstants.SHORT_TERM_COLOR,
        s=marker_size,
        label=left_label,
        zorder=ChartConstants.DUMBBELL_LEFT_POINT_ZORDER,
    )
    axis.scatter(
        right_values,
        row_positions,
        color=ChartConstants.MEDIUM_TERM_COLOR,
        s=marker_size,
        label=right_label,
        zorder=ChartConstants.DUMBBELL_RIGHT_POINT_ZORDER,
    )


def draw_group_boundaries(
    axis: Axes,
    boundaries: list[float],
    *,
    color: str = ChartConstants.GRID_COLOR,
    linewidth: float = ChartConstants.GROUP_BOUNDARY_LINEWIDTH,
) -> None:
    for boundary in boundaries:
        axis.axhline(boundary, color=color, linewidth=linewidth)


def style_outcome_axis(axis: Axes, *, title: str, x_label: str) -> None:
    axis.set_title(
        title,
        loc="left",
        fontsize=ChartConstants.AXIS_TITLE_FONT_SIZE,
        color=ChartConstants.TEXT_COLOR,
    )
    axis.set_xlabel(x_label)
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


def style_group_header_ticks(axis: Axes, header_mask: list[bool]) -> None:
    for tick_label, is_group_header in zip(axis.get_yticklabels(), header_mask):
        tick_label.set_fontweight("bold" if is_group_header else "normal")
        tick_label.set_fontsize(
            ChartConstants.SUBGROUP_Y_TICK_FONT_SIZE + (1 if is_group_header else 0)
        )
        tick_label.set_alpha(1.0 if is_group_header else 0.9)
        tick_label.set_color(ChartConstants.TEXT_COLOR)


def draw_group_pair_y_labels(
    axis: Axes,
    row_positions: Sequence[float] | np.ndarray,
    row_groups: Sequence[object] | pd.Series,
    pair_labels: Sequence[object] | pd.Series,
) -> None:
    axis.set_yticks(row_positions)
    axis.set_yticklabels([])
    axis.tick_params(axis="y", left=False, labelleft=False, pad=0)

    transform = blended_transform_factory(axis.transAxes, axis.transData)

    for row_position, row_group, pair_label in zip(row_positions, row_groups, pair_labels):
        pair_label_text = "Unavailable" if is_missing_value(pair_label) else str(pair_label)

        axis.text(
            ChartConstants.GROUP_PAIR_LABEL_X_POSITION,
            row_position - ChartConstants.GROUP_PAIR_LABEL_LINE_OFFSET,
            str(row_group),
            transform=transform,
            ha="right",
            va="center",
            fontsize=ChartConstants.SUBGROUP_Y_TICK_FONT_SIZE + 1,
            fontweight="bold",
            color=ChartConstants.TEXT_COLOR,
            clip_on=False,
        )
        axis.text(
            ChartConstants.GROUP_PAIR_LABEL_X_POSITION,
            row_position + ChartConstants.GROUP_PAIR_LABEL_LINE_OFFSET,
            pair_label_text,
            transform=transform,
            ha="right",
            va="center",
            fontsize=ChartConstants.SUBGROUP_Y_TICK_FONT_SIZE,
            color=ChartConstants.TEXT_COLOR,
            alpha=0.9,
            clip_on=False,
        )


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


def add_figure_legend(
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


def draw_figure(figure: Figure) -> Figure:
    figure.canvas.draw()
    _apply_source_sans_3_to_figure(figure)
    figure.canvas.draw()
    plt.close(figure)
    return figure
