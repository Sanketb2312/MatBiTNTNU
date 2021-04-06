function validateLogin(){
    let email = window.document.login_form.email.value;
    let password = window.document.login_form.password.value;
    if (!email || !password){
        document.getElementById("error_message").textContent = "Du må ha med brukernavn og passord"
        return false;
    }
    else {
        return true;
    }
}
