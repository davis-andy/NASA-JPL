from backend.daq.settings import E_34970_TEMPS, E_DAQ970_TEMPS, tests_screen, type_e_results, type_e_screen, \
    DATASHEET_COLUMNS, acceptance_criteria, type_e_acceptance, DATASHEET_ROWS, final_acceptance
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
def daq_setup_type_e():
    global ectron, daq
    ectron = Ectron1140A(settings.TC_SIMULATOR)
    daq = Keysight34970A(settings.UUT)

    # Set up Ectron to start settling temp
    ectron.set_temperature_value(0)
    ectron.set_tc_type_e()
    ectron.set_tc_offset_value(value=0)
    ectron.operate()

    # Set up DAQ for current channel
    daq.reset()
    daq.set_temp_tc_e_resol_max(settings.type_e_channel)
    daq.set_temp_tc_ref_jun_type_int(settings.type_e_channel)
    daq.set_temp_units_c_channel(settings.type_e_channel)
    daq.set_temp_nplc()
    daq.set_trig_count()
    daq.set_scan_list(settings.type_e_channel)
    daq.set_monitor_channel(settings.type_e_channel)
    daq.set_monitor_on()


@eel.expose
def daq_run_type_e():
    global daqm, temps, ectron, daq
    type_e_acceptance.clear()
    for sett in type_e_results:
        sett.clear()
    excel = Excel(AUTOSAVE_PATH, settings.uut_id)

    # Determine setpoints based on mainframe
    if settings.mainframe == 2:
        temps = E_DAQ970_TEMPS
        daqm = True
    else:
        temps = E_34970_TEMPS
        daqm = False

    tests_screen('Beginning Type E Test...<br/>')
    row = DATASHEET_ROWS[0]

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
            type_e_results[x].append(result)
            excel.write(f'{DATASHEET_COLUMNS[y]}{row}', type_e_results[x][y])
            eel.sleep(0.5)
        # Get the Acceptance Criteria
        pass_fail = acceptance_criteria('E', temp, type_e_results[x], daqm)
        excel.write(f'G{row}', pass_fail)
        type_e_acceptance.append(pass_fail)

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
    if FAIL in type_e_acceptance:
        eel.daq_tests_type_e_result(1)
        final_acceptance[0] = 1
    elif FAIL_DAG in type_e_acceptance:
        eel.daq_tests_type_e_result(2)
        final_acceptance[0] = 2
    elif PASS_DAG in type_e_acceptance:
        eel.daq_tests_type_e_result(3)
        final_acceptance[0] = 3
    else:
        eel.daq_tests_type_e_result(4)
        final_acceptance[0] = 4

    # Finish test, start next one
    tests_screen('Finished Type E Test.<br/>')
    settings.SUB_STATE = 0
    settings.STATE = 1
    ectron.close()
    daq.close()
    eel.daq_toggle_modal('J')


@eel.expose
def daq_run_type_e_params(channel, setpoints: list):
    global daqm, temps, ectron, daq
    type_e_acceptance.clear()
    for sett in type_e_results:
        sett.clear()

    excel = Excel(AUTOSAVE_PATH, settings.uut_id)
    ectron = Ectron1140A(settings.TC_SIMULATOR)
    daq = Keysight34970A(settings.UUT)

    # Set up Ectron to start settling temp
    ectron.set_temperature_value(0)
    ectron.set_tc_type_e()
    ectron.set_tc_offset_value(value=0)
    ectron.operate()

    # Set up DAQ for current channel
    daq.reset()
    daq.set_temp_tc_e_resol_max(channel)
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
        num = x + DATASHEET_ROWS[0]
        excel.write(f'C{num}', setts)

    # Determine type of Mainframe
    if settings.mainframe == 2:
        daqm = True
    else:
        daqm = False

    eel.daq_resetTypeEFails()
    type_e_screen('Beginning Type E Test...<br/>')
    row = DATASHEET_ROWS[0]

    eel.sleep(2)

    # Start taking measurements
    for x, temp in enumerate(setp):
        # Check if STOP button was pressed
        if settings.STOP:
            type_e_screen('<br/>Test has been aborted<br/>')
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
        type_e_screen(f'Applied temperature: {temp:.2f}°C')
        eel.sleep(1)

        # Get UUT readings
        readings = daq.get_measurements()
        avg = mean(readings)
        # Save the 5 readings to excel
        for y, result in enumerate(readings):
            type_e_results[x].append(result)
            excel.write(f'{DATASHEET_COLUMNS[y]}{row}', type_e_results[x][y])
            eel.sleep(0.5)
        # Get the Acceptance Criteria
        pass_fail = acceptance_criteria('E', temp, type_e_results[x], daqm)
        excel.write(f'G{row}', pass_fail)
        type_e_acceptance.append(pass_fail)

        # Print result to screen
        if settings.mainframe == 2:  # DAQ970A resolution of 2
            type_e_screen(f'Measured Temp: {avg:.2f}°C')
        else:  # others have resolution of 1
            type_e_screen(f'Measured Temp: {avg:.1f}°C')
        type_e_screen(f'Result: {pass_fail}<br/>')

        # Color border based on Acceptance Criteria
        if FAIL in pass_fail:
            eel.daq_typeEFails(x+1)
        else:
            eel.daq_typeEPass(x+1)

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
    if FAIL in type_e_acceptance:
        eel.daq_type_e_result(1)
        final_acceptance[0] = 1
    elif FAIL_DAG in type_e_acceptance:
        eel.daq_type_e_result(2)
        final_acceptance[0] = 2
    elif PASS_DAG in type_e_acceptance:
        eel.daq_type_e_result(3)
        final_acceptance[0] = 3
    else:
        eel.daq_type_e_result(4)
        final_acceptance[0] = 4

    # Finish test
    type_e_screen('Finished Type E Test.<br/>')
    settings.SUB_STATE = 0
    ectron.close()
    daq.close()
