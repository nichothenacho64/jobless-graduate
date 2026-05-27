from __future__ import annotations


# Generic transform constants
TOTAL_ROW_GROUP = "Total"
SHORT_TERM_TIME_WINDOW = "short_term"
MEDIUM_TERM_TIME_WINDOW = "medium_term"


# Chart ids
CHART_1A_ID = "chart_1a_degree_supply"
CHART_1B_ID = "chart_1b_skill_by_age"
CHART_2_ID = "chart_2_transition_window"
CHART_3_ID = "chart_3_subgroup_bottleneck"
CHART_4_ID = "chart_4_gap_shapes"
CHART_5_ID = "chart_5_field_conversion"
CHART_6_ID = "chart_6_work_fit"
CHART_7_ID = "chart_7_subgroup_comparator"

CHART_TABLE_IDS_BY_NUMBER = {
    1.1: CHART_1A_ID,
    1.2: CHART_1B_ID,
    2: CHART_2_ID,
    3: CHART_3_ID,
    4: CHART_4_ID,
    5: CHART_5_ID,
    6: CHART_6_ID,
    7: CHART_7_ID,
}


# Chart table schemas for referencing column names directly
CHART_TABLE_SCHEMAS = {
    CHART_1A_ID: [
        "year",
        "bachelor_degree_or_above_holders_population",
        "bachelor_degree_or_above_holders_increase_pct",
        "source_key",
    ],
    CHART_1B_ID: [
        "age_group",
        "age_order",
        "skill_level",
        "skill_order",
        "share_pct",
        "source_key",
    ],
    CHART_2_ID: [
        "display_year",
        "series_key",
        "value_pct",
        "source_key",
        "series_order",
    ],
    CHART_3_ID: [
        "subgroup_dimension",
        "gap_pp",
        "lower_group",
        "lower_group_pct",
        "higher_group",
        "higher_group_pct",
        "source_key",
        "sort_order",
    ],
    CHART_4_ID: [
        "subgroup_dimension",
        "time_window",
        "time_window_order",
        "reference_group",
        "reference_group_pct",
        "comparison_group",
        "comparison_group_pct",
        "signed_gap_pp",
        "source_key",
        "sort_order",
    ],
    CHART_5_ID: [
        "study_area",
        "short_term_fte_pct",
        "medium_term_fte_pct",
        "source_key",
    ],
    CHART_6_ID: [
        "study_area",
        "fte_gain_pp",
        "underutilisation_reduction_pp",
        "fit_metric_key",
        "employment_source_key",
        "fit_source_key",
    ],
    CHART_7_ID: [
        "selector_id",
        "subgroup_dimension",
        "time_window",
        "time_window_order",
        "reference_group",
        "reference_group_pct",
        "comparison_group",
        "comparison_group_pct",
        "signed_gap_pp",
        "source_key",
        "sort_order",
    ],
}

CHART_1A_TABLE_COLUMNS = CHART_TABLE_SCHEMAS[CHART_1A_ID]
CHART_1B_TABLE_COLUMNS = CHART_TABLE_SCHEMAS[CHART_1B_ID]
CHART_2_TABLE_COLUMNS = CHART_TABLE_SCHEMAS[CHART_2_ID]
CHART_3_TABLE_COLUMNS = CHART_TABLE_SCHEMAS[CHART_3_ID]
CHART_4_TABLE_COLUMNS = CHART_TABLE_SCHEMAS[CHART_4_ID]
CHART_5_TABLE_COLUMNS = CHART_TABLE_SCHEMAS[CHART_5_ID]
CHART_6_TABLE_COLUMNS = CHART_TABLE_SCHEMAS[CHART_6_ID]
CHART_7_TABLE_COLUMNS = CHART_TABLE_SCHEMAS[CHART_7_ID]


# Source keys
GOS_5_SOURCE_KEY = "gos_5"
GOS_8_SOURCE_KEY = "gos_8"
GOS_21_SOURCE_KEY = "gos_21"
GOS_L_1_SOURCE_KEY = "gos_l_1"
GOS_L_6_SOURCE_KEY = "gos_l_6"
GOS_L_26_SOURCE_KEY = "gos_l_26"
GOS_L_160_SOURCE_KEY = "gos_l_160"
SEW_32_SOURCE_KEY = "sew_32"
SEW_35_SOURCE_KEY = "sew_35"


# Shared QILT constants
GOS_SHORT_TERM_COMPARISON_COLUMNS = {
    "short_term_full_time_employment": "full_time_employment_2024",
    "short_term_overall_employment": "overall_employment_2024",
    "short_term_labour_force_participation": "labour_force_participation_rate_2024",
}

GOS_GENDER_SHORT_TERM_COLUMNS_BY_ROW_LABEL = {
    "Full-time employment": "short_term_full_time_employment",
    "Overall employment": "short_term_overall_employment",
    "Labour force participation rate": "short_term_labour_force_participation",
}

GOS_L_MEDIUM_TERM_COMPARISON_COLUMNS = {
    "medium_term_full_time_employment": "medium_term_full_time_employed",
    "medium_term_overall_employment": "medium_term_overall_employed",
    "medium_term_labour_force_participation": "medium_term_labour_force_participation",
}

QILT_SUBGROUP_TEXT_EQUIVALENTS = {
    "30 years or under": "30 and under",
    "Over 30 years": "Over 30",
    "Internal/Mixed study mode": "Internal/Mixed",
    "External study mode": "External",
    "Language other than English": "Other",
}

QILT_SUBGROUP_DISPLAY_ORDER_BY_ROW_GROUP = {
    "Socio-economic status": ("High", "Medium", "Low"),
}

QILT_SHORT_MEDIUM_OUTCOME_SPECS: tuple[tuple[str, str, str], ...] = (
    (
        "full_time_employment",
        "short_term_full_time_employment",
        "medium_term_full_time_employment",
    ),
    (
        "overall_employment",
        "short_term_overall_employment",
        "medium_term_overall_employment",
    ),
    (
        "labour_force_participation",
        "short_term_labour_force_participation",
        "medium_term_labour_force_participation",
    ),
)


# Shared SEW constants
SEW_SKILL_LEVEL_ORDER = {
    "Skill level 1 (highest)": 0,
    "Skill level 2": 1,
    "Skill level 3": 2,
    "Skill level 4": 3,
    "Skill level 5 (lowest)": 4,
}

SEW_AGE_GROUP_ORDER = {
    "15-24 years": 0,
    "15–24": 0,
    "25-34 years": 1,
    "25–34": 1,
    "35-44 years": 2,
    "35–44": 2,
    "45-54 years": 3,
    "45–54": 3,
    "55-64 years": 4,
    "55–64": 4,
    "65-74 years": 5,
    "65–74": 5,
}


# Chart 2 — transition window
CHART_2_GOS_L_SHORT_TERM_FTE_SERIES_KEY = "gos_l_short_term_fte"
CHART_2_GOS_L_MEDIUM_TERM_FTE_SERIES_KEY = "gos_l_medium_term_fte"
CHART_2_GOS_SHORT_TERM_FTE_SERIES_KEY = "gos_short_term_fte"

CHART_2_SERIES_ORDER = {
    CHART_2_GOS_L_SHORT_TERM_FTE_SERIES_KEY: 0,
    CHART_2_GOS_L_MEDIUM_TERM_FTE_SERIES_KEY: 1,
    CHART_2_GOS_SHORT_TERM_FTE_SERIES_KEY: 2,
}


# Chart 5 — field conversion
CHART_5_EXCLUDED_STUDY_AREAS = {
    "Standard deviation": "non-study-area summary/statistical row",
    "Total": "non-study-area summary row",
}


# Chart 6 — work fit
CHART_6_WORK_FIT_METRIC_KEY = "skills_education_utilisation"
CHART_6_SHORT_TERM_UNDERUTILISATION_COLUMN = (
    "extent_to_which_skills_and_education_not_fully_utilised_short_term_fte"
)
CHART_6_MEDIUM_TERM_UNDERUTILISATION_COLUMN = (
    "extent_to_which_skills_and_education_not_fully_utilised_medium_term_fte"
)
CHART_6_EXCLUDED_STUDY_AREAS = {
    "Total": "non-study-area summary row",
}


# Chart 1A — SEW degree supply
SEW_DEGREE_SUPPLY_BASE_YEAR = 2016
SEW_DEGREE_SUPPLY_YEARS = tuple(range(2016, 2026))


# Chart metadata additions
CHART_1A_METADATA = {
    "labels": {
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
        "time_windows": {
            SHORT_TERM_TIME_WINDOW: "Short term",
            MEDIUM_TERM_TIME_WINDOW: "Medium term",
        },
        "series": {
            CHART_2_GOS_L_SHORT_TERM_FTE_SERIES_KEY: "GOS-L short term",
            CHART_2_GOS_L_MEDIUM_TERM_FTE_SERIES_KEY: "GOS-L medium term",
            CHART_2_GOS_SHORT_TERM_FTE_SERIES_KEY: "GOS short term",
        },
        "metrics": {
            "value_pct": {
                "label": "Full-time employment",
                "unit": "percent",
            },
        },
    },
    "details": {
        "year_semantics": {
            "display_year": "terminal_year_extracted_from_source_year_or_period_label",
        },
    },
}

CHART_3_METADATA = {
    "labels": {
        "metrics": {
            "gap_pp": {
                "label": "Employment gap",
                "unit": "percentage_point",
            },
            "lower_group_pct": {
                "label": "Lower group full-time employment",
                "unit": "percent",
            },
            "higher_group_pct": {
                "label": "Higher group full-time employment",
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
                "label": "Signed employment gap",
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
        "reference_group_rule": "group_with_lower_short_term_full_time_employment",
    },
}

CHART_5_METADATA = {
    "labels": {
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
        "fit_metrics": {
            CHART_6_WORK_FIT_METRIC_KEY: "Skills and education not fully utilised",
        },
    },
    "details": {
        "fit_metric": {
            "fit_metric_key": CHART_6_WORK_FIT_METRIC_KEY,
            "employment_source_key": GOS_L_6_SOURCE_KEY,
            "fit_metric_source_key": GOS_L_26_SOURCE_KEY,
            "fit_metric_direction": "lower_underutilisation_is_better",
            "fit_change_formula": (
                "short_term_underutilisation_pct - medium_term_underutilisation_pct"
            ),
            "fit_metric_source_columns": {
                "short_term_underutilisation_pct": (
                    CHART_6_SHORT_TERM_UNDERUTILISATION_COLUMN
                ),
                "medium_term_underutilisation_pct": (
                    CHART_6_MEDIUM_TERM_UNDERUTILISATION_COLUMN
                ),
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
                "label": "Signed employment gap",
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
        "reference_group_rule": "group_with_lower_short_term_full_time_employment",
    },
}
