import eel
from time import sleep
from backend.globals.settings import RESOURCE_MANAGER, INSTR_DICT, gpib_instruments, com_instruments, usb_instruments, \
    logger

TIMEOUT = 250


@eel.expose
def set_instrs():
    # Clear dictionaries and lists
    INSTR_DICT.clear()
    gpib_instruments.clear()
    com_instruments.clear()
    usb_instruments.clear()

    # Get all resources
    resources_tup = RESOURCE_MANAGER.list_resources()

    # Sort by resource type
    for resource in resources_tup:
        if resource[:4] == 'GPIB':
            gpib_instruments.append(resource)
        elif resource[:4] == 'ASRL':
            com_instruments.append(resource)
        elif resource[:3] == 'USB':
            usb_instruments.append(resource)

    # Get the models of all GPIB instruments and add to dictionary
    for gpib in gpib_instruments:
        index = 0
        try:
            instr = RESOURCE_MANAGER.open_resource(gpib)
            instr.timeout = TIMEOUT
        except:
            logger.warning(f'Resource {gpib} cannot be accessed')
            continue
        try:
            instr.write('*CLS')
            instr.write('*IDN?')
        except:
            logger.warning(f'Resource {gpib} cannot be accessed')
            continue
        sleep(0.5)
        try:
            idn = instr.read()
        except:
            try:
                idn = instr.read_bytes(1)
            except:
                INSTR_DICT[gpib] = gpib
                continue

        idn_str = str(idn)
        if idn_str[1].isalpha():
            model = (idn_str.split(',')[1], index)

            if model not in INSTR_DICT:
                INSTR_DICT[model] = gpib
            else:
                while model in INSTR_DICT:
                    index += 1
                    model = (idn_str.split(',')[1], index)
                INSTR_DICT[model] = gpib
        else:
            instr.write('RESET')
            idn = instr.query('END ALWAYS;ID?')

            idn = idn[2:].strip()
            model = (idn, index)

            if model not in INSTR_DICT:
                INSTR_DICT[model] = gpib
            else:
                while model in INSTR_DICT:
                    index += 1
                    model = (idn, index)
                INSTR_DICT[model] = gpib
        instr.close()

    # Get the models of all USB instruments and add to dictionary
    for usb in usb_instruments:
        index = 0
        try:
            instr = RESOURCE_MANAGER.open_resource(usb)
            instr.timeout = TIMEOUT
        except:
            logger.warning(f'Resource {usb} cannot be accessed')
            continue
        try:
            instr.write('*CLS')
            instr.write('*IDN?')
        except:
            logger.warning(f'Resource {usb} cannot be accessed')
            continue
        sleep(0.5)
        try:
            idn = instr.read()
        except:
            try:
                idn = instr.read_bytes(1)
            except:
                INSTR_DICT[usb] = usb
                continue

        idn_str = str(idn)
        if idn_str[1].isalpha():
            model = (idn_str.split(',')[1], index)

            if model not in INSTR_DICT:
                INSTR_DICT[model] = usb
            else:
                while model in INSTR_DICT:
                    index += 1
                    model = (idn_str.split(',')[1], index)
                INSTR_DICT[model] = usb
        else:
            instr.write('RESET')
            idn = instr.query('END ALWAYS;ID?')

            idn = idn[2:].strip()
            model = (idn, index)

            if model not in INSTR_DICT:
                INSTR_DICT[model] = usb
            else:
                while model in INSTR_DICT:
                    index += 1
                    model = (idn, index)
                INSTR_DICT[model] = usb
        instr.close()

    # Get the models of all COM instruments and add to dictionary
    for com in com_instruments:
        index = 0
        try:
            instr = RESOURCE_MANAGER.open_resource(com)
            instr.timeout = TIMEOUT
        except:
            logger.warning(f'Resource {com} cannot be accessed')
            continue
        try:
            instr.write('*CLS')
            instr.write('*IDN?')
        except:
            logger.warning(f'Resource {com} cannot be accessed')
            continue
        sleep(0.5)
        try:
            idn = instr.read()
        except:
            try:
                idn = instr.read_bytes(1)
            except:
                INSTR_DICT[com] = com
                continue

        idn_str = str(idn)
        if idn_str[1].isalpha():
            model = (idn_str.split(',')[1], index)

            if model not in INSTR_DICT:
                INSTR_DICT[model] = com
            else:
                while model in INSTR_DICT:
                    index += 1
                    model = (idn_str.split(',')[1], index)
                INSTR_DICT[model] = com
        else:
            instr.write('RESET')
            idn = instr.query('END ALWAYS;ID?')

            idn = idn[2:].strip()
            model = (idn, index)

            if model not in INSTR_DICT:
                INSTR_DICT[model] = com
            else:
                while model in INSTR_DICT:
                    index += 1
                    model = (idn, index)
                INSTR_DICT[model] = com
        instr.close()

    logger.info(f'Instruments connected: {get_instrs()}')


@eel.expose
def get_instrs():
    return INSTR_DICT
