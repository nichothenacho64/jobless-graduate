import {
    FONT_FAMILY,
    GLOBAL_TRACES,
    HOVER_LABEL_RENDERING,
    THEME_COLOURS
} from "../core/config.js";

export function applyHoverLabelLayoutDefaults(layout) {
    return {
        ...layout,
        hoverlabel: {
            ...layout.hoverlabel,
            font: {
                ...layout.hoverlabel?.font,
                family: FONT_FAMILY
            }
        }
    };
}

function getHoverLabelTraceColour(trace) {
    const markerColour = trace.marker?.color;

    if (markerColour && markerColour !== THEME_COLOURS.background) {
        return markerColour;
    }

    return trace.marker?.line?.color ||
        markerColour ||
        trace.line?.color ||
        HOVER_LABEL_RENDERING.defaultShadowColour;
}

function getHoverLabelDefaults(trace) {
    const colour = getHoverLabelTraceColour(trace);

    return {
        ...GLOBAL_TRACES.hoverlabel,
        bgcolor: colour,
        bordercolor: colour,
        font: {
            ...GLOBAL_TRACES.hoverlabel.font
        }
    };
}

export function applyHoverLabelTraceDefaults(trace) {
    return {
        ...trace,
        hoverlabel: getHoverLabelDefaults(trace)
    };
}

function getRoundedRectPath(x, y, width, height, radius) {
    const right = x + width;
    const bottom = y + height;

    return `M${x + radius},${y}` +
        `H${right - radius}` +
        `Q${right},${y} ${right},${y + radius}` +
        `V${bottom - radius}` +
        `Q${right},${bottom} ${right - radius},${bottom}` +
        `H${x + radius}` +
        `Q${x},${bottom} ${x},${bottom - radius}` +
        `V${y + radius}` +
        `Q${x},${y} ${x + radius},${y}` +
        "Z";
}

function roundHoverLabels(chart) {
    const hoverLabels = chart.querySelectorAll(".hoverlayer .hovertext");

    for (let hoverLabel of hoverLabels) {
        const path = hoverLabel.querySelector("path");

        if (!path) return;

        const fillColour = path.style.fill || HOVER_LABEL_RENDERING.defaultShadowColour;
        hoverLabel.style.setProperty("--shadow-colour", fillColour);

        const box = path.getBBox();
        const radius = Math.min(HOVER_LABEL_RENDERING.borderRadius, box.width / 2, box.height / 2);

        const roundedPath = getRoundedRectPath(box.x, box.y, box.width, box.height, radius);

        path.setAttribute("d", roundedPath);
    }
}

export function resetHoverLabelHandler(chart) {
    if (chart.__hoverLabelState) {
        chart.__hoverLabelState.observer.disconnect();
    }

    const hoverLayer = chart.querySelector(".hoverlayer");

    if (!hoverLayer) return;

    const observer = new MutationObserver(() => {
        roundHoverLabels(chart);
    });

    observer.observe(hoverLayer, {
        childList: true,
        subtree: true
    });

    chart.__hoverLabelState = { observer };
}
