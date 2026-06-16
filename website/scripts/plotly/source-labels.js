import { SOURCE_LABEL_TEXT } from "../core/config.js";
import { objectHasValues, getRoundedNonNegativeValue } from "../core/utils.js";
import { getChartElementId } from "./rendering.js";

function resolveSourceLabel(source, sourceKey, sourceLabels) {
    const sourceLabelFieldSets = {
        reportFigure: ["source_system", "source", "figure", "description"],
        absTable: ["source_system", "dataset", "table_number", "sheet_title"],
        numberedSheet: ["source_system", "dataset", "sheet_number", "sheet_title"],
        datasetSheet: ["source_system", "dataset", "sheet_title"]
    };

    if (objectHasValues(source, sourceLabelFieldSets.reportFigure)) {
        return `${source.source_system} ${source.source}, ${source.figure} – ${source.description}`;
    }

    if (objectHasValues(source, sourceLabelFieldSets.absTable)) {
        return `${source.source_system} ${source.dataset} Table ${source.table_number} – ${source.sheet_title}`;
    }

    if (objectHasValues(source, sourceLabelFieldSets.numberedSheet)) {
        return `${source.source_system} ${source.dataset} Sheet ${source.sheet_number} – ${source.sheet_title}`;
    }

    if (objectHasValues(source, sourceLabelFieldSets.datasetSheet)) {
        return `${source.source_system} ${source.dataset} – ${source.sheet_title}`;
    }

    const fallbackLabel = sourceLabels[sourceKey];

    if (fallbackLabel) return fallbackLabel; /* in case no source key is found */
    return "N/A";
}

function getSourceLabels(chartMetadata) {
    const sources = chartMetadata?.sources;
    const fallbackSourceLabels = chartMetadata?.labels?.sources ?? {};
    const sourceLabels = [];

    if (!sources) return sourceLabels;

    for (let sourceKey in sources) {
        const sourceLabel = resolveSourceLabel(sources[sourceKey], sourceKey, fallbackSourceLabels);

        if (!sourceLabel) continue;

        if (!sourceLabels.includes(sourceLabel)) {
            sourceLabels.push(sourceLabel);
        }
    }

    return sourceLabels;
}

function getSourceLabelInsets(chart) {
    const chartSize = chart?._fullLayout?._size;

    if (!chartSize) {
        return { left: 0, right: 0 };
    }

    return {
        left: getRoundedNonNegativeValue(chartSize.l),
        right: getRoundedNonNegativeValue(chartSize.r)
    };
}

function applySourceLabelInsets(sourceLabel, chart) {
    const { left, right } = getSourceLabelInsets(chart);

    sourceLabel.style.setProperty("--left-inset", `${left}px`); /* responsively setting the insets */
    sourceLabel.style.setProperty("--right-inset", `${right}px`);
}

function renderSourceLabelContents(sourceLabel, sourceLabels) {
    if (sourceLabels.length === 1) {
        sourceLabel.textContent = `${SOURCE_LABEL_TEXT.singular}: ${sourceLabels[0]}`;
        return;
    }

    const sourceHeading = document.createElement("div");
    sourceHeading.textContent = `${SOURCE_LABEL_TEXT.plural}:`;

    const sourceList = document.createElement("ul");

    for (let label of sourceLabels) {
        const sourceItem = document.createElement("li");
        sourceItem.textContent = label;
        sourceList.appendChild(sourceItem);
    }

    sourceLabel.replaceChildren(sourceHeading, sourceList);
}

export function renderChartSourceLabel(chartId, chartMetadata, chart) {
    const chartElementId = getChartElementId(chartId);
    const chartElement = document.getElementById(chartElementId);
    const sourceLabelId = chartElementId + "Sources";
    let sourceLabel = document.getElementById(sourceLabelId);
    const sourceLabels = getSourceLabels(chartMetadata);

    if (sourceLabels.length === 0) {
        sourceLabel?.remove();
        return;
    }

    if (!sourceLabel) {
        sourceLabel = document.createElement("div");
        sourceLabel.id = sourceLabelId;
        sourceLabel.className = "chart-source-label";
        chartElement.insertAdjacentElement("afterend", sourceLabel);
    }

    renderSourceLabelContents(sourceLabel, sourceLabels);
    applySourceLabelInsets(sourceLabel, chart);
}
