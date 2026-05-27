import {
    CHART_TITLES,
    MARKER_SIZE,
    THEME_COLOURS,
    CHART_1A_HOVER_TEMPLATE
} from "../config.js";
import {
    getAxisLabel,
    getAxisValues,
    loadChartData,
} from "../data.js";
import { renderChart } from "../rendering.js";

export async function renderChart1a(chartId) {
    const { chartData, chartMetadata } = await loadChartData(chartId);

    const xKey = "year";
    const yKey = "bachelor_degree_or_above_holders_population";
    const increaseKey = "bachelor_degree_or_above_holders_increase_pct";

    const finalRow = chartData[chartData.length - 1];

    const data = [];

    const lineTrace = {
        x: getAxisValues(chartData, xKey),
        y: getAxisValues(chartData, yKey),
        customdata: getAxisValues(chartData, increaseKey),
        type: "scatter",
        mode: "lines+markers",
        showlegend: false,
        fill: "tozeroy", // 0.05 to hex = 12.75 (round to 13), which is D in hex (add the 0)
        fillcolor: THEME_COLOURS.amber500 + "0D",
        line: {
            color: THEME_COLOURS.amber500,
            width: 2
        },
        marker: {
            size: MARKER_SIZE.small,
            color: THEME_COLOURS.amber500,
        },
        hovertemplate: CHART_1A_HOVER_TEMPLATE
    };

    const finalPointTrace = {
        x: [finalRow[xKey]],
        y: [finalRow[yKey]],
        customdata: [finalRow[increaseKey]],
        type: "scatter",
        mode: "markers",
        showlegend: false,
        marker: {
            size: MARKER_SIZE.large,
            color: THEME_COLOURS.amber700,
        },
        hovertemplate: CHART_1A_HOVER_TEMPLATE
    };

    data.push(lineTrace, finalPointTrace);

    const layout = {
        title: { text: CHART_TITLES.chart1a },
        xaxis: {
            title: { text: "Year" },
            range: [2016, 2025.1],
            nticks: 12,
            zeroline: false
        },
        yaxis: {
            title: { text: getAxisLabel(chartMetadata, yKey, true) },
            range: [4500000, 7000000],
            zeroline: false
        },
    };

    renderChart(chartId, data, layout);
}
