import { CHART_7_GAPS, CHART_7_VALUES } from "../core/config.js";
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
        return CHART_7_VALUES.fieldAverageShortLabel;
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

export function getChart7FieldGap(row) {
    const gap = Number(row["signed_gap_pp"]);

    if (row["reference_group"] === CHART_7_VALUES.fieldAverageGroup) {
        return gap;
    }

    return -gap;
}

function getChart7GapSentenceGroups(row, comparisonKind) {
    if (comparisonKind === "discipline") {
        return {
            referenceGroup: getChart7GroupLabel(CHART_7_VALUES.fieldAverageGroup, comparisonKind),
            comparisonGroup: getChart7FieldName(row)
        };
    } else {
        return {
            referenceGroup: getChart7GroupLabel(row["reference_group"], comparisonKind),
            comparisonGroup: getChart7GroupLabel(row["comparison_group"], comparisonKind)
        };
    }
}

function getChart7GapSentenceText(referenceGroup, comparisonGroup, gap) {
    const gapSize = Math.abs(gap);

    if (gapSize <= CHART_7_GAPS.thresholds.equal) {
        return `${referenceGroup} and ${comparisonGroup} are about equal`;
    }

    const formattedGap = formatOneDecimal(gapSize);
    let higherGroup = referenceGroup;
    let lowerGroup = comparisonGroup;

    if (gap > 0) {
        higherGroup = comparisonGroup;
        lowerGroup = referenceGroup;
    }

    if (higherGroup === CHART_7_VALUES.fieldAverageShortLabel) {
        return `${higherGroup} are ${formattedGap} pp higher than ${lowerGroup}`;
    }

    return `${higherGroup} is ${formattedGap} pp higher than ${lowerGroup}`;
}

export function getChart7GapSentence(row, comparisonKind) {
    let gap = Number(row["signed_gap_pp"]);

    if (comparisonKind === "discipline") {
        gap = getChart7FieldGap(row);
    }

    const gapGroups = getChart7GapSentenceGroups(row, comparisonKind);
    return getChart7GapSentenceText(
        gapGroups.referenceGroup,
        gapGroups.comparisonGroup,
        gap
    );
}

export function getChart7DisciplineSummarySentence(gapSummary) {
    const fieldName = gapSummary.selectorLabel;
    const shortTermGap = gapSummary.shortTermGap;
    const mediumTermGap = gapSummary.mediumTermGap;
    const shortTermGapSize = Math.abs(shortTermGap);
    const mediumTermGapSize = Math.abs(mediumTermGap);
    const smallThroughoutGap = CHART_7_GAPS.thresholds.smallThroughout;
    const sentences = CHART_7_GAPS.discipline.sentences;

    if (
        shortTermGapSize <= smallThroughoutGap &&
        mediumTermGapSize <= smallThroughoutGap
    ) {
        return sentences.smallThroughout;
    } else if (shortTermGap < 0 && mediumTermGap > smallThroughoutGap) {
        return sentences.belowThenAhead;
    } else if (shortTermGap < 0 && mediumTermGap >= -smallThroughoutGap) {
        return sentences.belowThenClose;
    } else if (shortTermGap > 0 && mediumTermGap < -smallThroughoutGap) {
        return sentences.aboveThenBelow;
    } else if (shortTermGap > 0 && mediumTermGap <= smallThroughoutGap) {
        return sentences.aboveThenClose;
    } else if (shortTermGap > 0 && mediumTermGap > 0) {
        if (mediumTermGapSize < shortTermGapSize) {
            return `${fieldName}'s ${sentences.leadNarrows}`;
        } else {
            return `${fieldName} ${sentences.leadPersists}`;
        }
    } else if (shortTermGap < 0 && mediumTermGap < 0) {
        if (mediumTermGapSize < shortTermGapSize) {
            return sentences.belowNarrows;
        } else {
            return sentences.belowPersists;
        }
    }

    return sentences.differenceRemains;
}
