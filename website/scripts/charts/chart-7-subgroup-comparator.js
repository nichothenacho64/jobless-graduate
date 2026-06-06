import { CHART_7_TEXT, CHART_7_RENDERING } from "../core/config.js";
import { loadChartData } from "../core/data.js";
import {
    createChart7DropdownItems,
    getChart7Selectors,
    renderChart7SelectedComparison,
    updateChart7DropdownSelection,
} from "../interactions/subgroup-comparator.js";

export async function renderChart7(chartId) {
    const { chartData, chartMetadata } = await loadChartData(chartId);
    const selectors = getChart7Selectors(chartData);

    const dropdownButton = document.getElementById(CHART_7_RENDERING.elementIds.dropdownButton);
    const dropdownMenu = document.getElementById(CHART_7_RENDERING.elementIds.dropdownMenu);
    const selectorLabel = document.getElementById(CHART_7_RENDERING.elementIds.selectorLabel);
    const explanationCard = document.getElementById(CHART_7_RENDERING.elementIds.explanationCard);

    selectorLabel.textContent = CHART_7_TEXT.cardLabels.selector;
    createChart7DropdownItems(dropdownMenu, selectors);

    const defaultSelectorId = selectors[0].selectorId; /* for the intial rendering of the dropdown */
    const selectorId = updateChart7DropdownSelection(dropdownButton, dropdownMenu, selectors, defaultSelectorId);

    renderChart7SelectedComparison(chartId, chartData, chartMetadata, selectorId, explanationCard);

    dropdownMenu.addEventListener("click", (event) => { /* activated once a dropdown item is clicked on */
        const dropdownItem = event.target.closest(".dropdown-item");
        if (!dropdownItem) return;

        const newSelectorId = dropdownItem.dataset.selectorId;
        const selectorId = updateChart7DropdownSelection(dropdownButton, dropdownMenu, selectors, newSelectorId);

        renderChart7SelectedComparison(chartId, chartData, chartMetadata, selectorId, explanationCard);
    });
}
