export function createChart7DropdownItems(dropdownMenu, items, dataKey = "selectorId") {
    dropdownMenu.replaceChildren();

    for (let item of items) {
        const listItem = document.createElement("li");
        const dropdownItem = document.createElement("button");

        dropdownItem.className = "dropdown-item";
        dropdownItem.type = "button";
        dropdownItem.dataset[dataKey] = item[dataKey];
        dropdownItem.textContent = item.label;

        listItem.appendChild(dropdownItem);
        dropdownMenu.appendChild(listItem);
    }
}

export function updateChart7DropdownSelection(dropdownButton, dropdownMenu, items, selectedValue, dataKey = "selectorId") {
    let selectedItem = items[0];

    for (let item of items) {
        if (item[dataKey] === selectedValue) {
            selectedItem = item;
        }
    }

    dropdownButton.textContent = selectedItem.label;

    for (let dropdownItem of dropdownMenu.querySelectorAll(".dropdown-item")) {
        const isSelectedItem = dropdownItem.dataset[dataKey] === selectedItem[dataKey];
        dropdownItem.classList.toggle("active", isSelectedItem);
    }

    return selectedItem[dataKey];
}
