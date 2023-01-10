import os
import glob
import statistics
import logging
from datetime import date
from pyvisa import VisaIOError
from backend.globals.excel import Excel
from backend.instruments.Ectron import Ectron1140A
from backend.instruments.Instruments import Instr
from backend.instruments.Ectron import type_e_ranges, type_j_ranges, type_k_ranges, type_t_ranges
from backend.globals.settings import SL_PROC_FULL_PATH, PROJECT_ROOT_DIR, ELECTRICAL_REPORTS_FULL_PATH, STDDATA_PATH, \
    INSTR_DICT, RESOURCE_MANAGER, AUTOSAVE_PATH, USER_DEFAULTS, rss, PASS, PASS_DAG, FAIL_DAG, FAIL, fh
import eel


""" 
Footer Information 
"""
SOFTWARE_VERSION = '2.0.0'  # Do not forget to update txt file!
RELEASE_DATE = 'January 5, 2023'
PROCEDURE = 'SL0881'
FRONTEND_DEV = 'Andy Davis'
BACKEND_DEV = 'Andy Davis'


""" 
Logging updates 
"""
daq_log = logging.getLogger('MUX CARDS')
daq_log.setLevel(logging.INFO)
daq_log.addHandler(fh)


""" 
Path routes 
"""
SL_PATH = os.path.join(fr'{SL_PROC_FULL_PATH}\{PROCEDURE}')
DAQ_ROOT_DIR = os.path.join(fr'{PROJECT_ROOT_DIR}\backend\daq')
DAQ_REPORT_PATH = os.path.join(fr'{ELECTRICAL_REPORTS_FULL_PATH}\Temperature\Module Temp Cards')
DATASHEET_PATH = os.path.join(fr'{DAQ_ROOT_DIR}')
APPDATA_PATH = os.path.join(fr'{DAQ_ROOT_DIR}\AppData')  # TODO: Change when done


"""
Instrument variables
"""
STANDARDS_LOADED = False

UUT = None
TC_SIMULATOR = None

uut_id = ''
uut_model = ''
uut_serial = ''
temper = 0.0
humid = 0.0
probe_id = ''
type_e_channel = 201
type_j_channel = 206
type_k_channel = 211
type_t_channel = 217
mainframe = 1

temp_settle = 300


"""
Excel information
"""
EXCEL_TEMPLATE = 'MuxCard Datasheet'
# 34970/34980 values
E_34970_TEMPS = [-190, -80, 0, 200, 990]
J_34970_TEMPS = [-200, -80, 0, 200, 1190]
K_34970_TEMPS = [-190, -80, 0, 200, 1200]
T_34970_TEMPS = [-190, -80, 0, 100, 395]

# DAQ970 values
E_DAQ970_TEMPS = [-200, -80, 0, 200, 1000]
J_DAQ970_TEMPS = [-210, -80, 0, 200, 1200]
K_DAQ970_TEMPS = [-195, -80, 0, 200, 1200]
T_DAQ970_TEMPS = [-200, -80, 0, 100, 400]

type_e_results = [[], [], [], [], []]
type_j_results = [[], [], [], [], []]
type_k_results = [[], [], [], [], []]
type_t_results = [[], [], [], [], []]

type_e_acceptance = []
type_j_acceptance = []
type_k_acceptance = []
type_t_acceptance = []
final_acceptance = [0, 0, 0, 0]


DATASHEET_COLUMNS = ['S', 'T', 'U', 'V', 'W']
DATASHEET_ROWS = [11, 17, 23, 29]


"""
Instrument variables
"""
uut_specs_dict = {}
tc_sim_specs_dict = {}


"""
State and wrappers, aka safety / fallback stuff
"""
STATE = 0  # check to see at what point the calibration is at
SUB_STATE = 0  # check to see at what point the calibration is at
STOP = False  # will be used to close opened threads
CALLBACK_RETURN = None


def instr_wrapper(instr, func_name, *args, **kwargs):
    global STOP, CALLBACK_RETURN
    exception_types = (VisaIOError, AttributeError, Exception)

    try:
        CALLBACK_RETURN = getattr(instr, func_name)(*args, **kwargs)
    except exception_types as e:
        if isinstance(e, VisaIOError):
            daq_log.error('Error communicating with Instruments.  Please check your instrument connections and try '
                          'again.')
            daq_log.info('Attempting to reconnect...')
            STOP = True
        return False
    else:
        return True


"""
Functions for Eel
"""


@eel.expose
def daq_logger(message):
    daq_log.info(message)


@eel.expose
def daq_software_notes():
    return [SOFTWARE_VERSION, RELEASE_DATE, PROCEDURE, FRONTEND_DEV, BACKEND_DEV]


@eel.expose
def daq_get_temp_settle(letter):
    return [temp_settle, letter]


@eel.expose
def daq_get_state():
    return STATE


@eel.expose
def daq_stop_tests(stop):
    global STOP
    STOP = stop


@eel.expose
def daq_initial_excel_save():
    excel = Excel(DATASHEET_PATH, uut_id, EXCEL_TEMPLATE)
    excel.save(AUTOSAVE_PATH)


@eel.expose
def daq_ending_excel_save(result):
    adds = ['_A', '_B', '_C', '_D', '_E']
    index = 0

    # Save excel to proper folder
    excel = Excel(AUTOSAVE_PATH, uut_id)

    if result == 1:
        excel.write('E7', 'AS RECEIVED')
    elif result == 2:
        excel.write('E7', 'FINAL')
    else:
        excel.write('E7', 'AS RECEIVED / FINAL')

    # Cal Report folder
    folder = fr'{DAQ_REPORT_PATH}\{uut_id}'
    save_file = excel.fname

    # Check if file folder exists, otherwise create it
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Check if file already exists in the folder, change file name if so
    while os.path.exists(fr'{folder}\{save_file}'):
        checks = save_file[-7:-5]
        if checks in adds:
            save_file = save_file[:-7] + adds[index] + save_file[-5:]
        else:
            save_file = save_file[:-5] + adds[index] + save_file[-5:]
        excel.fname = save_file
        index += 1

    excel.save(folder)
    os.startfile(fr'"{folder}\{save_file}"')

    daq_reset_final_acceptance()

    # Search for UUT files in autosaves
    uut_files = glob.glob(fr'{AUTOSAVE_PATH}\{uut_id}*')
    for file in uut_files:
        os.remove(file)


@eel.expose
def daq_excel_info():
    excel = Excel(AUTOSAVE_PATH, uut_id)

    excel.write('H4', date.today().strftime('%#m/%#d/%Y'))  # Date
    excel.write('H5', USER_DEFAULTS['initials'])
    excel.write('F4', uut_id)
    excel.write('D4', uut_model)
    excel.write('D5', uut_serial)
    excel.write('L5', temper)
    excel.write('M5', humid)
    excel.write('L39', probe_id)

    excel.save(AUTOSAVE_PATH)


@eel.expose
def daq_test_setup(settings: dict):
    global uut_id, uut_model, uut_serial, type_e_channel, type_j_channel, type_k_channel, type_t_channel, \
        temper, humid, temp_settle, mainframe, probe_id

    for key, val in settings.items():
        if key == 'id':
            if val is None:
                uut_id = ''
            elif val != uut_id:
                uut_id = val
                daq_log.info(f'UUT ID updated to {val}')
        elif key == 'model':
            if val is None:
                uut_model = ''
            elif val != uut_model:
                uut_model = val
                daq_log.info(f'UUT Model updated to {val}')
        elif key == 'serial':
            if val is None:
                uut_serial = ''
            elif uut_serial != val:
                uut_serial = val
                daq_log.info(f'UUT Serial updated to {val}')
        elif key == 'type_e':
            if type_e_channel != int(val):
                type_e_channel = int(val)
                daq_log.info(f'Type E Channel updated to {val}')
        elif key == 'type_j':
            if type_j_channel != int(val):
                type_j_channel = int(val)
                daq_log.info(f'Type J Channel updated to {val}')
        elif key == 'type_k':
            if type_k_channel != int(val):
                type_k_channel = int(val)
                daq_log.info(f'Type K Channel updated to {val}')
        elif key == 'type_t':
            if type_t_channel != int(val):
                type_t_channel = int(val)
                daq_log.info(f'Type T Channel updated to {val}')
        elif key == 'temp':
            temper = float(val)
        elif key == 'humid':
            humid = float(val)
        elif key == 'settle':
            temp_settle_min = float(val)
            temp_settle_sec = temp_settle_min * 60
            if temp_settle != temp_settle_sec:
                temp_settle = temp_settle_sec
                daq_log.info(f'Temperature Settle Time updated to {val} mins')
        elif key == 'main':
            mainframe = int(val)
        elif key == 'probe_id':
            if val is None:
                probe_id = ''
            else:
                probe_id = val
        else:
            daq_log.warning(f'{key} not saved')
            continue


@eel.expose
def daq_show_setup() -> list:
    global uut_id, uut_model, uut_serial, temp_settle

    temp_settle_min = temp_settle / 60

    setups = [uut_id, uut_model, uut_serial, type_e_channel, type_j_channel, type_k_channel, type_t_channel,
              temp_settle_min]

    return setups


@eel.expose
def daq_get_type_e() -> list:
    if 'DAQ' in uut_model:
        setts = ['DAQ', type_e_channel, E_DAQ970_TEMPS[0], E_DAQ970_TEMPS[1], E_DAQ970_TEMPS[2], E_DAQ970_TEMPS[3],
                 E_DAQ970_TEMPS[4]]
    elif '21A' in uut_model:
        setts = ['21', type_e_channel, E_34970_TEMPS[0], E_34970_TEMPS[1], E_34970_TEMPS[2], E_34970_TEMPS[3],
                 E_34970_TEMPS[4]]
    else:
        setts = ['nope', type_e_channel, E_34970_TEMPS[0], E_34970_TEMPS[1], E_34970_TEMPS[2], E_34970_TEMPS[3],
                 E_34970_TEMPS[4]]

    return setts


@eel.expose
def daq_get_type_j() -> list:
    if 'DAQ' in uut_model:
        setts = ['DAQ', type_j_channel, J_DAQ970_TEMPS[0], J_DAQ970_TEMPS[1], J_DAQ970_TEMPS[2], J_DAQ970_TEMPS[3],
                 J_DAQ970_TEMPS[4]]
    elif '21A' in uut_model:
        setts = ['21', type_j_channel, J_34970_TEMPS[0], J_34970_TEMPS[1], J_34970_TEMPS[2], J_34970_TEMPS[3],
                 J_34970_TEMPS[4]]
    else:
        setts = ['nope', type_j_channel, J_34970_TEMPS[0], J_34970_TEMPS[1], J_34970_TEMPS[2], J_34970_TEMPS[3],
                 J_34970_TEMPS[4]]

    return setts


@eel.expose
def daq_get_type_k() -> list:
    if 'DAQ' in uut_model:
        setts = ['DAQ', type_k_channel, K_DAQ970_TEMPS[0], K_DAQ970_TEMPS[1], K_DAQ970_TEMPS[2], K_DAQ970_TEMPS[3],
                 K_DAQ970_TEMPS[4]]
    elif '21A' in uut_model:
        setts = ['21', type_k_channel, K_34970_TEMPS[0], K_34970_TEMPS[1], K_34970_TEMPS[2], K_34970_TEMPS[3],
                 K_34970_TEMPS[4]]
    else:
        setts = ['nope', type_k_channel, K_34970_TEMPS[0], K_34970_TEMPS[1], K_34970_TEMPS[2], K_34970_TEMPS[3],
                 K_34970_TEMPS[4]]

    return setts


@eel.expose
def daq_get_type_t() -> list:
    if 'DAQ' in uut_model:
        setts = ['DAQ', type_t_channel, T_DAQ970_TEMPS[0], T_DAQ970_TEMPS[1], T_DAQ970_TEMPS[2], T_DAQ970_TEMPS[3],
                 T_DAQ970_TEMPS[4]]
    elif '21A' in uut_model:
        setts = ['21', type_t_channel, T_34970_TEMPS[0], T_34970_TEMPS[1], T_34970_TEMPS[2], T_34970_TEMPS[3],
                 T_34970_TEMPS[4]]
    else:
        setts = ['nope', type_t_channel, T_34970_TEMPS[0], T_34970_TEMPS[1], T_34970_TEMPS[2], T_34970_TEMPS[3],
                 T_34970_TEMPS[4]]

    return setts


@eel.expose
# Set UUT Specs from Data file
def daq_set_uut_specs(frame: int):  # TODO: add dictionary for spec values from database
    if frame == 2:
        model = 'DAQ970A'
    else:
        model = '34970A'
    path = fr'{APPDATA_PATH}\{model}.txt'
    try:
        fhand = open(path, 'r')
    except:
        daq_log.warning('UUT is new to the program.  Please add UUT Specs')
        return

    with fhand:
        for line in fhand:
            line = line.rstrip()

            if line == '':
                continue

            temp_line = line.split(',')
            try:
                uut_specs_dict[temp_line[0]] = float(temp_line[1])
            except:
                uut_specs_dict[temp_line[0]] = temp_line[1]

    return uut_specs_dict


@eel.expose
def daq_save_uut_specs(model: str, settings: list, values: list):
    together = zip(settings, values)
    fname = fr'{APPDATA_PATH}\{model}.txt'

    with open(fname, 'w+') as specs:
        for sp in together:
            specs.write(f'{sp[0]},{sp[1]}\n')

    daq_log.info(f'{model} Specs saved')


@eel.expose
# Set STD Specs from Data file
def daq_set_std_specs(model: str):  # TODO: add dictionary for spec values from database
    path = fr'{STDDATA_PATH}\{model}.ini'
    try:
        fhand = open(path, 'r')
    except:
        daq_log.warning(f'{model} is new to the program.  Please add STD Specs')
        return

    with fhand:
        for line in fhand:
            line = line.rstrip()

            if line == '':
                continue

            temp_line = line.split(',')
            try:
                tc_sim_specs_dict[temp_line[0]] = float(temp_line[1])
            except:
                tc_sim_specs_dict[temp_line[0]] = temp_line[1]

    return tc_sim_specs_dict


@eel.expose
def daq_save_std_specs(model: str, settings: list, values: list):
    together = zip(settings, values)
    fname = fr'{STDDATA_PATH}\{model}.txt'

    with open(fname, 'w+') as specs:
        for sp in together:
            specs.write(f'{sp[0]},{sp[1]}\n')

    daq_log.info(f'{model} Specs saved')


@eel.expose
def daq_check_stds() -> list:
    global UUT
    global TC_SIMULATOR
    global STANDARDS_LOADED
    main = False
    mod = False
    ect = False
    ect_idn = 'Communication Error'
    card_type = 'Communication Error'
    main_model = '34970A'

    for model in INSTR_DICT.keys():
        if '1140A' in model[0]:
            TC_SIMULATOR = INSTR_DICT[model]
            ect = True
        elif model[0] in ('34970A', 'DAQ970A', '34980A'):
            UUT = INSTR_DICT[model]
            main = True

    if ect:
        ect_instr = Instr(TC_SIMULATOR)
        ect_idn = ect_instr.get_info()
        ect_instr.close()

    if main:
        main_instr = RESOURCE_MANAGER.open_resource(UUT)
        idn = main_instr.query('*IDN?').split(',')
        main_model = idn[1]
        card = main_instr.query('SYST:CTYPE? 200').split(',')
        if card != '0':
            card_type = f'Keysight {card[1]}'
            mod = True
        main_instr.close()

    if ect and mod:
        STANDARDS_LOADED = True

    return [ect_idn, card_type, main_model]


@eel.expose
def daq_get_stds_loaded() -> bool:
    return STANDARDS_LOADED


@eel.expose
def daq_setup_standards():
    ectron = Ectron1140A(TC_SIMULATOR)

    # Make sure all Ectron settings are correct
    ectron.set_mat_alloy()
    ectron.set_term_tc()
    ectron.set_source_mode()
    ectron.set_temperature_mode()
    ectron.set_temperature_units_c()

    ectron.close()


@eel.expose
def daq_get_type_e_acceptance() -> list:
    return type_e_acceptance


@eel.expose
def daq_get_type_j_acceptance() -> list:
    return type_j_acceptance


@eel.expose
def daq_get_type_k_acceptance() -> list:
    return type_k_acceptance


@eel.expose
def daq_get_type_t_acceptance() -> list:
    return type_t_acceptance


@eel.expose
def daq_get_final_acceptance() -> list:
    return final_acceptance


@eel.expose
def daq_reset_final_acceptance():
    global final_acceptance
    for x, _ in enumerate(final_acceptance):
        final_acceptance[x] = 0


@eel.expose
def daq_open_report_path():
    os.startfile(fr"{DAQ_REPORT_PATH}")


"""
Functions from Eel
"""


def tests_screen(message: str, end: str = '<br/>') -> None:
    eel.daq_tests_print(f'{message}{end}')

    if '<br/>' in message:
        message = message.replace('<br/>', '')
    daq_log.info(message)


def type_e_screen(message: str, end: str = '<br/>') -> None:
    eel.daq_type_e_print(f'{message}{end}')

    if '<br/>' in message:
        message = message.replace('<br/>', '')
    daq_log.info(message)


def type_j_screen(message: str, end: str = '<br/>') -> None:
    eel.daq_type_j_print(f'{message}{end}')

    if '<br/>' in message:
        message = message.replace('<br/>', '')
    daq_log.info(message)


def type_k_screen(message: str, end: str = '<br/>') -> None:
    eel.daq_type_k_print(f'{message}{end}')

    if '<br/>' in message:
        message = message.replace('<br/>', '')
    daq_log.info(message)


def type_t_screen(message: str, end: str = '<br/>') -> None:
    eel.daq_type_t_print(f'{message}{end}')

    if '<br/>' in message:
        message = message.replace('<br/>', '')
    daq_log.info(message)


"""
Tolerance Functions
"""


# Calculate Combined Uncertainty -- assumes 95% confidence, k Value of 2
def calculate_uncertainty(tc_type: str, setpoint: float, results: list) -> float:
    if tc_type not in ['E', 'J', 'K', 'T']:
        return 0

    std_resolution = tc_sim_specs_dict['Resolution']
    uut_resolution = uut_specs_dict['Resolution']

    uut_stdev = statistics.stdev(results)

    std_acc = 0
    if tc_type == 'E':
        for num in sorted(type_e_ranges.keys()):
            if setpoint < num:
                std_acc = tc_sim_specs_dict[f'Type{tc_type}Range{type_e_ranges[num]}']
                break
    elif tc_type == 'J':
        for num in sorted(type_j_ranges.keys()):
            if setpoint < num:
                std_acc = tc_sim_specs_dict[f'Type{tc_type}Range{type_j_ranges[num]}']
                break
    elif tc_type == 'K':
        for num in sorted(type_k_ranges.keys()):
            if setpoint < num:
                std_acc = tc_sim_specs_dict[f'Type{tc_type}Range{type_k_ranges[num]}']
                break
    elif tc_type == 'T':
        for num in sorted(type_t_ranges.keys()):
            if setpoint < num:
                std_acc = tc_sim_specs_dict[f'Type{tc_type}Range{type_t_ranges[num]}']
                break

    std_uncertainty = std_acc / 1.96
    sum_square = rss(std_uncertainty, std_resolution, uut_resolution, uut_stdev)
    combined = sum_square * 2

    return combined


def acceptance_criteria(tc_type: str, setpoint: float, results: list, daqm: bool = False) -> str:
    if tc_type == 'E' or tc_type == 'J':
        if setpoint < -150:
            tolerance = uut_specs_dict[f'Type{tc_type}Low']
        else:
            tolerance = uut_specs_dict[f'Type{tc_type}High']
    else:
        if setpoint < -100:
            tolerance = uut_specs_dict[f'Type{tc_type}Low']
        else:
            tolerance = uut_specs_dict[f'Type{tc_type}High']

    if daqm:
        reading = round(statistics.mean(results), 2)
        upperbound = round(setpoint + tolerance, 2)
        lowerbound = round(setpoint - tolerance, 2)
    else:
        reading = round(statistics.mean(results), 1)
        upperbound = round(setpoint + tolerance, 1)
        lowerbound = round(setpoint - tolerance, 1)

    # Was trying indeterminate calculations
    uncert = round(calculate_uncertainty(tc_type, setpoint, results), 3)
    indeterminate_pos = reading + uncert
    indeterminate_neg = reading - uncert

    if lowerbound <= reading <= upperbound:
        if lowerbound <= indeterminate_neg and indeterminate_pos <= upperbound:
            return PASS
        else:
            return PASS_DAG
    else:
        if reading < lowerbound:
            if lowerbound <= indeterminate_pos:
                return FAIL_DAG
            else:
                return FAIL
        else:
            if indeterminate_neg <= upperbound:
                return FAIL_DAG
            else:
                return FAIL
