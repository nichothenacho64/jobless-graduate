import { DATA_DIR, CHART_METADATA_ID } from "./config.js";
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