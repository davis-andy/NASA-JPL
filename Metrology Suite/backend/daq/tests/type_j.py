from backend.daq.settings import J_34970_TEMPS, J_DAQ970_TEMPS, tests_screen, type_j_results, type_j_screen, \
    DATASHEET_COLUMNS, acceptance_criteria, type_j_acceptance, DATASHEET_ROWS, final_acceptance
import backend.daq.settings as settings
from backend.instruments.Ectron import Ectron1140A
from backend.instruments.Keysight import Keysight34970A
from backend.globals.excel import Excel
from backend.globals.settings import AUTOSAVE_PATH, FAIL, FAIL_DAG, PASS_DAG
from statistics import mean
import eel

ectron: Ectron1140A
daq: Keysight34970A
daqm: bool
temps: list


@eel.expose
def daq_setup_type_j():
    global ectron, daq
    ectron = Ectron1140A(settings.TC_SIMULATOR)
    daq = Keysight34970A(settings.UUT)

    # Set up Ectron to start settling temp
    ectron.set_temperature_value(0)
    ectron.set_tc_type_j()
    ectron.set_tc_offset_value(value=0)
    ectron.operate()

    # Set up DAQ for current channel
    daq.reset()
    daq.set_temp_tc_j_resol_max(settings.type_j_channel)
    daq.set_temp_tc_ref_jun_type_int(settings.type_j_channel)
    daq.set_temp_units_c_channel(settings.type_j_channel)
    daq.set_temp_nplc()
    daq.set_trig_count()
    daq.set_scan_list(settings.type_j_channel)
    daq.set_monitor_channel(settings.type_j_channel)
    daq.set_monitor_on()


@eel.expose
def daq_run_type_j():
    global daqm, temps, ectron, daq
    type_j_acceptance.clear()
    for sett in type_j_results:
        sett.clear()
    excel = Excel(AUTOSAVE_PATH, settings.uut_id)

    # Determine setpoints based on mainframe
    if settings.mainframe == 2:
        temps = J_DAQ970_TEMPS
        daqm = True
    else:
        temps = J_34970_TEMPS
        daqm = False

    tests_screen('Beginning Type J Test...<br/>')
    row = DATASHEET_ROWS[1]

    # Start taking measurements
    for x, temp in enumerate(temps):
        # Check if STOP button was pressed
        if settings.STOP:
            tests_screen('<br/>Test has been aborted<br/>')
            settings.SUB_STATE -= 1
            ectron.close()
            daq.close()
            return

        # Check at which point the program stopped previously
        if settings.SUB_STATE > x:
            row += 1
            continue

        # Set Ectron to correct temp
        ectron.set_temperature_value(temp)
        tests_screen(f'Applied temperature: {temp:.2f}°C')
        eel.sleep(1)

        # Get UUT readings
        readings = daq.get_measurements()
        avg = mean(readings)
        # Save the 5 readings to excel
        for y, result in enumerate(readings):
            type_j_results[x].append(result)
            excel.write(f'{DATASHEET_COLUMNS[y]}{row}', type_j_results[x][y])
            eel.sleep(0.5)
        # Get the Acceptance Criteria
        pass_fail = acceptance_criteria('J', temp, type_j_results[x], daqm)
        excel.write(f'G{row}', pass_fail)
        type_j_acceptance.append(pass_fail)

        # Print result to screen
        if settings.mainframe == 2:  # DAQ970A resolution of 2
            tests_screen(f'Measured Temp: {avg:.2f}°C')
        else:  # others have resolution of 1
            tests_screen(f'Measured Temp: {avg:.1f}°C')
        tests_screen(f'Result: {pass_fail}<br/>')

        # Get things ready for next setpoint
        row += 1
        settings.SUB_STATE += 1
        eel.sleep(0.5)

    # Get STDs ready for next test
    daq.set_monitor_off()
    ectron.set_temperature_value(0)
    ectron.standby()
    excel.save(AUTOSAVE_PATH)

    # Print Acceptance Criteria to screen (worst one only)
    if FAIL in type_j_acceptance:
        eel.daq_tests_type_j_result(1)
        final_acceptance[1] = 1
    elif FAIL_DAG in type_j_acceptance:
        eel.daq_tests_type_j_result(2)
        final_acceptance[1] = 2
    elif PASS_DAG in type_j_acceptance:
        eel.daq_tests_type_j_result(3)
        final_acceptance[1] = 3
    else:
        eel.daq_tests_type_j_result(4)
        final_acceptance[1] = 4

    # Finish test, start next one
    tests_screen('Finished Type J Test.<br/>')
    settings.SUB_STATE = 0
    settings.STATE = 2
    ectron.close()
    daq.close()
    eel.daq_toggle_modal('K')


@eel.expose
def daq_run_type_j_params(channel, setpoints: list):
    global daqm, temps, ectron, daq
    type_j_acceptance.clear()
    for sett in type_j_results:
        sett.clear()

    excel = Excel(AUTOSAVE_PATH, settings.uut_id)
    ectron = Ectron1140A(settings.TC_SIMULATOR)
    daq = Keysight34970A(settings.UUT)

    # Set up Ectron to start settling temp
    ectron.set_temperature_value(0)
    ectron.set_tc_type_j()
    ectron.set_tc_offset_value(value=0)
    ectron.operate()

    # Set up DAQ for current channel
    daq.reset()
    daq.set_temp_tc_j_resol_max(channel)
    daq.set_temp_tc_ref_jun_type_int(channel)
    daq.set_temp_units_c_channel(channel)
    daq.set_temp_nplc()
    daq.set_trig_count()
    daq.set_scan_list(channel)
    daq.set_monitor_channel(channel)
    daq.set_monitor_on()

    # Convert setpoints to Float
    setp = [float(tep) for tep in setpoints]

    # Write correct setpoints on datasheet
    for x, setts in enumerate(setp):
        num = x + DATASHEET_ROWS[1]
        excel.write(f'C{num}', setts)

    # Determine type of Mainframe
    if settings.mainframe == 2:
        daqm = True
    else:
        daqm = False

    eel.daq_resetTypeJFails()
    type_j_screen('Beginning Type J Test...<br/>')
    row = DATASHEET_ROWS[1]

    eel.sleep(2)

    # Start taking measurements
    for x, temp in enumerate(setp):
        # Check if STOP button was pressed
        if settings.STOP:
            type_j_screen('<br/>Test has been aborted<br/>')
            settings.SUB_STATE -= 1
            ectron.close()
            daq.close()
            return

        # Check at which point the program stopped previously
        if settings.SUB_STATE > x:
            row += 1
            continue

        # Set Ectron to correct temp
        ectron.set_temperature_value(temp)
        type_j_screen(f'Applied temperature: {temp:.2f}°C')
        eel.sleep(1)

        # Get UUT readings
        readings = daq.get_measurements()
        avg = mean(readings)
        # Save the 5 readings to excel
        for y, result in enumerate(readings):
            type_j_results[x].append(result)
            excel.write(f'{DATASHEET_COLUMNS[y]}{row}', type_j_results[x][y])
            eel.sleep(0.5)
        # Get the Acceptance Criteria
        pass_fail = acceptance_criteria('J', temp, type_j_results[x], daqm)
        excel.write(f'G{row}', pass_fail)
        type_j_acceptance.append(pass_fail)

        # Print result to screen
        if settings.mainframe == 2:  # DAQ970A resolution of 2
            type_j_screen(f'Measured Temp: {avg:.2f}°C')
        else:  # others have resolution of 1
            type_j_screen(f'Measured Temp: {avg:.1f}°C')
        type_j_screen(f'Result: {pass_fail}<br/>')

        # Color border based on Acceptance Criteria
        if FAIL in pass_fail:
            eel.daq_typeJFails(x + 1)
        else:
            eel.daq_typeJPass(x + 1)

        # Get things ready for next setpoint
        row += 1
        settings.SUB_STATE += 1
        eel.sleep(0.5)

    # Get STDs ready for next test
    daq.set_monitor_off()
    ectron.set_temperature_value(0)
    ectron.standby()
    excel.save(AUTOSAVE_PATH)

    # Print Acceptance Criteria to screen (worst one only)
    if FAIL in type_j_acceptance:
        eel.daq_type_j_result(1)
        final_acceptance[1] = 1
    elif FAIL_DAG in type_j_acceptance:
        eel.daq_type_j_result(2)
        final_acceptance[1] = 2
    elif PASS_DAG in type_j_acceptance:
        eel.daq_type_j_result(3)
        final_acceptance[1] = 3
    else:
        eel.daq_type_j_result(4)
        final_acceptance[1] = 4

    # Finish test
    type_j_screen('Finished Type J Test.<br/>')
    settings.SUB_STATE = 0
    ectron.close()
    daq.close()
