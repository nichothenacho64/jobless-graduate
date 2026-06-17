import {
    CHART_RANGES,
    CHART_7_VALUES,
    DUMBBELL_LINE,
    MARKER_SIZE,
    THEME_COLOURS
} from "../core/config.js";
import { getAxisLabel, getTrace } from "../core/data.js";
import { formatOneDecimal, sortByKeyAscending } from "../core/utils.js";
import { createReferenceLine, renderChart } from "../plotly/rendering.js";
import { createChart7DropdownItems, updateChart7DropdownSelection } from "./dropdowns.js";
import {
    getChart7ComparisonLabel,
    getChart7GapSentence,
    getChart7GroupLabel,
    getChart7SelectorLabel,
    getChart7TimeWindowLabel
} from "./labels.js";
import {
    getChart7DemographicSelectors,
    getChart7DisciplineSelectors
} from "./selectors.js";

function createChart7Trace(selectedRows, chartMetadata, gapSummary, gapPattern, comparisonKind) {
    const xValues = [];
    const yValues = [];
    const customData = [];
    const referenceLabel = getAxisLabel(chartMetadata, "reference_group_pct");
    const comparisonLabel = getAxisLabel(chartMetadata, "comparison_group_pct");
    const comparisonReverses = gapSummary.shortTermGap * gapSummary.mediumTermGap < 0;

    const line = {
        color: gapPattern.colour,
        width: DUMBBELL_LINE.default.width
    };

    if (comparisonReverses) {
        line.dash = CHART_7_VALUES.gapPatterns.reverses.dash;
    }

    for (let row of selectedRows) {
        const timeWindowLabel = getChart7TimeWindowLabel(row, chartMetadata);
        xValues.push(timeWindowLabel);
        yValues.push(row["signed_gap_pp"]);
        customData.push([
            getChart7SelectorLabel(row, comparisonKind),
            row["time_window"].replace("_", "-"),
            getChart7GapSentence(row, comparisonKind),
            getChart7GroupLabel(row["reference_group"], comparisonKind),
            row["reference_group_pct"],
            getChart7GroupLabel(row["comparison_group"], comparisonKind),
            row["comparison_group_pct"]
        ]);
    }

    return {
        x: xValues,
        y: yValues,
        customdata: customData,
        name: gapSummary.selectorLabel,
        type: "scatter",
        mode: "lines+markers",
        showlegend: false,
        line,
        marker: {
            size: MARKER_SIZE.large,
            color: gapPattern.colour,
        },
        hovertemplate: `<b>%{customdata[0]} (%{customdata[1]} gap)</b><br>` +
            `<i>%{customdata[2]}</i><br>` +
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
        height: 360,
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
            l: 70,
            r: 20,
            t: 60,
            b: 50
        }
    };
}

function appendChart7CardValue(cardList, label, value) {
    const row = document.createElement("div");
    row.className = "mb-1";

    const labelElement = document.createElement("dt");
    labelElement.className = "d-inline mb-0";
    labelElement.textContent = `${label}: `;

    const valueElement = document.createElement("dd");
    valueElement.className = "d-inline mb-0";
    valueElement.textContent = value;

    row.append(labelElement, valueElement);
    cardList.appendChild(row);
}

function appendChart7PeriodSummary(cardBody, leadText, row, comparisonKind) {
    const sentence = document.createElement("p");
    sentence.className = "mb-1";

    const values = document.createElement("dl");
    values.className = "mb-3";

    if (comparisonKind === "discipline") {
        sentence.textContent = `${leadText}, ${getChart7GapSentence(row, comparisonKind)}.`;
    } else {
        sentence.textContent = `${leadText}, ${getChart7GapSentence(row, comparisonKind)} in full-time employment.`;
    }

    const referenceGroupPercentage = formatOneDecimal(row["reference_group_pct"]);
    const comparisonGroupPercentage = formatOneDecimal(row["comparison_group_pct"]);

    const referenceGroupLabel = getChart7GroupLabel(row["reference_group"], comparisonKind);
    const comparisonGroupLabel = getChart7GroupLabel(row["comparison_group"], comparisonKind);

    appendChart7CardValue(values, referenceGroupLabel, `${referenceGroupPercentage}%`);
    appendChart7CardValue(values, comparisonGroupLabel, `${comparisonGroupPercentage}%`);

    cardBody.append(sentence, values);
}

function getChart7GapSummary(selectedRows, comparisonKind) {
    const shortTermGap = selectedRows[0]["signed_gap_pp"];
    const mediumTermGap = selectedRows[1]["signed_gap_pp"];

    return {
        selectorLabel: getChart7SelectorLabel(selectedRows[0], comparisonKind),
        subgroupDimension: selectedRows[0]["subgroup_dimension"],
        shortTermGap,
        mediumTermGap
    };
}

function getChart7GapPattern(gapSummary) {
    const shortTermGapSize = Math.abs(gapSummary.shortTermGap);
    const mediumTermGapSize = Math.abs(gapSummary.mediumTermGap);

    const nearZeroGap = CHART_7_VALUES.gapPatternThresholds.nearZero;
    const smallThroughoutGap = CHART_7_VALUES.gapPatternThresholds.smallThroughout;
    const meaningfulGap = CHART_7_VALUES.gapPatternThresholds.meaningful;

    const substantialShrinkRatio = CHART_7_VALUES.gapPatternThresholds.substantialShrinkRatio;
    const signChanged = gapSummary.shortTermGap * gapSummary.mediumTermGap < 0;
    const substantiallyShrunk = mediumTermGapSize <= shortTermGapSize * substantialShrinkRatio;

    if (shortTermGapSize <= smallThroughoutGap && mediumTermGapSize <= smallThroughoutGap) {
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

function updateChart7ExplanationCard(explanationCard, selectedRows, gapSummary, gapPattern, comparisonKind) {
    explanationCard.replaceChildren();

    const cardBody = document.createElement("div");
    cardBody.className = "card-body";

    const title = document.createElement("h4");
    title.className = "mb-3";

    if (comparisonKind === "discipline") {
        title.textContent = getChart7ComparisonLabel(selectedRows[0], comparisonKind);
    } else {
        title.textContent = `${gapSummary.subgroupDimension}: ${getChart7ComparisonLabel(selectedRows[0], comparisonKind)}`;
    }

    const sentence = document.createElement("p");
    sentence.className = "mb-0";
    sentence.textContent = gapPattern.sentence;

    cardBody.appendChild(title);
    appendChart7PeriodSummary(
        cardBody,
        "4-6 months after graduation",
        selectedRows[0],
        comparisonKind
    );
    appendChart7PeriodSummary(
        cardBody,
        "3-4 years after graduation",
        selectedRows[1],
        comparisonKind
    );
    cardBody.appendChild(sentence);
    explanationCard.appendChild(cardBody);
}

export function renderChart7ComparisonState(
    chartId,
    chartData,
    chartMetadata,
    chartState,
    disciplineFamilies
) {
    const comparisonKind = chartState.comparisonKind;
    const comparisonRows = getTrace(chartData, "comparison_kind", comparisonKind);
    const dropdownButton = document.getElementById("chart7DropdownButton");
    const dropdownMenu = document.getElementById("chart7DropdownMenu");
    const explanationCard = document.getElementById("chart7ExplanationCard");
    const familyDropdown = document.getElementById("chart7FamilyDropdown");
    const familyDropdownButton = document.getElementById("chart7FamilyDropdownButton");
    const familyDropdownMenu = document.getElementById("chart7FamilyDropdownMenu");
    const modeButton = document.getElementById("chart7ModeButton");
    const selectorLabel = document.getElementById("chart7SelectorLabel");
    let selectors;
    
    if (comparisonKind === "discipline") {
        selectors = getChart7DisciplineSelectors(comparisonRows, chartState.disciplineFamily);
        selectorLabel.textContent = "Choose a discipline family and field:";
        modeButton.textContent = "Compare disciplines";
    } else {
        selectors = getChart7DemographicSelectors(comparisonRows);
        selectorLabel.textContent = "Choose a demographic comparison:";
        modeButton.textContent = "Compare demographics";
    }

    familyDropdown.hidden = comparisonKind !== "discipline";
    createChart7DropdownItems(dropdownMenu, selectors);

    if (comparisonKind === "discipline") {
        createChart7DropdownItems(familyDropdownMenu, disciplineFamilies, "family");
        chartState.disciplineFamily = updateChart7DropdownSelection(
            familyDropdownButton,
            familyDropdownMenu,
            disciplineFamilies,
            chartState.disciplineFamily,
            "family"
        );
    }

    const selectorId = updateChart7DropdownSelection(
        dropdownButton,
        dropdownMenu,
        selectors,
        chartState.selectorIdByKind[comparisonKind]
    );
    chartState.selectorIdByKind[comparisonKind] = selectorId;

    renderChart7SelectedComparison(
        chartId,
        comparisonRows,
        chartMetadata,
        chartState.selectorIdByKind[comparisonKind],
        explanationCard
    );
}

export function renderChart7SelectedComparison(
    chartId,
    chartData,
    chartMetadata,
    selectorId,
    explanationCard
) {
    const comparisonKind = chartData[0]["comparison_kind"];
    const selectedRows = getTrace(chartData, "selector_id", selectorId);
    sortByKeyAscending(selectedRows, "time_window_order");

    const gapSummary = getChart7GapSummary(selectedRows, comparisonKind);
    const gapPattern = getChart7GapPattern(gapSummary);
    const yAxisRange = comparisonKind === "discipline" ? CHART_RANGES.chart7.disciplines : CHART_RANGES.chart7.demographics;

    const trace = createChart7Trace(selectedRows, chartMetadata, gapSummary, gapPattern, comparisonKind);
    const layout = createChart7Layout(selectedRows, chartMetadata, yAxisRange);

    updateChart7ExplanationCard(explanationCard, selectedRows, gapSummary, gapPattern, comparisonKind);
    renderChart(chartId, [trace], layout, chartMetadata);
}
