export function transformValue(value) { /* turns all numeric values into integers */
    if (typeof value !== "string") return value;

    if (value.trim() === "") return value;

    const numericValue = Number(value.trim());
    if (Number.isFinite(numericValue)) return numericValue;

    return value;
}

export function capitaliseWord(word) {
    return word.charAt(0).toUpperCase() + word.slice(1);
}

export function unpack(data, key) {
    return data.map(row => row[key]);
}

export function sortAscending(a, b) {
    return a - b;
}

export function sortByKeyAscending(items, key) {
    return items.sort((a, b) => sortAscending(a[key], b[key]));
}

function createNumberArray(values) { /* creates an array with solely numeric values */
    const numericValues = [];

    for (let value of values) {
        const numericValue = Number(value);

        if (Number.isFinite(numericValue)) {
            numericValues.push(numericValue);
        }
    }

    return numericValues;
}

export function clampValue(value, min, max) {
    return Math.min(Math.max(value, min), max);
}

export function getRoundedNonNegativeValue(value) {
    return Math.max(0, Math.round(value ?? 0));
}

export function calculateMedian(values) {
    const numericValues = createNumberArray(values);

    numericValues.sort(sortAscending);

    const middleIndex = Math.floor(numericValues.length / 2);

    if (numericValues.length % 2 === 1) {
        return numericValues[middleIndex];
    }

    return (numericValues[middleIndex - 1] + numericValues[middleIndex]) / 2;
}

export function formatOneDecimal(value) {
    return Number(value).toFixed(1);
}

export function objectHasValues(object, keys) {
    if (!object) return false;

    for (let key of keys) {
        const value = object[key];

        if (value === undefined || value === null || value === "") {
            return false; /* if no value exists for the key, return false */
        }
    }

    return true;
}

export function joinArrayWithCommas(items) {
    let joinedItems = "";

    for (let i = 0; i < items.length; i++) {
        if (i > 0) {
            joinedItems += ", ";
        }

        joinedItems += items[i];
    }

    return joinedItems;
}

export function joinItemsWithAnd(items) { /* joins items with commas and & before the last item */
    let joinedItems = "";

    for (let i = 0; i < items.length; i++) {
        const item = items[i];
        const isFirstItem = i === 0;
        const isFinalItem = i === items.length - 1;

        if (isFirstItem) {
            joinedItems += item;
        } else if (isFinalItem) {
            joinedItems += " & " + item;
        } else {
            joinedItems += ", " + item;
        }
    }

    return joinedItems;
}
