// Save settings to backend
function save_settings() {
    let wheight;
    let wwidth;

    switch (window_size.val()) {
        case '1080':
            wwidth = 1920;
            wheight = 1080;
            break;
        case '900':
            wwidth = 1600;
            wheight = 900;
            break;
        case '720':
            wwidth = 1280;
            wheight = 720;
            break;
    }

    let values = [lab.val(), initials.val(), wheight, wwidth];

    let bench_values = [std_count.val(), std1_id.val(), std1_manu.val(), std1_model.val(), std1_interval.val(),
                        std2_id.val(), std2_manu.val(), std2_model.val(), std2_interval.val(),
                        std3_id.val(), std3_manu.val(), std3_model.val(), std3_interval.val(),
                        std4_id.val(), std4_manu.val(), std4_model.val(), std4_interval.val(),
                        std5_id.val(), std5_manu.val(), std5_model.val(), std5_interval.val(),
                        std6_id.val(), std6_manu.val(), std6_model.val(), std6_interval.val(),
                        std7_id.val(), std7_manu.val(), std7_model.val(), std7_interval.val(),
                        std8_id.val(), std8_manu.val(), std8_model.val(), std8_interval.val(),
                        std9_id.val(), std9_manu.val(), std9_model.val(), std9_interval.val(),
                        std10_id.val(), std10_manu.val(), std10_model.val(),  std10_interval.val()];

    eel.set_user_settings(user_settings, values)();
    eel.set_bench_configs(bench_values)();
    history.back();
}

// Change Window size
function window_size_change() {
    let wheight;
    let wwidth;

    switch (window_size.val()) {
        case '1080':
            wwidth = 1920; // 1904
            wheight = 1080; // 1041
            break;
        case '900':
            wwidth = 1600; // 1584
            wheight = 900; // 861
            break;
        case '720':
            wwidth = 1280; // 1264
            wheight = 720; // 681
            break;
    }

    window.resizeTo(wwidth+WINDOW_WIDTH_OFFSET, wheight+WINDOW_HEIGHT_OFFSET);
}

function show_settings_lab(labs) {
    if (labs === 'None' || labs === '') {
        lab.val(0);
    } else {
        lab.val(labs);
    }
}

function show_settings_initials(initial) {
    if (initial === 'None' || initial === '') {
        initials.val('');
        initials.attr('placeholder', 'Could not get Initials');
    } else {
        initials.val(initial);
    }
}

function show_settings_window_size(wheight) {
    if (wheight === 'None' || wheight === '') {
        window_size.val(0);
    } else {
        window_size.val(wheight);
    }
}

function show_bench_config(bench) {
    try {
        std_count.val((bench[0]));
    } catch (error) {
        std_count.val('4');
    }
    standard_display();


    // Standard 1
    try {
        std1_id.val((bench[1]));
    } catch (error) {
        std1_id.val('Undefined');
    }
    try {
        std1_manu.val((bench[2]));
    } catch (error) {
        std1_manu.val('Undefined');
    }
    try {
        std1_model.val((bench[3]));
    } catch (error) {
        std1_model.val('Undefined');
    }
    try {
        std1_interval.val((bench[4]));
    } catch (error) {
        std1_interval.val('year');
    }


    // Standard 2
    try {
        std2_id.val((bench[5]));
    } catch (error) {
        std2_id.val('Undefined');
    }
    try {
        std2_manu.val((bench[6]));
    } catch (error) {
        std2_manu.val('Undefined');
    }
    try {
        std2_model.val((bench[7]));
    } catch (error) {
        std2_model.val('Undefined');
    }
    try {
        std2_interval.val((bench[8]));
    } catch (error) {
        std2_interval.val('year');
    }


    // Standard 3
    try {
        std3_id.val((bench[9]));
    } catch (error) {
        std3_id.val('Undefined');
    }
    try {
        std3_manu.val((bench[10]));
    } catch (error) {
        std3_manu.val('Undefined');
    }
    try {
        std3_model.val((bench[11]));
    } catch (error) {
        std3_model.val('Undefined');
    }
    try {
        std3_interval.val((bench[12]));
    } catch (error) {
        std3_interval.val('year');
    }


    // Standard 4
    try {
        std4_id.val((bench[13]));
    } catch (error) {
        std4_id.val('Undefined');
    }
    try {
        std4_manu.val((bench[14]));
    } catch (error) {
        std4_manu.val('Undefined');
    }
    try {
        std4_model.val((bench[15]));
    } catch (error) {
        std4_model.val('Undefined');
    }
    try {
        std4_interval.val((bench[16]));
    } catch (error) {
        std4_interval.val('year');
    }


    // Standard 5
    try {
        std5_id.val((bench[17]));
    } catch (error) {
        std5_id.val('Undefined');
    }
    try {
        std5_manu.val((bench[18]));
    } catch (error) {
        std5_manu.val('Undefined');
    }
    try {
        std5_model.val((bench[19]));
    } catch (error) {
        std5_model.val('Undefined');
    }
    try {
        std5_interval.val((bench[20]));
    } catch (error) {
        std5_interval.val('year');
    }


    // Standard 6
    try {
        std6_id.val((bench[21]));
    } catch (error) {
        std6_id.val('Undefined');
    }
    try {
        std6_manu.val((bench[22]));
    } catch (error) {
        std6_manu.val('Undefined');
    }
    try {
        std6_model.val((bench[23]));
    } catch (error) {
        std6_model.val('Undefined');
    }
    try {
        std6_interval.val((bench[24]));
    } catch (error) {
        std6_interval.val('year');
    }


    // Standard 7
    try {
        std7_id.val((bench[25]));
    } catch (error) {
        std7_id.val('Undefined');
    }
    try {
        std7_manu.val((bench[26]));
    } catch (error) {
        std7_manu.val('Undefined');
    }
    try {
        std7_model.val((bench[27]));
    } catch (error) {
        std7_model.val('Undefined');
    }
    try {
        std7_interval.val((bench[28]));
    } catch (error) {
        std7_interval.val('year');
    }


    // Standard 8
    try {
        std8_id.val((bench[29]));
    } catch (error) {
        std8_id.val('Undefined');
    }
    try {
        std8_manu.val((bench[30]));
    } catch (error) {
        std8_manu.val('Undefined');
    }
    try {
        std8_model.val((bench[31]));
    } catch (error) {
        std8_model.val('Undefined');
    }
    try {
        std8_interval.val((bench[32]));
    } catch (error) {
        std8_interval.val('year');
    }


    // Standard 9
    try {
        std9_id.val((bench[33]));
    } catch (error) {
        std9_id.val('Undefined');
    }
    try {
        std9_manu.val((bench[34]));
    } catch (error) {
        std9_manu.val('Undefined');
    }
    try {
        std9_model.val((bench[35]));
    } catch (error) {
        std9_model.val('Undefined');
    }
    try {
        std9_interval.val((bench[36]));
    } catch (error) {
        std9_interval.val('year');
    }


    // Standard 10
    try {
        std10_id.val((bench[37]));
    } catch (error) {
        std10_id.val('Undefined');
    }
    try {
        std10_manu.val((bench[38]));
    } catch (error) {
        std10_manu.val('Undefined');
    }
    try {
        std10_model.val((bench[39]));
    } catch (error) {
        std10_model.val('Undefined');
    }
    try {
        std10_interval.val((bench[40]));
    } catch (error) {
        std10_interval.val('year');
    }
}

// Hide/Show extra standards based on dropdown
function standard_display() {
    switch (std_count.val()) {
        case '1':
            std2_row.addClass('error-hide');
            std3_row.addClass('error-hide');
            std4_row.addClass('error-hide');
            std5_row.addClass('error-hide');
            std6_row.addClass('error-hide');
            std7_row.addClass('error-hide');
            std8_row.addClass('error-hide');
            std9_row.addClass('error-hide');
            std10_row.addClass('error-hide');
            break;
        case '2':
            std2_row.removeClass('error-hide');
            std3_row.addClass('error-hide');
            std4_row.addClass('error-hide');
            std5_row.addClass('error-hide');
            std6_row.addClass('error-hide');
            std7_row.addClass('error-hide');
            std8_row.addClass('error-hide');
            std9_row.addClass('error-hide');
            std10_row.addClass('error-hide');
            break;
        case '3':
            std2_row.removeClass('error-hide');
            std3_row.removeClass('error-hide');
            std4_row.addClass('error-hide');
            std5_row.addClass('error-hide');
            std6_row.addClass('error-hide');
            std7_row.addClass('error-hide');
            std8_row.addClass('error-hide');
            std9_row.addClass('error-hide');
            std10_row.addClass('error-hide');
            break;
        case '4':
            std2_row.removeClass('error-hide');
            std3_row.removeClass('error-hide');
            std4_row.removeClass('error-hide');
            std5_row.addClass('error-hide');
            std6_row.addClass('error-hide');
            std7_row.addClass('error-hide');
            std8_row.addClass('error-hide');
            std9_row.addClass('error-hide');
            std10_row.addClass('error-hide');
            break;
        case '5':
            std2_row.removeClass('error-hide');
            std3_row.removeClass('error-hide');
            std4_row.removeClass('error-hide');
            std5_row.removeClass('error-hide');
            std6_row.addClass('error-hide');
            std7_row.addClass('error-hide');
            std8_row.addClass('error-hide');
            std9_row.addClass('error-hide');
            std10_row.addClass('error-hide');
            break;
        case '6':
            std2_row.removeClass('error-hide');
            std3_row.removeClass('error-hide');
            std4_row.removeClass('error-hide');
            std5_row.removeClass('error-hide');
            std6_row.removeClass('error-hide');
            std7_row.addClass('error-hide');
            std8_row.addClass('error-hide');
            std9_row.addClass('error-hide');
            std10_row.addClass('error-hide');
            break;
        case '7':
            std2_row.removeClass('error-hide');
            std3_row.removeClass('error-hide');
            std4_row.removeClass('error-hide');
            std5_row.removeClass('error-hide');
            std6_row.removeClass('error-hide');
            std7_row.removeClass('error-hide');
            std8_row.addClass('error-hide');
            std9_row.addClass('error-hide');
            std10_row.addClass('error-hide');
            break;
        case '8':
            std2_row.removeClass('error-hide');
            std3_row.removeClass('error-hide');
            std4_row.removeClass('error-hide');
            std5_row.removeClass('error-hide');
            std6_row.removeClass('error-hide');
            std7_row.removeClass('error-hide');
            std8_row.removeClass('error-hide');
            std9_row.addClass('error-hide');
            std10_row.addClass('error-hide');
            break;
        case '9':
            std2_row.removeClass('error-hide');
            std3_row.removeClass('error-hide');
            std4_row.removeClass('error-hide');
            std5_row.removeClass('error-hide');
            std6_row.removeClass('error-hide');
            std7_row.removeClass('error-hide');
            std8_row.removeClass('error-hide');
            std9_row.removeClass('error-hide');
            std10_row.addClass('error-hide');
            break;
        case '10':
            std2_row.removeClass('error-hide');
            std3_row.removeClass('error-hide');
            std4_row.removeClass('error-hide');
            std5_row.removeClass('error-hide');
            std6_row.removeClass('error-hide');
            std7_row.removeClass('error-hide');
            std8_row.removeClass('error-hide');
            std9_row.removeClass('error-hide');
            std10_row.removeClass('error-hide');
            break;
        default:
            std2_row.removeClass('error-hide');
            std3_row.removeClass('error-hide');
            std4_row.removeClass('error-hide');
            std5_row.addClass('error-hide');
            std6_row.addClass('error-hide');
            std7_row.addClass('error-hide');
            std8_row.addClass('error-hide');
            std9_row.addClass('error-hide');
            std10_row.addClass('error-hide');
            break;
    }
}

// Dropdown change function
$(function() {
    std_count.change(function () {
        standard_display();
    });
});

eel.get_user_setting('lab')(show_settings_lab);
eel.get_user_setting('initials')(show_settings_initials);
eel.get_user_setting('window_height')(show_settings_window_size);
eel.get_bench_configs()(show_bench_config);