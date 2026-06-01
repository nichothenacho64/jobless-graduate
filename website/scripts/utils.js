export function transformValue(value) {
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

function createNumberArray(values) {
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
