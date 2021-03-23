
function field(name) {
    const object = document.querySelector("#" + name);

    if (object === null) {
        throw "No such field: \"" + name + "\"";
    }

    return object;
}

function setField(name, value) {
    field(name).value = value || "";
}

/// Overwrites or adds a subtitle under the input field of name `fieldName`
function setSubtitleForField(fieldName, text) {
    const inputField = field(fieldName);

    const className = "form-field-subtitle";

    for (const paragraphEntry of inputField.parentNode.querySelectorAll("p").entries()) {
        const paragraph = paragraphEntry[1];

        if (paragraph.classList.contains(className)) {
            paragraph.textContent = text;
            return;
        }
    }

    const paragraph = document.createElement("p");
    paragraph.classList.add(className);
    paragraph.textContent = text;

    inputField.parentNode.insertBefore(paragraph, inputField.nextSibling);
}

function warnProblemForField(fieldName, problemMessage) {
    console.log(problemMessage);
    setSubtitleForField(fieldName, problemMessage);
}

function validatePassword() {
    return field("password").value === field("re_password").value;
}

function validatePostCode() {
    return !/\D/.test(field("post_code").value);
}

function validate() {
    console.log("Validating");

    if (!validatePostCode()) {
        warnProblemForField("post_code", "Feil format på postnummeret");
        return false;
    }

    if (!validatePassword()) {
        warnProblemForField("password", "Passordene må være like");
        return false;
    }

    return true;
}

function init() {

    // Sets a requirement of 15 years or older.
    const maxDate = new Date();
    maxDate.setFullYear(maxDate.getFullYear() - 15);

    field("birth_date").max = maxDate.toISOString().split("T")[0];

    const properties = JSON.parse(document.getElementById("properties").textContent);

    if (properties.emailUsed) {
        console.log("E-mail already in use");

        setField("first_name", properties.firstName);
        setField("last_name", properties.lastName);
        setField("birth_date", properties.birthDate);
        setField("address", properties.address);
        setField("post_code", properties.postCode);
        setField("location", properties.location);

        setSubtitleForField("email", "Denne e-posten er allerede i bruk");
    }
}

document.addEventListener("DOMContentLoaded", init);