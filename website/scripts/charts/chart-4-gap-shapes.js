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
    createDumbbellChartLegend,
    createChart4HoverLabels,
    getChartHeight,
    getChart4YTickLabels,
    getYTickValues,
} from "../chart-helpers.js";
import {
    CHART_4_DIMENSIONS,
    CHART_AXES,
    CHART_TITLES,
    DUMBBELL_LINE,
    THEME_COLOURS
} from "../config.js";

export async function renderChart4(chartId) {
    const { chartData } = await loadChartData(chartId);
    const shortTermRows = getTrace(chartData, "time_window", "short_term");
    const mediumTermRows = getTrace(chartData, "time_window", "medium_term");

    const data = [];
    let showTimeWindowLegend = true;

    for (let i = 0; i < shortTermRows.length; i++) {
        const shortTermRow = shortTermRows[i];
        const mediumTermRow = getTraceRow(mediumTermRows, "subgroup_dimension", shortTermRow["subgroup_dimension"]);
        const traceNumber = shortTermRows.length - shortTermRow["sort_order"];

        const shortTermMarker = createChart4HoverLabels(shortTermRow, traceNumber, THEME_COLOURS.amber700);
        const mediumTermMarker = createChart4HoverLabels(mediumTermRow, traceNumber, THEME_COLOURS.blue700);

        createDumbbellChartLegend(shortTermMarker, "Short-term gap (4 months)", "short_term", showTimeWindowLegend);
        createDumbbellChartLegend(mediumTermMarker, "Medium-term gap (3 years)", "medium_term", showTimeWindowLegend);

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
        title: { text: CHART_TITLES.chart4 }, // short-term and medium-term full-time employment gap shapes
        height: getChartHeight(CHART_4_DIMENSIONS.baseHeight, shortTermRows.length, CHART_4_DIMENSIONS.rowHeight),
        showlegend: true,
        xaxis: {
            showline: true,
            title: { text: CHART_AXES.chart4XAxis },
            range: [-3, 19],
            dtick: 3
        },
        yaxis: {
            showline: true,
            showgrid: false,
            tickvals: getYTickValues(shortTermRows),
            ticktext: getChart4YTickLabels(shortTermRows)
        },
        shapes: [createReferenceLine("x", 0, THEME_COLOURS.textColour, 1)],
        margin: {
            l: CHART_4_DIMENSIONS.leftMargin,
            r: CHART_4_DIMENSIONS.rightMargin,
        }
    };

    renderChart(chartId, data, layout);
}
