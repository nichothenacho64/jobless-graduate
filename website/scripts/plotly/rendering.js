import {
    FONT_FAMILY,
    GLOBAL_TRACES,
    GLOBAL_CONFIG,
    GLOBAL_LAYOUT,
    VIEWPORT_MEDIA_QUERIES
} from "../core/config.js";
import { capitaliseWord, clampValue } from "../core/utils.js";
import {
    applyHoverLabelLayoutDefaults,
    applyHoverLabelTraceDefaults,
    resetHoverLabelHandler
} from "./hover-labels.js";
import { renderChartSourceLabel } from "./source-labels.js";

export function addGlobalLayoutDefaults(layout) {
    const renderedLayout = { 
        ...GLOBAL_LAYOUT,
        ...layout,
        font: {
            ...layout.font,
            family: FONT_FAMILY /* applies the font to the layout of every chart */
        }
    };

    return applyHoverLabelLayoutDefaults(renderedLayout);
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

export function addGlobalTraceDefaults(data) {
    const renderedData = [];

    for (let trace of data) {
        const marker = applyMarkerDefaults(trace.marker);
        const renderedTrace = {
            ...trace,
            ...(marker ? { marker } : {})
        };

        const modifiedRenderedTrace = applyHoverLabelTraceDefaults(renderedTrace);
        renderedData.push(modifiedRenderedTrace);
    }

    return renderedData;
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

export function createReferenceLine(axis, value, lineColour, lineWidth, layer = "below") { /* for creating any sort of line */
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

export function createTransparentFillColour(colour, opacity) {
    const clampedOpacity = clampValue(opacity, 0, 1);
    const alphaValue = Math.round(clampedOpacity * 255);
    const alphaHex = alphaValue.toString(16).padStart(2, "0").toUpperCase();

    return colour + alphaHex;
}

export function getViewportAnnotations(annotations, mediaQuery) {
    const viewportAnnotations = [];

    for (let annotation of annotations) {
        if (annotation.unresponsive && !mediaQuery.matches) {
            continue; // skip annotations marked as unresponsive (i.e those that stay on smaller viewports)
        }

        const { unresponsive, ...plotlyAnnotation } = annotation; // remove unresponsive before passing to Plotly
        viewportAnnotations.push(plotlyAnnotation);
    }

    return viewportAnnotations; // return only annotations that should be shown in the current viewport size
}

function resetAnnotationHandler(chart, annotations, mediaQuery) {
    if (chart.__annotationState) { // remove the preious media query listener to prevent stacking listeners
        chart.__annotationState.mediaQuery.removeEventListener("change", chart.__annotationState.handler);
    }

    chart.__annotationState = undefined;

    if (!annotations?.some((annotation) => annotation.unresponsive)) return;

    const handler = () => { // recalculate annnotations when the viewport crosses the media query
        Plotly.relayout(chart, {
            annotations: getViewportAnnotations(annotations, mediaQuery)
        });
    };

    mediaQuery.addEventListener("change", handler);
    chart.__annotationState = { mediaQuery, handler };
}

export async function renderChart(chartId, data, layout, chartMetadata) {
    const chartElementId = getChartElementId(chartId);
    const renderedData = addGlobalTraceDefaults(data);
    const renderedLayout = addGlobalLayoutDefaults(layout);
    const layoutAnnotations = renderedLayout.annotations;

    const largeMediaQuery = window.matchMedia(VIEWPORT_MEDIA_QUERIES.large); // whether or not larger-screen annotations should appear

    if (layoutAnnotations) {
        renderedLayout.annotations = getViewportAnnotations(layoutAnnotations, largeMediaQuery);
    }

    const chart = await Plotly.newPlot(chartElementId, renderedData, renderedLayout, GLOBAL_CONFIG);

    resetAnnotationHandler(chart, layoutAnnotations, largeMediaQuery);
    resetHoverLabelHandler(chart);

    if (chart.__sourceHandler) { 
        chart.removeListener("plotly_afterplot", chart.__sourceHandler);
    }

    const sourceHandler = () => { // reposition the source label after Plotly finishes drawing or redrawing the chart
        renderChartSourceLabel(chartId, chartMetadata, chart);
    };

    chart.__sourceHandler = sourceHandler;
    chart.on("plotly_afterplot", sourceHandler);
    sourceHandler(); // render the source label immediately after the first plot

    return chart;
}
