import {
    CHART_5_GAIN_VALUES,
    CHART_TITLES,
    MARKER_SIZE
} from "../config.js";
import {
    getAxisLabel,
    loadChartData,
} from "../data.js";
import {
    createChart5GainLegend,
    createChart5EqualityTrace,
    getChart5MarkerColour,
} from "../chart-helpers.js";
import {
    renderChart,
} from "../rendering.js";

export async function renderChart5(chartId) {
    const { chartData, chartMetadata } = await loadChartData(chartId);

    const xKey = "short_term_fte_pct";
    const yKey = "medium_term_fte_pct";

    const xLabel = getAxisLabel(chartMetadata, xKey);
    const yLabel = getAxisLabel(chartMetadata, yKey);

    const data = [];
    const equalityLineTrace = createChart5EqualityTrace(50, 100);
    const gainLegendTraces = createChart5GainLegend(CHART_5_GAIN_VALUES);

    equalityLineTrace.showlegend = false;
    
    data.push(equalityLineTrace);

    for (let gainLegendTrace of gainLegendTraces) {
        data.push(gainLegendTrace);
    }

    for (let row of chartData) {
        const employmentGain = row[yKey] - row[xKey];

        const trace = {
            x: [row[xKey]],
            y: [row[yKey]],
            name: row["study_area"],
            mode: "markers",
            type: "scatter",
            showlegend: false,
            marker: {
                size: MARKER_SIZE.small,
                color: getChart5MarkerColour(row, CHART_5_GAIN_VALUES),
            },
            hovertemplate: `<b>%{fullData.name}</b><br>` +
                `${xLabel}: %{x}%<br>` +
                `${yLabel}: %{y}%<br>` +
                `${"Change"}: ${employmentGain.toFixed(1)} pp` +
                `<extra></extra>`
        };

        data.push(trace);
    }

    const layout = {
        title: { text: CHART_TITLES.chart5 },
        showlegend: true,
        legend: {
            title: { text: "Medium-term gain over short-term FTE" },
            traceorder: "normal"
        },
        xaxis: {
            title: { text: getAxisLabel(chartMetadata, xKey, true) },
            range: [55, 100],
        },
        yaxis: {
            title: { text: getAxisLabel(chartMetadata, yKey, true) },
            range: [55, 100],
        },
    };

    renderChart(chartId, data, layout);
}
