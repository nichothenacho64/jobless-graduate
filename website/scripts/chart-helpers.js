import {
    DIAGONAL_LINE,
    MARKER_SIZE,
    THEME_COLOURS
} from "./config.js";
import { getAxisValues, getChartPoints } from "./data.js";
import { calculateMean, getBestFitNumerator, getBestFitDenominator } from "./utils.js";

export function createAxisMarker(row, traceNumber, groupColumn, colour) {
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
            `Full-time employment: %{x}%` +
            `<extra></extra>`
    };
}

export function createHollowAxisMarker(row, traceNumber, groupColumn, colour) {
    const axisMarker = createAxisMarker(row, traceNumber, groupColumn, colour);

    axisMarker.marker.color = THEME_COLOURS.backgroundColour;
    axisMarker.marker.line = {
        color: colour,
        width: 2
    };

    return axisMarker;
}

export function getComparisonLabel(row) {
    return row["reference_group"] + " vs " + row["comparison_group"];
}

export function createGapMarker(row, traceNumber, colour) {
    const comparisonLabel = getComparisonLabel(row);

    return {
        x: [row["signed_gap_pp"]],
        y: [traceNumber],
        mode: "markers",
        marker: {
            size: MARKER_SIZE.large,
            color: colour
        },
        hovertemplate: `<b>${row["subgroup_dimension"]} gap: %{x} pp</b><br>` +
            `${row["reference_group"]}: ${row["reference_group_pct"]}%<br>` +
            `${row["comparison_group"]}: ${row["comparison_group_pct"]}%<br>` +
            `<extra></extra>`
    };
}

export function getGapShapeYTickLabels(chartData) {
    const yTickLabels = [];

    for (let row of chartData) {
        const yTickLabel = `<b>${row["subgroup_dimension"]}</b><br>${getComparisonLabel(row)}`;
        yTickLabels.push(yTickLabel);
    }

    return yTickLabels;
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
    const yTickLabels = [];

    for (let row of chartData) {
        const subgroupComparison = row["lower_group"] + " vs " + row["higher_group"];
        const yTickLabel = `<b>${row["subgroup_dimension"]}</b><br>${subgroupComparison}`;
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

export function createEqualityLineTrace(xStart, xEnd) {
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

export function getFieldConversionColour(row, gainValues) {
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

export function getWorkFitColour(row, quadrantValues) {
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

export function getChartHeight(baseHeight, numRows, rowHeight) {
    return baseHeight + (numRows * rowHeight);
}

export function createChart4GainLegendTrace(gainTrace) {
    const legendRow = {
        short_term_fte_pct: 0,
        medium_term_fte_pct: gainTrace.gainPp
    };

    return {
        x: [null],
        y: [null],
        name: gainTrace.name,
        mode: "markers",
        type: "scatter",
        marker: {
            size: MARKER_SIZE.small,
            color: getFieldConversionColour(legendRow, gainTrace.thresholds)
        },
        hoverinfo: "skip",
        showlegend: true
    };
}

export function createChart4GainLegend(gainValues) {
    const gain4Trace = createChart4GainLegendTrace({
        name: `${gainValues.high}+ pp`,
        gainPp: gainValues.high,
        thresholds: gainValues
    });
    const gain3Trace = createChart4GainLegendTrace({
        name: `${gainValues.medium}-${gainValues.high - 1} pp`,
        gainPp: gainValues.medium,
        thresholds: gainValues
    });
    const gain2Trace = createChart4GainLegendTrace({
        name: `${gainValues.low}-${gainValues.medium - 1} pp`,
        gainPp: gainValues.low,
        thresholds: gainValues
    });
    const gain1Trace = createChart4GainLegendTrace({
        name: `<${gainValues.low} pp`,
        gainPp: gainValues.low - 1,
        thresholds: gainValues
    });

    return [gain4Trace, gain3Trace, gain2Trace, gain1Trace];
}

export function getChart5WorkFitQuadrants(chartData, medianQuadrants) {
    const workFitQuadrants = [
        {
            name: "High gain / high fit improvement",
            colour: THEME_COLOURS.blue700,
            rows: []
        },
        {
            name: "High gain / low fit improvement",
            colour: THEME_COLOURS.amber700,
            rows: []
        },
        {
            name: "Low gain / high fit improvement",
            colour: THEME_COLOURS.blue500,
            rows: []
        },
        {
            name: "Low gain / low fit improvement",
            colour: THEME_COLOURS.grey500,
            rows: []
        },
    ];

    for (let row of chartData) {
        const quadrantColour = getWorkFitColour(row, medianQuadrants);

        for (let workFitQuadrant of workFitQuadrants) {
            if (workFitQuadrant.colour === quadrantColour) {
                workFitQuadrant.rows.push(row);
            }
        }
    }

    return workFitQuadrants;
}