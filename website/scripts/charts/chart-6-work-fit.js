import {
    CHART_TITLES,
    MARKER_SIZE,
    THEME_COLOURS
} from "../config.js";
import {
    getAxisLabel,
    getAxisValues,
    loadChartData,
} from "../data.js";
import {
    createChart6QuadrantPanels,
    getRowsByFamilyColourKey
} from "../chart-helpers.js";
import { createReferenceLine, renderChart } from "../rendering.js";
import { calculateMedian, unpack } from "../utils.js";

export async function renderChart6(chartId) {
    const { chartData, chartMetadata } = await loadChartData(chartId);

    const xKey = "fte_gain_pp";
    const yKey = "underutilisation_reduction_pp";

    const xLabel = getAxisLabel(chartMetadata, xKey);
    const yLabel = getAxisLabel(chartMetadata, yKey);

    const xValues = getAxisValues(chartData, xKey);
    const yValues = getAxisValues(chartData, yKey);

    const medianEmploymentGain = calculateMedian(xValues);
    const medianWorkFitImprovement = calculateMedian(yValues);
    const xRange = [0, medianEmploymentGain * 2];
    const yRange = [-8, 17];

    const medianLines = [];
    const xMedianLine = createReferenceLine("x", medianEmploymentGain, THEME_COLOURS.text, 2, "above");
    const yMedianLine = createReferenceLine("y", medianWorkFitImprovement, THEME_COLOURS.text, 2, "above");
    const quadrantPanels = createChart6QuadrantPanels(
        medianEmploymentGain,
        medianWorkFitImprovement,
        xRange,
        yRange
    );
    const shapes = [];

    for (let quadrantPanel of quadrantPanels) {
        shapes.push(quadrantPanel);
    }

    medianLines.push(xMedianLine);
    medianLines.push(yMedianLine);

    for (let medianLine of medianLines) {
        shapes.push(medianLine);
    }

    const data = [];
    const familyColourGroups = getRowsByFamilyColourKey(chartData);

    for (let familyColourGroup of familyColourGroups) {
        const customData = [];

        for (let row of familyColourGroup.rows) {
            customData.push(row["discipline_family"]);
        }

        const trace = {
            x: unpack(familyColourGroup.rows, xKey),
            y: unpack(familyColourGroup.rows, yKey),
            text: unpack(familyColourGroup.rows, "study_area"),
            customdata: customData,
            name: familyColourGroup.name,
            mode: "markers",
            type: "scatter",
            showlegend: true,
            marker: {
                size: MARKER_SIZE.small,
                color: familyColourGroup.colour,
            },
            hovertemplate: `<b>%{text}</b><br>` +
                `${xLabel}: %{x} pp<br>` +
                `${yLabel}: %{y} pp<br>` +
                `Discipline family: %{customdata}` +
                `<extra></extra>`
        };

        data.push(trace);
    }

    const layout = {
        title: { text: CHART_TITLES.chart6 },
        showlegend: true,
        legend: {
            title: { text: "Family average on this chart" },
            traceorder: "normal"
        },
        xaxis: {
            title: { text: getAxisLabel(chartMetadata, xKey, true) },
            zeroline: false,
            range: xRange
        },
        yaxis: {
            title: { text: getAxisLabel(chartMetadata, yKey, true) },
            zeroline: false,
            range: yRange
        },
        shapes: shapes,
    };

    renderChart(chartId, data, layout);
}
