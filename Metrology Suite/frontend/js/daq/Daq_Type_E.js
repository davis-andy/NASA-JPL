// Variable for correct channel
let channel;

// Show channel and setpoints
function daq_show_type_e(setups) {
    if (setups[0] === '21') {
        daq_type_e_test_channel_col.addClass('error-hide');
        daq_type_e_test_channel_double_col.removeClass('error-hide');
        daq_type_e_test_channel_double.val(setups[1]);
    }
    else {
        daq_type_e_test_channel_col.removeClass('error-hide');
        daq_type_e_test_channel_double_col.addClass('error-hide');
        daq_type_e_test_channel.val(setups[1]);
    }

    channel = setups[1];
    daq_type_e_1.val(setups[2]);
    daq_type_e_2.val(setups[3]);
    daq_type_e_3.val(setups[4]);
    daq_type_e_4.val(setups[5]);
    daq_type_e_5.val(setups[6]);
}

// Highlight border with Acceptance color
function daq_show_acceptance(accept) {
    if (~accept[0].indexOf('Fail'))
        fail_border(daq_type_e_1);
    else if (~accept[0].indexOf('Pass'))
        pass_border(daq_type_e_1);
    else
        reset_border(daq_type_e_1);

    if (~accept[1].indexOf('Fail'))
        fail_border(daq_type_e_2);
    else if (~accept[1].indexOf('Pass'))
        pass_border(daq_type_e_2);
    else
        reset_border(daq_type_e_2);

    if (~accept[2].indexOf('Fail'))
        fail_border(daq_type_e_3);
    else if (~accept[2].indexOf('Pass'))
        pass_border(daq_type_e_3);
    else
        reset_border(daq_type_e_3);

    if (~accept[3].indexOf('Fail'))
        fail_border(daq_type_e_4);
    else if (~accept[3].indexOf('Pass'))
        pass_border(daq_type_e_4);
    else
        reset_border(daq_type_e_4);

    if (~accept[4].indexOf('Fail'))
        fail_border(daq_type_e_5);
    else if (~accept[4].indexOf('Pass'))
        pass_border(daq_type_e_5);
    else
        reset_border(daq_type_e_5);
}

// Color border for Fails
eel.expose(daq_typeEFails)
function daq_typeEFails(content) {
    switch (content) {
        case 1:
            fail_border(daq_type_e_1);
            break;
        case 2:
            fail_border(daq_type_e_2);
            break;
        case 3:
            fail_border(daq_type_e_3);
            break;
        case 4:
            fail_border(daq_type_e_4);
            break;
        case 5:
            fail_border(daq_type_e_5);
            break;
    }
}

// Color border for Passes
eel.expose(daq_typeEPass)
function daq_typeEPass(content) {
    switch (content) {
        case 1:
            pass_border(daq_type_e_1);
            break;
        case 2:
            pass_border(daq_type_e_2);
            break;
        case 3:
            pass_border(daq_type_e_3);
            break;
        case 4:
            pass_border(daq_type_e_4);
            break;
        case 5:
            pass_border(daq_type_e_5);
            break;
    }
}

// Reset border colors
eel.expose(daq_resetTypeEFails)
function daq_resetTypeEFails() {
    daq_type_e_result(0);
    daq_type_e_print_area.html('');
    reset_border(daq_type_e_1);
    reset_border(daq_type_e_2);
    reset_border(daq_type_e_3);
    reset_border(daq_type_e_4);
    reset_border(daq_type_e_5);
}

// Insert Connect modal button actions
$(function(){
    daq_type_e_modal_btn.click(function () {
        let setpoints = [daq_type_e_1.val(), daq_type_e_2.val(), daq_type_e_3.val(), daq_type_e_4.val(), daq_type_e_5.val()];
        eel.daq_run_type_e_params(channel, setpoints)();
    });
});

// Show results of test
eel.expose(daq_type_e_result)
function daq_type_e_result(result) {
    if (result === 1) {  // Fail
        daq_type_e_none.addClass('error-hide');
        daq_type_e_pass.addClass('error-hide');
        daq_type_e_pass_dag.addClass('error-hide');
        daq_type_e_fail_dag.addClass('error-hide');
        daq_type_e_fail.removeClass('error-hide');
    }
    else if (result === 2) {  // Fail Dagger
        daq_type_e_none.addClass('error-hide');
        daq_type_e_pass.addClass('error-hide');
        daq_type_e_pass_dag.addClass('error-hide');
        daq_type_e_fail_dag.removeClass('error-hide');
        daq_type_e_fail.addClass('error-hide');
    }
    else if (result === 3) {  // Pass Dagger
        daq_type_e_none.addClass('error-hide');
        daq_type_e_pass.addClass('error-hide');
        daq_type_e_pass_dag.removeClass('error-hide');
        daq_type_e_fail_dag.addClass('error-hide');
        daq_type_e_fail.addClass('error-hide');
    }
    else if (result === 4) {  // Pass
        daq_type_e_none.addClass('error-hide');
        daq_type_e_pass.removeClass('error-hide');
        daq_type_e_pass_dag.addClass('error-hide');
        daq_type_e_fail_dag.addClass('error-hide');
        daq_type_e_fail.addClass('error-hide');
    }
    else {
        daq_type_e_none.removeClass('error-hide');
        daq_type_e_pass.addClass('error-hide');
        daq_type_e_pass_dag.addClass('error-hide');
        daq_type_e_fail_dag.addClass('error-hide');
        daq_type_e_fail.addClass('error-hide');
    }
}

// Channel dropdown actions
$(function(){
    daq_type_e_test_channel.change(function () {
        channel = daq_type_e_test_channel.val();
    });
});

// Channel dropdown actions
$(function(){
    daq_type_e_test_channel_double.change(function () {
        channel = daq_type_e_test_channel_double.val();
    });
});

// Print to screen
eel.expose(daq_type_e_print)
function daq_type_e_print(words) {
    let area = daq_type_e_print_area.html();
    let results = words.split(' ');
    let newHTML = '';
    newHTML += area;
    if (words.includes('Pass'))
        newHTML += results[0] + ' <span class="alert-success-text">' + results[1] + '</span>';
    else if (words.includes('Fail'))
        newHTML += results[0] + ' <span class="alert-danger-text">' + results[1] + '</span>';
    else
        newHTML += words;

    daq_type_e_print_area.html(newHTML);
}

// Run button actions
$(function(){
    daq_run_type_e.click(function () {
        daq_type_e_modal.modal('toggle');
    });
});


// Get channel and setpoints from backend
eel.daq_get_type_e()(daq_show_type_e);
// Get Pass/Fail from backend
eel.daq_get_type_e_acceptance()(daq_show_acceptance);