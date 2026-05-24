import { THEME_COLOURS } from "../config.js";
import {
    getAxisLabel,
    getAxisValues,
    loadChartData,
} from "../data.js";
import { getWorkFitColour } from "../chart-helpers.js";
import { createReferenceLine, renderChart } from "../rendering.js";
import { calculateMedian } from "../utils.js";

export async function renderChart5(chartId) {
    const { chartData, chartMetadata } = await loadChartData(chartId);
    const metadataMetricLabels = chartMetadata.labels.metrics;
    console.log(metadataMetricLabels);

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
    const xMedianLine = createReferenceLine("x", medianEmploymentGain, THEME_COLOURS.textColour, 2, "above");
    const yMedianLine = createReferenceLine("y", medianWorkFitImprovement, THEME_COLOURS.textColour, 2, "above");

    medianLines.push(xMedianLine);
    medianLines.push(yMedianLine);

    const data = [];

    for (let row of chartData) {
        const trace = {
            x: [row[xKey]],
            y: [row[yKey]],
            name: row["study_area"],
            mode: "markers",
            type: "scatter",
            showlegend: false,
            marker: {
                size: 8,
                color: getWorkFitColour(row, medianQuadrants),
            },
            hovertemplate: `<b>%{fullData.name}</b><br>` +
                `${xLabel}: %{x} pp<br>` +
                `${yLabel}: %{y} pp<br>` +
                `<extra></extra>`,
            hoverlabel: {
                font: { color: "#FFF" },
            }
        };

        data.push(trace);
    }

    const layout = {
        title: { text: "Chart 5" },
        showlegend: true,
        legend: {
            title: { text: "Legend title" },
            traceorder: "normal"
        },
        xaxis: {
            title: { text: getAxisLabel(chartMetadata, xKey, true) },
            zeroline: false
        },
        yaxis: {
            title: { text: getAxisLabel(chartMetadata, yKey, true) },
            zeroline: false
        },
        shapes: medianLines,
    };

    renderChart(chartId, data, layout);
}
