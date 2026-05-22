import {
    createAxisMarker,
    createHollowAxisMarker,
    renderChart,
    getYTickLabels,
    getYTickValues,
    getGapLabelAnnotations,
} from "../setup.js";
import { loadChartData } from "../data.js";
import {
    CHART_2_DIMENSIONS,
    THEME_COLOURS
} from "../config.js";

export async function renderChart2(chartId) {
    const { chartData, chartMetadata } = await loadChartData(chartId);

    const data = [];

    console.log(chartData);

    for (let row of chartData) {
        const traceNumber = chartData.length - row["sort_order"];

        const lowerGroupPercentage = row["lower_group_pct"];
        const higherGroupPercentage = row["higher_group_pct"];

        const lowerGroupMarker = createAxisMarker(row, traceNumber, "lower_group", THEME_COLOURS.amber500);
        const higherGroupMarker = createHollowAxisMarker(row, traceNumber, "higher_group", THEME_COLOURS.amber500);

        const lineTrace = {
            x: [lowerGroupPercentage, higherGroupPercentage],
            y: [traceNumber, traceNumber],
            mode: "lines",
            marker: {
                width: 5,
                color: "rgb(120, 120, 120)"
            },
            hoverinfo: "none"
        };

        data.push(lineTrace, lowerGroupMarker, higherGroupMarker);
    }

    const layout = {
        title: "2024 short-term full-time employment gaps by subgroup dimension",
        height: CHART_2_DIMENSIONS.baseHeight + (chartData.length * CHART_2_DIMENSIONS.rowHeight),
        showlegend: false,
        xaxis: {
            showline: true,
            title: {
                text: "2024 short-term full-time employment (%)"
            },
            range: [55, 86],
            dtick: 5
        },
        yaxis: {
            showline: true,
            showgrid: false,
            nticks: 18,
            tickvals: getYTickValues(chartData),
            ticktext: getYTickLabels(chartData)
        },
        annotations: getGapLabelAnnotations(chartData),
        margin: {
            l: CHART_2_DIMENSIONS.leftMargin,
        }
    };

    renderChart(chartId, data, layout);
    // console.log(chartData);
}
