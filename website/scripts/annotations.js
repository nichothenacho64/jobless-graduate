import {
    CHART_4_ANNOTATIONS,
    FONT_FAMILY,
    LINE_ANNOTATIONS,
    THEME_COLOURS
} from "./config.js";
import { getTrace, getTraceRow } from "./data.js";
import { createTransparentFillColour } from "./rendering.js";

export function createChart3Labels(chartData) {
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

function createChart4Annotation(row, chartRowCount, label) {
    return {
        x: row["signed_gap_pp"],
        y: chartRowCount - row["sort_order"],
        xref: "x",
        yref: "y",
        text: label.text,
        showarrow: true,
        arrowhead: CHART_4_ANNOTATIONS.arrowhead,
        arrowsize: CHART_4_ANNOTATIONS.arrowsize,
        arrowwidth: CHART_4_ANNOTATIONS.arrowwidth,
        arrowcolor: THEME_COLOURS.text,
        standoff: CHART_4_ANNOTATIONS.standoff,
        startstandoff: CHART_4_ANNOTATIONS.startstandoff,
        xanchor: CHART_4_ANNOTATIONS.xanchor,
        yanchor: CHART_4_ANNOTATIONS.yanchor,
        ax: label.ax,
        ay: label.ay,
        font: {
            family: FONT_FAMILY,
            size: LINE_ANNOTATIONS.fontSize,
            color: THEME_COLOURS.text
        }
    };
}

export function createChart4Annotations(chartData) {
    const chartAnnotations = [];
    const shortTermRows = getTrace(chartData, "time_window", "short_term");
    const mediumTermRows = getTrace(chartData, "time_window", "medium_term");

    for (let label of CHART_4_ANNOTATIONS.labels) {
        const row = getTraceRow(mediumTermRows, "subgroup_dimension", label.subgroupDimension);
        const chartAnnotation = createChart4Annotation(row, shortTermRows.length, label);

        chartAnnotations.push(chartAnnotation);
    }

    return chartAnnotations;
}

export function createChart5EqualityAnnotation(xRange, yRange, equalityLineName) {
    return {
        x: xRange[0],
        y: yRange[0],
        xref: "x",
        yref: "y",
        text: equalityLineName,
        showarrow: false,
        font: {
            family: FONT_FAMILY,
            size: LINE_ANNOTATIONS.fontSize,
            color: THEME_COLOURS.text
        },
        bgcolor: createTransparentFillColour(
            THEME_COLOURS.label,
            LINE_ANNOTATIONS.backgroundOpacity
        ),
        xanchor: "left",
        yanchor: "bottom",
        xshift: LINE_ANNOTATIONS.offset,
        yshift: LINE_ANNOTATIONS.offset,
        textangle: LINE_ANNOTATIONS.diagonalTextAngle
    };
}

export function createChart6XAnnotation(medianEmploymentGain, xLabel) {
    return {
        x: medianEmploymentGain - 0.5,
        y: 1,
        xref: "x",
        yref: "paper",
        text: "Median " + xLabel,
        showarrow: false,
        font: {
            family: FONT_FAMILY,
            size: LINE_ANNOTATIONS.fontSize,
            color: THEME_COLOURS.text
        },
        bgcolor: createTransparentFillColour(
            THEME_COLOURS.label,
            LINE_ANNOTATIONS.backgroundOpacity
        ),
        xanchor: "right",
        yanchor: "top",
        xshift: LINE_ANNOTATIONS.offset,
        yshift: -LINE_ANNOTATIONS.offset
    };
}

export function createChart6YAnnotation(medianWorkFitImprovement, yLabel) {
    return {
        x: 1,
        y: medianWorkFitImprovement,
        xref: "paper",
        yref: "y",
        text: "Median " + yLabel.toLowerCase(),
        showarrow: false,
        font: {
            family: FONT_FAMILY,
            size: LINE_ANNOTATIONS.fontSize,
            color: THEME_COLOURS.text
        },
        bgcolor: createTransparentFillColour(
            THEME_COLOURS.label,
            LINE_ANNOTATIONS.backgroundOpacity
        ),
        xanchor: "right",
        yanchor: "bottom",
        xshift: -LINE_ANNOTATIONS.offset,
        yshift: LINE_ANNOTATIONS.offset
    };
}
