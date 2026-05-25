import {
    getTrace,
    getTraceRow,
    loadChartData,
} from "../data.js";
import {
    createReferenceLine,
    renderChart,
} from "../rendering.js";
import {
    addDumbbellChartLegend,
    createGapMarker,
    getChartHeight,
    getGapShapeYTickLabels,
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
    const { chartData } = await loadChartData(chartId);
    const shortTermRows = getTrace(chartData, "time_window", "short_term");
    const mediumTermRows = getTrace(chartData, "time_window", "medium_term");

    const data = [];
    let showTimeWindowLegend = true;

    for (let i = 0; i < shortTermRows.length; i++) {
        const shortTermRow = shortTermRows[i];
        const mediumTermRow = getTraceRow(mediumTermRows, "subgroup_dimension", shortTermRow["subgroup_dimension"]);
        const traceNumber = shortTermRows.length - shortTermRow["sort_order"];

        const shortTermMarker = createGapMarker(shortTermRow, traceNumber, THEME_COLOURS.amber700);
        const mediumTermMarker = createGapMarker(mediumTermRow, traceNumber, THEME_COLOURS.blue700);

        addDumbbellChartLegend(shortTermMarker, "Short-term gap (4 months)", "short_term", showTimeWindowLegend);
        addDumbbellChartLegend(mediumTermMarker, "Medium-term gap (3 years)", "medium_term", showTimeWindowLegend);

        showTimeWindowLegend = false;

        const shortTermGap = shortTermRow["signed_gap_pp"];
        const mediumTermGap = mediumTermRow["signed_gap_pp"];

        const lineTrace = {
            x: [shortTermGap, mediumTermGap],
            y: [traceNumber, traceNumber],
            mode: "lines",
            line: DUMBBELL_LINE,
            showlegend: false,
            hoverinfo: "none"
        };

        data.push(lineTrace, shortTermMarker, mediumTermMarker);
    }

    const layout = {
        title: { text: CHART_TITLES.chart3 }, // short-term and medium-term full-time employment gap shapes
        height: getChartHeight(CHART_3_DIMENSIONS.baseHeight, shortTermRows.length, CHART_3_DIMENSIONS.rowHeight),
        showlegend: true,
        xaxis: {
            showline: true,
            title: { text: CHART_AXES.chart3XAxis },
            range: [-3, 19],
            dtick: 3
        },
        yaxis: {
            showline: true,
            showgrid: false,
            tickvals: getYTickValues(shortTermRows),
            ticktext: getGapShapeYTickLabels(shortTermRows)
        },
        shapes: [createReferenceLine("x", 0, THEME_COLOURS.textColour, 1)],
        margin: {
            l: CHART_3_DIMENSIONS.leftMargin,
            r: CHART_3_DIMENSIONS.rightMargin,
        }
    };

    renderChart(chartId, data, layout);
}
