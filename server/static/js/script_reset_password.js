const form = document.getElementById("login-reset-form");
const submit = document.getElementById("submit-button");

function passwordsCheck() {
    password = form.password.value;
    password_verify = form.password_verify.value;

    if (password.length < 8) {
        submit.disabled = true;
        form.password.style["border"] = "3px solid #ff0000";
        form.password_verify.style["border"] = "3px solid #ff0000";
        return;
    } else {
        if (form.password.matches(":hover")) {
            form.password.style["border"] = "3px solid #ffffff";
        } else {
            form.password.style["border"] = "3px solid #cccccc";
        }
    }

    if (password == password_verify) {
        submit.disabled = false;
        if (form.password_verify.matches(":hover")) {
            form.password_verify.style["border"] = "3px solid #ffffff";
        } else {
            form.password_verify.style["border"] = "3px solid #cccccc";
        }
    } else {
        submit.disabled = true;
        form.password_verify.style["border"] = "3px solid #ff0000";
    }
}

function passwordHover() {
    password = form.password.value;

    if (password.length > 0 && password.length < 8) {
        form.password.style["border"] = "3px solid #ff0000";
    } else {
        form.password.style["border"] = "3px solid #ffffff";
    }
}
function passwordUnHover() {
    password = form.password.value;

    if (password.length > 0 && password.length < 8) {
        form.password.style["border"] = "3px solid #ff0000";
    } else {
        form.password.style["border"] = "3px solid #cccccc";
    }
}

function passwordVerifyHover() {
    password = form.password.value;
    password_verify = form.password_verify.value;

    if (password == password_verify) {
        form.password_verify.style["border"] = "3px solid #ffffff";
    }
}
function passwordVerifyUnHover() {
    password = form.password.value;
    password_verify = form.password_verify.value;

    if (password == password_verify) {
        form.password_verify.style["border"] = "3px solid #cccccc";
    }
}
