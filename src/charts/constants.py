from __future__ import annotations

import numpy as np

from src.constants import ASSETS_DIR
from src.types import AxisSpec

SOURCE_SANS_3_FONT_FAMILY = "Source Sans 3"
SOURCE_SANS_3_DIRECTORY = ASSETS_DIR / "fonts" / "source_sans_3"

SOURCE_SANS_3_VARIANTS = {
    "regular": "SourceSans3-Regular.ttf",
    "bold": "SourceSans3-Bold.ttf",
    "italic": "SourceSans3-Italic.ttf",
    "bold_italic": "SourceSans3-BoldItalic.ttf",
}

SHORT_TERM_COLOR = "#A55A1F"
MEDIUM_TERM_COLOR = "#2F5D7E"
CONNECTOR_COLOR = "#A9B0B5"
GRID_COLOR = "#E6E6E6"
TEXT_COLOR = "#222222"

GROUP_BOUNDARY_POSITION_OFFSET = 0.5

DUMBBELL_CONNECTOR_LINEWIDTH = 1.5
DUMBBELL_CONNECTOR_ZORDER = 1
DUMBBELL_LEFT_POINT_ZORDER = 2
DUMBBELL_RIGHT_POINT_ZORDER = 3

GROUP_BOUNDARY_LINEWIDTH = 1.0
AXIS_TITLE_FONT_SIZE = 12
AXIS_GRID_LINEWIDTH = 0.8

SUBGROUP_CHART_TITLE_FONT_SIZE = 11
SUBGROUP_Y_TICK_FONT_SIZE = 8
GROUP_PAIR_LABEL_X_POSITION = -0.04
GROUP_PAIR_LABEL_LINE_OFFSET = 0.18
LEVELS_CHART_AXIS_PADDING = 3
GAP_WIDTH_CHART_AXIS_PADDING = 1

SUBGROUP_LEVELS_X_AXIS = AxisSpec(55, 95, 10)
SUBGROUP_GAP_WIDTH_X_AXIS = AxisSpec(0, 18, 6)

SUBGROUP_CHANGE_HEATMAP_MIN_ABS_CHANGE = 1.0

QILT_OUTCOME_TITLES = {
    "full_time_employment": "Full-time employment",
    "overall_employment": "Overall employment",
    "labour_force_participation": "Labour force participation",
}

QILT_OUTCOME_SHORT_TITLES = {
    "full_time_employment": "Full-time",
    "overall_employment": "Overall",
    "labour_force_participation": "LFP",
}

TRANSITION_SUPTITLE_Y = 0.975
TRANSITION_LEGEND_ANCHOR = (0.98, 0.945)  # 0.985 is lower
TRANSITION_TIGHT_LAYOUT_RECT = (0, 0, 1, 0.90)
TRANSITION_Y_LIMITS = (65, 95)
TRANSITION_Y_TICKS = np.arange(65, 96, 5)
TRANSITION_SHORT_TERM_LABEL = "Short-term (4 months after graduation)"
TRANSITION_MEDIUM_TERM_LABEL = "Medium-term (3 years after graduation)"
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

CATCH_UP_SHORT_TERM_LABEL = "Short-term gap (4 months)"
CATCH_UP_MEDIUM_TERM_LABEL = "Medium-term gap (3 years)"
CATCH_UP_LEVELS_TITLE = "Short-term and medium-term subgroup levels"
CATCH_UP_CHANGE_HEATMAP_TITLE = "Change from short-term to medium-term"
CATCH_UP_GAP_WIDTH_TITLE = "Within-group inequality gap widths"
GAP_WIDTH_PANEL_WIDTH_RATIOS = (1.24, 1.0, 0.86)
GAP_WIDTH_PANEL_STYLES = {
    "full_time_employment": {
        "alpha": 1.0,
        "line_width": 2.2,
        "marker_size": 42,
        "title_alpha": 1.0,
    },
    "overall_employment": {
        "alpha": 0.9,
        "line_width": 1.9,
        "marker_size": 38,
        "title_alpha": 0.95,
    },
    "labour_force_participation": {
        "alpha": 0.62,
        "line_width": 1.5,
        "marker_size": 34,
        "title_alpha": 0.78,
    },
}

UNEQUAL_DISTRIBUTION_TITLE = "2024 short-term subgroup gaps by dimension"
UNEQUAL_PANEL_WIDTH_RATIOS = (1.24, 1.0, 0.86)
UNEQUAL_GAP_LABEL_OFFSET = 1.35
UNEQUAL_PANEL_STYLES = {
    "full_time_employment": {
        "alpha": 1.0,
        "line_width": 2.3,
        "marker_size": 42,
        "title_alpha": 1.0,
    },
    "overall_employment": {
        "alpha": 0.9,
        "line_width": 1.9,
        "marker_size": 38,
        "title_alpha": 0.95,
    },
    "labour_force_participation": {
        "alpha": 0.62,
        "line_width": 1.5,
        "marker_size": 34,
        "title_alpha": 0.78,
    },
}
