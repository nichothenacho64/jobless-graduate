import { CHART_7_VALUES } from "../core/config.js";
import { loadChartData } from "../core/data.js";
import { renderChart7ComparisonState } from "../group-field-comparator/render.js";

export async function renderChart7(chartId) {
    const { chartData, chartMetadata } = await loadChartData(chartId);
    const disciplineFamilies = [];

    for (let family in CHART_7_VALUES.disciplineFamilies) {
        disciplineFamilies.push({
            family,
            label: family
        });
    }

    const chartState = {
        comparisonKind: "demographic",
        disciplineFamily: disciplineFamilies[0].family,
        selectorIdByKind: {}
    };

    const dropdownMenu = document.getElementById("chart7DropdownMenu");
    const familyDropdownMenu = document.getElementById("chart7FamilyDropdownMenu");
    const modeButton = document.getElementById("chart7ModeButton");

    renderChart7ComparisonState(chartId, chartData, chartMetadata, chartState, disciplineFamilies);

    dropdownMenu.addEventListener("click", (event) => { /* activated once a dropdown item is clicked on */
        const dropdownItem = event.target.closest(".dropdown-item");
        if (!dropdownItem) return;

        chartState.selectorIdByKind[chartState.comparisonKind] = dropdownItem.dataset.selectorId;
        renderChart7ComparisonState(chartId, chartData, chartMetadata, chartState, disciplineFamilies);
    });

    familyDropdownMenu.addEventListener("click", (event) => { /* for when a discipline family is selected */
        const dropdownItem = event.target.closest(".dropdown-item");
        if (!dropdownItem) return;

        chartState.disciplineFamily = dropdownItem.dataset.family;
        chartState.selectorIdByKind["discipline"] = null;
        renderChart7ComparisonState(chartId, chartData, chartMetadata, chartState, disciplineFamilies);
    });

    modeButton.addEventListener("click", () => {
        if (chartState.comparisonKind === "demographic") {
            chartState.comparisonKind = "discipline";
        } else {
            chartState.comparisonKind = "demographic";
        }

        renderChart7ComparisonState(chartId, chartData, chartMetadata, chartState, disciplineFamilies);
    });
}
