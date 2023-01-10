// Variable to save temp probe ID
let temp_id;

// Display information from backend
function daq_show_settings(setups) {
    daq_uut_id.val(setups[0]);
    daq_set_model(setups[1]);
    daq_set_serial(setups[2]);

    daq_type_e_channel.val(setups[3]);
    daq_type_j_channel.val(setups[4]);
    daq_type_k_channel.val(setups[5]);
    daq_type_t_channel.val(setups[6]);

    daq_settle.val(setups[7]);
}

// Get UUT Model and Serial after leaving UUT ID input
$(function(){
    daq_uut_id.blur(function () {
        eel.instr_serial(this.value)(daq_set_serial);
        eel.instr_model(this.value)(daq_set_model);
        eel.daq_reset_final_acceptance()();
    });
});

// Inputs UUT Serial
function daq_set_serial(serial) {
    daq_uut_serial.val(serial);
}

// Inputs UUT Model
function daq_set_model(model) {
    if (model === '' || model === null)
        daq_uut_model.val('none');
    else
        daq_uut_model.val(model);
    daq_model_change();
}

// Get Temp/Humidity data
function daq_get_lab(lab) {
    eel.temp_data(parseInt(lab))(daq_temp_humid);
}

// Input Temp/Humidity data
function daq_temp_humid(th) {
    let temp = th['ch1_temp'];
    let humid = th['ch1_humidity'];
    temp_id = th['sensor1_id'];
    daq_temp.val(parseFloat(temp).toFixed(1));
    daq_humid.val(parseFloat(humid).toFixed(1));
}

// Change channel dropdowns based on model
function daq_model_change() {
    switch (daq_uut_model.val()) {
        case '34921A':
            daq_type_e_channel_col.addClass('error-hide');
            daq_type_j_channel_col.addClass('error-hide');
            daq_type_k_channel_col.addClass('error-hide');
            daq_type_t_channel_col.addClass('error-hide');

            daq_type_e_channel_double_col.removeClass('error-hide');
            daq_type_j_channel_double_col.removeClass('error-hide');
            daq_type_k_channel_double_col.removeClass('error-hide');
            daq_type_t_channel_double_col.removeClass('error-hide');

            daq_type_e_channel_double.val('2001');
            daq_type_j_channel_double.val('2006');
            daq_type_k_channel_double.val('2011');
            daq_type_t_channel_double.val('2016');
            break;
        case '34902A':
            daq_type_e_channel_col.removeClass('error-hide');
            daq_type_j_channel_col.removeClass('error-hide');
            daq_type_k_channel_col.removeClass('error-hide');
            daq_type_t_channel_col.removeClass('error-hide');

            daq_type_e_channel_double_col.addClass('error-hide');
            daq_type_j_channel_double_col.addClass('error-hide');
            daq_type_k_channel_double_col.addClass('error-hide');
            daq_type_t_channel_double_col.addClass('error-hide');

            daq_type_e_channel.val('201');
            daq_type_j_channel.val('206');
            daq_type_k_channel.val('211');
            daq_type_t_channel.val('216');
            break;
        case 'DAQM902A':
            daq_type_e_channel_col.removeClass('error-hide');
            daq_type_j_channel_col.removeClass('error-hide');
            daq_type_k_channel_col.removeClass('error-hide');
            daq_type_t_channel_col.removeClass('error-hide');

            daq_type_e_channel_double_col.addClass('error-hide');
            daq_type_j_channel_double_col.addClass('error-hide');
            daq_type_k_channel_double_col.addClass('error-hide');
            daq_type_t_channel_double_col.addClass('error-hide');

            daq_type_e_channel.val('201');
            daq_type_j_channel.val('206');
            daq_type_k_channel.val('211');
            daq_type_t_channel.val('216');
            break;
        default:
            daq_type_e_channel_col.removeClass('error-hide');
            daq_type_j_channel_col.removeClass('error-hide');
            daq_type_k_channel_col.removeClass('error-hide');
            daq_type_t_channel_col.removeClass('error-hide');

            daq_type_e_channel_double_col.addClass('error-hide');
            daq_type_j_channel_double_col.addClass('error-hide');
            daq_type_k_channel_double_col.addClass('error-hide');
            daq_type_t_channel_double_col.addClass('error-hide');

            daq_type_e_channel.val('201');
            daq_type_j_channel.val('206');
            daq_type_k_channel.val('211');
            daq_type_t_channel.val('217');
            break;
    }
}

// Run channel change function when Model dropdown changes
$(function(){
    daq_uut_model.change(function (){
       daq_model_change();
   });
});

// Save information to the backend
function daq_save_settings() {
    let uut_model = daq_uut_model.val();
    let mainframe = '34970';
    let uut_main;
    let e_channel;
    let j_channel;
    let k_channel;
    let t_channel;

    if (uut_model === null)
        mainframe = '970';
    else if (~uut_model.indexOf('DAQ'))
        mainframe = 'DAQ'
    else if (~uut_model.indexOf('921'))
        mainframe = '980'

    switch (mainframe) {
        case '980':
            uut_main = 3;
            e_channel = daq_type_e_channel_double.val();
            j_channel = daq_type_j_channel_double.val();
            k_channel = daq_type_k_channel_double.val();
            t_channel = daq_type_t_channel_double.val();
            break;
        case 'DAQ':
            uut_main = 2;
            e_channel = daq_type_e_channel.val();
            j_channel = daq_type_j_channel.val();
            k_channel = daq_type_k_channel.val();
            t_channel = daq_type_t_channel.val();
            break;
        default:
            uut_main = 1;
            e_channel = daq_type_e_channel.val();
            j_channel = daq_type_j_channel.val();
            k_channel = daq_type_k_channel.val();
            t_channel = daq_type_t_channel.val();
            break;
    }

    let settings = {'id': daq_uut_id.val(), 'model': uut_model, 'serial': daq_uut_serial.val(),
        'type_e': e_channel, 'type_j': j_channel, 'type_k': k_channel, 'type_t': t_channel,
        'temp': daq_temp.val(), 'humid': daq_humid.val(), 'settle': daq_settle.val(), 'main': uut_main,
        'probe_id': temp_id};

    eel.daq_test_setup(settings)();
    eel.daq_set_uut_specs(uut_main)();
    eel.daq_initial_excel_save()();
    eel.daq_excel_info()();
}


// Previous button actions
$(function(){
    daq_setup_prev.click(function () {
        daq_save_settings();
        location.href = '../daq/instruments.html';
    });
});

// Instruments button actions
$(function(){
    daq_setup_instr.click(function () {
        daq_save_settings();
        location.href = '../daq/instruments.html';
    });
});

// Setup button actions
$(function(){
    daq_setup_setup.click(function () {
        daq_save_settings();
    });
});

// Tests button actions
$(function(){
    daq_setup_tests.click(function () {
        if (!daq_uut_id.val()) {
            daq_setup_modal.modal('toggle');
        }
        else {
            daq_save_settings();
            location.href = '../daq/tests.html';
        }
    });
});

// Next button actions
$(function(){
    daq_setup_next.click(function () {
        if (!daq_uut_id.val()) {
            daq_setup_modal.modal('toggle');
        }
        else {
            daq_save_settings();
            location.href = '../daq/tests.html';
        }
    });
});


// Get saved information from backend
eel.daq_show_setup()(daq_show_settings);
// Get lab number from backend
eel.get_user_setting('lab')(daq_get_lab);