// Tutorial button action
$(function(){
    daq_tutorial.click(function () {
        location.href = '../daq/tutorial.html';
    });
});

// New Calibration button action
$(function(){
    daq_new_cal.click(function () {
        location.href = '../daq/instruments.html';
    });
});

// Resume Calibration button action
$(function(){
    daq_resume_cal.click(function () {
        location.href = '../daq/instruments.html';
    });
});

// Report of Measurement button action
$(function(){
    daq_reports.click(function () {
        eel.daq_open_report_path()();
    });
});