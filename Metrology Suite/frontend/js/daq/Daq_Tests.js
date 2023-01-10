// Run All button actions
$(function(){
    daq_run_all.click(function () {
        eel.daq_stop_tests(false)();
        eel.daq_get_state()(daq_choose_modal);
    });
});

// Stop button actions
$(function(){
    daq_stop_tests.click(function () {
        eel.daq_stop_tests(true)();
    });
});

// Choose which TC Type to run based on State
function daq_choose_modal(state) {
    if (state === 0)
        daq_toggle_modal('E');
    else if (state === 1)
        daq_toggle_modal('J');
    else if (state === 2)
        daq_toggle_modal('K');
    else if (state === 3)
        daq_toggle_modal('T');
}

// Display Modal of chosen TC Type
eel.expose(daq_toggle_modal)
function daq_toggle_modal(letter){
    if (letter === 'E')
        daq_change_modal_e.modal('toggle');
    else if (letter === 'J')
        daq_change_modal_j.modal('toggle');
    else if (letter === 'K')
        daq_change_modal_k.modal('toggle');
    else if (letter === 'T')
        daq_change_modal_t.modal('toggle');
}

// Setup Type E Test
$(function(){
    daq_tests_e_modal_btn.click(function () {
        eel.daq_setup_type_e()();
        eel.daq_get_temp_settle('E')(daq_begin_test);
    });
});

// Setup Type J Test
$(function(){
    daq_tests_j_modal_btn.click(function () {
        eel.daq_setup_type_j()();
        eel.daq_get_temp_settle('J')(daq_begin_test);
    });
});

// Setup Type K Test
$(function(){
    daq_tests_k_modal_btn.click(function () {
        eel.daq_setup_type_k()();
        eel.daq_get_temp_settle('K')(daq_begin_test);
    });
});

// Setup Type T Test
$(function(){
    daq_tests_t_modal_btn.click(function () {
        eel.daq_setup_type_t()();
        eel.daq_get_temp_settle('T')(daq_begin_test);
    });
});

// Begin countdown for tests
function daq_begin_test(begin) {
    if (begin[1] === 'E')
        countdown(begin[0], eel.daq_run_type_e);
    else if (begin[1] === 'J')
        countdown(begin[0], eel.daq_run_type_j);
    else if (begin[1] === 'K')
        countdown(begin[0], eel.daq_run_type_k);
    else if (begin[1] === 'T')
        countdown(begin[0], eel.daq_run_type_t);
}

// Print to tests screen
eel.expose(daq_tests_print)
function daq_tests_print(words) {
    let area = daq_main_print.html();
    let results = words.split(' ');
    let newHTML = '';
    newHTML += area;
    if (words.includes('Pass'))
        newHTML += results[0] + ' <span class="alert-success-text">' + results[1] + '</span>';
    else if (words.includes('Fail'))
        newHTML += results[0] + ' <span class="alert-danger-text">' + results[1] + '</span>';
    else
        newHTML += words;

    daq_main_print.html(newHTML);
}

// Show Type E Result
eel.expose(daq_tests_type_e_result)
function daq_tests_type_e_result(result) {
    if (result === 1) {  // Fail
        daq_tests_type_e_none.addClass('error-hide');
        daq_tests_type_e_pass.addClass('error-hide');
        daq_tests_type_e_pass_dag.addClass('error-hide');
        daq_tests_type_e_fail_dag.addClass('error-hide');
        daq_tests_type_e_fail.removeClass('error-hide');
    }
    else if (result === 2) {  // Fail Dagger
        daq_tests_type_e_none.addClass('error-hide');
        daq_tests_type_e_pass.addClass('error-hide');
        daq_tests_type_e_pass_dag.addClass('error-hide');
        daq_tests_type_e_fail_dag.removeClass('error-hide');
        daq_tests_type_e_fail.addClass('error-hide');
    }
    else if (result === 3) {  // Pass Dagger
        daq_tests_type_e_none.addClass('error-hide');
        daq_tests_type_e_pass.addClass('error-hide');
        daq_tests_type_e_pass_dag.removeClass('error-hide');
        daq_tests_type_e_fail_dag.addClass('error-hide');
        daq_tests_type_e_fail.addClass('error-hide');
    }
    else if (result === 4) {  // Pass
        daq_tests_type_e_none.addClass('error-hide');
        daq_tests_type_e_pass.removeClass('error-hide');
        daq_tests_type_e_pass_dag.addClass('error-hide');
        daq_tests_type_e_fail_dag.addClass('error-hide');
        daq_tests_type_e_fail.addClass('error-hide');
    }
    else {
        daq_tests_type_e_none.removeClass('error-hide');
        daq_tests_type_e_pass.addClass('error-hide');
        daq_tests_type_e_pass_dag.addClass('error-hide');
        daq_tests_type_e_fail_dag.addClass('error-hide');
        daq_tests_type_e_fail.addClass('error-hide');
    }
}

// Show Type J Result
eel.expose(daq_tests_type_j_result)
function daq_tests_type_j_result(result) {
    if (result === 1) {  // Fail
        daq_tests_type_j_none.addClass('error-hide');
        daq_tests_type_j_pass.addClass('error-hide');
        daq_tests_type_j_pass_dag.addClass('error-hide');
        daq_tests_type_j_fail_dag.addClass('error-hide');
        daq_tests_type_j_fail.removeClass('error-hide');
    }
    else if (result === 2) {  // Fail Dagger
        daq_tests_type_j_none.addClass('error-hide');
        daq_tests_type_j_pass.addClass('error-hide');
        daq_tests_type_j_pass_dag.addClass('error-hide');
        daq_tests_type_j_fail_dag.removeClass('error-hide');
        daq_tests_type_j_fail.addClass('error-hide');
    }
    else if (result === 3) {  // Pass Dagger
        daq_tests_type_j_none.addClass('error-hide');
        daq_tests_type_j_pass.addClass('error-hide');
        daq_tests_type_j_pass_dag.removeClass('error-hide');
        daq_tests_type_j_fail_dag.addClass('error-hide');
        daq_tests_type_j_fail.addClass('error-hide');
    }
    else if (result === 4) {  // Pass
        daq_tests_type_j_none.addClass('error-hide');
        daq_tests_type_j_pass.removeClass('error-hide');
        daq_tests_type_j_pass_dag.addClass('error-hide');
        daq_tests_type_j_fail_dag.addClass('error-hide');
        daq_tests_type_j_fail.addClass('error-hide');
    }
    else {
        daq_tests_type_j_none.removeClass('error-hide');
        daq_tests_type_j_pass.addClass('error-hide');
        daq_tests_type_j_pass_dag.addClass('error-hide');
        daq_tests_type_j_fail_dag.addClass('error-hide');
        daq_tests_type_j_fail.addClass('error-hide');
    }
}

// Show Type K Result
eel.expose(daq_tests_type_k_result)
function daq_tests_type_k_result(result) {
    if (result === 1) {  // Fail
        daq_tests_type_k_none.addClass('error-hide');
        daq_tests_type_k_pass.addClass('error-hide');
        daq_tests_type_k_pass_dag.addClass('error-hide');
        daq_tests_type_k_fail_dag.addClass('error-hide');
        daq_tests_type_k_fail.removeClass('error-hide');
    }
    else if (result === 2) {  // Fail Dagger
        daq_tests_type_k_none.addClass('error-hide');
        daq_tests_type_k_pass.addClass('error-hide');
        daq_tests_type_k_pass_dag.addClass('error-hide');
        daq_tests_type_k_fail_dag.removeClass('error-hide');
        daq_tests_type_k_fail.addClass('error-hide');
    }
    else if (result === 3) {  // Pass Dagger
        daq_tests_type_k_none.addClass('error-hide');
        daq_tests_type_k_pass.addClass('error-hide');
        daq_tests_type_k_pass_dag.removeClass('error-hide');
        daq_tests_type_k_fail_dag.addClass('error-hide');
        daq_tests_type_k_fail.addClass('error-hide');
    }
    else if (result === 4) {  // Pass
        daq_tests_type_k_none.addClass('error-hide');
        daq_tests_type_k_pass.removeClass('error-hide');
        daq_tests_type_k_pass_dag.addClass('error-hide');
        daq_tests_type_k_fail_dag.addClass('error-hide');
        daq_tests_type_k_fail.addClass('error-hide');
    }
    else {
        daq_tests_type_k_none.removeClass('error-hide');
        daq_tests_type_k_pass.addClass('error-hide');
        daq_tests_type_k_pass_dag.addClass('error-hide');
        daq_tests_type_k_fail_dag.addClass('error-hide');
        daq_tests_type_k_fail.addClass('error-hide');
    }
}

// Show Type T Result
eel.expose(daq_tests_type_t_result)
function daq_tests_type_t_result(result) {
    if (result === 1) {  // Fail
        daq_tests_type_t_none.addClass('error-hide');
        daq_tests_type_t_pass.addClass('error-hide');
        daq_tests_type_t_pass_dag.addClass('error-hide');
        daq_tests_type_t_fail_dag.addClass('error-hide');
        daq_tests_type_t_fail.removeClass('error-hide');
    }
    else if (result === 2) {  // Fail Dagger
        daq_tests_type_t_none.addClass('error-hide');
        daq_tests_type_t_pass.addClass('error-hide');
        daq_tests_type_t_pass_dag.addClass('error-hide');
        daq_tests_type_t_fail_dag.removeClass('error-hide');
        daq_tests_type_t_fail.addClass('error-hide');
    }
    else if (result === 3) {  // Pass Dagger
        daq_tests_type_t_none.addClass('error-hide');
        daq_tests_type_t_pass.addClass('error-hide');
        daq_tests_type_t_pass_dag.removeClass('error-hide');
        daq_tests_type_t_fail_dag.addClass('error-hide');
        daq_tests_type_t_fail.addClass('error-hide');
    }
    else if (result === 4) {  // Pass
        daq_tests_type_t_none.addClass('error-hide');
        daq_tests_type_t_pass.removeClass('error-hide');
        daq_tests_type_t_pass_dag.addClass('error-hide');
        daq_tests_type_t_fail_dag.addClass('error-hide');
        daq_tests_type_t_fail.addClass('error-hide');
    }
    else {
        daq_tests_type_t_none.removeClass('error-hide');
        daq_tests_type_t_pass.addClass('error-hide');
        daq_tests_type_t_pass_dag.addClass('error-hide');
        daq_tests_type_t_fail_dag.addClass('error-hide');
        daq_tests_type_t_fail.addClass('error-hide');
    }
}

// Show all results on page load
function daq_show_results(acceptance) {
    daq_tests_type_e_result(acceptance[0]);
    daq_tests_type_j_result(acceptance[1]);
    daq_tests_type_k_result(acceptance[2]);
    daq_tests_type_t_result(acceptance[3]);
}

// As Received button actions
$(function(){
    daq_received.click(function () {
        eel.daq_ending_excel_save(1)();

        let settings = {'id': '', 'model': '', 'serial': ''};
        eel.daq_test_setup(settings)();

        location.href = '../daq/setup.html';
    });
});

// Final button actions
$(function(){
    daq_final.click(function () {
        eel.daq_ending_excel_save(2)();

        let settings = {'id': '', 'model': '', 'serial': ''};
        eel.daq_test_setup(settings)();

        location.href = '../daq/setup.html';
    });
});

// As Received / Final button actions
$(function(){
    daq_received_final.click(function () {
        eel.daq_ending_excel_save(3)();

        let settings = {'id': '', 'model': '', 'serial': ''};
        eel.daq_test_setup(settings)();

        location.href = '../daq/setup.html';
    });
});

// Previous button actions
$(function(){
    daq_tests_prev.click(function () {
        location.href = '../daq/setup.html';
    });
});

// Instruments button actions
$(function(){
    daq_tests_instr.click(function () {
        location.href = '../daq/instruments.html';
    });
});

// Setup button actions
$(function(){
    daq_tests_setup.click(function () {
        location.href = '../daq/setup.html';
    });
});


// Get Final Acceptance from backend
eel.daq_get_final_acceptance()(daq_show_results);