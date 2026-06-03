import {
    ANNOTATION_LABELS,
    CHART_RANGES,
    CHART_TITLES,
    MARKER_SIZE
} from "../core/config.js";
import {
    getAxisLabel,
    loadChartData,
} from "../core/data.js";
import {
    createChart5EqualityTrace,
    getRowsByFamilyColourKey,
} from "../plotly/chart-primitives.js";
import {
    createAnnotations,
    createChart5Annotation,
    createChart5EqualityAnnotation
} from "../plotly/annotations.js";
import { renderChart } from "../plotly/rendering.js";
import { unpack } from "../core/utils.js";

export async function renderChart5(chartId) {
    const { chartData, chartMetadata } = await loadChartData(chartId);

    const xKey = "short_term_fte_pct";
    const yKey = "medium_term_fte_pct";

    const xLabel = getAxisLabel(chartMetadata, xKey);
    const yLabel = getAxisLabel(chartMetadata, yKey);

    const data = [];
    const equalityLineTrace = createChart5EqualityTrace(45, 100);
    const familyColourGroups = getRowsByFamilyColourKey(chartData);

    equalityLineTrace.showlegend = false;
    
    data.push(equalityLineTrace);

    for (let familyColourGroup of familyColourGroups) {
        const customData = [];

        for (let row of familyColourGroup.rows) {
            customData.push([
                row[yKey] - row[xKey],
                row["discipline_family"]
            ]);
        }

        const trace = {
            x: unpack(familyColourGroup.rows, xKey),
            y: unpack(familyColourGroup.rows, yKey),
            text: unpack(familyColourGroup.rows, "study_area"),
            customdata: customData,
            name: familyColourGroup.name,
            mode: "markers",
            type: "scatter",
            showlegend: true,
            marker: {
                size: MARKER_SIZE.small,
                color: familyColourGroup.colour,
            },
            hovertemplate: `<b>%{text}</b><br>` +
                `${xLabel}: %{x}%<br>` +
                `${yLabel}: %{y}%<br>` +
                `Change: %{customdata[0]:.1f} pp<br>` +
                `Discipline family: %{customdata[1]}` +
                `<extra></extra>`
        };

        data.push(trace);
    }

    const equalityLineAnnotation = createChart5EqualityAnnotation(CHART_RANGES.chart5.x, CHART_RANGES.chart5.y, equalityLineTrace.name);
    const chartAnnotations = createAnnotations(
        chartData,
        ANNOTATION_LABELS.chart5,
        "study_area",
        "studyArea",
        createChart5Annotation
    );

    const layout = {
        title: { text: CHART_TITLES.chart5 },
        showlegend: true,
        legend: {
            title: { text: "Family average on this chart" },
            traceorder: "normal"
        },
        xaxis: {
            title: { text: getAxisLabel(chartMetadata, xKey, true) },
            range: CHART_RANGES.chart5.x,
        },
        yaxis: {
            title: { text: getAxisLabel(chartMetadata, yKey, true) },
            range: CHART_RANGES.chart5.y,
        },
        annotations: [equalityLineAnnotation, ...chartAnnotations]
    };

    renderChart(chartId, data, layout, chartMetadata);
}
