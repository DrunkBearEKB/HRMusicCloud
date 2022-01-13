const form = document.getElementById("register-form");
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

function loginHover() {
    form.login.style["border"] = "3px solid #ffffff";
}
function loginUnHover() {
    form.login.style["border"] = "3px solid #cccccc";
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

jQuery(($) => {
    $('.div-select-register').on('click', '.div-select-head-register', function () {
        if ($(this).hasClass('open')) {
            $(this).removeClass('open');
            $(this).next().fadeOut();
        } else {
            $('.div-select-head-register').removeClass('open');
            $('.ul-select-list').fadeOut();
            $(this).addClass('open');
            $(this).next().fadeIn();
        }
    });

    $('.div-select-register').on('click', '.li-select-item', function () {
        $('.div-select-head-register').removeClass('open');
        $(this).parent().fadeOut();
        $(this).parent().prev().text($(this).text());
        $(this).parent().prev().prev().val($(this).text());
    });

    $(document).click(function (e) {
        if (!$(e.target).closest('.div-select-register').length) {
            $('.div-select-head-register').removeClass('open');
            $('.ul-select-list').fadeOut();
        }
    });
});