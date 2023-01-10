// Show Standard specs
function daq_assign_std_specs(specs){
    if (daq_std_model_dropdown.val() === 'Ectron1140A')
        // hide other specs, show ectron specs
        assign_ectron_1140a_specs(specs);
}

// Cancel button actions
$(function() {
    daq_std_specs_cancel.click(function () {
        history.back();
    });
});

// Save button actions
function daq_save_std_specs() {
    if (daq_std_model_dropdown.val() === 'Ectron1140A')
        var values = [ectron_1140a_specs_e_range_1.val(), ectron_1140a_specs_e_range_2.val(),
                      ectron_1140a_specs_e_range_3.val(), ectron_1140a_specs_e_range_4.val(),
                      ectron_1140a_specs_e_range_5.val(), ectron_1140a_specs_e_range_6.val(),
                      ectron_1140a_specs_e_range_7.val(),
                      ectron_1140a_specs_j_range_1.val(), ectron_1140a_specs_j_range_2.val(),
                      ectron_1140a_specs_j_range_3.val(), ectron_1140a_specs_j_range_4.val(),
                      ectron_1140a_specs_j_range_5.val(),
                      ectron_1140a_specs_k_range_1.val(), ectron_1140a_specs_k_range_2.val(),
                      ectron_1140a_specs_k_range_3.val(), ectron_1140a_specs_k_range_4.val(),
                      ectron_1140a_specs_k_range_5.val(), ectron_1140a_specs_k_range_6.val(),
                      ectron_1140a_specs_t_range_1.val(), ectron_1140a_specs_t_range_2.val(),
                      ectron_1140a_specs_t_range_3.val(), ectron_1140a_specs_t_range_4.val(),
                      ectron_1140a_specs_t_range_5.val(), ectron_1140a_specs_t_range_6.val(),
                      ectron_1140a_specs_t_range_7.val(),]
        eel.daq_save_std_specs('Ectron1140A', ectron_1140a_specs_settings, values)();
    history.back();
}

// Get STD specs from backend
eel.daq_set_std_specs(daq_std_model_dropdown.val())(daq_assign_std_specs);

