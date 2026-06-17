import { CHART_7_VALUES } from "../core/config.js";
import { getChart7FieldName, getChart7SelectorLabel } from "./labels.js";

export function getChart7DemographicSelectors(chartData) {
    const selectors = [];
    const selectorIds = new Set();

    for (let row of chartData) {
        const selectorId = row["selector_id"];
        const label = getChart7SelectorLabel(row, "demographic");

        if (!selectorIds.has(selectorId)) {
            selectors.push({selectorId, label});
            selectorIds.add(selectorId);
        }
    }

    return selectors;
}

export function getChart7DisciplineSelectors(chartData, disciplineFamily) {
    const selectors = [];
    const studyAreas = CHART_7_VALUES.disciplineFamilies[disciplineFamily] ?? [];

    for (let studyArea of studyAreas) {
        for (let row of chartData) {
            if (row["time_window_order"] !== 0) continue;
            if (getChart7FieldName(row) !== studyArea) continue;

            const selectorId = row["selector_id"];
            const label = getChart7SelectorLabel(row, "discipline");

            selectors.push({ selectorId, label });
            break;
        }
    }

    return selectors;
}
