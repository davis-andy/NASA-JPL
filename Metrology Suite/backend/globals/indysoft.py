"""
GitHub Repo:
https://github.jpl.nasa.gov/stimpe/indysoft-cal
"""

from indysoft_cal import IndySoft
from backend.globals.settings import APP_DESCRIPTION, APP_NAME, EMS_API_URL, BACKEND_GLOBALS_DIR
import json
import requests
import os
import eel

USE_PRODUCTION = False  # TODO: Change to production when ready
IS_CONN_FILE = os.path.abspath(os.path.join(BACKEND_GLOBALS_DIR, 'secret.ini'))
IS_ARGS_LONG = [USE_PRODUCTION, IS_CONN_FILE, APP_NAME, APP_DESCRIPTION]


@eel.expose
def indy_login(username: str, password: str) -> str:
    with IndySoft(*IS_ARGS_LONG) as indysoft:
        success = False
        while not success:
            success, message = indysoft.login(username.upper(), password)
            if not success:
                result = message
            else:
                result = 'Success!'
            return result


@eel.expose
def instr_due_date(id_number: str):
    with IndySoft(*IS_ARGS_LONG) as indysoft:
        imte_objs = indysoft.get_imte([id_number])
        for imte in imte_objs:
            return imte.cal_due_date.strftime('%m/%d/%Y')


@eel.expose
def instr_model(id_number: str):
    with IndySoft(*IS_ARGS_LONG) as indysoft:
        imte_objs = indysoft.get_imte([id_number])
        for imte in imte_objs:
            return imte.model


@eel.expose
def instr_serial(id_number: str):
    with IndySoft(*IS_ARGS_LONG) as indysoft:
        imte_objs = indysoft.get_imte([id_number])
        for imte in imte_objs:
            return imte.serial_num


@eel.expose
def temp_data(location: int) -> str:
    params = {'site_id': location}

    api_response = requests.get(EMS_API_URL, params=params)

    if api_response.status_code in [200, 202]:  # 200 - OK, 202 - Accepted
        attributes = json.loads(api_response.text)
    else:
        response_attributes = vars(api_response)
        attributes = json.loads(', '.join('%s: %s' % item for item in response_attributes.items()))

    return attributes
