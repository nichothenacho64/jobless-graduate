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


# Chart-specific constants
CHART_1A_CONSTANTS = {
    "table_columns": [
        "year",
        "bachelor_degree_or_above_holders_population",
        "bachelor_degree_or_above_holders_increase_pct",
        "source_key",
    ],
    "source_table_number": 35,
    "qualification_filter": (
        "highest non-school qualification at bachelor degree level or above"
    ),
    "population_group": "Persons",
    "row_label": "Total",
    "base_year": 2016,
    "years": tuple(range(2016, 2026)),
}

CHART_1B_CONSTANTS = {
    "table_columns": [
        "age_group",
        "age_order",
        "skill_level",
        "skill_order",
        "share_pct",
        "source_key",
    ],
}

CHART_2_CONSTANTS = {
    "table_columns": [
        "display_year",
        "series_key",
        "value_pct",
        "source_key",
        "series_order",
    ],
    "series_keys": {
        "gos_l_short_term": "gos_l_short_term_fte",
        "gos_l_medium_term": "gos_l_medium_term_fte",
        "gos_short_term": "gos_short_term_fte",
    },
    "series_order": {
        "gos_l_short_term_fte": 0,
        "gos_l_medium_term_fte": 1,
        "gos_short_term_fte": 2,
    },
}

CHART_3_CONSTANTS = {
    "table_columns": [
        "subgroup_dimension",
        "gap_pp",
        "lower_group",
        "lower_group_pct",
        "higher_group",
        "higher_group_pct",
        "source_key",
        "sort_order",
    ],
}

CHART_4_CONSTANTS = {
    "table_columns": [
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

CHART_5_CONSTANTS = {
    "table_columns": [
        "study_area",
        "short_term_fte_pct",
        "medium_term_fte_pct",
        "source_key",
    ],
    "excluded_study_areas": {"Standard deviation", "Total"},
}

CHART_6_CONSTANTS = {
    "table_columns": [
        "study_area",
        "fte_gain_pp",
        "underutilisation_reduction_pp",
        "fit_metric_key",
        "employment_source_key",
        "fit_source_key",
    ],
    "work_fit_metric_key": "skills_education_utilisation",
    "underutilisation_columns": {
        "short_term": (
            "extent_to_which_skills_and_education_not_fully_utilised_short_term_fte"
        ),
        "medium_term": (
            "extent_to_which_skills_and_education_not_fully_utilised_medium_term_fte"
        ),
    },
    "excluded_study_areas": {"Total"},
}

CHART_7_CONSTANTS = {
    "table_columns": [
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
