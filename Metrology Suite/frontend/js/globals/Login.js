// Get information from back
eel.get_user_setting('user')(load_user);
eel.get_user_password()(load_pass);

// If errors, change border color and show text
function loginErrors(content, content_error) {
    content_error.removeClass('error-hide');
    fail_border(content);
}

// If no more errors, reset border color and hide text
function resetFormErrors() {
    username_error.addClass('error-hide');
    reset_border(username);

    password_error.addClass('error-hide');
    reset_border(password);

    software_error.addClass('error-hide');
    reset_border(software);
}

// Check for login errors
async function errorCheck(result) {
    resetFormErrors();
    result = result.toLowerCase();

    if (software.val()==='none') loginErrors(software, software_error);

    if (result.includes('password')) {
        loginErrors(password, password_error);
        return false;
    }
    else if (result.includes('user')) {
        loginErrors(username, username_error);
        return false;
    }

    software_select();
}

// Check which software is selected
function software_select() {
    switch (software.val()) {
        case 'daq':
            eel.set_user_settings(['user'],[username.val()])();
            eel.set_user_password(password.val())();
            location.href = '../daq/index.html';
            break;
        default:
            loginErrors(software, software_error);
            break;
    }
}

// Change software without re-logging in
function software_select_no_indy() {
    switch (software.val()) {
        case 'daq':
            location.href = '../daq/index.html';
            break;
        default:
            loginErrors(software, software_error);
            break;
    }
}

// Show username
function load_user(user) {
    if (user === 'False' || user === '') {
        username.val('');
    } else {
        username.val(user);
    }
}

// Show password
function load_pass(pass) {
    if (pass === 'False' || pass === '') {
        password.val('');
    } else {
        password.val(pass);
    }
}

// Validate login
function validate() {
    eel.indy_login(username.val(), password.val())(errorCheck);
}

// Software switch no login
function no_indy() {
    software_select_no_indy();
}