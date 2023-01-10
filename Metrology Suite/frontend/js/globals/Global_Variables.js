let WINDOW_WIDTH_OFFSET;
let WINDOW_HEIGHT_OFFSET;

function set_window_offsets(offsets) {
    WINDOW_WIDTH_OFFSET = offsets[0];
    WINDOW_HEIGHT_OFFSET = offsets[1];
}
eel.get_window_offsets()(set_window_offsets);




// Login
let username = $('#username');
let username_error = $('#username_error');
let password = $('#password');
let password_error = $('#password_error');
let software = $('#softwareOption');
let software_error = $('#software_error');




// User Preferences
let lab = $('#lab');
let initials = $('#initials');
let window_size = $('#window-size');

let user_settings = ['lab', 'initials', 'window_height', 'window_width'];




// Bench config
let std_count = $('#std-count');

// let std1_row = $('#std1');
let std1_id = $('#std1-id');
let std1_manu = $('#std1-manu');
let std1_model = $('#std1-model');
let std1_interval = $('#std1-interval');

let std2_row = $('#std2');
let std2_id = $('#std2-id');
let std2_manu = $('#std2-manu');
let std2_model = $('#std2-model');
let std2_interval = $('#std2-interval');

let std3_row = $('#std3');
let std3_id = $('#std3-id');
let std3_manu = $('#std3-manu');
let std3_model = $('#std3-model');
let std3_interval = $('#std3-interval');

let std4_row = $('#std4');
let std4_id = $('#std4-id');
let std4_manu = $('#std4-manu');
let std4_model = $('#std4-model');
let std4_interval = $('#std4-interval');

let std5_row = $('#std5');
let std5_id = $('#std5-id');
let std5_manu = $('#std5-manu');
let std5_model = $('#std5-model');
let std5_interval = $('#std5-interval');

let std6_row = $('#std6');
let std6_id = $('#std6-id');
let std6_manu = $('#std6-manu');
let std6_model = $('#std6-model');
let std6_interval = $('#std6-interval');

let std7_row = $('#std7');
let std7_id = $('#std7-id');
let std7_manu = $('#std7-manu');
let std7_model = $('#std7-model');
let std7_interval = $('#std7-interval');

let std8_row = $('#std8');
let std8_id = $('#std8-id');
let std8_manu = $('#std8-manu');
let std8_model = $('#std8-model');
let std8_interval = $('#std8-interval');

let std9_row = $('#std9');
let std9_id = $('#std9-id');
let std9_manu = $('#std9-manu');
let std9_model = $('#std9-model');
let std9_interval = $('#std9-interval');

let std10_row = $('#std10');
let std10_id = $('#std10-id');
let std10_manu = $('#std10-manu');
let std10_model = $('#std10-model');
let std10_interval = $('#std10-interval');




// Window resize
function static_window(wsize) {
    window.resizeTo(parseInt(wsize[0])+WINDOW_WIDTH_OFFSET, parseInt(wsize[1])+WINDOW_HEIGHT_OFFSET);
}
eel.get_user_settings(['window_width', 'window_height'])(static_window);




// Countdown Timer
let countdown_modal = $('#countdown');
let timer = $('#timer');
let advance_timer = $('#countdown-advance-btn');
let cancel_timer = $('#countdown-cancel-btn');
let timing;
let funct;

function show_countdown(time) {
    let mins = Math.floor(time / 60) + "";
    let secs = (time % 60) + "";
    if (mins.length < 2) {
        mins = '0' + mins;
    }
    if (secs.length < 2) {
        secs = '0' + secs;
    }
    timer.html(mins + ":" + secs);
}

function startTimer(time) {
    timing = setInterval(function () {
        if (time > 1) {
            time -= 1;
            show_countdown(time);
        } else {
            countdown_modal.modal('toggle');
            clearInterval(timing);
            funct();
        }
    }, 1000);
}

eel.expose(countdown)
function countdown(time, func) {
    funct = func;
    show_countdown(time);
    countdown_modal.modal('toggle');
    startTimer(time);
}

$(function (){
    advance_timer.click(function (){
        clearInterval(timing);
        countdown_modal.modal('toggle');
        funct();
    });
});

$(function (){
    cancel_timer.click(function (){
        clearInterval(timing);
        countdown_modal.modal('toggle');
    });
});




// Border Colors
function fail_border(ids) {
    ids.css('borderColor', '#FF321E');
    ids.css('borderWidth', '0.125rem');
}

function pass_border(ids) {
    ids.css('borderColor', '#00AD69');
    ids.css('borderWidth', '0.125rem');
}

function reset_border(ids) {
    ids.css('borderColor', '#C8C8C8');
    ids.css('borderWidth', '0.063rem');
}