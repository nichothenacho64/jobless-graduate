from __future__ import annotations

TOTAL_ROW_GROUP = "Total"

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

CHART_1_ID = "chart_1_transition_window"
CHART_2_ID = "chart_2_subgroup_bottleneck"
CHART_3_ID = "chart_3_gap_shapes"
CHART_4_ID = "chart_4_field_conversion"
CHART_5_ID = "chart_5_work_fit"
CHART_6A_ID = "chart_6a_sew_skill_by_age"
CHART_6B_ID = "chart_6b_sew_degree_supply"
CHART_7_ID = "chart_7_subgroup_comparator"

CHART_TABLE_SCHEMAS = {
    CHART_1_ID: [
        "year",
        "series_key",
        "value_pct",
        "source_key",
    ],
    CHART_2_ID: [
        "subgroup_dimension",
        "gap_pp",
        "lower_group",
        "lower_group_pct",
        "higher_group",
        "higher_group_pct",
        "source_key",
        "sort_order",
    ],
    CHART_3_ID: [
        "comparison_id",
        "subgroup_dimension",
        "comparison_label",
        "time_window",
        "time_window_order",
        "lower_group",
        "lower_group_pct",
        "higher_group",
        "higher_group_pct",
        "gap_pp",
        "source_key",
        "sort_order",
    ],
    CHART_4_ID: [
        "study_area",
        "short_term_fte_pct",
        "medium_term_fte_pct",
        "source_key",
    ],
    CHART_5_ID: [
        "study_area",
        "fte_gain_pp",
        "fit_change_pp",
        "fit_metric_key",
        "employment_source_key",
        "fit_source_key",
    ],
    CHART_6A_ID: [
        "age_group",
        "age_order",
        "skill_level",
        "skill_order",
        "share_pct",
        "source_key",
    ],
    CHART_6B_ID: [
        "year",
        "index_2016_100",
        "source_key",
    ],
    CHART_7_ID: [
        "selector_id",
        "selector_label",
        "subgroup_dimension",
        "comparison_label",
        "group_role",
        "group_label",
        "time_window",
        "time_window_order",
        "value_pct",
        "source_key",
        "sort_order",
    ],
}

CHART_1_TABLE_COLUMNS = CHART_TABLE_SCHEMAS[CHART_1_ID]
CHART_2_TABLE_COLUMNS = CHART_TABLE_SCHEMAS[CHART_2_ID]
CHART_3_TABLE_COLUMNS = CHART_TABLE_SCHEMAS[CHART_3_ID]
CHART_4_TABLE_COLUMNS = CHART_TABLE_SCHEMAS[CHART_4_ID]
CHART_5_TABLE_COLUMNS = CHART_TABLE_SCHEMAS[CHART_5_ID]
CHART_6A_TABLE_COLUMNS = CHART_TABLE_SCHEMAS[CHART_6A_ID]
CHART_6B_TABLE_COLUMNS = CHART_TABLE_SCHEMAS[CHART_6B_ID]
CHART_7_TABLE_COLUMNS = CHART_TABLE_SCHEMAS[CHART_7_ID]

CHART_1_GOS_L_SHORT_TERM_FTE_SERIES_KEY = "gos_l_short_term_fte"
CHART_1_GOS_L_MEDIUM_TERM_FTE_SERIES_KEY = "gos_l_medium_term_fte"
CHART_1_GOS_SHORT_TERM_FTE_SERIES_KEY = "gos_short_term_fte"

CHART_1_SERIES_ORDER = {
    CHART_1_GOS_L_SHORT_TERM_FTE_SERIES_KEY: 0,
    CHART_1_GOS_L_MEDIUM_TERM_FTE_SERIES_KEY: 1,
    CHART_1_GOS_SHORT_TERM_FTE_SERIES_KEY: 2,
}

GOS_5_SOURCE_KEY = "gos_5"
GOS_8_SOURCE_KEY = "gos_8"
GOS_21_SOURCE_KEY = "gos_21"
GOS_L_1_SOURCE_KEY = "gos_l_1"
GOS_L_6_SOURCE_KEY = "gos_l_6"
GOS_L_26_SOURCE_KEY = "gos_l_26"
GOS_L_160_SOURCE_KEY = "gos_l_160"
SEW_32_SOURCE_KEY = "sew_32"
SEW_35_SOURCE_KEY = "sew_35"
SEW_DEGREE_SUPPLY_BASE_YEAR = 2016

SHORT_TERM_TIME_WINDOW = "short_term"
MEDIUM_TERM_TIME_WINDOW = "medium_term"
CHART_7_LOWER_GROUP_ROLE = "lower_reference"
CHART_7_HIGHER_GROUP_ROLE = "higher_reference"

CHART_5_WORK_FIT_METRIC_KEY = "skills_education_utilisation"

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

CHART_METADATA_FILE_NAME = "chart_metadata.json"

CHART_OUTPUT_FILENAMES = {
    CHART_1_ID: "chart_1_transition_window.csv",
    CHART_2_ID: "chart_2_subgroup_bottleneck.csv",
    CHART_3_ID: "chart_3_gap_shapes.csv",
    CHART_4_ID: "chart_4_field_conversion.csv",
    CHART_5_ID: "chart_5_work_fit.csv",
    CHART_6A_ID: "chart_6a_sew_skill_by_age.csv",
    CHART_6B_ID: "chart_6b_sew_degree_supply.csv",
    CHART_7_ID: "chart_7_subgroup_comparator.csv",
}

CHART_SOURCE_KEY_COLUMNS = (
    "source_key",
    "employment_source_key",
    "fit_source_key",
)
