import {
    ANNOTATION_FONT,
    LINE_ANNOTATIONS,
    THEME_COLOURS
} from "../core/config.js";
import { getTrace, getTraceRow } from "../core/data.js";
import { createTransparentFillColour } from "./rendering.js";

export function createChart1aAnnotations(chartData) {
    const label = {
        year: 2025,
        text: "As of 2025, approximately <br><b>6.8 million</b> Australians <br>hold degrees",
        ax: 40,
        ay: 0
    };
    const row = getTraceRow(chartData, "year", label.year);
    const chartAnnotation = {
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

    return [chartAnnotation];
}

export function createChart1bAnnotations(chartData) {
    const label = {
        ageGroup: "15–24",
        text: "15–24 year-olds have the <br><b>largest share</b> of lower skill work",
        ax: 0,
        ay: -40
    };
    const ageGroupRows = getTrace(chartData, "age_group", label.ageGroup);
    let barTop = 0;

    for (let row of ageGroupRows) {
        barTop += row["share_pct"];
    }

    const chartAnnotation = {
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

function createChart4Annotation(row, chartRowCount, label) {
    return {
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

export function createChart4Annotations(chartData) {
    const chartAnnotations = [];
    const shortTermRows = getTrace(chartData, "time_window", "short_term");
    const mediumTermRows = getTrace(chartData, "time_window", "medium_term");
    const chartAnnotationLabels = [
        {
            subgroupDimension: "Home language",
            text: "The home language<br> gap <b>closes</b>",
            ax: 150,
            ay: -26
        },
        {
            subgroupDimension: "Disability",
            text: "The disability gap <b>persists</b>",
            ax: 200,
            ay: -26
        }
    ];

    for (let label of chartAnnotationLabels) {
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

function createChart5Annotation(row, label) {
    return {
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

export function createChart5Annotations(chartData) {
    const chartAnnotations = [];
    const chartAnnotationLabels = [
        {
            studyArea: "Creative arts",
            text: "Creative arts has the largest later recovery",
            xanchor: "left",
            ax: 20,
            ay: -80
        },
        {
            studyArea: "Rehabilitation",
            text: "Rehabilitation is already high after year one",
            xanchor: "left",
            ax: 40,
            ay: -40
        }
    ];

    for (let label of chartAnnotationLabels) {
        const row = getTraceRow(chartData, "study_area", label.studyArea);
        const chartAnnotation = createChart5Annotation(row, label);

        chartAnnotations.push(chartAnnotation);
    }

    return chartAnnotations;
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
