import { getAxisLabel, loadChartData } from "../data.js";
import { renderChart } from "../rendering.js";
import { createChart3Labels } from "../annotations.js";
import {
    createDumbbellChartLegend,
    createAxisMarker,
    createHollowAxisMarker,
    getChartHeight,
    getChart3YTickLabels,
    getYTickValues,
} from "../chart-helpers.js";
import {
    CHART_3_DIMENSIONS,
    CHART_3_RENDERING,
    CHART_RANGES,
    CHART_TITLES,
    DUMBBELL_LINE
} from "../config.js";

export async function renderChart3(chartId) {
    const { chartData, chartMetadata } = await loadChartData(chartId);
    const xKey = "lower_group_pct";
    const xLabel = getAxisLabel(chartMetadata, xKey);

    const data = [];
    let showSubgroupLegend = true;

    for (let row of chartData) {
        const traceNumber = chartData.length - row["sort_order"];

        const lowerGroupPercentage = row["lower_group_pct"];
        const higherGroupPercentage = row["higher_group_pct"];
        const isHomeLanguage = row["subgroup_dimension"] === CHART_3_RENDERING.homeLanguageDimension;
        
        let traceColour = CHART_3_RENDERING.defaultColour;
        let dumbbellLine = DUMBBELL_LINE;

        if (isHomeLanguage) {
            traceColour = CHART_3_RENDERING.homeLanguageColour;
            dumbbellLine = {
                width: DUMBBELL_LINE.width,
                color: CHART_3_RENDERING.homeLanguageColour
            };
        }

        const lowerGroupMarker = createAxisMarker(row, traceNumber, "lower_group", traceColour, xLabel);
        const higherGroupMarker = createHollowAxisMarker(row, traceNumber, "higher_group", traceColour, xLabel);

        const showLegend = showSubgroupLegend && !isHomeLanguage;

        createDumbbellChartLegend(lowerGroupMarker, "Lower FTE group", "lower_group", showLegend);
        createDumbbellChartLegend(higherGroupMarker, "Higher FTE group", "higher_group", showLegend);

        if (showLegend) {
            showSubgroupLegend = false;
        }

        const lineTrace = {
            x: [lowerGroupPercentage, higherGroupPercentage],
            y: [traceNumber, traceNumber],
            mode: "lines",
            line: dumbbellLine,
            showlegend: false,
            hoverinfo: "none"
        };

        data.push(lineTrace, lowerGroupMarker, higherGroupMarker);
    }

    const layout = {
        title: { text: CHART_TITLES.chart3 },
        height: getChartHeight(
            CHART_3_DIMENSIONS.baseHeight,
            chartData.length,
            CHART_3_DIMENSIONS.rowHeight
        ),
        showlegend: true,
        xaxis: {
            showline: true,
            title: { text: getAxisLabel(chartMetadata, xKey, true) },
            range: CHART_RANGES.chart3.x,
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
