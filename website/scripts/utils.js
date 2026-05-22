export function transformValue(value) {
    if (typeof value !== "string") return value;

    if (value.trim() === "") return value;

    const numericValue = Number(value.trim());
    if (Number.isFinite(numericValue)) return numericValue;

    return value;
}

export function formatPercentage(value) {
    return Number.isFinite(value) ? `${value}%` : value;
}

export function unpack(data, key) {
    return data.map(row => row[key]);
}

export function capitaliseWord(word) {
    return word.charAt(0).toUpperCase() + word.slice(1);
}

export function createNumberList(value) {
    let numberArray = [];
    
    for (let i = 1; i <= value; i++) {
        numberArray.push(i);
    }
    return numberArray;
}
