import { CHART_1_ID, CHART_METADATA_ID, DATA_DIR, GLOBAL_CONFIG, GLOBAL_LAYOUT } from "./config.js";
import {
    capitaliseWord,
    transformValue,
    formatPercentage,
    unpack
} from "./utils.js";

export function addGlobalLayoutDefaults(layout) {
    const fontFamily = '"Source Sans 3", sans-serif';

    return {
        ...GLOBAL_LAYOUT,
        ...layout,
        font: {
            ...layout.font,
            family: fontFamily
        },
        hoverlabel: {
            ...layout.hoverlabel,
            font: {
                ...layout.hoverlabel?.font, // optional chaining is neeeded here to prevent accessing .font on undefined
                family: fontFamily
            }
        }
    };
}

export function buildPercentageHoverTemplate(xLabel, yLabel) {
    const percentageHoverTemplate =
        `${xLabel}: %{x}<br>` +
        `${yLabel}: %{y}%` +
        `<extra></extra>`;
    return percentageHoverTemplate;
}

export function getChartElementId(chartId) {
    let splitChartId = chartId.split("_");
    let chartElementId;

    for (let i = 0; i < splitChartId.length; i++) {
        if (i !== 0) {
            chartElementId += capitaliseWord(splitChartId[i]);
        } else {
            chartElementId = splitChartId[i];
        }
    }

    return chartElementId;
}

export function getTrace(rows, traceKey, targetTraceOrderValue) {
    const trace = [];

    for (let row of rows) {
        const traceOrderValue = row[traceKey];
        if (traceOrderValue === targetTraceOrderValue) {
            trace.push(row);
        }
    }

    return trace;
}

export function getAxisValues(chartData, axisKey) {
    const axisValues = [];

    for (let row of chartData) {
        const axisValue = row[axisKey];
        axisValues.push(axisValue);
    }

    return axisValues;
}

export function createAxisMarker(row, traceNumber, groupColumn, colour) {
    const group = row[groupColumn];
    const groupPercentage = row[groupColumn + "_pct"];

    return {
        x: [groupPercentage],
        y: [traceNumber],
        mode: "markers",
        marker: {
            size: 10,
            color: colour
        },
        hovertemplate: `${row["subgroup_dimension"]}: ${group}<br>` +
            `Full-time employment: %{x}%` +
            `<extra></extra>`,
        hoverlabel: {
            font: { color: "#FFF" },
            bordercolor: colour,
        }
    };
}

export function createHollowAxisMarker(row, traceNumber, groupColumn, colour) {
    const axisMarker = createAxisMarker(row, traceNumber, groupColumn, colour);

    axisMarker.marker.color = "#FFF";
    axisMarker.hoverlabel.font.color = "#000";
    axisMarker.marker.line = {
        color: colour,
        width: 2
    };

    return axisMarker;
}

export function addDumbbellChartLegend(marker, name, group, showLegend) {
    marker.name = name;
    marker.legendgroup = group;
    marker.showlegend = showLegend;

    return marker;
}

export function getYTickValues(chartData) {
    const yTickValues = [];

    for (let row of chartData) {
        const yTickValue = chartData.length - row["sort_order"];
        yTickValues.push(yTickValue);
    }

    return yTickValues;
}

export function getYTickLabels(chartData) {
    const subgroupDimensions = getAxisValues(chartData, "subgroup_dimension");
    const lowerSubgroups = getAxisValues(chartData, "lower_group");
    const higherSubgroups = getAxisValues(chartData, "higher_group");
    const yTickLabels = [];

    for (let i = 0; i < chartData.length; i++) {
        const subgroupComparison = lowerSubgroups[i] + " vs " + higherSubgroups[i];
        const yTickLabel = `<b>${subgroupDimensions[i]}</b><br>${subgroupComparison}`;
        yTickLabels.push(yTickLabel);
    }

    return yTickLabels;
}

export function getGapLabelAnnotations(chartData) {
    const gapLabelAnnotations = [];

    for (let row of chartData) {
        const traceNumber = chartData.length - row["sort_order"];
        const gapAnnotation = row["gap_pp"] + " pp";

        const gapLabelAnnotation = {
            x: row["higher_group_pct"],
            y: traceNumber,
            text: gapAnnotation,
            xanchor: "left",
            xshift: 12,
            yanchor: "middle",
            showarrow: false
        };

        gapLabelAnnotations.push(gapLabelAnnotation);
    }

    return gapLabelAnnotations;
}

export function getSeriesValue(chartData, seriesKeyLabel, metadataLabels) {
    const seriesKey = chartData[0][seriesKeyLabel];
    const seriesValue = metadataLabels[seriesKey];

    return seriesValue;
}

export function renderChart(chartId, data, layout) {
    const chartElementId = getChartElementId(chartId);
    const renderedLayout = addGlobalLayoutDefaults(layout);
    return Plotly.newPlot(chartElementId, data, renderedLayout, GLOBAL_CONFIG);
}
