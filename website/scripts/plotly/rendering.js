import {
    FONT_FAMILY,
    GLOBAL_TRACES,
    GLOBAL_CONFIG,
    GLOBAL_LAYOUT,
    THEME_COLOURS,
    HOVERLABEL_BORDER_COLOURS,
    VIEWPORT_MEDIA_QUERIES
} from "../core/config.js";
import { capitaliseWord, clampValue } from "../core/utils.js";
import { renderChartSourceLabel } from "./source-labels.js";

export function addGlobalLayoutDefaults(layout) {
    return { 
        ...GLOBAL_LAYOUT,
        ...layout,
        font: {
            ...layout.font,
            family: FONT_FAMILY /* applies the font to the layout of every chart */
        },
        hoverlabel: {
            ...layout.hoverlabel,
            font: {
                ...layout.hoverlabel?.font,
                family: FONT_FAMILY /* applies the font to the hover labels of every chart */
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
    let textColour = THEME_COLOURS.background;
    const amberTrace = traceColour === THEME_COLOURS.amber300;
    const blueTrace = traceColour === THEME_COLOURS.blue300;
    const backgroundTrace = traceColour === THEME_COLOURS.background;

    if (amberTrace || blueTrace || backgroundTrace) {
        textColour = THEME_COLOURS.text;
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
        const traceColour = marker?.color ?? marker?.line?.color ?? trace.line?.color; /* seeing if any colouring exists */

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
