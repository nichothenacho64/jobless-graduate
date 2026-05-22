import {
    getSeriesValue,
    getTrace,
    getAxisValues,
    renderChart,
    buildPercentageHoverTemplate,
} from "../setup.js";
import { loadChartData } from "../data.js";
import {
    CHART_1_TRACE_COLOURS,
    CHART_AXES,
} from "../config.js";

// chart 1: gradually built up from basic examples featured here: https://plotly.com/javascript/line-charts/

export async function renderChart1(chartId) {
    const { chartData, chartMetadata } = await loadChartData(chartId);
    const metadataSeriesLabels = chartMetadata.labels.series;

    const data = [];

    for (let seriesOrder = 0; seriesOrder < 3; seriesOrder++) {
        const chartTrace = getTrace(chartData, "series_order", seriesOrder);
        const seriesValue = getSeriesValue(chartTrace, "series_key", metadataSeriesLabels);

        const trace = {
            x: getAxisValues(chartTrace, "display_year"),
            y: getAxisValues(chartTrace, "value_pct"),
            name: seriesValue,
            type: "scatter",
            mode: "lines+markers",
            marker: {
                color: CHART_1_TRACE_COLOURS[seriesOrder],
            },
            hovertemplate: buildPercentageHoverTemplate(CHART_AXES.chart1XAxis, "Full-time employment"),
            hoverlabel: {
                font: { color: "#FFF" },
                bordercolor: CHART_1_TRACE_COLOURS[seriesOrder],
            }

        };

        data.push(trace);
    }

    const layout = {
        title: { text: "Chart 1" },
        showlegend: true, // false by default
        xaxis: {
            title: { text: CHART_AXES.chart1XAxis },
            showgrid: false,
            dtick: 1, // the increment step
        },
        yaxis: {
            title: { text: CHART_AXES.chart1YAxis },
            showline: false,
            range: [69, 96]
        },
    };

    renderChart(chartId, data, layout);
}
