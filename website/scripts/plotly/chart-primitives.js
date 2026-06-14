import {
    CHART_3_SHORT_LABELS,
    CHART_6_RENDERING,
    DIAGONAL_LINE,
    DISCIPLINE_FAMILY_RENDERING,
    MARKER_SIZE,
    THEME_COLOURS
} from "../core/config.js";
import { getAxisLabel } from "../core/data.js";
import { createTransparentFillColour } from "./rendering.js";
import { formatOneDecimal } from "../core/utils.js";

// Shared chart helpers
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

export function createDumbbellChartLegend(marker, name, group, showLegend) {
    marker.name = name;
    marker.legendgroup = group;
    marker.showlegend = showLegend;

    return marker;
}

export function getYTickValues(chartData) { /* for getting y-axis tick value depending on sort order */
    const yTickValues = [];

    for (let row of chartData) {
        const yTickValue = chartData.length - row["sort_order"]; /* reverse to start on the correct axis position */
        yTickValues.push(yTickValue);
    }

    return yTickValues;
}

export function getRowsByFamilyColourKey(chartData) {
    const familyGroups = [];

    for (let colourKey of DISCIPLINE_FAMILY_RENDERING.order) {
        for (let row of chartData) {
            if (row["family_colour_key"] !== colourKey) continue;

            let familyGroup;
            const disciplineFamily = row["discipline_family"];

            for (let group of familyGroups) {
                const sameFamily = group.disciplineFamily === disciplineFamily;
                const sameColourKey = group.familyColourKey === colourKey;

                if (sameFamily && sameColourKey) {
                    familyGroup = group;
                    break;
                }
            }

            if (!familyGroup) {
                familyGroup = {
                    name: disciplineFamily,
                    disciplineFamily,
                    familyColourKey: colourKey,
                    colour: DISCIPLINE_FAMILY_RENDERING.colours[colourKey],
                    rows: []
                };

                familyGroups.push(familyGroup);
            }

            familyGroup.rows.push(row);
        }
    }

    return familyGroups;
}

// Chart 3
export function createAxisMarker(row, traceNumber, groupColumn, colour, valueLabel) { /* for creating a simple axis marker */
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
        hovertemplate: `<b>${row["subgroup_dimension"]}: ${group}</b><br>` +
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
    const axisMarker = createAxisMarker(row, traceNumber, groupColumn, colour, valueLabel);

    axisMarker.marker.color = THEME_COLOURS.background;
    axisMarker.marker.line = {
        color: colour,
        width: 2
    };

    return axisMarker;
}

function getChart3ShortLabel(label) {
    return CHART_3_SHORT_LABELS[label] ?? label;
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

// Chart 4
export function createChart4HoverLabels(row, traceNumber, colour, chartMetadata) {
    const referenceLabel = getAxisLabel(chartMetadata, "reference_group_pct");
    const comparisonLabel = getAxisLabel(chartMetadata, "comparison_group_pct");
    const timeWindowLabel = chartMetadata.labels.time_windows[row["time_window"]];

    const referenceGroup = row["reference_group"];
    const comparisonGroup = row["comparison_group"];

    const referenceGroupPercentage = formatOneDecimal(row["reference_group_pct"]);
    const comparisonGroupPercentage = formatOneDecimal(row["comparison_group_pct"]);

    const hoverTemplate = `<b>${row["subgroup_dimension"]} (${timeWindowLabel} gap)</b><br>` +
        `<i>${getGapSentence(row)}</i><br>` +
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

// Chart 5
export function createChart5EqualityTrace(xStart, xEnd) {
    return {
        x: [xStart, xEnd],
        y: [xStart, xEnd],
        name: "Same employment rate in both periods",
        mode: "lines",
        type: "scatter",
        line: DIAGONAL_LINE,
        hoverinfo: "skip"
    };
}

// Chart 6
export function createChart6QuadrantPanels(xMedian, yMedian, xRange, yRange) {
    const quadrantPanels = [];
    const leftPanelOpacity = CHART_6_RENDERING.leftQuadrantPanelOpacity;
    const rightPanelOpacity = CHART_6_RENDERING.rightQuadrantPanelOpacity;
    const topRightPanel = createChart6QuadrantPanel(
        xMedian,
        xRange[1],
        yMedian,
        yRange[1],
        THEME_COLOURS.blue700,
        rightPanelOpacity
    );
    const bottomRightPanel = createChart6QuadrantPanel(
        xMedian,
        xRange[1],
        yRange[0],
        yMedian,
        THEME_COLOURS.amber700,
        rightPanelOpacity
    );
    const topLeftPanel = createChart6QuadrantPanel(
        xRange[0],
        xMedian,
        yMedian,
        yRange[1],
        THEME_COLOURS.blue300,
        leftPanelOpacity
    );
    const bottomLeftPanel = createChart6QuadrantPanel(
        xRange[0],
        xMedian,
        yRange[0],
        yMedian,
        THEME_COLOURS.amber300,
        leftPanelOpacity
    );

    quadrantPanels.push(topRightPanel);
    quadrantPanels.push(bottomRightPanel);
    quadrantPanels.push(topLeftPanel);
    quadrantPanels.push(bottomLeftPanel);

    return quadrantPanels;
}

function createChart6QuadrantPanel(x0, x1, y0, y1, colour, opacity) {
    return {
        type: "rect",
        xref: "x",
        yref: "y",
        layer: "below",
        x0,
        x1,
        y0,
        y1,
        line: { width: 0 },
        fillcolor: createTransparentFillColour(colour, opacity)
    };
}
