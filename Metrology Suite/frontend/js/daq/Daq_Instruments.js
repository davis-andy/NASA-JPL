// Variable to check if instruments are connected
let loaded;

// Function to show correct instrument image and information
function change_info(info) {
    daq_ectron_info.html(info[0]);
    daq_card_info.html(info[1]);
    daq_mainframe_model.html(info[2]);

    switch (info[2]) {
        case '34980A':
            daq_mainframe_img.attr('src', '../../images/daq/34980A_front.png');
            break;
        case 'DAQ970A':
            daq_mainframe_img.attr('src', '../../images/daq/DAQ970A_front.png');
            break;
        default:
            daq_mainframe_img.attr('src', '../../images/daq/34970A_front.png');
            break;
    }
}

// Get loaded variable from backend to frontend
function instrs_loaded(loads) {
    loaded = loads;
}

// Modal button action
$(function(){
    daq_instr_modal_rescan.click(function () {
        daq_rescan_modal.modal('toggle');
        eel.set_instrs()();
        location.reload();
    });
});

// Rescan button action
$(function(){
    daq_rescan.click(function () {
        daq_rescan_modal.modal('toggle');
        eel.set_instrs()();
        location.reload();
    });
});

// Previous button action
$(function(){
    daq_instr_prev.click(function () {
        location.href = '../daq/index.html';
    });
});

// Setup button action
$(function(){
    daq_instr_setup.click(function () {
        if (loaded) {
            eel.daq_set_std_specs('Ectron1140A')();  // TODO: I don't like this hardcoded
            eel.daq_setup_standards()();
            location.href = '../daq/setup.html';
        }
        else
            daq_instr_modal.modal('toggle');
    });
});

// Tests button action
$(function(){
    daq_instr_tests.click(function () {
        daq_instr_tests_modal.modal('toggle');
    });
});

// Next button action
$(function(){
    daq_instr_next.click(function () {
        if (loaded) {
            eel.daq_set_std_specs('Ectron1140A')();  // TODO: I don't like this hardcoded
            eel.daq_setup_standards()();
            location.href = '../daq/setup.html';
        }
        else
            daq_instr_modal.modal('toggle');
    });
});


// Get instrument information from backend
eel.daq_check_stds()(change_info);
// Get loaded variable from backend
eel.daq_get_stds_loaded()(instrs_loaded);