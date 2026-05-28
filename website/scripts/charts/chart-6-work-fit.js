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
import { getChart6MarkerColour, groupRowsByMarkerColour } from "../chart-helpers.js";
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
    const medianQuadrants = {
        highEmploymentGain: medianEmploymentGain,
        highWorkFitImprovement: medianWorkFitImprovement
    };

    const medianLines = [];
    const xMedianLine = createReferenceLine("x", medianEmploymentGain, THEME_COLOURS.text, 2, "above");
    const yMedianLine = createReferenceLine("y", medianWorkFitImprovement, THEME_COLOURS.text, 2, "above");

    medianLines.push(xMedianLine);
    medianLines.push(yMedianLine);

    const data = [];
    const workFitQuadrants = [
        {
            name: "High gain/high fit improvement",
            colour: THEME_COLOURS.blue700,
            rows: []
        },
        {
            name: "High gain/low fit improvement",
            colour: THEME_COLOURS.amber700,
            rows: []
        },
        {
            name: "Low gain/high fit improvement",
            colour: THEME_COLOURS.blue500,
            rows: []
        },
        {
            name: "Low gain/low fit improvement",
            colour: THEME_COLOURS.grey500,
            rows: []
        },
    ];

    groupRowsByMarkerColour(workFitQuadrants, chartData, getChart6MarkerColour, medianQuadrants);

    for (let workFitQuadrant of workFitQuadrants) {
        const trace = {
            x: unpack(workFitQuadrant.rows, xKey),
            y: unpack(workFitQuadrant.rows, yKey),
            text: unpack(workFitQuadrant.rows, "study_area"),
            name: workFitQuadrant.name,
            mode: "markers",
            type: "scatter",
            showlegend: true,
            marker: {
                size: MARKER_SIZE.small,
                color: workFitQuadrant.colour,
            },
            hovertemplate: `<b>%{text}</b><br>` +
                `${xLabel}: %{x} pp<br>` +
                `${yLabel}: %{y} pp<br>` +
                `<extra></extra>`
        };

        data.push(trace);
    }

    const layout = {
        title: { text: CHART_TITLES.chart6 },
        showlegend: true,
        legend: {
            title: { text: "Employment gain/work fit" },
            traceorder: "normal"
        },
        xaxis: {
            title: { text: getAxisLabel(chartMetadata, xKey, true) },
            zeroline: false,
            range: [0, medianEmploymentGain * 2]
        },
        yaxis: {
            title: { text: getAxisLabel(chartMetadata, yKey, true) },
            zeroline: false,
            range: [-8, 17]
        },
        shapes: medianLines,
    };

    renderChart(chartId, data, layout);
}
