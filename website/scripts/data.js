import { DATA_DIR, CHART_METADATA_ID, UNITS_TO_LABELS } from "./config.js";
import { transformValue } from "./utils.js";

export async function loadChartData(chartId) {
    const metadataPath = DATA_DIR + CHART_METADATA_ID + ".json";
    const chartMetadata = await d3.json(metadataPath).then(metadata => metadata[chartId]);
    const dataPath = DATA_DIR + chartId + ".csv";
    const rawChartData = await d3.csv(dataPath).then(data => data);
    const chartData = transformChartData(rawChartData);

    return { chartData, chartMetadata };
}

function transformChartData(chartData) {
    let transformedChartData = [];

    for (let row of chartData) {
        Object.entries(row).forEach(([columnName, value]) => {
            row[columnName] = transformValue(value);
        });

        transformedChartData.push(row);
    }

    return transformedChartData;
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

export function getTraceRow(rows, traceKey, targetTraceOrderValue) {
    for (let row of rows) {
        const traceOrderValue = row[traceKey];
        if (traceOrderValue === targetTraceOrderValue) {
            return row;
        }
    }
}

function getLabelDefinition(chartMetadata, key) {
    const metadataLabels = chartMetadata.labels ?? {};
    const labelSections = [
        metadataLabels.metrics,
        metadataLabels.dimensions,
        metadataLabels.axes
    ];

    for (let labelDefinitions of labelSections) {
        if (labelDefinitions === undefined) {
            continue;
        }

        const labelDefinition = labelDefinitions[key];

        if (labelDefinition === undefined) {
            continue;
        }

        if (typeof labelDefinition === "string") {
            return { label: labelDefinition };
        }

        return labelDefinition;
    }
}

export function getAxisLabel(chartMetadata, key, useUnit = false) {
    const labelDefinition = getLabelDefinition(chartMetadata, key);
    const axisLabel = labelDefinition.label;

    if (!useUnit) return axisLabel;

    const axisUnit = labelDefinition.unit;
    if (!axisUnit) return axisLabel;

    return axisLabel + UNITS_TO_LABELS[axisUnit];
}

export function getAxisValues(chartData, axisKey) {
    const axisValues = [];

    for (let row of chartData) {
        const axisValue = row[axisKey];
        axisValues.push(axisValue);
    }

    return axisValues;
}

export function getSeriesValue(chartData, seriesKeyLabel, metadataLabels) {
    const seriesKey = chartData[0][seriesKeyLabel];
    const seriesValue = metadataLabels[seriesKey];

    return seriesValue;
}
