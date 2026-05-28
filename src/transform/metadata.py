from __future__ import annotations

from src.transform.constants import (
    CHART_2_CONSTANTS,
    CHART_6_CONSTANTS,
    MEDIUM_TERM_TIME_WINDOW,
    SHORT_TERM_TIME_WINDOW,
)


CHART_1A_METADATA = {
    "labels": {
        "dimensions": {
            "year": {
                "label": "Year",
            },
        },
        "metrics": {
            "bachelor_degree_or_above_holders_population": {
                "label": "Population with bachelor degree or above",
                "unit": "people",
            },
            "bachelor_degree_or_above_holders_increase_pct": {
                "label": "Increase in bachelor-degree-or-above holders since 2016",
                "unit": "percent",
            },
        },
    },
}

CHART_1B_METADATA = {
    "labels": {
        "dimensions": {
            "age_group": {
                "label": "Age group",
            },
            "skill_level": {
                "label": "Skill levels",
            },
        },
        "metrics": {
            "share_pct": {
                "label": "Share",
                "unit": "percent",
            },
        },
    },
}

CHART_2_METADATA = {
    "labels": {
        "dimensions": {
            "display_year": {
                "label": "Graduation year",
            },
        },
        "series": {
            CHART_2_CONSTANTS["series_keys"]["gos_l_short_term"]: "GOS-L short term",
            CHART_2_CONSTANTS["series_keys"]["gos_l_medium_term"]: "GOS-L medium term",
            CHART_2_CONSTANTS["series_keys"]["gos_short_term"]: "GOS short term",
        },
        "metrics": {
            "value_pct": {
                "label": "Full-time employment",
                "unit": "percent",
            },
        },
    },
}

CHART_3_METADATA = {
    "labels": {
        "dimensions": {
            "subgroup_dimension": {
                "label": "Subgroup dimension",
            },
        },
        "metrics": {
            "gap_pp": {
                "label": "2024 short-term full-time employment gap",
                "unit": "percentage_point",
            },
            "lower_group_pct": {
                "label": "2024 short-term full-time employment",
                "unit": "percent",
            },
            "higher_group_pct": {
                "label": "2024 short-term full-time employment",
                "unit": "percent",
            },
        },
    },
}

CHART_4_METADATA = {
    "labels": {
        "time_windows": {
            SHORT_TERM_TIME_WINDOW: "Short term",
            MEDIUM_TERM_TIME_WINDOW: "Medium term",
        },
        "metrics": {
            "signed_gap_pp": {
                "label": "Signed full-time employment gap",
                "unit": "percentage_point",
            },
            "reference_group_pct": {
                "label": "Reference group full-time employment",
                "unit": "percent",
            },
            "comparison_group_pct": {
                "label": "Comparison group full-time employment",
                "unit": "percent",
            },
        },
    },
}

CHART_5_METADATA = {
    "labels": {
        "dimensions": {
            "study_area": {
                "label": "Study area",
            },
        },
        "metrics": {
            "short_term_fte_pct": {
                "label": "Short-term full-time employment",
                "unit": "percent",
            },
            "medium_term_fte_pct": {
                "label": "Medium-term full-time employment",
                "unit": "percent",
            },
        },
    },
}

CHART_6_METADATA = {
    "labels": {
        "dimensions": {
            "study_area": {
                "label": "Study area",
            },
        },
        "fit_metrics": {
            CHART_6_CONSTANTS["work_fit_metric_key"]: "Skills and education not fully utilised",
        },
        "metrics": {
            "fte_gain_pp": {
                "label": "Full-time employment gain",
                "unit": "percentage_point",
            },
            "underutilisation_reduction_pp": {
                "label": "Underutilisation reduction",
                "unit": "percentage_point",
            },
        },
    },
}

CHART_7_METADATA = {
    "labels": {
        "time_windows": {
            SHORT_TERM_TIME_WINDOW: "Short term",
            MEDIUM_TERM_TIME_WINDOW: "Medium term",
        },
        "metrics": {
            "signed_gap_pp": {
                "label": "Full-time employment gap",
                "unit": "percentage_point",
            },
            "reference_group_pct": {
                "label": "Reference group full-time employment",
                "unit": "percent",
            },
            "comparison_group_pct": {
                "label": "Comparison group full-time employment",
                "unit": "percent",
            },
        },
    },
    "details": {
        "signed_gap_direction": "comparison_group_pct - reference_group_pct",
    },
}
