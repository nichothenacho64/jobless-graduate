import {
    CHART_7_GAPS,
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
    getChart7DisciplineSummarySentence,
    getChart7FieldGap,
    getChart7GapSentence,
    getChart7GroupLabel,
    getChart7SelectorLabel,
    getChart7TimeWindowLabel
} from "./labels.js";
import {
    getChart7DemographicSelectors,
    getChart7DisciplineSelectors
} from "./selectors.js";

function createChart7Trace(selectedRows, chartMetadata, comparisonKind) {
    const xValues = [];
    const yValues = [];
    const customData = [];
    const referenceLabel = getAxisLabel(chartMetadata, "reference_group_pct");
    const comparisonLabel = getAxisLabel(chartMetadata, "comparison_group_pct");
    const gapTypeLabel = comparisonKind === "discipline" ? "difference" : "gap";
    const gapSummary = getChart7GapSummary(selectedRows, comparisonKind);
    const gapPattern = getChart7GapPattern(gapSummary, comparisonKind);

    const line = {
        color: gapPattern.colour,
        width: DUMBBELL_LINE.default.width
    };

    if (gapPattern.dash) {
        line.dash = gapPattern.dash;
    }

    for (let row of selectedRows) {
        const timeWindowLabel = getChart7TimeWindowLabel(row, chartMetadata);
        const valueRows = getChart7ValueRows(row, comparisonKind);
        let gap = row["signed_gap_pp"];

        if (comparisonKind === "discipline") {
            gap = getChart7FieldGap(row);
        }

        xValues.push(timeWindowLabel);
        yValues.push(gap);
        customData.push([
            getChart7SelectorLabel(row, comparisonKind),
            row["time_window"].replace("_", "-"),
            getChart7GapSentence(row, comparisonKind),
            valueRows[0].label,
            valueRows[0].value,
            valueRows[1].label,
            valueRows[1].value
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
        hovertemplate: `<b>%{customdata[0]} (%{customdata[1]} ${gapTypeLabel})</b><br>` +
            `<i>%{customdata[2]}</i><br>` +
            `%{customdata[3]}: %{customdata[4]:.1f}% ${referenceLabel}<br>` +
            `%{customdata[5]}: %{customdata[6]:.1f}% ${comparisonLabel}` +
            `<extra></extra>`
    };
}

function createChart7Layout(selectedRows, chartMetadata, comparisonKind) {
    const xValues = [];
    const yAxisLine = createReferenceLine("y", 0, THEME_COLOURS.text, 2, "above");
    let yAxisLabel = getAxisLabel(chartMetadata, "signed_gap_pp", true);
    let yAxisRange = CHART_RANGES.chart7.demographics;

    if (comparisonKind === "discipline") {
        yAxisLabel = CHART_7_VALUES.disciplineYAxisLabel;
        yAxisRange = CHART_RANGES.chart7.disciplines;
    }

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
            title: { text: yAxisLabel },
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

function getChart7ValueRows(row, comparisonKind) {
    let firstLabel;
    let firstValue;
    let secondLabel;
    let secondValue;

    if (comparisonKind === "discipline") {
        firstLabel = getChart7SelectorLabel(row, comparisonKind);
        secondLabel = getChart7GroupLabel(CHART_7_VALUES.fieldAverageGroup, comparisonKind);
        firstValue = row["reference_group_pct"];
        secondValue = row["comparison_group_pct"];

        if (row["reference_group"] === CHART_7_VALUES.fieldAverageGroup) {
            firstValue = row["comparison_group_pct"];
            secondValue = row["reference_group_pct"];
        }
    } else {
        firstLabel = getChart7GroupLabel(row["reference_group"], comparisonKind);
        firstValue = row["reference_group_pct"];
        secondLabel = getChart7GroupLabel(row["comparison_group"], comparisonKind);
        secondValue = row["comparison_group_pct"];
    }

    return [
        { label: firstLabel, value: firstValue },
        { label: secondLabel, value: secondValue }
    ];
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

    const gapSentence = getChart7GapSentence(row, comparisonKind);
    sentence.textContent = `${leadText}, ${gapSentence} in full-time employment.`;

    const valueRows = getChart7ValueRows(row, comparisonKind);

    for (let valueRow of valueRows) {
        const percentage = formatOneDecimal(valueRow.value);
        appendChart7CardValue(values, valueRow.label, `${percentage}%`);
    }

    cardBody.append(sentence, values);
}

function getChart7GapSummary(selectedRows, comparisonKind) {
    let shortTermGap = selectedRows[0]["signed_gap_pp"];
    let mediumTermGap = selectedRows[1]["signed_gap_pp"];

    if (comparisonKind === "discipline") {
        shortTermGap = getChart7FieldGap(selectedRows[0]);
        mediumTermGap = getChart7FieldGap(selectedRows[1]);
    }

    return {
        selectorLabel: getChart7SelectorLabel(selectedRows[0], comparisonKind),
        subgroupDimension: selectedRows[0]["subgroup_dimension"],
        shortTermGap,
        mediumTermGap
    };
}

function getChart7GapPatternKey(gapSummary) {
    const thresholds = CHART_7_GAPS.thresholds;
    const shortTermGapSize = Math.abs(gapSummary.shortTermGap);
    const mediumTermGapSize = Math.abs(gapSummary.mediumTermGap);
    const smallThroughout =
        shortTermGapSize <= thresholds.smallThroughout &&
        mediumTermGapSize <= thresholds.smallThroughout;
    const signChanged = gapSummary.shortTermGap * gapSummary.mediumTermGap < 0;
    const substantiallyShrunk = mediumTermGapSize <= shortTermGapSize * thresholds.substantialShrinkRatio;

    if (smallThroughout) {
        return "smallThroughout";
    } else if (signChanged) {
        return "reverses";
    } else if (mediumTermGapSize <= thresholds.nearZero) {
        return "mostlyCloses";
    } else if (mediumTermGapSize >= thresholds.meaningful && !substantiallyShrunk) {
        return "persists";
    }

    return "mostlyCloses";
}

function getChart7DisciplineGapColour(gapSummary) {
    const thresholds = CHART_7_GAPS.thresholds;
    const colours = CHART_7_GAPS.discipline.colours;
    const shortTermGap = gapSummary.shortTermGap;
    const mediumTermGap = gapSummary.mediumTermGap;
    const shortTermGapSize = Math.abs(shortTermGap);
    const mediumTermGapSize = Math.abs(mediumTermGap);

    if (
        shortTermGapSize <= thresholds.smallThroughout &&
        mediumTermGapSize <= thresholds.smallThroughout
    ) {
        return colours.closeToAverage;
    } else if (mediumTermGap > thresholds.smallThroughout) {
        return colours.aboveAverage;
    } else if (mediumTermGap < -thresholds.smallThroughout) {
        return colours.belowAverage;
    } else if (shortTermGap < -thresholds.smallThroughout) {
        return colours.catchesUp;
    }

    return colours.closeToAverage;
}

function getChart7GapPattern(gapSummary, comparisonKind) {
    const gapPatternKey = getChart7GapPatternKey(gapSummary);
    const gapPattern = CHART_7_GAPS[comparisonKind].patterns[gapPatternKey];
    let colour = gapPattern.colour;
    let sentence = gapPattern.sentence;

    if (comparisonKind === "discipline") {
        sentence = getChart7DisciplineSummarySentence(gapSummary);
        colour = getChart7DisciplineGapColour(gapSummary);
    }

    return {
        label: gapPattern.label,
        colour,
        dash: gapPattern.dash,
        sentence
    };
}

function updateChart7ExplanationCard(
    explanationCard,
    selectedRows,
    comparisonKind
) {
    explanationCard.replaceChildren();
    const gapSummary = getChart7GapSummary(selectedRows, comparisonKind);
    const gapPattern = getChart7GapPattern(gapSummary, comparisonKind);

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

    appendChart7PeriodSummary(cardBody, "4-6 months after graduation", selectedRows[0], comparisonKind);
    appendChart7PeriodSummary(cardBody, "3-4 years after graduation", selectedRows[1], comparisonKind);

    cardBody.appendChild(sentence);
    explanationCard.appendChild(cardBody);
}

function renderChart7SelectedComparison(
    chartId,
    chartData,
    chartMetadata,
    selectorId,
    explanationCard
) {
    const comparisonKind = chartData[0]["comparison_kind"];
    const selectedRows = getTrace(chartData, "selector_id", selectorId);
    sortByKeyAscending(selectedRows, "time_window_order");

    const trace = createChart7Trace(selectedRows, chartMetadata, comparisonKind);
    const layout = createChart7Layout(selectedRows, chartMetadata, comparisonKind);

    updateChart7ExplanationCard(explanationCard, selectedRows, comparisonKind);
    renderChart(chartId, [trace], layout, chartMetadata);
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
