from __future__ import annotations


CHART_1A_METADATA = {
    "labels": {
        "dimensions": {
            "year": {
                "label": "Year",
            },
        },
        "metrics": {
            "bachelor_degree_or_above_holders_population": {
                "label": "Bachelor+ population",
                "unit": "people",
            },
            "bachelor_degree_or_above_holders_increase_pct": {
                "label": "Increase since 2016",
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
                "label": "Year",
            },
        },
        "series": {
            "gos_l_short_term_fte": "Matched cohort (GOS-L, 4–6 months)",
            "gos_l_medium_term_fte": "Matched cohort (GOS-L, 3–4 years)",
            "gos_short_term_fte": "Recent graduates (GOS, 4–6 months)",
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
                "label": "2024 short-term FTE gap",
                "unit": "percentage_point",
            },
            "lower_group_pct": {
                "label": "2024 short-term FTE",
                "unit": "percent",
            },
            "higher_group_pct": {
                "label": "2024 short-term FTE",
                "unit": "percent",
            },
        },
    },
}

CHART_4_METADATA = {
    "labels": {
        "time_windows": {
            "short_term": "short-term",
            "medium_term": "medium-term",
        },
        "metrics": {
            "signed_gap_pp": {
                "label": "FTE gap",
                "unit": "percentage_point",
            },
            "reference_group_pct": {
                "label": "full-time employed",
                "unit": "percent",
            },
            "comparison_group_pct": {
                "label": "full-time employed",
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
                "label": "4–6 months FTE",
                "unit": "percent",
            },
            "medium_term_fte_pct": {
                "label": "3–4 years FTE",
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
            "skills_education_utilisation": "Skills and education not fully utilised",
        },
        "metrics": {
            "fte_gain_pp": {
                "label": "FTE gain",
                "unit": "percentage_point",
            },
            "underutilisation_reduction_pp": {
                "label": "Work fit improvement",
                "unit": "percentage_point",
            },
        },
    },
}

CHART_7_METADATA = {
    "labels": {
        "time_windows": {
            "short_term": "4–6 months",
            "medium_term": "3–4 years",
        },
        "metrics": {
            "signed_gap_pp": {
                "label": "FTE gap",
                "unit": "percentage_point",
            },
            "reference_group_pct": {
                "label": "full-time employed",
                "unit": "percent",
            },
            "comparison_group_pct": {
                "label": "full-time employed",
                "unit": "percent",
            },
        },
    },
    "details": {
        "signed_gap_direction": "comparison_group_pct - reference_group_pct",
    },
}
