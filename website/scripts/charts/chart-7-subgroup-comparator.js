import { CHART_7_CARD_LABELS, CHART_7_ELEMENT_IDS } from "../config.js";
import { loadChartData } from "../data.js";
import {
    createChart7DropdownItems,
    getChart7Selectors,
    renderChart7SelectedComparison,
    updateChart7DropdownSelection,
} from "../subgroup-comparator-helpers.js";

export async function renderChart7(chartId) {
    const { chartData, chartMetadata } = await loadChartData(chartId);
    const selectors = getChart7Selectors(chartData);

    const dropdownButton = document.getElementById(CHART_7_ELEMENT_IDS.dropdownButton);
    const dropdownMenu = document.getElementById(CHART_7_ELEMENT_IDS.dropdownMenu);
    const selectorLabel = document.getElementById(CHART_7_ELEMENT_IDS.selectorLabel);
    const explanationCard = document.getElementById(CHART_7_ELEMENT_IDS.explanationCard);

    selectorLabel.textContent = CHART_7_CARD_LABELS.selector;
    createChart7DropdownItems(dropdownMenu, selectors);

    const defaultSelectorId = selectors[0].selectorId;
    const selectorId = updateChart7DropdownSelection(dropdownButton, dropdownMenu, selectors, defaultSelectorId);

    console.log(selectors);
    console.log(selectors[0].selectorId);
    console.log(selectorId);

    renderChart7SelectedComparison(
        chartId,
        chartData,
        chartMetadata,
        selectorId,
        explanationCard
    );

    dropdownMenu.addEventListener("click", (event) => {
        const dropdownItem = event.target.closest(".dropdown-item");
        if (!dropdownItem) return;

        const newSelectorId = dropdownItem.dataset.selectorId;
        const selectorId = updateChart7DropdownSelection(dropdownButton, dropdownMenu, selectors, newSelectorId);

        renderChart7SelectedComparison(
            chartId,
            chartData,
            chartMetadata,
            selectorId,
            explanationCard
        );
    });
}
