import { CHART_7_VALUES } from "../core/config.js";
import { formatOneDecimal } from "../core/utils.js";

export function getChart7TimeWindowLabel(row, chartMetadata) {
    return chartMetadata.labels.time_windows[row["time_window"]];
}

export function getChart7FieldName(row) {
    if (row["reference_group"] === CHART_7_VALUES.fieldAverageGroup) {
        return row["comparison_group"];
    }

    return row["reference_group"];
}

export function getChart7GroupLabel(group, comparisonKind) {
    if (
        comparisonKind === "discipline" &&
        group === CHART_7_VALUES.fieldAverageGroup
    ) {
        return "All fields";
    }

    return group;
}

export function getChart7SelectorLabel(row, comparisonKind) {
    if (comparisonKind === "discipline") {
        return getChart7FieldName(row);
    }

    return row["subgroup_dimension"];
}

export function getChart7ComparisonLabel(row, comparisonKind) {
    if (comparisonKind === "discipline") {
        return `${getChart7FieldName(row)} compared with all fields`;
    }

    return row["reference_group"] + " vs " + row["comparison_group"];
}

function getChart7DisciplineGapSentence(row, gap) {
    const fieldName = getChart7FieldName(row);
    const gapSize = Math.abs(gap);

    if (gapSize <= CHART_7_VALUES.equalGapThreshold) {
        return `${fieldName} matched the overall undergraduate full-time employment rate`;
    }

    let fieldGap = -gap;

    if (row["reference_group"] === CHART_7_VALUES.fieldAverageGroup) {
        fieldGap = gap;
    }

    const formattedGap = formatOneDecimal(gapSize);
    let direction = fieldGap > 0 ? "above" : "below";

    return `${fieldName} was ${formattedGap} pp ${direction} the overall undergraduate full-time employment rate`;
}

function getChart7DemographicGapSentence(row, gap, comparisonKind) {
    const gapSize = Math.abs(gap);
    const referenceGroup = getChart7GroupLabel(row["reference_group"], comparisonKind);
    const comparisonGroup = getChart7GroupLabel(row["comparison_group"], comparisonKind);

    if (gapSize <= CHART_7_VALUES.equalGapThreshold) {
        return `${referenceGroup} and ${comparisonGroup} are about equal`;
    }

    const formattedGap = formatOneDecimal(gapSize);
    let higherGroup = referenceGroup;
    let lowerGroup = comparisonGroup;

    if (gap > 0) {
        higherGroup = comparisonGroup;
        lowerGroup = referenceGroup;
    }

    return `${higherGroup} is ${formattedGap} pp higher than ${lowerGroup}`;
}

export function getChart7GapSentence(row, comparisonKind) {
    const gap = Number(row["signed_gap_pp"]);

    if (comparisonKind === "discipline") {
        return getChart7DisciplineGapSentence(row, gap);
    } else {
        return getChart7DemographicGapSentence(row, gap, comparisonKind);
    }
}
