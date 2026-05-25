import {
    GLOBAL_TRACES,
    GLOBAL_CONFIG,
    GLOBAL_LAYOUT,
    THEME_COLOURS,
    HOVERLABEL_BORDER_COLOURS
} from "./config.js";
import { capitaliseWord } from "./utils.js";

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
                ...layout.hoverlabel?.font,
                family: fontFamily
            }
        }
    };
}

function applyMarkerDefaults(marker) {
    if (!marker?.color) {
        return marker;
    }

    return {
        ...GLOBAL_TRACES.marker,
        ...marker,
        line: {
            ...GLOBAL_TRACES.marker.line,
            color: marker.color,
            ...marker.line
        }
    };
}

function getHoverlabelColours(traceColour) {
    let textColour = "#FFF";
    const amberTrace = traceColour === THEME_COLOURS.amber300;
    const blueTrace = traceColour === THEME_COLOURS.blue300;
    const whiteTrace = traceColour === "#FFF";

    if (amberTrace || blueTrace || whiteTrace) {
        textColour = THEME_COLOURS.textColour;
    }

    return {
        borderColour: HOVERLABEL_BORDER_COLOURS[traceColour],
        textColour
    };
}

function applyHoverlabelDefaults(traceColour) {
    const hoverlabelColours = getHoverlabelColours(traceColour);

    return {
        ...GLOBAL_TRACES.hoverlabel,
        ...(hoverlabelColours.borderColour ? { bordercolor: hoverlabelColours.borderColour } : {}),
        font: {
            ...GLOBAL_TRACES.hoverlabel.font,
            color: hoverlabelColours.textColour
        }
    };
}

export function addGlobalTraceDefaults(data) {
    return data.map((trace) => {
        const marker = applyMarkerDefaults(trace.marker);
        const traceColour = marker?.color ?? marker?.line?.color ?? trace.line?.color;

        return {
            ...trace,
            ...(marker ? { marker } : {}),
            hoverlabel: applyHoverlabelDefaults(traceColour)
        };
    });
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

export function createReferenceLine(axis, value, lineColour, lineWidth, layer = "below") {
    const isXAxis = axis === "x";

    return {
        type: "line",
        layer,
        x0: isXAxis ? value : 0,
        x1: isXAxis ? value : 1,
        y0: isXAxis ? 0 : value,
        y1: isXAxis ? 1 : value,
        xref: isXAxis ? "x" : "paper",
        yref: isXAxis ? "paper" : "y",
        line: {
            color: lineColour,
            width: lineWidth
        }
    };
}

export function renderChart(chartId, data, layout) {
    const chartElementId = getChartElementId(chartId);
    const renderedData = addGlobalTraceDefaults(data);
    const renderedLayout = addGlobalLayoutDefaults(layout);
    return Plotly.newPlot(chartElementId, renderedData, renderedLayout, GLOBAL_CONFIG);
}
