import {
    DIAGONAL_LINE,
    MARKER_SIZE,
    THEME_COLOURS
} from "./config.js";
import { getAxisLabel, getAxisValues, getChartPoints } from "./data.js";
import { calculateMean, getBestFitNumerator, getBestFitDenominator, formatOneDecimal } from "./utils.js";

const CHART_3_SHORT_LABELS = {
    "Socio-economic status": "Socio-economic",
    "Disability reported": "Disability",
    "No disability reported": "No disability"
};

function getChart3ShortLabel(label) {
    return CHART_3_SHORT_LABELS[label] ?? label;
}

export function createAxisMarker(row, traceNumber, groupColumn, colour, valueLabel) {
    const group = row[groupColumn];
    const groupPercentage = row[groupColumn + "_pct"];

    return {
        x: [groupPercentage],
        y: [traceNumber],
        mode: "markers",
        marker: {
            size: MARKER_SIZE.large,
            color: colour
        },
        hovertemplate: `${row["subgroup_dimension"]}: ${group}<br>` +
            `${valueLabel}: %{x}%` +
            `<extra></extra>`
    };
}

export function createHollowAxisMarker(
    row,
    traceNumber,
    groupColumn,
    colour,
    valueLabel
) {
    const axisMarker = createAxisMarker(
        row,
        traceNumber,
        groupColumn,
        colour,
        valueLabel
    );

    axisMarker.marker.color = THEME_COLOURS.background;
    axisMarker.marker.line = {
        color: colour,
        width: 2
    };

    return axisMarker;
}

export function getChartHeight(baseHeight, numRows, rowHeight) {
    return baseHeight + (numRows * rowHeight);
}

export function getComparisonLabel(row) {
    return row["reference_group"] + " vs " + row["comparison_group"];
}

export function getGapSentence(row) {
    const gap = Number(row["signed_gap_pp"]);
    const absoluteGap = Math.abs(gap);
    const referenceGroup = row["reference_group"];
    const comparisonGroup = row["comparison_group"];

    if (absoluteGap <= 0.1) {
        return `${referenceGroup} and ${comparisonGroup} are about equal`;
    }

    const formattedGap = formatOneDecimal(absoluteGap);

    if (gap > 0) {
        return `${comparisonGroup} is ${formattedGap} pp higher than ${referenceGroup}`;
    }

    return `${referenceGroup} is ${formattedGap} pp higher than ${comparisonGroup}`;
}

export function createChart4HoverLabels(row, traceNumber, colour, chartMetadata) {
    const referenceLabel = getAxisLabel(chartMetadata, "reference_group_pct");
    const comparisonLabel = getAxisLabel(chartMetadata, "comparison_group_pct");
    const timeWindowLabel = chartMetadata.labels.time_windows[row["time_window"]];

    const referenceGroup = row["reference_group"];
    const comparisonGroup = row["comparison_group"];

    const referenceGroupPercentage = formatOneDecimal(row["reference_group_pct"]);
    const comparisonGroupPercentage = formatOneDecimal(row["comparison_group_pct"]);

    const hoverTemplate = `<b>${row["subgroup_dimension"]} (${timeWindowLabel} gap)</b><br>` +
        `${getGapSentence(row)}<br>` +
        `${referenceGroup}: ${referenceGroupPercentage}% ${referenceLabel}<br>` +
        `${comparisonGroup}: ${comparisonGroupPercentage}% ${comparisonLabel}<br>` +
        `<extra></extra>`;

    return {
        x: [row["signed_gap_pp"]],
        y: [traceNumber],
        mode: "markers",
        marker: {
            size: MARKER_SIZE.large,
            color: colour
        },
        hovertemplate: hoverTemplate
    };
}

export function getChart4YTickLabels(chartData) {
    const yTickLabels = [];

    for (let row of chartData) {
        const yTickLabel = `<b>${row["subgroup_dimension"]}</b><br>${getComparisonLabel(row)}`;
        yTickLabels.push(yTickLabel);
    }

    return yTickLabels;
}

export function createDumbbellChartLegend(marker, name, group, showLegend) {
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

export function getChart3YTickLabels(chartData) {
    const yTickLabels = [];

    for (let row of chartData) {
        const subgroupComparison = getChart3ShortLabel(row["lower_group"]) +
            " vs " +
            getChart3ShortLabel(row["higher_group"]);
        const yTickLabel = `<b>${getChart3ShortLabel(row["subgroup_dimension"])}</b><br>` +
            subgroupComparison;
        yTickLabels.push(yTickLabel);
    }

    return yTickLabels;
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

export function createChart5EqualityTrace(xStart, xEnd) {
    return {
        x: [xStart, xEnd],
        y: [xStart, xEnd],
        name: "y = x",
        mode: "lines",
        type: "scatter",
        line: DIAGONAL_LINE,
        hoverinfo: "skip"
    };
}

export function createBestFitLineTrace(chartData, xKey, yKey) {
    const xValues = getAxisValues(chartData, xKey);
    const yValues = getAxisValues(chartData, yKey);
    const chartPoints = getChartPoints(chartData, xKey, yKey);

    const xMean = calculateMean(xValues);
    const yMean = calculateMean(yValues);

    const slopeNumerator = getBestFitNumerator(chartPoints, xMean, yMean);
    const slopeDenominator = getBestFitDenominator(chartPoints, xMean);

    const slope = slopeNumerator / slopeDenominator;
    const intercept = yMean - (slope * xMean);

    const xStart = Math.min(...xValues);
    const xEnd = Math.max(...xValues);
    const yStart = (slope * xStart) + intercept;
    const yEnd = (slope * xEnd) + intercept;

    return {
        x: [xStart, xEnd],
        y: [yStart, yEnd],
        name: "Line of best fit",
        mode: "lines",
        type: "scatter",
        line: DIAGONAL_LINE,
        hoverinfo: "skip"
    };
}

export function getChart5MarkerColour(row, gainValues) {
    const gain = row["medium_term_fte_pct"] - row["short_term_fte_pct"];

    if (gain >= gainValues.high) {
        return THEME_COLOURS.amber700;
    } else if (gain >= gainValues.medium) {
        return THEME_COLOURS.amber500;
    } else if (gain >= gainValues.low) {
        return THEME_COLOURS.blue500;
    }

    return THEME_COLOURS.blue700;
}

export function getChart6MarkerColour(row, quadrantValues) {
    const highEmploymentGain = row["fte_gain_pp"] >= quadrantValues.highEmploymentGain;
    const highWorkFitImprovement = row["underutilisation_reduction_pp"] >= quadrantValues.highWorkFitImprovement;

    if (highEmploymentGain && !highWorkFitImprovement) {
        return THEME_COLOURS.amber700;
    } else if (highEmploymentGain && highWorkFitImprovement) {
        return THEME_COLOURS.blue700;
    } else if (!highEmploymentGain && highWorkFitImprovement) {
        return THEME_COLOURS.blue500;
    } 
    
    return THEME_COLOURS.grey500;
}

export function groupRowsByMarkerColour(colourGroups, chartData, getMarkerColour, markerColourValues) {
    for (let row of chartData) {
        const markerColour = getMarkerColour(row, markerColourValues);

        for (let colourGroup of colourGroups) {
            if (colourGroup.colour === markerColour) {
                colourGroup.rows.push(row);
            }
        }
    }

    return colourGroups;
}
