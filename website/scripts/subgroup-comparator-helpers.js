import {
    CHART_RANGES,
    CHART_7_TEXT,
    CHART_7_RENDERING,
    CHART_7_VALUES,
    CHART_TITLES,
    DUMBBELL_LINE,
    MARKER_SIZE,
    THEME_COLOURS
} from "./config.js";
import { getComparisonLabel, getGapSentence } from "./chart-helpers.js";
import { getAxisLabel } from "./data.js";
import { createReferenceLine, renderChart } from "./rendering.js";
import { formatOneDecimal, sortByKeyAscending } from "./utils.js";

function getChart7TimeWindowLabel(row, chartMetadata) {
    return chartMetadata.labels.time_windows[row["time_window"]];
}

function createChart7Trace(selectedRows, chartMetadata, gapPattern) {
    const xValues = [];
    const yValues = [];
    const customData = [];
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
            row["subgroup_dimension"],
            row["time_window"].replace("_", "-"),
            getGapSentence(row),
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
        hovertemplate: `<b>%{customdata[0]} (%{customdata[1]} gap)</b><br>` +
            `%{customdata[2]}<br>` +
            `%{customdata[3]}: %{customdata[4]:.1f}% ${referenceLabel}<br>` +
            `%{customdata[5]}: %{customdata[6]:.1f}% ${comparisonLabel}` +
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
        // title: { text: CHART_TITLES.chart7 },
        height: CHART_7_RENDERING.dimensions.height,
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
            l: CHART_7_RENDERING.dimensions.leftMargin,
            r: CHART_7_RENDERING.dimensions.rightMargin,
            t: CHART_7_RENDERING.dimensions.topMargin,
            b: CHART_7_RENDERING.dimensions.bottomMargin
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
    valueElement.textContent = value;

    row.append(labelElement, valueElement);
    cardList.appendChild(row);
}

function getChart7SentenceGroupLabel(label) {
    if (label === "Other") {
        return "other";
    }

    return label;
}

function getChart7PanelGapSentence(row) {
    const gap = Number(row["signed_gap_pp"]);
    const absoluteGap = Math.abs(gap);
    const referenceGroup = getChart7SentenceGroupLabel(row["reference_group"]);
    const comparisonGroup = getChart7SentenceGroupLabel(row["comparison_group"]);

    if (absoluteGap <= 0.1) {
        return `${referenceGroup} and ${comparisonGroup} are about equal`;
    }

    const formattedGap = formatOneDecimal(absoluteGap);

    if (gap > 0) {
        return `${comparisonGroup} is ${formattedGap} pp higher than ${referenceGroup}`;
    }

    return `${referenceGroup} is ${formattedGap} pp higher than ${comparisonGroup}`;
}

function appendChart7PeriodSummary(cardBody, leadText, row, suffixText = "") {
    const sentenceText = `${leadText}, ${getChart7PanelGapSentence(row)}${suffixText}.`;

    const sentence = document.createElement("p");
    sentence.className = "mb-1";
    sentence.textContent = sentenceText;

    const values = document.createElement("dl");
    values.className = "mb-3";

    appendChart7CardValue(
        values,
        row["reference_group"],
        `${formatOneDecimal(row["reference_group_pct"])}%`
    );
    appendChart7CardValue(
        values,
        row["comparison_group"],
        `${formatOneDecimal(row["comparison_group_pct"])}%`
    );

    cardBody.append(sentence, values);
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
        subgroupDimension: selectedRows[0]["subgroup_dimension"],
        referenceGroup: selectedRows[0]["reference_group"],
        comparisonGroup: selectedRows[0]["comparison_group"],
        shortTermGap,
        mediumTermGap,
        change: mediumTermGap - shortTermGap
    };
}

export function getChart7GapPattern(gapSummary) {
    const shortTermGapSize = Math.abs(gapSummary.shortTermGap);
    const mediumTermGapSize = Math.abs(gapSummary.mediumTermGap);

    const nearZeroGap = CHART_7_VALUES.gapPatternThresholds.nearZero;
    const meaningfulGap = CHART_7_VALUES.gapPatternThresholds.meaningful;
    
    const substantialShrinkRatio = CHART_7_VALUES.gapPatternThresholds.substantialShrinkRatio;
    const signChanged = gapSummary.shortTermGap * gapSummary.mediumTermGap < 0;
    const substantiallyShrunk = mediumTermGapSize <= shortTermGapSize * substantialShrinkRatio;

    if (shortTermGapSize <= nearZeroGap && mediumTermGapSize <= nearZeroGap) {
        return CHART_7_VALUES.gapPatterns.smallThroughout;
    } else if (signChanged) {
        return CHART_7_VALUES.gapPatterns.reverses;
    } else if (mediumTermGapSize <= nearZeroGap) {
        return CHART_7_VALUES.gapPatterns.mostlyCloses;
    } else if (mediumTermGapSize >= meaningfulGap && !substantiallyShrunk) {
        return CHART_7_VALUES.gapPatterns.persists;
    }

    return CHART_7_VALUES.gapPatterns.mostlyCloses;
}

export function getChart7SignCaption(chartMetadata) {
    const signedGapDirection = chartMetadata.details.signed_gap_direction;

    if (signedGapDirection === CHART_7_VALUES.signDirections.comparisonMinusReference) {
        return CHART_7_TEXT.signCaptions.comparisonMinusReference;
    } else if (signedGapDirection === CHART_7_VALUES.signDirections.referenceMinusComparison) {
        return CHART_7_TEXT.signCaptions.referenceMinusComparison;
    }

    return CHART_7_TEXT.signCaptions.referenceMinusComparison; // shouldn't get here
}

export function updateChart7ExplanationCard(explanationCard, selectedRows, gapSummary, gapPattern) {
    explanationCard.replaceChildren();

    const cardBody = document.createElement("div");
    cardBody.className = "card-body";

    const title = document.createElement("p");
    title.className = "fw-semibold mb-3";
    title.textContent = `${gapSummary.subgroupDimension}: ` +
        `${gapSummary.referenceGroup} vs ${gapSummary.comparisonGroup}`;

    const sentence = document.createElement("p");
    sentence.className = "mb-0";
    sentence.textContent = gapPattern.sentence;

    cardBody.appendChild(title);
    appendChart7PeriodSummary(cardBody, "4-6 months after graduation", selectedRows[0], " in full-time employment");
    appendChart7PeriodSummary(cardBody, "3 years later", selectedRows[1]);
    cardBody.appendChild(sentence);
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
    const trace = createChart7Trace(selectedRows, chartMetadata, gapPattern);
    const layout = createChart7Layout(selectedRows, chartMetadata, CHART_RANGES.chart7.y);

    updateChart7ExplanationCard(explanationCard, selectedRows, gapSummary, gapPattern);
    renderChart(chartId, [trace], layout);
}
