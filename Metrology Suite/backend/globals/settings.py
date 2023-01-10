import pyvisa
import os
import eel
import math
import wmi
import subprocess
import statistics
import time
import logging
from configobj import ConfigObj


""" 
Version
"""
SOFTWARE_VERSION = '0.1.2'


""" 
Path routes 
"""
# Project \ backends \ globals folder
BACKEND_GLOBALS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# Project \ backends \ folder
BACKEND_DIR = os.path.abspath(os.path.join(BACKEND_GLOBALS_DIR, '..'))

# Project folder
PROJECT_ROOT_DIR = os.path.abspath(os.path.join(BACKEND_GLOBALS_DIR, '../..'))

# Virtual Environment Path
VENV_PATH = os.path.abspath(os.path.join(PROJECT_ROOT_DIR, r'\venv\Scripts\python.exe'))

# Desktop and Documents paths
DESKTOP_PATH = os.path.abspath(os.path.join(os.environ['USERPROFILE'], 'Desktop'))  # Windows
DOCUMENTS_PATH = os.path.abspath(os.path.join(os.environ['USERPROFILE'], 'Documents'))  # Windows

# Software files paths
STDDATA_PATH = os.path.join(fr'{PROJECT_ROOT_DIR}\backend\instruments\StdData')
AUTOSAVE_PATH = os.path.join(fr'{PROJECT_ROOT_DIR}\backend\autosaves')


""" 
Logging 
"""
# Set up Log File
login = os.getlogin().upper()
t = time.strftime('%Y-%m-%d %Hh%Mm')
fh = logging.FileHandler(fr'backend\logs\{login}_{t}.log', 'w+')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s:%(levelname)s: %(message)s')
fh.setFormatter(formatter)

logger = logging.getLogger('SUITE')
logger.setLevel(logging.INFO)
logger.addHandler(fh)


""" 
Config Parser for ini files 
"""
USER_SETTINGS = os.path.abspath(os.path.join(BACKEND_GLOBALS_DIR, 'user_settings.ini'))
BENCH_SETTINGS = os.path.abspath(os.path.join(BACKEND_GLOBALS_DIR, 'bench.ini'))
PATHS = os.path.abspath(os.path.join(BACKEND_GLOBALS_DIR, 'file_paths.ini'))  # TODO: Find a better way to do this

# Get User Settings
user_conf = ConfigObj(USER_SETTINGS)
bench_conf = ConfigObj(BENCH_SETTINGS)
path_conf = ConfigObj(PATHS)

# Get User Settings
USER_DEFAULTS = user_conf['DEFAULT']
BENCH_CONFIG = bench_conf['BENCH']
FILE_PATHS = path_conf['PATHS']

METSRV_PATH = FILE_PATHS['metsrv']
SL_PROC_PATH = FILE_PATHS['sl_procedures']
ELECTRICAL_REPORTS_PATH = FILE_PATHS['electrical_cal_reports']
VERSIONS_FILE = FILE_PATHS['versions_file'].strip()
INSTALLER_LAUNCHER = FILE_PATHS['installer_launcher'].strip()
SL_PROC_FULL_PATH = os.path.join(fr'{METSRV_PATH}{SL_PROC_PATH}')
ELECTRICAL_REPORTS_FULL_PATH = os.path.join(fr'{METSRV_PATH}{ELECTRICAL_REPORTS_PATH}')
VERSIONS_FILE_PATH = os.path.join(fr'{METSRV_PATH}{VERSIONS_FILE}')  # TODO: change version path


""" 
Bench Settings 
"""
BENCH_DICT = {}
STANDARD_COUNT: int


def update_bench():
    global BENCH_DICT, STANDARD_COUNT
    BENCH_DICT.clear()
    STANDARD_COUNT = int(BENCH_CONFIG['std_count'])
    for std_num in range(1, STANDARD_COUNT + 1):
        stad = f'STANDARD {std_num}'
        std = BENCH_CONFIG[stad]
        std_id = std['id']
        std_manu = std['manufacturer']
        std_model = std['model']
        std_interval = std['interval']
        BENCH_DICT[std_id] = (std_manu, std_model, std_interval)
    logger.info(BENCH_DICT)


update_bench()


""" 
Tolerance Phrasing 
"""
PASS = 'Pass'
PASS_DAG = 'Pass‡'
FAIL_DAG = 'Fail‡'
FAIL = 'Fail'


""" 
Global Settings 
"""
# Window settings
WINDOW_WIDTH_OFFSET = 16
WINDOW_HEIGHT_OFFSET = 39
WINDOW_WIDTH = int(USER_DEFAULTS['window_width']) + WINDOW_WIDTH_OFFSET
WINDOW_HEIGHT = int(USER_DEFAULTS['window_height']) + WINDOW_HEIGHT_OFFSET

ROM_FILE_TYPE = '*.pdf'

# Instrument settings
RESOURCE_MANAGER = pyvisa.ResourceManager()
gpib_instruments = []
com_instruments = []
usb_instruments = []
INSTR_DICT = {}

# Database settings
APP_NAME = 'Software Suite'
APP_DESCRIPTION = 'In-House Calibration Suite'

# EMS API URL
EMS_API_URL = FILE_PATHS.get('ems_api_url')
LOCATION_DICT = {
    '122-B01': 20,
    '125-B42': 22,
    '125-B64': 24,
    '125-B66': 25,
    '125-B67': 26,
    '125-B68': 27,
    '125-B72': 28,
    '170-120': 30,
    '229-100': 69
}


""" 
Global Variables 
"""

BASE_to_TERA = 10 ** (-12)
BASE_to_GIGA = 10 ** (-9)
BASE_to_MEGA = 10 ** (-6)
BASE_to_KILO = 10 ** (-3)
BASE_to_MILLI = 10 ** 3
BASE_to_MICRO = 10 ** 6
BASE_to_NANO = 10 ** 9
BASE_to_PICO = 10 ** 12
BASE_to_FEMTO = 10 ** 15

TERA_to_BASE = 10 ** 12
GIGA_to_BASE = 10 ** 9
MEGA_to_BASE = 10 ** 6
KILO_to_BASE = 10 ** 3
MILLI_to_BASE = 10 ** (-3)
MICRO_to_BASE = 10 ** (-6)
NANO_to_BASE = 10 ** (-9)
PICO_to_BASE = 10 ** (-12)
FEMTO_to_BASE = 10 ** (-15)

indy_password = ''

original_indexs = ''
comp_ip: str

stddev_threshhold = 0.001  # Arbitrary number
timeout = time.time() + 5  # 5 seconds


""" 
Global Functions 
"""


# Wait until readings are stable
def wait_for_stable(func):
    sdev = 100
    while sdev > stddev_threshhold:
        readings = []
        for _ in range(10):
            readings.append(func())
        sdev = statistics.stdev(readings)
        if time.time() > timeout:
            break


""" 
Functions for Eel 
"""


@eel.expose
def main_logger(message):
    logger.info(message)


@eel.expose
def get_window_offsets():
    return [WINDOW_WIDTH_OFFSET, WINDOW_HEIGHT_OFFSET]


@eel.expose
def set_user_settings(settings: list, values: list):
    for idx, setting in enumerate(settings):
        tmp = get_user_setting(setting)
        if values[idx] != tmp:
            USER_DEFAULTS[setting] = f'{values[idx]}'
            logger.info(f'User setting {setting} changed to {values[idx]}')

    user_conf.write()


@eel.expose
def set_user_password(passw: str):
    global indy_password
    indy_password = passw


@eel.expose
def get_user_setting(setting: str) -> str:
    return USER_DEFAULTS[setting]


@eel.expose
def get_user_settings(settings: list) -> list:
    results = []
    for setting in settings:
        results.append(USER_DEFAULTS[setting])

    return results


@eel.expose
def get_user_password() -> str:
    return indy_password


@eel.expose
def set_bench_configs(values: list):
    for idx, val in enumerate(values):
        if idx == 0:
            BENCH_CONFIG['std_count'] = val
            continue

        if idx % 4 == 0:
            stand = idx // 4
        else:
            stand = (idx // 4) + 1
        std = f'STANDARD {stand}'
        standard = BENCH_CONFIG[std]
        if idx % 4 == 1:
            standard['id'] = val
        elif idx % 4 == 2:
            standard['manufacturer'] = val
        elif idx % 4 == 3:
            standard['model'] = val
        else:
            standard['interval'] = val
        logger.info(f'Bench setting changed to {val}')

    bench_conf.write()
    update_bench()


@eel.expose
def get_bench_configs() -> list:
    results = [BENCH_CONFIG['std_count']]
    for num in range(1, 11):
        stand = BENCH_CONFIG[f'STANDARD {num}']
        results.append(stand['id'])
        results.append(stand['manufacturer'])
        results.append(stand['model'])
        results.append(stand['interval'])

    return results


@eel.expose
def get_nics():
    global original_indexs
    og_index = []
    c = wmi.WMI()
    original = c.Win32_NetworkAdapterConfiguration(IPEnabled=True)
    for orig in original:
        og_index.append(orig.Index)

    for x, idx in enumerate(og_index):
        if x == 0:
            original_indexs = f'{idx}'
        else:
            original_indexs += f'.{idx}'


@eel.expose
def set_ip(addr):
    global comp_ip

    last_period = addr.rfind('.')

    add_one = int(addr[last_period+1:])
    if add_one == 255:
        add_one -= 1
    else:
        add_one += 1
    comp_ip = addr[:last_period+1] + str(add_one)


@eel.expose
def change_ip():
    subprocess.call(fr'python "{BACKEND_GLOBALS_DIR}\network_test.py" {original_indexs} {comp_ip}')


"""
Tolerance Functions
"""


# Root Sum Square
def rss(std_uncert, std_resol, uut_resol, uut_std) -> float:
    sum_square = (std_uncert ** 2) + ((std_resol / math.sqrt(12)) ** 2) + ((uut_resol / math.sqrt(12)) ** 2) + \
              ((uut_std / math.sqrt(5)) ** 2)
    root_ss = math.sqrt(sum_square)
    return root_ss


def calculate_tur(total_uncert: float, uut_acc: float) -> float:
    return round(uut_acc / total_uncert, 2)
