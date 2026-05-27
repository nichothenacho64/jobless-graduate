import {
    CHART_5_GAIN_VALUES,
    CHART_TITLES,
    MARKER_SIZE,
    THEME_COLOURS
} from "../config.js";
import {
    getAxisLabel,
    loadChartData,
} from "../data.js";
import {
    createChart5EqualityTrace,
    getChart5MarkerColour,
    groupRowsByMarkerColour,
} from "../chart-helpers.js";
import {
    renderChart,
} from "../rendering.js";
import { unpack } from "../utils.js";

export async function renderChart5(chartId) {
    const { chartData, chartMetadata } = await loadChartData(chartId);

    const xKey = "short_term_fte_pct";
    const yKey = "medium_term_fte_pct";

    const xLabel = getAxisLabel(chartMetadata, xKey);
    const yLabel = getAxisLabel(chartMetadata, yKey);

    const data = [];
    const equalityLineTrace = createChart5EqualityTrace(50, 100);
    const gainGroups = [
        {
            name: `${CHART_5_GAIN_VALUES.high}+ pp`,
            colour: THEME_COLOURS.amber700,
            rows: []
        },
        {
            name: `${CHART_5_GAIN_VALUES.medium}-${CHART_5_GAIN_VALUES.high - 1} pp`,
            colour: THEME_COLOURS.amber500,
            rows: []
        },
        {
            name: `${CHART_5_GAIN_VALUES.low}-${CHART_5_GAIN_VALUES.medium - 1} pp`,
            colour: THEME_COLOURS.blue500,
            rows: []
        },
        {
            name: `<${CHART_5_GAIN_VALUES.low} pp`,
            colour: THEME_COLOURS.blue700,
            rows: []
        },
    ];

    groupRowsByMarkerColour(gainGroups, chartData, getChart5MarkerColour, CHART_5_GAIN_VALUES);

    equalityLineTrace.showlegend = false;
    
    data.push(equalityLineTrace);

    for (let gainGroup of gainGroups) {
        const trace = {
            x: unpack(gainGroup.rows, xKey),
            y: unpack(gainGroup.rows, yKey),
            text: unpack(gainGroup.rows, "study_area"),
            customdata: gainGroup.rows.map(row => row[yKey] - row[xKey]),
            name: gainGroup.name,
            mode: "markers",
            type: "scatter",
            showlegend: true,
            marker: {
                size: MARKER_SIZE.small,
                color: gainGroup.colour,
            },
            hovertemplate: `<b>%{text}</b><br>` +
                `${xLabel}: %{x}%<br>` +
                `${yLabel}: %{y}%<br>` +
                `Change: %{customdata:.1f} pp` +
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
