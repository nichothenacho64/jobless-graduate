from __future__ import annotations

TOTAL_ROW_GROUP = "Total"

GOS_SOURCE_LABEL = "GOS"
GOS_L_SOURCE_LABEL = "GOS-L"

GOS_AGGREGATE_SHORT_TERM_COMPARISON_COLUMNS = {
    "short_term_full_time_employment": "full_time_employment",
    "short_term_overall_employment": "overall_employment",
    "short_term_labour_force_participation": "labour_force_participation_rate",
}

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
