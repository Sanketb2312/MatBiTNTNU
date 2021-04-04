

export function field(name) {
    const object = document.querySelector("#" + name);

    if (object === null) {
        throw "No such field: \"" + name + "\"";
    }

    return object;
}

export function setDateLimits(fieldName, minDate, maxDate) {
    const field = field(fieldName);

    if (minDate != null) {
        field.min = minDate.toISOString().split("T")[0];
    }
    if (maxDate != null) {
        field.max = maxDate.toISOString().split("T")[0];
    }
}