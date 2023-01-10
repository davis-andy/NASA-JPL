// Model dropdown actions
$(function() {
    let mainframe;
    daq_uut_model_dropdown.change(function () {
        if (daq_uut_model_dropdown.val() === 'DAQ970A') {
            mainframe = 2;
        }
        else mainframe = 1;
        eel.daq_set_uut_specs(mainframe)(daq_assign_uut_specs);
    });
});

// Show UUT specs
function daq_assign_uut_specs(specs) {
    if (daq_uut_model_dropdown.val() === 'DAQ970A'){
        // Type E
        try {
            daq_uut_e_low.val(parseFloat(specs[daq_type_e_low]).toFixed(2));
        } catch (error) {
            daq_uut_e_low.val('Undefined');
        }

        try {
            daq_uut_e_high.val(parseFloat(specs[daq_type_e_high]).toFixed(2));
        } catch (error) {
            daq_uut_e_high.val('Undefined');
        }

        // Type J
        try {
            daq_uut_j_low.val(parseFloat(specs[daq_type_j_low]).toFixed(2));
        } catch (error) {
            daq_uut_j_low.val('Undefined');
        }

        try {
            daq_uut_j_high.val(parseFloat(specs[daq_type_j_high]).toFixed(2));
        } catch (error) {
            daq_uut_j_high.val('Undefined');
        }

        // Type K
        try {
            daq_uut_k_low.val(parseFloat(specs[daq_type_k_low]).toFixed(2));
        } catch (error) {
            daq_uut_k_low.val('Undefined');
        }

        try {
            daq_uut_k_high.val(parseFloat(specs[daq_type_k_high]).toFixed(2));
        } catch (error) {
            daq_uut_k_high.val('Undefined');
        }

        // Type T
        try {
            daq_uut_t_low.val(parseFloat(specs[daq_type_t_low]).toFixed(2));
        } catch (error) {
            daq_uut_t_low.val('Undefined');
        }

        try {
            daq_uut_t_high.val(parseFloat(specs[daq_type_t_high]).toFixed(2));
        } catch (error) {
            daq_uut_t_high.val('Undefined');
        }
    }
    else {
        // Type E
        try {
            daq_uut_e_low.val(parseFloat(specs[daq_type_e_low]).toFixed(1));
        } catch (error) {
            daq_uut_e_low.val('Undefined');
        }

        try {
            daq_uut_e_high.val(parseFloat(specs[daq_type_e_high]).toFixed(1));
        } catch (error) {
            daq_uut_e_high.val('Undefined');
        }

        // Type J
        try {
            daq_uut_j_low.val(parseFloat(specs[daq_type_j_low]).toFixed(1));
        } catch (error) {
            daq_uut_j_low.val('Undefined');
        }

        try {
            daq_uut_j_high.val(parseFloat(specs[daq_type_j_high]).toFixed(1));
        } catch (error) {
            daq_uut_j_high.val('Undefined');
        }

        // Type K
        try {
            daq_uut_k_low.val(parseFloat(specs[daq_type_k_low]).toFixed(1));
        } catch (error) {
            daq_uut_k_low.val('Undefined');
        }

        try {
            daq_uut_k_high.val(parseFloat(specs[daq_type_k_high]).toFixed(1));
        } catch (error) {
            daq_uut_k_high.val('Undefined');
        }

        // Type T
        try {
            daq_uut_t_low.val(parseFloat(specs[daq_type_t_low]).toFixed(1));
        } catch (error) {
            daq_uut_t_low.val('Undefined');
        }

        try {
            daq_uut_t_high.val(parseFloat(specs[daq_type_t_high]).toFixed(1));
        } catch (error) {
            daq_uut_t_high.val('Undefined');
        }
    }
}

// Cancel button actions
$(function() {
    daq_uut_specs_cancel.click(function () {
        history.back();
    });
});

// Save button actions
function daq_save_uut_specs() {
    var settings = [daq_type_e_low, daq_type_e_high,
                    daq_type_j_low, daq_type_j_high,
                    daq_type_k_low, daq_type_k_high,
                    daq_type_t_low, daq_type_t_high];
    var values = [daq_uut_e_low.val(), daq_uut_e_high.val(),
                  daq_uut_j_low.val(), daq_uut_j_high.val(),
                  daq_uut_k_low.val(), daq_uut_k_high.val(),
                  daq_uut_t_low.val(), daq_uut_t_high.val()]

    eel.daq_save_uut_specs(daq_uut_model_dropdown.val(), settings, values)();
    history.back();
}

