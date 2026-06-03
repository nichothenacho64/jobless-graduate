import {
    ANNOTATION_FONT,
    ANNOTATION_LABELS,
    LINE_ANNOTATIONS,
    THEME_COLOURS
} from "../core/config.js";
import { getTrace, getTraceRow } from "../core/data.js";
import { createTransparentFillColour } from "./rendering.js";

export function createAnnotations(
    rows,
    labels,
    traceKey,
    labelKey,
    createAnnotation,
    annotationArgument
) {
    const chartAnnotations = [];

    for (let label of labels) {
        const row = getTraceRow(rows, traceKey, label[labelKey]);
        const chartAnnotation = createAnnotation(row, label, annotationArgument);

        chartAnnotations.push(chartAnnotation);
    }

    return chartAnnotations;
}

function createChart1aAnnotation(row, label) {
    return {
        unresponsive: true,
        x: row["year"],
        y: row["bachelor_degree_or_above_holders_population"],
        xref: "x",
        yref: "y",
        text: label.text,
        showarrow: true,
        arrowhead: 3,
        arrowsize: 1,
        arrowwidth: 1.5,
        arrowcolor: THEME_COLOURS.text,
        standoff: 7,
        startstandoff: 2,
        xanchor: "left",
        yanchor: "middle",
        ax: label.ax,
        ay: label.ay,
        font: ANNOTATION_FONT.default
    };
}

export function createChart1aAnnotations(chartData) {
    const label = ANNOTATION_LABELS.chart1a[0];
    const row = getTraceRow(chartData, "year", label.year);
    const chartAnnotation = createChart1aAnnotation(row, label);

    return [chartAnnotation];
}

export function createChart1bAnnotations(chartData) {
    const label = ANNOTATION_LABELS.chart1b[0];
    const ageGroupRows = getTrace(chartData, "age_group", label.ageGroup);
    let barTop = 0;

    for (let row of ageGroupRows) {
        barTop += row["share_pct"];
    }

    const chartAnnotation = {
        unresponsive: true,
        x: label.ageGroup,
        y: barTop,
        xref: "x",
        yref: "y",
        text: label.text,
        showarrow: true,
        arrowhead: 3,
        arrowsize: 1,
        arrowwidth: 1.5,
        arrowcolor: THEME_COLOURS.text,
        standoff: 7,
        startstandoff: 2,
        xanchor: "left",
        yanchor: "bottom",
        ax: label.ax,
        ay: label.ay,
        font: ANNOTATION_FONT.default
    };

    return [chartAnnotation];
}

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

export function createChart4Annotation(row, label, chartRowCount) {
    return {
        unresponsive: true,
        x: row["signed_gap_pp"],
        y: chartRowCount - row["sort_order"],
        xref: "x",
        yref: "y",
        text: label.text,
        showarrow: true,
        arrowhead: 3,
        arrowsize: 1,
        arrowwidth: 1.5,
        arrowcolor: THEME_COLOURS.text,
        standoff: 7,
        startstandoff: 2,
        xanchor: "left",
        yanchor: "middle",
        ax: label.ax,
        ay: label.ay,
        font: ANNOTATION_FONT.default
    };
}

export function createChart5EqualityAnnotation(xRange, yRange, equalityLineName) {
    return {
        x: xRange[0],
        y: yRange[0],
        xref: "x",
        yref: "y",
        text: equalityLineName,
        showarrow: false,
        font: ANNOTATION_FONT.default,
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

export function createChart5Annotation(row, label) {
    return {
        unresponsive: true,
        x: row["short_term_fte_pct"],
        y: row["medium_term_fte_pct"],
        xref: "x",
        yref: "y",
        text: label.text,
        showarrow: true,
        arrowhead: 3,
        arrowsize: 1,
        arrowwidth: 1.5,
        arrowcolor: THEME_COLOURS.text,
        standoff: 7,
        startstandoff: 2,
        xanchor: label.xanchor,
        yanchor: "middle",
        ax: label.ax,
        ay: label.ay,
        font: ANNOTATION_FONT.default
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
        font: ANNOTATION_FONT.default,
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
        font: ANNOTATION_FONT.default,
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

export function createChart6Annotation(row, label) {
    return {
        unresponsive: true,
        x: row["fte_gain_pp"],
        y: row["underutilisation_reduction_pp"],
        xref: "x",
        yref: "y",
        text: label.text,
        showarrow: true,
        arrowhead: 3,
        arrowsize: 1,
        arrowwidth: 1.5,
        arrowcolor: THEME_COLOURS.text,
        standoff: 7,
        startstandoff: 2,
        xanchor: label.xanchor,
        yanchor: "middle",
        ax: label.ax,
        ay: label.ay,
        font: ANNOTATION_FONT.default
    };
}
