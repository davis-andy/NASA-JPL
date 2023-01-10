import os
from backend.instruments.Instruments import Instr
from backend.globals.settings import BACKEND_GLOBALS_DIR
from configobj import ConfigObj

DATA_PATH = os.path.abspath(os.path.join(BACKEND_GLOBALS_DIR, '../instruments/StdData/Ectron1140A.ini'))
ECTRON_SPECS = ConfigObj(DATA_PATH)
operating_environment = ECTRON_SPECS['ENVIRONMENT']
voltage_specs = ECTRON_SPECS['VOLTAGE']
temperature_specs = ECTRON_SPECS['TEMPERATURE']


def get_volt_range() -> str:
    return voltage_specs['range']


def get_temp_spec(spec: str) -> str:
    return temperature_specs[spec]


type_e_ranges = {-245: 1, -195: 2, -155: 3, -90: 4, 15: 5, 890: 6, 1000: 7}
type_j_ranges = {-180: 1, -120: 2, -50: 3, 990: 4, 1200: 5}
type_k_ranges = {-255: 1, -195: 2, -115: 3, -55: 4, 1000: 5, 1372: 6}
type_t_ranges = {-255: 1, -240: 2, -210: 3, -150: 4, -40: 5, 100: 6, 400: 7}


class Ectron1140A(Instr):
    # Retrieve serial number
    def get_serial(self) -> str:
        return self.instr.query(':SYST:SER?')

    # Retrieve catalog of tc types
    def get_tc_catalog(self) -> str:
        return self.instr.query(':INST:THER:TYPE:CAT?')

    # Operate instrument
    def operate(self):
        self.instr.write(f':OUTP:STAN OFF')

    # Put on Standby
    def standby(self):
        self.instr.write(':OUTP:STAN ON')

    # Set instrument to Source mode
    def set_source_mode(self):
        self.instr.write(':INST:MODE SOUR')

    # Set instrument to Meter mode
    def set_meter_mode(self):
        self.instr.write(':INST:MODE METER')

    # Retrieve Meter mode value
    def get_meter_value(self) -> str:
        return self.instr.query(':SENS:VAL?')

    # Set instrument to Temperature mode
    def set_temperature_mode(self):
        self.instr.write(':INST:MODE:ENTR TEMP')

    # Set instrument to Voltage mode
    def set_voltage_mode(self):
        self.instr.write(':INST:MODE:ENTR VOLT')

    # Set instrument temperature units to C
    def set_temperature_units_c(self):
        self.instr.write(':UNIT:TEMP C')

    # Set instrument temperature units to F
    def set_temperature_units_f(self):
        self.instr.write(':UNIT:TEMP F')

    # Set instrument temperature units to R
    def set_temperature_units_r(self):
        self.instr.write(':UNIT:TEMP R')

    # Set instrument temperature units to K
    def set_temperature_units_k(self):
        self.instr.write(':UNIT:TEMP K')

    # Set instrument temperature standard to ITS-90
    def set_temperature_standard_its90(self):
        self.instr.write(':INST:TEMP:STAN ITS-90')

    # Set instrument temperature standard to IPTS-68
    def set_temperature_standard_ipts68(self):
        self.instr.write(':INST:TEMP:STAN IPTS-68')

    # Set instrument voltage units to mV
    def set_voltage_units_mv(self):
        self.instr.write(':UNIT:VOLT mV')

    # Set instrument voltage units to V
    def set_voltage_units_v(self):
        self.instr.write(':UNIT:VOLT V')

    # Set TC type to E
    def set_tc_type_e(self):
        self.instr.write(':INST:THER:TYPE E-MN175')

    # Set TC type to J
    def set_tc_type_j(self):
        self.instr.write(':INST:THER:TYPE J-MN175')

    # Set TC type to K
    def set_tc_type_k(self):
        self.instr.write(':INST:THER:TYPE K-MN175')

    # Set TC type to T
    def set_tc_type_t(self):
        self.instr.write(':INST:THER:TYPE T-MN175')

    # Set TC type to R
    def set_tc_type_r(self):
        self.instr.write(':INST:THER:TYPE R-MN175')

    # Set TC type to S
    def set_tc_type_s(self):
        self.instr.write(':INST:THER:TYPE S-MN175')

    # Set TC type to B
    def set_tc_type_b(self):
        self.instr.write(':INST:THER:TYPE B-MN175')

    # Set TC type to N
    def set_tc_type_n(self):
        self.instr.write(':INST:THER:TYPE N-MN175')

    # Set TC type to PLII
    def set_tc_type_plii(self):
        self.instr.write(':INST:THER:TYPE PLII')

    # Set TC type to G
    def set_tc_type_g(self):
        self.instr.write(':INST:THER:TYPE G')

    # Set TC type to C
    def set_tc_type_c(self):
        self.instr.write(':INST:THER:TYPE C')

    # Set TC type to D
    def set_tc_type_d(self):
        self.instr.write(':INST:THER:TYPE D')

    # Set output Temperature Value
    def set_temperature_value(self, temp: float):
        self.instr.write(f':SOUR:TEMP:VAL {temp}')  # Output values for calibration

    # Set output Voltage Value
    def set_voltage_value(self, volt: float):
        self.instr.write(f':SOUR:VOLT:VAL {volt}')  # Output values for calibration

    # Set instrument thermocouple offset units to C
    def set_tc_offset_units_c(self):
        self.instr.write(':UNIT:THER:OFFS C')

    # Set instrument thermocouple offset units to F
    def set_tc_offset_units_f(self):
        self.instr.write(':UNIT:THER:OFFS F')

    # Set instrument thermocouple offset units to R
    def set_tc_offset_units_r(self):
        self.instr.write(':UNIT:THER:OFFS R')

    # Set instrument thermocouple offset units to K
    def set_tc_offset_units_k(self):
        self.instr.write(':UNIT:THER:OFFS K')

    # Set instrument thermocouple offset units to SYSTEM
    def set_tc_offset_units_sys(self):
        self.instr.write(':UNIT:THER:OFFS SYSTEM')

    # Set TC Offset
    def set_tc_offset_value(self, **kwargs):
        tc = kwargs.get('tc')
        value = kwargs.get('value', 0)

        if tc is None:
            self.instr.write(f':INST:THER:OFFS:VAL {value}')
        elif tc.upper() == 'E':
            self.instr.write(f':INST:THER:OFFS:VAL {self.E_OFFSET}')
        elif tc.upper() == 'J':
            self.instr.write(f':INST:THER:OFFS:VAL {self.J_OFFSET}')
        elif tc.upper() == 'K':
            self.instr.write(f':INST:THER:OFFS:VAL {self.K_OFFSET}')
        elif tc.upper() == 'T':
            self.instr.write(f':INST:THER:OFFS:VAL {self.T_OFFSET}')

    # Set Reference-Junction Units to C
    def set_ref_units_c(self):
        self.instr.write(':UNIT:REFJ C')

    # Set Reference-Junction Units to F
    def set_ref_units_f(self):
        self.instr.write(':UNIT:REFJ F')

    # Set Reference-Junction Units to R
    def set_ref_units_r(self):
        self.instr.write(':UNIT:REFJ R')

    # Set Reference-Junction Units to K
    def set_ref_units_k(self):
        self.instr.write(':UNIT:REFJ K')

    # Set Reference-Junction Units to SYSTEM
    def set_ref_units_sys(self):
        self.instr.write(':UNIT:REFJ SYSTEM')

    # Set Reference-Junction Value
    def set_ref_value(self, value: float = 0):
        self.instr.write(f':OUTP:REFJ:VAL {value}')

    # Set voltage offset units to SYSTEM
    def set_volt_offset_units_sys(self):
        self.instr.write(':UNIT:VOLT:OFFS SYSTEM')

    # Set voltage offset units to mV
    def set_volt_offset_units_mv(self):
        self.instr.write(':UNIT:VOLT:OFFS mV')

    # Set voltage offset units to V
    def set_volt_offset_units_volt(self):
        self.instr.write(':UNIT:VOLT:OFFS V')

    # Set voltage offset value
    def set_volt_offset_value(self, value: float = 0):
        self.instr.write(f':INST:VOLT:OFFS:VAL {value}')

    # Set instrument material to ALLOY
    def set_mat_alloy(self):
        self.instr.write(':INST:MAT ALLOY')

    # Set instrument material to COPPER
    def set_mat_copper(self):
        self.instr.write(':INST:MAT COPPER')

    # Set instrument output terminal to TC
    def set_term_tc(self):
        self.instr.write(':INST:TERM TC')

    # Set instrument output terminal to POST
    def set_term_post(self):
        self.instr.write(':INST:TERM POST')

    # Perform autozero
    def autozero(self):
        self.instr.write(':INP:AZER')

    # Turn off autozero
    def autozero_off(self):
        self.instr.write(':INP:AZERO:STAT OFF')

    # Retrieve autozero offset
    def get_autozero(self) -> str:
        return self.instr.query(':INP:AZER:VAL?')

    # Place instrument in remote
    def remote(self):
        self.instr.write(':SYST:REM')

    # Place instrument in local
    def local(self):
        self.instr.write(':SYST:LOC')

    # Revert user settings to default
    def preset(self):
        self.instr.write(':STAT:PRES')
