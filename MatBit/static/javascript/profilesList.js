
// From: https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function decrementAccountNumber() {
    const titleField = document.querySelector("#title");
    let title = titleField.value;
    const components = title.split(" ");

    title = (Number(components[0]) - 1) + components[1];
    titleField.value = title;
}

async function deleteProfile(event, form) {
    if (event.preventDefault) {
       event.preventDefault();
    }

    if (!form) {
        form = event.target;
    }

    //const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const csrfToken = getCookie("csrftoken");
    const userID = form.querySelector("input[name='userID']").value;

    await fetch(window.location, {
        headers: { "X-CSRFToken": csrfToken, "Content-Type": "application/x-www-form-urlencoded" },
        credentials: "include",
        method: "POST",
        mode: "same-origin",
        body: new URLSearchParams(new FormData(form))
    }).then(response => response.json()).then(response => {
        if (response.didDelete) {
            decrementAccountNumber();
            const container = document.querySelector("#userContainer" + userID);
            container.parentNode.removeChild(container);
        } else {
            alert("Action failed\n" + response.message);
        }
    }).catch(error => {
        console.log(error);
        alert("Action failed\n" + "unknown error");
    });

    return false;
}