
/*
const firstName = "";
const lastName = "";
const birthDate = "";
const address = "";
const post_code = "";
const location = "";
*/

function field(name) {
    const object = document.querySelector("#" + name);

    if (object === null) {
        throw "No such field";
    }

    return object;
}

function setField(name, value) {
    field(name).value = value;
}

/// Adds a subtitle under the input field of name `fieldName`
function setSubtitleForField(fieldName, text) {

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
        console.log("Postcode has incorrect format");
        alert("Postcode has incorrect format");
        return false;
    }

    if (!validatePassword()) {
        console.log("Passwords not equal");
        alert("Passwords not equal");
        return false;
    }

    return true;
}

// TODO: set max date value. Today - 15 years.

if (emailUsed) {
    console.log("E-mail already in use");

    setField("first_name", first_name);
    setField("last_name", last_name);
    setField("birth_date", birth_date);
    setField("address", address);
    setField("post_code", post_code);
    setField("location", location);

    // Set <p> in div form-group for e-mail used.
    setSubtitleForField("email", "Denne e-posten er allerede i bruk")
}