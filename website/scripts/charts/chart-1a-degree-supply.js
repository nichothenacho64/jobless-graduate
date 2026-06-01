import {
    CHART_RANGES,
    CHART_TITLES,
    MARKER_SIZE,
    THEME_COLOURS
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

    const xLabel = getAxisLabel(chartMetadata, xKey);
    const increaseLabel = getAxisLabel(chartMetadata, increaseKey);
    const hoverTemplate = `<b>${xLabel}: %{x}</b><br>` +
        `Bachelor degree+ population: ~%{y:,.0f} people<br>` +
        `${increaseLabel}: %{customdata:.1f}%` +
        `<extra></extra>`;

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
        hovertemplate: hoverTemplate
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
        hovertemplate: hoverTemplate
    };

    data.push(lineTrace, finalPointTrace);

    const layout = {
        title: { text: CHART_TITLES.chart1a },
        xaxis: {
            title: { text: xLabel },
            range: CHART_RANGES.chart1a.x,
            nticks: 12,
            zeroline: false
        },
        yaxis: {
            title: { text: getAxisLabel(chartMetadata, yKey, true) },
            range: CHART_RANGES.chart1a.y,
            zeroline: false
        },
    };

    renderChart(chartId, data, layout);
}
