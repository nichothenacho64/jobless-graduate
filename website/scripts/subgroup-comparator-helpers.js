import {
    CHART_7_CARD_LABELS,
    CHART_7_DIMENSIONS,
    CHART_7_GAP_PATTERNS,
    CHART_7_GAP_PATTERN_THRESHOLDS,
    CHART_7_SIGN_CAPTIONS,
    CHART_7_SIGN_DIRECTIONS,
    CHART_7_Y_AXIS_PADDING,
    CHART_TITLES,
    DUMBBELL_LINE,
    MARKER_SIZE,
    THEME_COLOURS
} from "./config.js";
import { getComparisonLabel } from "./chart-helpers.js";
import { getAxisLabel, getAxisValues } from "./data.js";
import { createReferenceLine, renderChart } from "./rendering.js";
import { sortByKeyAscending } from "./utils.js";

function getChart7TimeWindowLabel(row, chartMetadata) {
    return chartMetadata.labels.time_windows[row["time_window"]];
}

function createChart7Trace(selectedRows, chartMetadata, gapPattern) {
    const xValues = [];
    const yValues = [];
    const customData = [];
    const gapLabel = getAxisLabel(chartMetadata, "signed_gap_pp");
    const referenceLabel = getAxisLabel(chartMetadata, "reference_group_pct");
    const comparisonLabel = getAxisLabel(chartMetadata, "comparison_group_pct");

    const line = {
        color: gapPattern.colour,
        width: DUMBBELL_LINE.width
    };

    if (gapPattern.dash) {
        line.dash = gapPattern.dash;
    }

    for (let row of selectedRows) {
        const timeWindowLabel = getChart7TimeWindowLabel(row, chartMetadata);
        xValues.push(timeWindowLabel);
        yValues.push(row["signed_gap_pp"]);
        customData.push([
            row["reference_group"],
            row["reference_group_pct"],
            row["comparison_group"],
            row["comparison_group_pct"]
        ]);
    }

    return {
        x: xValues,
        y: yValues,
        customdata: customData,
        name: selectedRows[0]["subgroup_dimension"],
        type: "scatter",
        mode: "lines+markers",
        showlegend: false,
        line,
        marker: {
            size: MARKER_SIZE.large,
            color: gapPattern.colour,
        },
        hovertemplate: `<b>%{x}: ${gapLabel} %{y:.1f} pp</b><br>` +
            `${referenceLabel} (%{customdata[0]}): %{customdata[1]:.1f}%<br>` +
            `${comparisonLabel} (%{customdata[2]}): %{customdata[3]:.1f}%` +
            `<extra></extra>`
    };
}

function createChart7Layout(selectedRows, chartMetadata, yAxisRange) {
    const xValues = [];
    const yAxisLine = createReferenceLine("y", 0, THEME_COLOURS.text, 2, "above");

    for (let row of selectedRows) {
        const timeWindowLabel = getChart7TimeWindowLabel(row, chartMetadata);
        xValues.push(timeWindowLabel);
    }

    return {
        title: { text: CHART_TITLES.chart7 },
        height: CHART_7_DIMENSIONS.height,
        showlegend: false,
        xaxis: {
            categoryorder: "array",
            categoryarray: xValues,
            showgrid: false,
            fixedrange: true
        },
        yaxis: {
            title: { text: getAxisLabel(chartMetadata, "signed_gap_pp", true) },
            range: yAxisRange,
            zeroline: false,
            fixedrange: true
        },
        shapes: [yAxisLine],
        margin: {
            l: CHART_7_DIMENSIONS.leftMargin,
            r: CHART_7_DIMENSIONS.rightMargin,
            t: CHART_7_DIMENSIONS.topMargin,
            b: CHART_7_DIMENSIONS.bottomMargin
        }
    };
}

function appendChart7CardValue(cardList, label, value) {
    const row = document.createElement("div");
    row.className = "d-flex justify-content-between gap-3 mb-1";

    const labelElement = document.createElement("dt");
    labelElement.className = "mb-0";
    labelElement.textContent = label;

    const valueElement = document.createElement("dd");
    valueElement.className = "mb-0";
    valueElement.textContent = `${value.toFixed(1)} pp`;

    row.append(labelElement, valueElement);
    cardList.appendChild(row);
}

export function getChart7Selectors(chartData) {
    const selectors = [];
    const selectorIds = new Set();

    for (let row of chartData) {
        const selectorId = row["selector_id"];

        if (!selectorIds.has(selectorId)) {
            let selectorLabel = row["selector_label"];

            if (!selectorLabel) {
                selectorLabel = row["subgroup_dimension"] + ": " + getComparisonLabel(row);
            }

            selectors.push({
                selectorId,
                label: selectorLabel,
                sortOrder: row["sort_order"]
            });
            selectorIds.add(selectorId);
        }
    }

    sortByKeyAscending(selectors, "sortOrder");

    return selectors;
}

export function createChart7DropdownItems(dropdownMenu, selectors) {
    dropdownMenu.replaceChildren();

    for (let selector of selectors) {
        const listItem = document.createElement("li");
        const dropdownItem = document.createElement("button");

        dropdownItem.className = "dropdown-item";
        dropdownItem.type = "button";
        dropdownItem.dataset.selectorId = selector.selectorId;
        dropdownItem.textContent = selector.label;

        listItem.appendChild(dropdownItem);
        dropdownMenu.appendChild(listItem);
    }
}

export function updateChart7DropdownSelection(dropdownButton, dropdownMenu, selectors, selectorId) {
    let selectedSelector = selectors[0];

    for (let selector of selectors) {
        if (selector.selectorId === selectorId) {
            selectedSelector = selector;
        }
    }

    dropdownButton.textContent = selectedSelector.label;

    for (let dropdownItem of dropdownMenu.querySelectorAll(".dropdown-item")) {
        const selectedItem = dropdownItem.dataset.selectorId === selectedSelector.selectorId;
        dropdownItem.classList.toggle("active", selectedItem);
    }

    return selectedSelector.selectorId;
}

export function getChart7SelectedRows(chartData, selectorId) {
    const selectedRows = [];

    for (let row of chartData) {
        if (row["selector_id"] === selectorId) {
            selectedRows.push(row);
        }
    }

    sortByKeyAscending(selectedRows, "time_window_order");

    return selectedRows;
}

export function getChart7GapSummary(selectedRows) {
    const shortTermGap = selectedRows[0]["signed_gap_pp"];
    const mediumTermGap = selectedRows[1]["signed_gap_pp"];

    return {
        shortTermGap,
        mediumTermGap,
        change: mediumTermGap - shortTermGap
    };
}

export function getChart7GapPattern(gapSummary) {
    const shortTermGapSize = Math.abs(gapSummary.shortTermGap);
    const mediumTermGapSize = Math.abs(gapSummary.mediumTermGap);
    const nearZeroGap = CHART_7_GAP_PATTERN_THRESHOLDS.nearZero;
    const meaningfulGap = CHART_7_GAP_PATTERN_THRESHOLDS.meaningful;
    const substantialShrinkRatio = CHART_7_GAP_PATTERN_THRESHOLDS.substantialShrinkRatio;
    const signChanged = gapSummary.shortTermGap * gapSummary.mediumTermGap < 0;
    const substantiallyShrunk = mediumTermGapSize <= shortTermGapSize * substantialShrinkRatio;

    if (shortTermGapSize <= nearZeroGap && mediumTermGapSize <= nearZeroGap) {
        return CHART_7_GAP_PATTERNS.smallThroughout;
    } else if (signChanged) {
        return CHART_7_GAP_PATTERNS.reverses;
    } else if (mediumTermGapSize <= nearZeroGap) {
        return CHART_7_GAP_PATTERNS.mostlyCloses;
    } else if (mediumTermGapSize >= meaningfulGap && !substantiallyShrunk) {
        return CHART_7_GAP_PATTERNS.persists;
    }

    return CHART_7_GAP_PATTERNS.mostlyCloses;
}

export function getChart7YAxisRange(chartData) {
    const gapValues = getAxisValues(chartData, "signed_gap_pp");
    const minGap = Math.min(0, ...gapValues);
    const maxGap = Math.max(0, ...gapValues);

    return [
        minGap - CHART_7_Y_AXIS_PADDING.lower,
        maxGap + CHART_7_Y_AXIS_PADDING.upper
    ];
}

export function getChart7SignCaption(chartMetadata) {
    const signedGapDirection = chartMetadata.details.signed_gap_direction;

    if (signedGapDirection === CHART_7_SIGN_DIRECTIONS.comparisonMinusReference) {
        return CHART_7_SIGN_CAPTIONS.comparisonMinusReference;
    } else if (signedGapDirection === CHART_7_SIGN_DIRECTIONS.referenceMinusComparison) {
        return CHART_7_SIGN_CAPTIONS.referenceMinusComparison;
    }

    return CHART_7_SIGN_CAPTIONS.referenceMinusComparison; // shouldn't get here
}

export function updateChart7ExplanationCard(explanationCard, gapSummary, gapPattern, signCaption) {
    explanationCard.replaceChildren();

    const cardBody = document.createElement("div");
    cardBody.className = "card-body";

    const cardList = document.createElement("dl");
    cardList.className = "mb-0";

    appendChart7CardValue(cardList, CHART_7_CARD_LABELS.shortTermGap, gapSummary.shortTermGap);
    appendChart7CardValue(cardList, CHART_7_CARD_LABELS.mediumTermGap, gapSummary.mediumTermGap);
    appendChart7CardValue(cardList, CHART_7_CARD_LABELS.change, gapSummary.change);

    const sentence = document.createElement("p");
    sentence.className = "mt-3 mb-0";
    sentence.textContent = gapPattern.sentence;

    const caption = document.createElement("p");
    caption.className = "chart-7-caption small mt-3 mb-0";
    caption.textContent = signCaption;

    cardBody.append(cardList, sentence, caption);
    explanationCard.appendChild(cardBody);
}

export function renderChart7SelectedComparison(
    chartId,
    chartData,
    chartMetadata,
    selectorId,
    explanationCard
) {
    const selectedRows = getChart7SelectedRows(chartData, selectorId);
    const gapSummary = getChart7GapSummary(selectedRows);
    const gapPattern = getChart7GapPattern(gapSummary);
    const yAxisRange = getChart7YAxisRange(chartData);
    const signCaption = getChart7SignCaption(chartMetadata);
    const trace = createChart7Trace(selectedRows, chartMetadata, gapPattern);
    const layout = createChart7Layout(selectedRows, chartMetadata, yAxisRange);

    updateChart7ExplanationCard(explanationCard, gapSummary, gapPattern, signCaption);
    renderChart(chartId, [trace], layout);
}
