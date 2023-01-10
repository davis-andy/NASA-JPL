// Show Footer information
function software_info(info) {
    daq_version.html(info[0]);
    daq_release.html(info[1]);
    daq_procedure.html(info[2]);
    daq_frontend.html(info[3]);
    daq_backend.html(info[4]);
}

// Get Footer information from backend
eel.daq_software_notes()(software_info)