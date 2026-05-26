import { loadChartData } from "../data.js";
import { renderChart } from "../rendering.js";
import {
    createDumbbellChartLegend,
    createAxisMarker,
    createHollowAxisMarker,
    getChartHeight,
    createChart3Labels,
    getChart3YTickLabels,
    getYTickValues,
} from "../chart-helpers.js";
import {
    CHART_3_DIMENSIONS,
    CHART_AXES,
    CHART_TITLES,
    DUMBBELL_LINE,
    THEME_COLOURS
} from "../config.js";

export async function renderChart3(chartId) {
    const { chartData, chartMetadata } = await loadChartData(chartId);

    const data = [];
    let showSubgroupLegend = true;

    for (let row of chartData) {
        const traceNumber = chartData.length - row["sort_order"];

        const lowerGroupPercentage = row["lower_group_pct"];
        const higherGroupPercentage = row["higher_group_pct"];

        const lowerGroupMarker = createAxisMarker(row, traceNumber, "lower_group", THEME_COLOURS.amber500);
        const higherGroupMarker = createHollowAxisMarker(row, traceNumber, "higher_group", THEME_COLOURS.amber500);

        createDumbbellChartLegend(lowerGroupMarker, "Lower subgroup", "lower_group", showSubgroupLegend);
        createDumbbellChartLegend(higherGroupMarker, "Higher subgroup", "higher_group", showSubgroupLegend);

        showSubgroupLegend = false;

        const lineTrace = {
            x: [lowerGroupPercentage, higherGroupPercentage],
            y: [traceNumber, traceNumber],
            mode: "lines",
            line: DUMBBELL_LINE,
            showlegend: false,
            hoverinfo: "none"
        };

        data.push(lineTrace, lowerGroupMarker, higherGroupMarker);
    }

    const layout = {
        title: { text: CHART_TITLES.chart3 },
        height: getChartHeight(CHART_3_DIMENSIONS.baseHeight, chartData.length, CHART_3_DIMENSIONS.rowHeight),
        showlegend: true,
        xaxis: {
            showline: true,
            title: { text: CHART_AXES.chart3XAxis },
            range: [55, 86],
            dtick: 5
        },
        yaxis: {
            showline: true,
            showgrid: false,
            nticks: 18,
            tickvals: getYTickValues(chartData),
            ticktext: getChart3YTickLabels(chartData)
        },
        annotations: createChart3Labels(chartData),
        margin: {
            l: CHART_3_DIMENSIONS.leftMargin,
            r: CHART_3_DIMENSIONS.rightMargin,
        }
    };

    renderChart(chartId, data, layout);
}
