from __future__ import annotations

import pandas as pd
from matplotlib.figure import Figure

from src.charts.subgroup_comparison import (
    create_subgroup_change_heatmap,
    create_subgroup_gap_width_chart,
    create_subgroup_levels_chart,
)
from src.transform.subgroup_comparison import (
    build_subgroup_chart_table,
    build_subgroup_gap_summary_table,
    load_subgroup_comparison_table,
)

def build_subgroup_comparison_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    comparison_table = load_subgroup_comparison_table()
    chart_table = build_subgroup_chart_table(comparison_table)
    gap_summary_table = build_subgroup_gap_summary_table(chart_table)
    return comparison_table, chart_table, gap_summary_table

def build_subgroup_comparison_figures() -> tuple[Figure, Figure, Figure]:
    _, chart_table, gap_summary_table = build_subgroup_comparison_tables()
    return (
        create_subgroup_levels_chart(chart_table),
        create_subgroup_change_heatmap(chart_table),
        create_subgroup_gap_width_chart(gap_summary_table),
    )
