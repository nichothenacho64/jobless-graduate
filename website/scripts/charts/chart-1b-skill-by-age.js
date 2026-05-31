import {
    getAxisLabel,
    getTrace,
    loadChartData,
} from "../data.js";
import {
    CHART_1B_TRACE_COLOURS,
    CHART_TITLES
} from "../config.js";
import { renderChart } from "../rendering.js";
import { unpack } from "../utils.js";

const SKILL_LEVEL_LEGEND_LABELS = [
    "Skill level 1 (highest)",
    "Skill level 2",
    "Skill level 3",
    "Skill level 4",
    "Skill level 5 (lowest)"
];

export async function renderChart1b(chartId) {
    const { chartData, chartMetadata } = await loadChartData(chartId);
    const xLabel = getAxisLabel(chartMetadata, "age_group");
    const skillLevelLabel = getAxisLabel(chartMetadata, "skill_level");
    const shareLabel = getAxisLabel(chartMetadata, "share_pct");

    const data = [];

    for (let seriesOrder = 0; seriesOrder < 5; seriesOrder++) {
        const chartTrace = getTrace(chartData, "skill_order", seriesOrder);
        const traceName = SKILL_LEVEL_LEGEND_LABELS[seriesOrder] ?? chartTrace[0]["skill_level"];

        const trace = {
            x: unpack(chartTrace, "age_group"),
            y: unpack(chartTrace, "share_pct"),
            name: traceName,
            type: "bar",
            marker: {
                color: CHART_1B_TRACE_COLOURS[seriesOrder],
            },
            hovertemplate: `<b>%{fullData.name}</b><br>` +
                `${xLabel}: %{x}<br>` +
                `${shareLabel}: %{y}%<br>` +
                `<extra></extra>`,
        };

        data.push(trace);
    }

    const layout = {
        title: { text: CHART_TITLES.chart1b },
        showlegend: true,
        legend: {
            title: { text: skillLevelLabel },
            traceorder: "normal", // this is reversed by default
        },
        barmode: "stack",
        xaxis: {
            title: { text: xLabel },
        },
        yaxis: {
            title: { text: getAxisLabel(chartMetadata, "share_pct", true) },
        },
    };

    renderChart(chartId, data, layout);
}
