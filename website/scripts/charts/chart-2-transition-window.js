import {
    getAxisLabel,
    getAxisValues,
    getSeriesValue,
    getTrace,
    loadChartData,
} from "../core/data.js";
import { renderChart } from "../plotly/rendering.js";
import {
    CHART_2_TRACE_COLOURS,
    CHART_RANGES,
    CHART_TITLES,
} from "../core/config.js";

// chart 2: gradually built up from basic examples featured here: https://plotly.com/javascript/line-charts/

export async function renderChart2(chartId) {
    const { chartData, chartMetadata } = await loadChartData(chartId);
    const metadataSeriesLabels = chartMetadata.labels.series;
    
    const xKey = "display_year";
    const yKey = "value_pct";

    const xLabel = getAxisLabel(chartMetadata, xKey);
    const yLabel = getAxisLabel(chartMetadata, yKey);

    const data = [];

    for (let seriesOrder = 0; seriesOrder < 3; seriesOrder++) {
        const chartTrace = getTrace(chartData, "series_order", seriesOrder);
        const seriesValue = getSeriesValue(chartTrace, "series_key", metadataSeriesLabels);

        const trace = {
            x: getAxisValues(chartTrace, xKey),
            y: getAxisValues(chartTrace, yKey),
            name: seriesValue,
            type: "scatter",
            mode: "lines+markers",
            marker: {
                color: CHART_2_TRACE_COLOURS[seriesOrder],
            },
            hovertemplate: `${xLabel}: %{x}<br>` +
                `${yLabel}: %{y}%` +
                `<extra></extra>`
        };

        data.push(trace);
    }

    const layout = {
        title: { text: CHART_TITLES.chart2 },
        xaxis: {
            title: { text: xLabel },
            showgrid: false,
            dtick: 1, // the increment step
        },
        yaxis: {
            title: { text: getAxisLabel(chartMetadata, yKey, true) },
            showline: false,
            range: CHART_RANGES.chart2.y
        },
    };

    renderChart(chartId, data, layout, chartMetadata);
}
