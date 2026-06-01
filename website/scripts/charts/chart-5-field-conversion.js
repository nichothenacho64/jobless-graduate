import {
    CHART_TITLES,
    MARKER_SIZE
} from "../config.js";
import {
    getAxisLabel,
    loadChartData,
} from "../data.js";
import {
    createChart5EqualityTrace,
    getRowsByFamilyColourKey,
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
    const familyColourGroups = getRowsByFamilyColourKey(chartData);

    equalityLineTrace.showlegend = false;
    
    data.push(equalityLineTrace);

    for (let familyColourGroup of familyColourGroups) {
        const customData = [];

        for (let row of familyColourGroup.rows) {
            customData.push([
                row[yKey] - row[xKey],
                row["discipline_family"]
            ]);
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
                `${xLabel}: %{x}%<br>` +
                `${yLabel}: %{y}%<br>` +
                `Change: %{customdata[0]:.1f} pp<br>` +
                `Discipline family: %{customdata[1]}` +
                `<extra></extra>`
        };

        data.push(trace);
    }

    const layout = {
        title: { text: CHART_TITLES.chart5 },
        showlegend: true,
        legend: {
            title: { text: "Family average on this chart" },
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
