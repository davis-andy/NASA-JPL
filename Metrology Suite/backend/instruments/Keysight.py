from backend.instruments.Instruments import Instr


class Keysight34970A(Instr):
    # Initiate readings (stores to memory)
    def initiate(self):
        self.instr.write('INIT')

    # Fetch data
    def fetch(self) -> str:
        return self.instr.query('FETC?')

    # Abort a measurement in scan
    def abort(self):
        self.instr.write('ABOR')

    # Check if all commands are complete
    def get_complete(self) -> str:
        return self.instr.query('*OPC?')

    # Retrieve module information in slot 100
    def get_module_one(self) -> str:
        return self.instr.query('SYST:CTYP? 100')

    # Retrieve module information in slot 200
    def get_module_two(self) -> str:
        return self.instr.query('SYST:CTYP? 200')

    # Retrieve module information in slot 300
    def get_module_three(self) -> str:
        return self.instr.query('SYST:CTYP? 300')

    # Read the instrument, return list of floats
    def get_measurements(self) -> list:
        readings = self.instr.query('READ?').split(',')
        result = []
        for num in readings:
            try:
                result.append(float(num))
            except:
                result.append(-9999)
        return result

    # Turn off input resistance for channel(s) (10 MΩ fixed)
    def set_impedance_off_channel(self, channel):
        self.instr.write(f'INP:IMP:AUTO OFF,(@{channel})')

    # Turn off input resistance for the scan list (10 MΩ fixed)
    def set_impedance_off_scan(self):
        self.instr.write('INP:IMP:AUTO OFF')

    # Turn off input resistance for channel(s) (>10 GΩ for 100mV, 1V and 10V ranges)
    def set_impedance_on_channel(self, channel):
        self.instr.write(f'INP:IMP:AUTO ON,(@{channel})')

    # Turn off input resistance for the scan list (>10 GΩ for 100mV, 1V and 10V ranges)
    def set_impedance_on_scan(self):
        self.instr.write('INP:IMP:AUTO ON')

    # Retrieve input resistance for channel(s)
    def get_impedance_channel(self, channel) -> str:
        return self.instr.query(f'INP:IMP:AUTO? (@{channel})')

    # Retrieve input resistance for the scan list
    def get_impedance_scan(self) -> str:
        return self.instr.query('INP:IMP:AUTO?')

    # Set temperature units to C for channel(s)
    def set_temp_units_c_channel(self, channel):
        self.instr.write(f'UNIT:TEMP C,(@{channel})')

    # Set temperature units to C for the scan list
    def set_temp_units_c_scan(self):
        self.instr.write('UNIT:TEMP C')

    # Set temperature units to F for channel(s)
    def set_temp_units_f_channel(self, channel):
        self.instr.write(f'UNIT:TEMP F,(@{channel})')

    # Set temperature units to F for the scan list
    def set_temp_units_f_scan(self):
        self.instr.write('UNIT:TEMP F')

    # Set temperature units to K for channel(s)
    def set_temp_units_k_channel(self, channel):
        self.instr.write(f'UNIT:TEMP K,(@{channel})')

    # Set temperature units to K for the scan list
    def set_temp_units_k_scan(self):
        self.instr.write('UNIT:TEMP K')

    # Retrieve temperature units for channel(s)
    def get_temp_units_channel(self, channel) -> str:
        return self.instr.query(f'UNIT:TEMP? (@{channel})')

    # Retrieve temperature units for the scan list
    def get_temp_units_scan(self) -> str:
        return self.instr.query('UNIT:TEMP?')

    # Retrieve minimum value of readings for channel(s)
    def get_min_value_channel(self, channel) -> str:
        return self.instr.query(f'CALC:AVER:MIN? (@{channel})')

    # Retrieve minimum value of readings for the scan list
    def get_min_value_scan(self) -> str:
        return self.instr.query('CALC:AVER:MIN?')

    # Retrieve maximum value of readings for channel(s)
    def get_max_value_channel(self, channel) -> str:
        return self.instr.query(f'CALC:AVER:MAX? (@{channel})')

    # Retrieve maximum value of readings for the scan list
    def get_max_value_scan(self) -> str:
        return self.instr.query('CALC:AVER:MAX?')

    # Retrieve average value of readings for channel(s)
    def get_avg_value_channel(self, channel) -> str:
        return self.instr.query(f'CALC:AVER:AVER? (@{channel})')

    # Retrieve average value of readings for the scan list
    def get_avg_value_scan(self) -> str:
        return self.instr.query('CALC:AVER:AVER?')

    # Clear calculation readings for channel(s)
    def clear_calc_channel(self, channel) -> str:
        return self.instr.query(f'CALC:AVER:CLE (@{channel})')

    # Clear calculation readings for the scan list
    def clear_calc_scan(self) -> str:
        return self.instr.query('CALC:AVER:CLE')

    # Retrieve number of readings for channel(s)
    def get_calc_count_channel(self, channel) -> str:
        return self.instr.query(f'CALC:AVER:COUN? (@{channel})')

    # Retrieve number of readings for the scan list
    def get_calc_count_scan(self) -> str:
        return self.instr.query('CALC:AVER:COUN?')

    # Retrieve minimum value of readings for channel(s)
    def get_min_time_channel(self, channel) -> str:
        return self.instr.query(f'CALC:AVER:MIN:TIME? (@{channel})')

    # Retrieve minimum value of readings for the scan list
    def get_min_time_scan(self) -> str:
        return self.instr.query('CALC:AVER:MIN:TIME?')

    # Retrieve maximum value of readings for channel(s)
    def get_max_time_channel(self, channel) -> str:
        return self.instr.query(f'CALC:AVER:MAX:TIME? (@{channel})')

    # Retrieve maximum value of readings for the scan list
    def get_max_time_scan(self) -> str:
        return self.instr.query('CALC:AVER:MAX:TIME?')

    # Retrieve peak to peak value of readings for channel(s)
    def get_peak_channel(self, channel) -> str:
        return self.instr.query(f'CALC:AVER:PTP? (@{channel})')

    # Retrieve peak to peak value of readings for the scan list
    def get_peak_scan(self) -> str:
        return self.instr.query('CALC:AVER:PTP?')

    # Retrieve configuration for channel(s)
    def get_config_channel(self, channel) -> str:
        return self.instr.query(f'CONF? (@{channel})')

    # Retrieve configuration for the scan list
    def get_config_scan(self) -> str:
        return self.instr.query('CONF?')

    # Set current to AC range for channel(s)
    def set_current_ac_range_value(self, rnge, channel):
        self.instr.write(f'CONF:CURR:AC {rnge},(@{channel})')

    # Set current to AC range with resolution for channel(s)
    def set_current_ac_range_resol_value(self, rnge, resolution: int, channel):
        self.instr.write(f'CONF:CURR:AC {rnge},{resolution},(@{channel})')

    # Set current to AC range with resolution to MIN for channel(s)
    def set_current_ac_range_resol_min(self, rnge, channel):
        self.instr.write(f'CONF:CURR:AC {rnge},MIN,(@{channel})')

    # Set current to AC range with resolution to MAX for channel(s)
    def set_current_ac_range_resol_max(self, rnge, channel):
        self.instr.write(f'CONF:CURR:AC {rnge},MAX,(@{channel})')

    # Set current to AC range with resolution to DEF for channel(s)
    def set_current_ac_range_resol_def(self, rnge, channel):
        self.instr.write(f'CONF:CURR:AC {rnge},DEF,(@{channel})')

    # Set current to AC to AUTO for channel(s)
    def set_current_ac_auto(self, channel):
        self.instr.write(f'CONF:CURR:AC AUTO,(@{channel})')

    # Set current to AC to AUTO with resolution for channel(s)
    def set_current_ac_auto_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:CURR:AC AUTO,{resolution},(@{channel})')

    # Set current to AC to AUTO with resolution to MIN for channel(s)
    def set_current_ac_auto_resol_min(self, channel):
        self.instr.write(f'CONF:CURR:AC AUTO,MIN,(@{channel})')

    # Set current to AC to AUTO with resolution to MAX for channel(s)
    def set_current_ac_auto_resol_max(self, channel):
        self.instr.write(f'CONF:CURR:AC AUTO,MAX,(@{channel})')

    # Set current to AC to AUTO with resolution to DEF for channel(s)
    def set_current_ac_auto_resol_def(self, channel):
        self.instr.write(f'CONF:CURR:AC AUTO,DEF,(@{channel})')

    # Set current to AC to MIN for channel(s)
    def set_current_ac_min(self, channel):
        self.instr.write(f'CONF:CURR:AC MIN,(@{channel})')

    # Set current to AC to MIN with resolution for channel(s)
    def set_current_ac_min_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:CURR:AC MIN,{resolution},(@{channel})')

    # Set current to AC to MIN with resolution to MIN for channel(s)
    def set_current_ac_min_resol_min(self, channel):
        self.instr.write(f'CONF:CURR:AC MIN,MIN,(@{channel})')

    # Set current to AC to MIN with resolution to MAX for channel(s)
    def set_current_ac_min_resol_max(self, channel):
        self.instr.write(f'CONF:CURR:AC MIN,MAX,(@{channel})')

    # Set current to AC to MIN with resolution to DEF for channel(s)
    def set_current_ac_min_resol_def(self, channel):
        self.instr.write(f'CONF:CURR:AC MIN,DEF,(@{channel})')

    # Set current to AC to MAX for channel(s)
    def set_current_ac_max(self, channel):
        self.instr.write(f'CONF:CURR:AC MAX,(@{channel})')

    # Set current to AC to MAX with resolution for channel(s)
    def set_current_ac_max_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:CURR:AC MAX,{resolution},(@{channel})')

    # Set current to AC to MAX with resolution to MIN for channel(s)
    def set_current_ac_max_resol_min(self, channel):
        self.instr.write(f'CONF:CURR:AC MAX,MIN,(@{channel})')

    # Set current to AC to MAX with resolution to MAX for channel(s)
    def set_current_ac_max_resol_max(self, channel):
        self.instr.write(f'CONF:CURR:AC MAX,MAX,(@{channel})')

    # Set current to AC to MAX with resolution to DEF for channel(s)
    def set_current_ac_max_resol_def(self, channel):
        self.instr.write(f'CONF:CURR:AC MAX,DEF,(@{channel})')

    # Set current to AC to DEF for channel(s)
    def set_current_ac_def(self, channel):
        self.instr.write(f'CONF:CURR:AC DEF,(@{channel})')

    # Set current to AC to DEF with resolution for channel(s)
    def set_current_ac_def_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:CURR:AC DEF,{resolution},(@{channel})')

    # Set current to AC to DEF with resolution to MIN for channel(s)
    def set_current_ac_def_resol_min(self, channel):
        self.instr.write(f'CONF:CURR:AC DEF,MIN,(@{channel})')

    # Set current to AC to DEF with resolution to MAX for channel(s)
    def set_current_ac_def_resol_max(self, channel):
        self.instr.write(f'CONF:CURR:AC DEF,MAX,(@{channel})')

    # Set current to AC to DEF with resolution to DEF for channel(s)
    def set_current_ac_def_resol_def(self, channel):
        self.instr.write(f'CONF:CURR:AC DEF,DEF,(@{channel})')

    # Set current to DC range for channel(s)
    def set_current_dc_range_value(self, rnge, channel):
        self.instr.write(f'CONF:CURR:DC {rnge},(@{channel})')

    # Set current to DC range with resolution for channel(s)
    def set_current_dc_range_resol_value(self, rnge, resolution: float, channel):
        self.instr.write(f'CONF:CURR:DC {rnge},{resolution},(@{channel})')

    # Set current to DC range with resolution to MIN for channel(s)
    def set_current_dc_range_resol_min(self, rnge, channel):
        self.instr.write(f'CONF:CURR:DC {rnge},MIN,(@{channel})')

    # Set current to DC range with resolution to MAX for channel(s)
    def set_current_dc_range_resol_max(self, rnge, channel):
        self.instr.write(f'CONF:CURR:DC {rnge},MAX,(@{channel})')

    # Set current to DC range with resolution to DEF for channel(s)
    def set_current_dc_range_resol_def(self, rnge, channel):
        self.instr.write(f'CONF:CURR:DC {rnge},DEF,(@{channel})')

    # Set current to DC to AUTO for channel(s)
    def set_current_dc_auto(self, channel):
        self.instr.write(f'CONF:CURR:DC AUTO,(@{channel})')

    # Set current to DC to AUTO with resolution for channel(s)
    def set_current_dc_auto_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:CURR:DC AUTO,{resolution},(@{channel})')

    # Set current to DC to AUTO with resolution to MIN for channel(s)
    def set_current_dc_auto_resol_min(self, channel):
        self.instr.write(f'CONF:CURR:DC AUTO,MIN,(@{channel})')

    # Set current to DC to AUTO with resolution to MAX for channel(s)
    def set_current_dc_auto_resol_max(self, channel):
        self.instr.write(f'CONF:CURR:DC AUTO,MAX,(@{channel})')

    # Set current to DC to AUTO with resolution to DEF for channel(s)
    def set_current_dc_auto_resol_def(self, channel):
        self.instr.write(f'CONF:CURR:DC AUTO,DEF,(@{channel})')

    # Set current to DC to MIN for channel(s)
    def set_current_dc_min(self, channel):
        self.instr.write(f'CONF:CURR:DC MIN,(@{channel})')

    # Set current to DC to MIN with resolution for channel(s)
    def set_current_dc_min_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:CURR:DC MIN,{resolution},(@{channel})')

    # Set current to DC to MIN with resolution to MIN for channel(s)
    def set_current_dc_min_resol_min(self, channel):
        self.instr.write(f'CONF:CURR:DC MIN,MIN,(@{channel})')

    # Set current to DC to MIN with resolution to MAX for channel(s)
    def set_current_dc_min_resol_max(self, channel):
        self.instr.write(f'CONF:CURR:DC MIN,MAX,(@{channel})')

    # Set current to DC to MIN with resolution to DEF for channel(s)
    def set_current_dc_min_resol_def(self, channel):
        self.instr.write(f'CONF:CURR:DC MIN,DEF,(@{channel})')

    # Set current to DC to MAX for channel(s)
    def set_current_dc_max(self, channel):
        self.instr.write(f'CONF:CURR:DC MAX,(@{channel})')

    # Set current to DC to MAX with resolution for channel(s)
    def set_current_dc_max_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:CURR:DC MAX,{resolution},(@{channel})')

    # Set current to DC to MAX with resolution to MIN for channel(s)
    def set_current_dc_max_resol_min(self, channel):
        self.instr.write(f'CONF:CURR:DC MAX,MIN,(@{channel})')

    # Set current to DC to MAX with resolution to MAX for channel(s)
    def set_current_dc_max_resol_max(self, channel):
        self.instr.write(f'CONF:CURR:DC MAX,MAX,(@{channel})')

    # Set current to DC to MAX with resolution to DEF for channel(s)
    def set_current_dc_max_resol_def(self, channel):
        self.instr.write(f'CONF:CURR:DC MAX,DEF,(@{channel})')

    # Set current to DC to DEF for channel(s)
    def set_current_dc_def(self, channel):
        self.instr.write(f'CONF:CURR:DC DEF,(@{channel})')

    # Set current to DC to DEF with resolution for channel(s)
    def set_current_dc_def_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:CURR:DC DEF,{resolution},(@{channel})')

    # Set current to DC to DEF with resolution to MIN for channel(s)
    def set_current_dc_def_resol_min(self, channel):
        self.instr.write(f'CONF:CURR:DC DEF,MIN,(@{channel})')

    # Set current to DC to DEF with resolution to MAX for channel(s)
    def set_current_dc_def_resol_max(self, channel):
        self.instr.write(f'CONF:CURR:DC DEF,MAX,(@{channel})')

    # Set current to DC to DEF with resolution to DEF for channel(s)
    def set_current_dc_def_resol_def(self, channel):
        self.instr.write(f'CONF:CURR:DC DEF,DEF,(@{channel})')

    # Set frequency range for channel(s)
    def set_frequency_range_value(self, rnge, channel):
        self.instr.write(f'CONF:FREQ {rnge},(@{channel})')

    # Set frequency range with resolution for channel(s)
    def set_frequency_range_resol_value(self, rnge, resolution: float, channel):
        self.instr.write(f'CONF:FREQ {rnge},{resolution},(@{channel})')

    # Set frequency range with resolution to MIN for channel(s)
    def set_frequency_range_resol_min(self, rnge, channel):
        self.instr.write(f'CONF:FREQ {rnge},MIN,(@{channel})')

    # Set frequency range with resolution to MAX for channel(s)
    def set_frequency_range_resol_max(self, rnge, channel):
        self.instr.write(f'CONF:FREQ {rnge},MAX,(@{channel})')

    # Set frequency range with resolution to DEF for channel(s)
    def set_frequency_range_resol_def(self, rnge, channel):
        self.instr.write(f'CONF:FREQ {rnge},DEF,(@{channel})')

    # Set frequency to AUTO for channel(s)
    def set_frequency_auto(self, channel):
        self.instr.write(f'CONF:FREQ AUTO,(@{channel})')

    # Set frequency to AUTO with resolution for channel(s)
    def set_frequency_auto_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:FREQ AUTO,{resolution},(@{channel})')

    # Set frequency to AUTO with resolution to MIN for channel(s)
    def set_frequency_auto_resol_min(self, channel):
        self.instr.write(f'CONF:FREQ AUTO,MIN,(@{channel})')

    # Set frequency to AUTO with resolution to MAX for channel(s)
    def set_frequency_auto_resol_max(self, channel):
        self.instr.write(f'CONF:FREQ AUTO,MAX,(@{channel})')

    # Set frequency to AUTO with resolution to DEF for channel(s)
    def set_frequency_auto_resol_def(self, channel):
        self.instr.write(f'CONF:FREQ AUTO,DEF,(@{channel})')

    # Set frequency to MIN for channel(s)
    def set_frequency_min(self, channel):
        self.instr.write(f'CONF:FREQ MIN,(@{channel})')

    # Set frequency to MIN with resolution for channel(s)
    def set_frequency_min_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:FREQ MIN,{resolution},(@{channel})')

    # Set frequency to MIN with resolution to MIN for channel(s)
    def set_frequency_min_resol_min(self, channel):
        self.instr.write(f'CONF:FREQ MIN,MIN,(@{channel})')

    # Set frequency to MIN with resolution to MAX for channel(s)
    def set_frequency_min_resol_max(self, channel):
        self.instr.write(f'CONF:FREQ MIN,MAX,(@{channel})')

    # Set frequency to MIN with resolution to DEF for channel(s)
    def set_frequency_min_resol_def(self, channel):
        self.instr.write(f'CONF:FREQ MIN,DEF,(@{channel})')

    # Set frequency to MAX for channel(s)
    def set_frequency_max(self, channel):
        self.instr.write(f'CONF:FREQ MAX,(@{channel})')

    # Set frequency to MAX with resolution for channel(s)
    def set_frequency_max_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:FREQ MAX,{resolution},(@{channel})')

    # Set frequency to MAX with resolution to MIN for channel(s)
    def set_frequency_max_resol_min(self, channel):
        self.instr.write(f'CONF:FREQ MAX,MIN,(@{channel})')

    # Set frequency to MAX with resolution to MAX for channel(s)
    def set_frequency_max_resol_max(self, channel):
        self.instr.write(f'CONF:FREQ MAX,MAX,(@{channel})')

    # Set frequency to MAX with resolution to DEF for channel(s)
    def set_frequency_max_resol_def(self, channel):
        self.instr.write(f'CONF:FREQ MAX,DEF,(@{channel})')

    # Set frequency to DEF for channel(s)
    def set_frequency_def(self, channel):
        self.instr.write(f'CONF:FREQ DEF,(@{channel})')

    # Set frequency to DEF with resolution for channel(s)
    def set_frequency_def_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:FREQ DEF,{resolution},(@{channel})')

    # Set frequency to DEF with resolution to MIN for channel(s)
    def set_frequency_def_resol_min(self, channel):
        self.instr.write(f'CONF:FREQ DEF,MIN,(@{channel})')

    # Set frequency to DEF with resolution to MAX for channel(s)
    def set_frequency_def_resol_max(self, channel):
        self.instr.write(f'CONF:FREQ DEF,MAX,(@{channel})')

    # Set frequency to DEF with resolution to DEF for channel(s)
    def set_frequency_def_resol_def(self, channel):
        self.instr.write(f'CONF:FREQ DEF,DEF,(@{channel})')

    # Set period range for channel(s)
    def set_period_range_value(self, rnge, channel):
        self.instr.write(f'CONF:PER {rnge},(@{channel})')

    # Set period range with resolution for channel(s)
    def set_period_range_resol_value(self, rnge, resolution: float, channel):
        self.instr.write(f'CONF:PER {rnge},{resolution},(@{channel})')

    # Set period range with resolution to MIN for channel(s)
    def set_period_range_resol_min(self, rnge, channel):
        self.instr.write(f'CONF:PER {rnge},MIN,(@{channel})')

    # Set period range with resolution to MAX for channel(s)
    def set_period_range_resol_max(self, rnge, channel):
        self.instr.write(f'CONF:PER {rnge},MAX,(@{channel})')

    # Set period range with resolution to DEF for channel(s)
    def set_period_range_resol_def(self, rnge, channel):
        self.instr.write(f'CONF:PER {rnge},DEF,(@{channel})')

    # Set period to AUTO for channel(s)
    def set_period_auto(self, channel):
        self.instr.write(f'CONF:PER AUTO,(@{channel})')

    # Set period to AUTO with resolution for channel(s)
    def set_period_auto_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:PER AUTO,{resolution},(@{channel})')

    # Set period to AUTO with resolution to MIN for channel(s)
    def set_period_auto_resol_min(self, channel):
        self.instr.write(f'CONF:PER AUTO,MIN,(@{channel})')

    # Set period to AUTO with resolution to MAX for channel(s)
    def set_period_auto_resol_max(self, channel):
        self.instr.write(f'CONF:PER AUTO,MAX,(@{channel})')

    # Set period to AUTO with resolution to DEF for channel(s)
    def set_period_auto_resol_def(self, channel):
        self.instr.write(f'CONF:PER AUTO,DEF,(@{channel})')

    # Set period to MIN for channel(s)
    def set_period_min(self, channel):
        self.instr.write(f'CONF:PER MIN,(@{channel})')

    # Set period to MIN with resolution for channel(s)
    def set_period_min_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:PER MIN,{resolution},(@{channel})')

    # Set period to MIN with resolution to MIN for channel(s)
    def set_period_min_resol_min(self, channel):
        self.instr.write(f'CONF:PER MIN,MIN,(@{channel})')

    # Set period to MIN with resolution to MAX for channel(s)
    def set_period_min_resol_max(self, channel):
        self.instr.write(f'CONF:PER MIN,MAX,(@{channel})')

    # Set period to MIN with resolution to DEF for channel(s)
    def set_period_min_resol_def(self, channel):
        self.instr.write(f'CONF:PER MIN,DEF,(@{channel})')

    # Set period to MAX for channel(s)
    def set_period_max(self, channel):
        self.instr.write(f'CONF:PER MAX,(@{channel})')

    # Set period to MAX with resolution for channel(s)
    def set_period_max_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:PER MAX,{resolution},(@{channel})')

    # Set period to MAX with resolution to MIN for channel(s)
    def set_period_max_resol_min(self, channel):
        self.instr.write(f'CONF:PER MAX,MIN,(@{channel})')

    # Set period to MAX with resolution to MAX for channel(s)
    def set_period_max_resol_max(self, channel):
        self.instr.write(f'CONF:PER MAX,MAX,(@{channel})')

    # Set period to MAX with resolution to DEF for channel(s)
    def set_period_max_resol_def(self, channel):
        self.instr.write(f'CONF:PER MAX,DEF,(@{channel})')

    # Set period to DEF for channel(s)
    def set_period_def(self, channel):
        self.instr.write(f'CONF:PER DEF,(@{channel})')

    # Set period to DEF with resolution for channel(s)
    def set_period_def_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:PER DEF,{resolution},(@{channel})')

    # Set period to DEF with resolution to MIN for channel(s)
    def set_period_def_resol_min(self, channel):
        self.instr.write(f'CONF:PER DEF,MIN,(@{channel})')

    # Set period to DEF with resolution to MAX for channel(s)
    def set_period_def_resol_max(self, channel):
        self.instr.write(f'CONF:PER DEF,MAX,(@{channel})')

    # Set period to DEF with resolution to DEF for channel(s)
    def set_period_def_resol_def(self, channel):
        self.instr.write(f'CONF:PER DEF,DEF,(@{channel})')

    # Set resistance range for channel(s)
    def set_resistance_range_value(self, rnge, channel):
        self.instr.write(f'CONF:RES {rnge},(@{channel})')

    # Set resistance range with resolution for channel(s)
    def set_resistance_range_resol_value(self, rnge, resolution: float, channel):
        self.instr.write(f'CONF:RES {rnge},{resolution},(@{channel})')

    # Set resistance range with resolution to MIN for channel(s)
    def set_resistance_range_resol_min(self, rnge, channel):
        self.instr.write(f'CONF:RES {rnge},MIN,(@{channel})')

    # Set resistance range with resolution to MAX for channel(s)
    def set_resistance_range_resol_max(self, rnge, channel):
        self.instr.write(f'CONF:RES {rnge},MAX,(@{channel})')

    # Set resistance range with resolution to DEF for channel(s)
    def set_resistance_range_resol_def(self, rnge, channel):
        self.instr.write(f'CONF:RES {rnge},DEF,(@{channel})')

    # Set resistance to AUTO for channel(s)
    def set_resistance_auto(self, channel):
        self.instr.write(f'CONF:RES AUTO,(@{channel})')

    # Set resistance to AUTO with resolution for channel(s)
    def set_resistance_auto_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:RES AUTO,{resolution},(@{channel})')

    # Set resistance to AUTO with resolution to MIN for channel(s)
    def set_resistance_auto_resol_min(self, channel):
        self.instr.write(f'CONF:RES AUTO,MIN,(@{channel})')

    # Set resistance to AUTO with resolution to MAX for channel(s)
    def set_resistance_auto_resol_max(self, channel):
        self.instr.write(f'CONF:RES AUTO,MAX,(@{channel})')

    # Set resistance to AUTO with resolution to DEF for channel(s)
    def set_resistance_auto_resol_def(self, channel):
        self.instr.write(f'CONF:RES AUTO,DEF,(@{channel})')

    # Set resistance to MIN for channel(s)
    def set_resistance_min(self, channel):
        self.instr.write(f'CONF:RES MIN,(@{channel})')

    # Set resistance to MIN with resolution for channel(s)
    def set_resistance_min_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:RES MIN,{resolution},(@{channel})')

    # Set resistance to MIN with resolution to MIN for channel(s)
    def set_resistance_min_resol_min(self, channel):
        self.instr.write(f'CONF:RES MIN,MIN,(@{channel})')

    # Set resistance to MIN with resolution to MAX for channel(s)
    def set_resistance_min_resol_max(self, channel):
        self.instr.write(f'CONF:RES MIN,MAX,(@{channel})')

    # Set resistance to MIN with resolution to DEF for channel(s)
    def set_resistance_min_resol_def(self, channel):
        self.instr.write(f'CONF:RES MIN,DEF,(@{channel})')

    # Set resistance to MAX for channel(s)
    def set_resistance_max(self, channel):
        self.instr.write(f'CONF:RES MAX,(@{channel})')

    # Set resistance to MAX with resolution for channel(s)
    def set_resistance_max_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:RES MAX,{resolution},(@{channel})')

    # Set resistance to MAX with resolution to MIN for channel(s)
    def set_resistance_max_resol_min(self, channel):
        self.instr.write(f'CONF:RES MAX,MIN,(@{channel})')

    # Set resistance to MAX with resolution to MAX for channel(s)
    def set_resistance_max_resol_max(self, channel):
        self.instr.write(f'CONF:RES MAX,MAX,(@{channel})')

    # Set resistance to MAX with resolution to DEF for channel(s)
    def set_resistance_max_resol_def(self, channel):
        self.instr.write(f'CONF:RES MAX,DEF,(@{channel})')

    # Set resistance to DEF for channel(s)
    def set_resistance_def(self, channel):
        self.instr.write(f'CONF:RES DEF,(@{channel})')

    # Set resistance to DEF with resolution for channel(s)
    def set_resistance_def_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:RES DEF,{resolution},(@{channel})')

    # Set resistance to DEF with resolution to MIN for channel(s)
    def set_resistance_def_resol_min(self, channel):
        self.instr.write(f'CONF:RES DEF,MIN,(@{channel})')

    # Set resistance to DEF with resolution to MAX for channel(s)
    def set_resistance_def_resol_max(self, channel):
        self.instr.write(f'CONF:RES DEF,MAX,(@{channel})')

    # Set resistance to DEF with resolution to DEF for channel(s)
    def set_resistance_def_resol_def(self, channel):
        self.instr.write(f'CONF:RES DEF,DEF,(@{channel})')

    # Set resistance four-wire range for channel(s)
    def set_resistance_four_range_value(self, rnge, channel):
        self.instr.write(f'CONF:FRES {rnge},(@{channel})')

    # Set resistance four-wire range with resolution for channel(s)
    def set_resistance_four_range_resol_value(self, rnge, resolution: float, channel):
        self.instr.write(f'CONF:FRES {rnge},{resolution},(@{channel})')

    # Set resistance four-wire range with resolution to MIN for channel(s)
    def set_resistance_four_range_resol_min(self, rnge, channel):
        self.instr.write(f'CONF:FRES {rnge},MIN,(@{channel})')

    # Set resistance four-wire range with resolution to MAX for channel(s)
    def set_resistance_four_range_resol_max(self, rnge, channel):
        self.instr.write(f'CONF:FRES {rnge},MAX,(@{channel})')

    # Set resistance four-wire range with resolution to DEF for channel(s)
    def set_resistance_four_range_resol_def(self, rnge, channel):
        self.instr.write(f'CONF:FRES {rnge},DEF,(@{channel})')

    # Set resistance four-wire to AUTO for channel(s)
    def set_resistance_four_auto(self, channel):
        self.instr.write(f'CONF:FRES AUTO,(@{channel})')

    # Set resistance four-wire to AUTO with resolution for channel(s)
    def set_resistance_four_auto_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:FRES AUTO,{resolution},(@{channel})')

    # Set resistance four-wire to AUTO with resolution to MIN for channel(s)
    def set_resistance_four_auto_resol_min(self, channel):
        self.instr.write(f'CONF:FRES AUTO,MIN,(@{channel})')

    # Set resistance four-wire to AUTO with resolution to MAX for channel(s)
    def set_resistance_four_auto_resol_max(self, channel):
        self.instr.write(f'CONF:FRES AUTO,MAX,(@{channel})')

    # Set resistance four-wire to AUTO with resolution to DEF for channel(s)
    def set_resistance_four_auto_resol_def(self, channel):
        self.instr.write(f'CONF:FRES AUTO,DEF,(@{channel})')

    # Set resistance four-wire to MIN for channel(s)
    def set_resistance_four_min(self, channel):
        self.instr.write(f'CONF:FRES MIN,(@{channel})')

    # Set resistance four-wire to MIN with resolution for channel(s)
    def set_resistance_four_min_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:FRES MIN,{resolution},(@{channel})')

    # Set resistance four-wire to MIN with resolution to MIN for channel(s)
    def set_resistance_four_min_resol_min(self, channel):
        self.instr.write(f'CONF:FRES MIN,MIN,(@{channel})')

    # Set resistance four-wire to MIN with resolution to MAX for channel(s)
    def set_resistance_four_min_resol_max(self, channel):
        self.instr.write(f'CONF:FRES MIN,MAX,(@{channel})')

    # Set resistance four-wire to MIN with resolution to DEF for channel(s)
    def set_resistance_four_min_resol_def(self, channel):
        self.instr.write(f'CONF:FRES MIN,DEF,(@{channel})')

    # Set resistance four-wire to MAX for channel(s)
    def set_resistance_four_max(self, channel):
        self.instr.write(f'CONF:FRES MAX,(@{channel})')

    # Set resistance four-wire to MAX with resolution for channel(s)
    def set_resistance_four_max_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:FRES MAX,{resolution},(@{channel})')

    # Set resistance four-wire to MAX with resolution to MIN for channel(s)
    def set_resistance_four_max_resol_min(self, channel):
        self.instr.write(f'CONF:FRES MAX,MIN,(@{channel})')

    # Set resistance four-wire to MAX with resolution to MAX for channel(s)
    def set_resistance_four_max_resol_max(self, channel):
        self.instr.write(f'CONF:FRES MAX,MAX,(@{channel})')

    # Set resistance four-wire to MAX with resolution to DEF for channel(s)
    def set_resistance_four_max_resol_def(self, channel):
        self.instr.write(f'CONF:FRES MAX,DEF,(@{channel})')

    # Set resistance four-wire to DEF for channel(s)
    def set_resistance_four_def(self, channel):
        self.instr.write(f'CONF:FRES DEF,(@{channel})')

    # Set resistance four-wire to DEF with resolution for channel(s)
    def set_resistance_four_def_resol_value(self, resolution: float, channel):
        self.instr.write(f'CONF:FRES DEF,{resolution},(@{channel})')

    # Set resistance four-wire to DEF with resolution to MIN for channel(s)
    def set_resistance_four_def_resol_min(self, channel):
        self.instr.write(f'CONF:FRES DEF,MIN,(@{channel})')

    # Set resistance four-wire to DEF with resolution to MAX for channel(s)
    def set_resistance_four_def_resol_max(self, channel):
        self.instr.write(f'CONF:FRES DEF,MAX,(@{channel})')

    # Set resistance four-wire to DEF with resolution to DEF for channel(s)
    def set_resistance_four_def_resol_def(self, channel):
        self.instr.write(f'CONF:FRES DEF,DEF,(@{channel})')

    # Change TC type on channel(s)
    def set_temp_tc(self, tc: str, channel):
        self.instr.write(f'CONF:TEMP TC,{tc},(@{channel})')

    # Change TC type with resolution on channel(s)
    def set_temp_tc_resol(self, tc: str, resolution: float, channel):
        self.instr.write(f'CONF:TEMP TC,{tc},1,{resolution},(@{channel})')

    # Change TC type with resolution to MIN on channel(s)
    def set_temp_tc_resol_min(self, tc: str, channel):
        self.instr.write(f'CONF:TEMP TC,{tc},1,MIN,(@{channel})')

    # Change TC type with resolution to MAX on channel(s)
    def set_temp_tc_resol_max(self, tc: str, channel):
        self.instr.write(f'CONF:TEMP TC,{tc},1,MAX,(@{channel})')

    # Change TC type with resolution to DEF on channel(s)
    def set_temp_tc_resol_def(self, tc: str, channel):
        self.instr.write(f'CONF:TEMP TC,{tc},1,DEF,(@{channel})')

    # Change TC type to B on channel(s)
    def set_temp_tc_b(self, channel):
        self.instr.write(f'CONF:TEMP TC,B,(@{channel})')

    # Change TC type to B with resolution on channel(s)
    def set_temp_tc_b_resol(self, resolution: float, channel):
        self.instr.write(f'CONF:TEMP TC,B,1,{resolution},(@{channel})')

    # Change TC type to B with resolution to MIN on channel(s)
    def set_temp_tc_b_resol_min(self, channel):
        self.instr.write(f'CONF:TEMP TC,B,1,MIN,(@{channel})')

    # Change TC type to B with resolution to MAX on channel(s)
    def set_temp_tc_b_resol_max(self, channel):
        self.instr.write(f'CONF:TEMP TC,B,1,MAX,(@{channel})')

    # Change TC type to B with resolution to DEF on channel(s)
    def set_temp_tc_b_resol_def(self, channel):
        self.instr.write(f'CONF:TEMP TC,B,1,DEF,(@{channel})')

    # Change TC type to E on channel(s)
    def set_temp_tc_e(self, channel):
        self.instr.write(f'CONF:TEMP TC,E,(@{channel})')

    # Change TC type to E with resolution on channel(s)
    def set_temp_tc_e_resol(self, resolution: float, channel):
        self.instr.write(f'CONF:TEMP TC,E,1,{resolution},(@{channel})')

    # Change TC type to E with resolution to MIN on channel(s)
    def set_temp_tc_e_resol_min(self, channel):
        self.instr.write(f'CONF:TEMP TC,E,1,MIN,(@{channel})')

    # Change TC type to E with resolution to MAX on channel(s)
    def set_temp_tc_e_resol_max(self, channel):
        self.instr.write(f'CONF:TEMP TC,E,1,MAX,(@{channel})')

    # Change TC type to E with resolution to DEF on channel(s)
    def set_temp_tc_e_resol_def(self, channel):
        self.instr.write(f'CONF:TEMP TC,E,1,DEF,(@{channel})')

    # Change TC type to J on channel(s)
    def set_temp_tc_j(self, channel):
        self.instr.write(f'CONF:TEMP TC,J,(@{channel})')

    # Change TC type to J with resolution on channel(s)
    def set_temp_tc_j_resol(self, resolution: float, channel):
        self.instr.write(f'CONF:TEMP TC,J,1,{resolution},(@{channel})')

    # Change TC type to J with resolution to MIN on channel(s)
    def set_temp_tc_j_resol_min(self, channel):
        self.instr.write(f'CONF:TEMP TC,J,1,MIN,(@{channel})')

    # Change TC type to J with resolution to MAX on channel(s)
    def set_temp_tc_j_resol_max(self, channel):
        self.instr.write(f'CONF:TEMP TC,J,1,MAX,(@{channel})')

    # Change TC type to J with resolution to DEF on channel(s)
    def set_temp_tc_j_resol_def(self, channel):
        self.instr.write(f'CONF:TEMP TC,J,1,DEF,(@{channel})')

    # Change TC type to K on channel(s)
    def set_temp_tc_k(self, channel):
        self.instr.write(f'CONF:TEMP TC,K,(@{channel})')

    # Change TC type to K with resolution on channel(s)
    def set_temp_tc_k_resol(self, resolution: float, channel):
        self.instr.write(f'CONF:TEMP TC,K,1,{resolution},(@{channel})')

    # Change TC type to K with resolution to MIN on channel(s)
    def set_temp_tc_k_resol_min(self, channel):
        self.instr.write(f'CONF:TEMP TC,K,1,MIN,(@{channel})')

    # Change TC type to K with resolution to MAX on channel(s)
    def set_temp_tc_k_resol_max(self, channel):
        self.instr.write(f'CONF:TEMP TC,K,1,MAX,(@{channel})')

    # Change TC type to K with resolution to DEF on channel(s)
    def set_temp_tc_k_resol_def(self, channel):
        self.instr.write(f'CONF:TEMP TC,K,1,DEF,(@{channel})')

    # Change TC type to N on channel(s)
    def set_temp_tc_n(self, channel):
        self.instr.write(f'CONF:TEMP TC,N,(@{channel})')

    # Change TC type to N with resolution on channel(s)
    def set_temp_tc_n_resol(self, resolution: float, channel):
        self.instr.write(f'CONF:TEMP TC,N,1,{resolution},(@{channel})')

    # Change TC type to N with resolution to MIN on channel(s)
    def set_temp_tc_n_resol_min(self, channel):
        self.instr.write(f'CONF:TEMP TC,N,1,MIN,(@{channel})')

    # Change TC type to N with resolution to MAX on channel(s)
    def set_temp_tc_n_resol_max(self, channel):
        self.instr.write(f'CONF:TEMP TC,N,1,MAX,(@{channel})')

    # Change TC type to N with resolution to DEF on channel(s)
    def set_temp_tc_n_resol_def(self, channel):
        self.instr.write(f'CONF:TEMP TC,N,1,DEF,(@{channel})')

    # Change TC type to R on channel(s)
    def set_temp_tc_r(self, channel):
        self.instr.write(f'CONF:TEMP TC,R,(@{channel})')

    # Change TC type to R with resolution on channel(s)
    def set_temp_tc_r_resol(self, resolution: float, channel):
        self.instr.write(f'CONF:TEMP TC,R,1,{resolution},(@{channel})')

    # Change TC type to R with resolution to MIN on channel(s)
    def set_temp_tc_r_resol_min(self, channel):
        self.instr.write(f'CONF:TEMP TC,R,1,MIN,(@{channel})')

    # Change TC type to R with resolution to MAX on channel(s)
    def set_temp_tc_r_resol_max(self, channel):
        self.instr.write(f'CONF:TEMP TC,R,1,MAX,(@{channel})')

    # Change TC type to R with resolution to DEF on channel(s)
    def set_temp_tc_r_resol_def(self, channel):
        self.instr.write(f'CONF:TEMP TC,R,1,DEF,(@{channel})')

    # Change TC type to S on channel(s)
    def set_temp_tc_s(self, channel):
        self.instr.write(f'CONF:TEMP TC,S,(@{channel})')

    # Change TC type to S with resolution on channel(s)
    def set_temp_tc_s_resol(self, resolution: float, channel):
        self.instr.write(f'CONF:TEMP TC,S,1,{resolution},(@{channel})')

    # Change TC type to S with resolution to MIN on channel(s)
    def set_temp_tc_s_resol_min(self, channel):
        self.instr.write(f'CONF:TEMP TC,S,1,MIN,(@{channel})')

    # Change TC type to S with resolution to MAX on channel(s)
    def set_temp_tc_s_resol_max(self, channel):
        self.instr.write(f'CONF:TEMP TC,S,1,MAX,(@{channel})')

    # Change TC type to S with resolution to DEF on channel(s)
    def set_temp_tc_s_resol_def(self, channel):
        self.instr.write(f'CONF:TEMP TC,S,1,DEF,(@{channel})')

    # Change TC type to T on channel(s)
    def set_temp_tc_t(self, channel):
        self.instr.write(f'CONF:TEMP TC,T,(@{channel})')

    # Change TC type to T with resolution on channel(s)
    def set_temp_tc_t_resol(self, resolution: float, channel):
        self.instr.write(f'CONF:TEMP TC,T,1,{resolution},(@{channel})')

    # Change TC type to T with resolution to MIN on channel(s)
    def set_temp_tc_t_resol_min(self, channel):
        self.instr.write(f'CONF:TEMP TC,T,1,MIN,(@{channel})')

    # Change TC type to T with resolution to MAX on channel(s)
    def set_temp_tc_t_resol_max(self, channel):
        self.instr.write(f'CONF:TEMP TC,T,1,MAX,(@{channel})')

    # Change TC type to T with resolution to DEF on channel(s)
    def set_temp_tc_t_resol_def(self, channel):
        self.instr.write(f'CONF:TEMP TC,T,1,DEF,(@{channel})')

    # Change RTD type on channel(s)
    def set_temp_rtd(self, rtd: str, channel):
        self.instr.write(f'CONF:TEMP RTD,{rtd},(@{channel})')

    # Change RTD type with resolution on channel(s)
    def set_temp_rtd_resol(self, rtd: str, resolution: float, channel):
        self.instr.write(f'CONF:TEMP RTD,{rtd},1,{resolution},(@{channel})')

    # Change RTD type with resolution to MIN on channel(s)
    def set_temp_rtd_resol_min(self, rtd: str, channel):
        self.instr.write(f'CONF:TEMP RTD,{rtd},1,MIN,(@{channel})')

    # Change RTD type with resolution to MAX on channel(s)
    def set_temp_rtd_resol_max(self, rtd: str, channel):
        self.instr.write(f'CONF:TEMP RTD,{rtd},1,MAX,(@{channel})')

    # Change RTD type with resolution to DEF on channel(s)
    def set_temp_rtd_resol_def(self, rtd: str, channel):
        self.instr.write(f'CONF:TEMP RTD,{rtd},1,DEF,(@{channel})')

    # Change RTD type to 85 on channel(s)
    def set_temp_rtd_85(self, channel):
        self.instr.write(f'CONF:TEMP RTD,85,(@{channel})')

    # Change RTD type to 85 with resolution on channel(s)
    def set_temp_rtd_85_resol(self, resolution: float, channel):
        self.instr.write(f'CONF:TEMP RTD,85,1,{resolution},(@{channel})')

    # Change RTD type to 85 with resolution to MIN on channel(s)
    def set_temp_rtd_85_resol_min(self, channel):
        self.instr.write(f'CONF:TEMP RTD,85,1,MIN,(@{channel})')

    # Change RTD type to 85 with resolution to MAX on channel(s)
    def set_temp_rtd_85_resol_max(self, channel):
        self.instr.write(f'CONF:TEMP RTD,85,1,MAX,(@{channel})')

    # Change RTD type to 85 with resolution to DEF on channel(s)
    def set_temp_rtd_85_resol_def(self, channel):
        self.instr.write(f'CONF:TEMP RTD,85,1,DEF,(@{channel})')

    # Change RTD type to 91 on channel(s)
    def set_temp_rtd_91(self, channel):
        self.instr.write(f'CONF:TEMP RTD,91,(@{channel})')

    # Change RTD type to 91 with resolution on channel(s)
    def set_temp_rtd_91_resol(self, resolution: float, channel):
        self.instr.write(f'CONF:TEMP RTD,91,1,{resolution},(@{channel})')

    # Change RTD type to 91 with resolution to MIN on channel(s)
    def set_temp_rtd_91_resol_min(self, channel):
        self.instr.write(f'CONF:TEMP RTD,91,1,MIN,(@{channel})')

    # Change RTD type to 91 with resolution to MAX on channel(s)
    def set_temp_rtd_91_resol_max(self, channel):
        self.instr.write(f'CONF:TEMP RTD,91,1,MAX,(@{channel})')

    # Change RTD type to 91 with resolution to DEF on channel(s)
    def set_temp_rtd_91_resol_def(self, channel):
        self.instr.write(f'CONF:TEMP RTD,91,1,DEF,(@{channel})')

    # Change FRTD type on channel(s)
    def set_temp_rtd_four(self, rtd_four: str, channel):
        self.instr.write(f'CONF:TEMP FRTD,{rtd_four},(@{channel})')

    # Change FRTD type with resolution on channel(s)
    def set_temp_rtd_four_resol(self, rtd_four: str, resolution: float, channel):
        self.instr.write(f'CONF:TEMP FRTD,{rtd_four},1,{resolution},(@{channel})')

    # Change FRTD type with resolution to MIN on channel(s)
    def set_temp_rtd_four_resol_min(self, rtd_four: str, channel):
        self.instr.write(f'CONF:TEMP FRTD,{rtd_four},1,MIN,(@{channel})')

    # Change FRTD type with resolution to MAX on channel(s)
    def set_temp_rtd_four_resol_max(self, rtd_four: str, channel):
        self.instr.write(f'CONF:TEMP FRTD,{rtd_four},1,MAX,(@{channel})')

    # Change FRTD type with resolution to DEF on channel(s)
    def set_temp_rtd_four_resol_def(self, rtd_four: str, channel):
        self.instr.write(f'CONF:TEMP FRTD,{rtd_four},1,DEF,(@{channel})')

    # Change FRTD type to 85 on channel(s)
    def set_temp_rtd_four_85(self, channel):
        self.instr.write(f'CONF:TEMP FRTD,85,(@{channel})')

    # Change FRTD type to 85 with resolution on channel(s)
    def set_temp_rtd_four_85_resol(self, resolution: float, channel):
        self.instr.write(f'CONF:TEMP FRTD,85,1,{resolution},(@{channel})')

    # Change FRTD type to 85 with resolution to MIN on channel(s)
    def set_temp_rtd_four_85_resol_min(self, channel):
        self.instr.write(f'CONF:TEMP FRTD,85,1,MIN,(@{channel})')

    # Change FRTD type to 85 with resolution to MAX on channel(s)
    def set_temp_rtd_four_85_resol_max(self, channel):
        self.instr.write(f'CONF:TEMP FRTD,85,1,MAX,(@{channel})')

    # Change FRTD type to 85 with resolution to DEF on channel(s)
    def set_temp_rtd_four_85_resol_def(self, channel):
        self.instr.write(f'CONF:TEMP FRTD,85,1,DEF,(@{channel})')

    # Change FRTD type to 91 on channel(s)
    def set_temp_rtd_four_91(self, channel):
        self.instr.write(f'CONF:TEMP FRTD,91,(@{channel})')

    # Change FRTD type to 91 with resolution on channel(s)
    def set_temp_rtd_four_91_resol(self, resolution: float, channel):
        self.instr.write(f'CONF:TEMP FRTD,91,1,{resolution},(@{channel})')

    # Change FRTD type to 91 with resolution to MIN on channel(s)
    def set_temp_rtd_four_91_resol_min(self, channel):
        self.instr.write(f'CONF:TEMP FRTD,91,1,MIN,(@{channel})')

    # Change FRTD type to 91 with resolution to MAX on channel(s)
    def set_temp_rtd_four_91_resol_max(self, channel):
        self.instr.write(f'CONF:TEMP FRTD,91,1,MAX,(@{channel})')

    # Change FRTD type to 91 with resolution to DEF on channel(s)
    def set_temp_rtd_four_91_resol_def(self, channel):
        self.instr.write(f'CONF:TEMP FRTD,91,1,DEF,(@{channel})')

    # Change Thermistor type on channel(s)
    def set_temp_therm(self, therm: str, channel):
        self.instr.write(f'CONF:TEMP THER,{therm},(@{channel})')

    # Change Thermistor type with resolution on channel(s)
    def set_temp_therm_resol(self, therm: str, resolution: float, channel):
        self.instr.write(f'CONF:TEMP THER,{therm},1,{resolution},(@{channel})')

    # Change Thermistor type with resolution to MIN on channel(s)
    def set_temp_therm_resol_min(self, therm: str, channel):
        self.instr.write(f'CONF:TEMP THER,{therm},1,MIN,(@{channel})')

    # Change Thermistor type with resolution to MAX on channel(s)
    def set_temp_therm_resol_max(self, therm: str, channel):
        self.instr.write(f'CONF:TEMP THER,{therm},1,MAX,(@{channel})')

    # Change Thermistor type with resolution to DEF on channel(s)
    def set_temp_therm_resol_def(self, therm: str, channel):
        self.instr.write(f'CONF:TEMP THER,{therm},1,DEF,(@{channel})')

    # Change Thermistor type to 2252 on channel(s)
    def set_temp_therm_2252(self, channel):
        self.instr.write(f'CONF:TEMP THER,2252,(@{channel})')

    # Change Thermistor type to 2252 with resolution on channel(s)
    def set_temp_therm_2252_resol(self, resolution: float, channel):
        self.instr.write(f'CONF:TEMP THER,2252,1,{resolution},(@{channel})')

    # Change Thermistor type to 2252 with resolution to MIN on channel(s)
    def set_temp_therm_2252_resol_min(self, channel):
        self.instr.write(f'CONF:TEMP THER,2252,1,MIN,(@{channel})')

    # Change Thermistor type to 2252 with resolution to MAX on channel(s)
    def set_temp_therm_2252_resol_max(self, channel):
        self.instr.write(f'CONF:TEMP THER,2252,1,MAX,(@{channel})')

    # Change Thermistor type to 2252 with resolution to DEF on channel(s)
    def set_temp_therm_2252_resol_def(self, channel):
        self.instr.write(f'CONF:TEMP THER,2252,1,DEF,(@{channel})')

    # Change Thermistor type to 5000 on channel(s)
    def set_temp_therm_5000(self, channel):
        self.instr.write(f'CONF:TEMP THER,5000,(@{channel})')

    # Change Thermistor type to 5000 with resolution on channel(s)
    def set_temp_therm_5000_resol(self, resolution: float, channel):
        self.instr.write(f'CONF:TEMP THER,5000,1,{resolution},(@{channel})')

    # Change Thermistor type to 5000 with resolution to MIN on channel(s)
    def set_temp_therm_5000_resol_min(self, channel):
        self.instr.write(f'CONF:TEMP THER,5000,1,MIN,(@{channel})')

    # Change Thermistor type to 5000 with resolution to MAX on channel(s)
    def set_temp_therm_5000_resol_max(self, channel):
        self.instr.write(f'CONF:TEMP THER,5000,1,MAX,(@{channel})')

    # Change Thermistor type to 5000 with resolution to DEF on channel(s)
    def set_temp_therm_5000_resol_def(self, channel):
        self.instr.write(f'CONF:TEMP THER,5000,1,DEF,(@{channel})')

    # Change Thermistor type to 10000 on channel(s)
    def set_temp_therm_10000(self, channel):
        self.instr.write(f'CONF:TEMP THER,10000,(@{channel})')

    # Change Thermistor type to 10000 with resolution on channel(s)
    def set_temp_therm_10000_resol(self, resolution: float, channel):
        self.instr.write(f'CONF:TEMP THER,10000,1,{resolution},(@{channel})')

    # Change Thermistor type to 10000 with resolution to MIN on channel(s)
    def set_temp_therm_10000_resol_min(self, channel):
        self.instr.write(f'CONF:TEMP THER,10000,1,MIN,(@{channel})')

    # Change Thermistor type to 10000 with resolution to MAX on channel(s)
    def set_temp_therm_10000_resol_max(self, channel):
        self.instr.write(f'CONF:TEMP THER,10000,1,MAX,(@{channel})')

    # Change Thermistor type to 10000 with resolution to DEF on channel(s)
    def set_temp_therm_10000_resol_def(self, channel):
        self.instr.write(f'CONF:TEMP THER,10000,1,DEF,(@{channel})')

    # Set monitor channel
    def set_monitor_channel(self, channel):
        self.instr.write(f'ROUT:MON (@{channel})')

    # Set monitor on
    def set_monitor_on(self):
        self.instr.write('ROUT:MON:STAT ON')

    # Set monitor off
    def set_monitor_off(self):
        self.instr.write('ROUT:MON:STAT OFF')

    # Set scan list
    def set_scan_list(self, channel):
        self.instr.write(f'ROUT:SCAN (@{channel})')

    # Set Temperature Aperture value
    def set_temp_aperature(self, seconds: float):
        self.instr.write(f'TEMP:APER {seconds}')

    # Set Temperature Aperture value with channel
    def set_temp_aperature_channel(self, seconds: float, channel):
        self.instr.write(f'TEMP:APER {seconds},(@{channel})')

    # Set Temperature Aperture to MIN
    def set_temp_aperature_min(self):
        self.instr.write(f'TEMP:APER MIN')

    # Set Temperature Aperture to MIN with channel
    def set_temp_aperature_min_channel(self, channel):
        self.instr.write(f'TEMP:APER MIN,(@{channel})')

    # Set Temperature Aperture to MAX
    def set_temp_aperature_max(self):
        self.instr.write(f'TEMP:APER MAX')

    # Set Temperature Aperture to MAX with channel
    def set_temp_aperature_max_channel(self, channel):
        self.instr.write(f'TEMP:APER MAX,(@{channel})')

    # Set Temperature Aperture to DEF
    def set_temp_aperature_def(self):
        self.instr.write(f'TEMP:APER DEF')

    # Set Temperature Aperture to DEF with channel
    def set_temp_aperature_def_channel(self, channel):
        self.instr.write(f'TEMP:APER DEF,(@{channel})')

    # Change Temp NPLC value
    def set_temp_nplc(self, nplc: int = 10):
        self.instr.write(f'TEMP:NPLC {nplc}')  # usually 10

    # Change Temp NPLC value with channel
    def set_temp_nplc_channel(self, channel, nplc: int = 10):
        self.instr.write(f'TEMP:NPLC {nplc},(@{channel})')  # usually 10

    # Change Temp NPLC to MIN
    def set_temp_nplc_min(self):
        self.instr.write('TEMP:NPLC MIN')

    # Change Temp NPLC to MIN with channel
    def set_temp_nplc_min_channel(self, channel):
        self.instr.write(f'TEMP:NPLC MIN,(@{channel})')

    # Change Temp NPLC to MAX
    def set_temp_nplc_max(self):
        self.instr.write('TEMP:NPLC MAX')

    # Change Temp NPLC to MAX with channel
    def set_temp_nplc_max_channel(self, channel):
        self.instr.write(f'TEMP:NPLC MAX,(@{channel})')

    # Set Ref Junction Type to INT
    def set_temp_tc_ref_jun_type_int(self, channel):
        self.instr.write(f'TEMP:TRAN:TC:RJUN:TYPE INT,(@{channel})')

    # Set Ref Junction Type to EXT
    def set_temp_tc_ref_jun_type_ext(self, channel):
        self.instr.write(f'TEMP:TRAN:TC:RJUN:TYPE EXT,(@{channel})')

    # Set Ref Junction Type to FIX
    def set_temp_tc_ref_jun_type_fix(self, channel):
        self.instr.write(f'TEMP:TRAN:TC:RJUN:TYPE FIX,(@{channel})')

    # Change Trigger count
    def set_trig_count(self, count: int = 5):
        self.instr.write(f'TRIG:COUN {count}')  # usually 5 measurements per reading


class Keysight33250A(Instr):
    # Apply Sine wave, hertz, Vpp, no offset
    def apply_sine_hz_vpp(self, freq, vpp):
        self.instr.write(f'APPL:SIN {freq}HZ, {vpp}VPP')

    # Apply Sine wave, kilohertz, Vpp, no offset
    def apply_sine_khz_vpp(self, freq, vpp):
        self.instr.write(f'APPL:SIN {freq}KHZ, {vpp}VPP')

    # Apply Sine wave, hertz, Vrms, no offset
    def apply_sine_hz_vrms(self, freq, vrms):
        self.instr.write(f'APPL:SIN {freq}HZ, {vrms}VRMS')

    # Apply Sine wave, kilohertz, Vrms, no offset
    def apply_sine_khz_vrms(self, freq, vrms):
        self.instr.write(f'APPL:SIN {freq}KHZ, {vrms}VRMS')

    # Set Function to Sine
    def set_sine_mode(self):
        self.instr.write('FUNC SIN')

    # Set Frequency in µHz
    def set_freq_uhz(self, freq):
        self.instr.write(f'FREQ {freq}UHZ')

    # Set Frequency in Hz
    def set_freq_hz(self, freq):
        self.instr.write(f'FREQ {freq}HZ')

    # Set Frequency in kHz
    def set_freq_khz(self, freq):
        self.instr.write(f'FREQ {freq}kHZ')

    # Set Frequency in MHz
    def set_freq_mhz(self, freq):
        self.instr.write(f'FREQ {freq}MHZ')

    # Set Voltage Units to Vrms
    def set_volt_unit_vrms(self):
        self.instr.write('VOLT:UNIT VRMS')

    # Set Voltage Units to Vpp
    def set_volt_unit_vpp(self):
        self.instr.write('VOLT:UNIT VPP')

    # Set Voltage in Vpp
    def set_volt_vpp(self, volt):
        self.instr.write(f'VOLT {volt}VPP')

    # Set Voltage in Vrms
    def set_volt_vrms(self, volt):
        self.instr.write(f'VOLT {volt}VRMS')

    # Set Voltage to Max
    def set_volt_max(self):
        self.instr.write('VOLT MAX')

    # Set Output to On
    def set_output_on(self):
        self.instr.write('OUTP ON')

    # Set Output to Off
    def set_output_off(self):
        self.instr.write('OUTP OFF')


class Keysight3458A(Instr):
    # Initialize with resource
    def __init__(self, resource):
        super().__init__(resource)
        self.instr.write('END')

    # Reset instrument
    def reset(self):
        self.instr.write('RESET')
        self.instr.write('END')

    # Clear instrument
    def clear(self):
        self.instr.write('CLEAR')
        self.instr.write('END')

    # Retrieve instrument ID
    def get_id(self) -> str:
        return self.instr.query('ID?')

    # Retrieve instrument Information
    def get_info(self) -> str:
        idn = self.instr.query('ID?')

        manu = 'Keysight'
        if manu in idn:
            model = idn[8:].strip()
        else:
            model = idn[2:].strip()

        return f'{manu} {model}'

    # Set FUNC to DCV
    def set_func_dcv(self):
        self.instr.write('FUNC DCV')

    # Set FUNC to ACV
    def set_func_acv(self):
        self.instr.write('FUNC ACV')

    # Set FUNC to ACDCV
    def set_func_acdcv(self):
        self.instr.write('FUNC ACDCV')

    # Set FUNC to OHM
    def set_func_ohm(self):
        self.instr.write('FUNC OHM')

    # Set FUNC to OHMF
    def set_func_ohmf(self):
        self.instr.write('FUNC OHMF')

    # Set FUNC to DCI
    def set_func_dci(self):
        self.instr.write('FUNC DCI')

    # Set FUNC to ACI
    def set_func_aci(self):
        self.instr.write('FUNC ACI')

    # Set FUNC to ACDCI
    def set_func_acdci(self):
        self.instr.write('FUNC ACDCI')

    # Set FUNC to FREQ
    def set_func_freq(self):
        self.instr.write('FUNC FREQ')

    # Set FUNC to PER
    def set_func_per(self):
        self.instr.write('FUNC PER')

    # Set FUNC to DSAC
    def set_func_dsac(self):
        self.instr.write('FUNC DSAC')

    # Set FUNC to DSDC
    def set_func_dsdc(self):
        self.instr.write('FUNC DSDC')

    # Set FUNC to SSAC
    def set_func_ssac(self):
        self.instr.write('FUNC SSAC')

    # Set FUNC to SSDC
    def set_func_ssdc(self):
        self.instr.write('FUNC SSDC')

    # Set the NPLC
    def set_nplc(self, nplc: int = 25):
        self.instr.write(f'NPLC {nplc}')

    # Set LFILTER to OFF
    def set_lfilter_off(self):
        self.instr.write('LFILTER OFF')

    # Set LFILTER to ON
    def set_lfilter_on(self):
        self.instr.write('LFILTER ON')

    # Set MATH to OFF
    def set_math_off(self):
        self.instr.write('MATH OFF')

    # Set MATH to CONT
    def set_math_cont(self):
        self.instr.write('MATH CONT')

    # Set MATH to CTHRM
    def set_math_cthrm(self):
        self.instr.write('MATH CTHRM')

    # Set MATH to DB
    def set_math_db(self):
        self.instr.write('MATH DB')

    # Set MATH to DBM
    def set_math_dbm(self):
        self.instr.write('MATH DBM')

    # Set MATH to FILTER
    def set_math_filter(self):
        self.instr.write('MATH FILTER')

    # Set MATH to FTHRM
    def set_math_fthrm(self):
        self.instr.write('MATH FTHRM')

    # Set MATH to NULL
    def set_math_null(self):
        self.instr.write('MATH NULL')

    # Set MATH to PERC
    def set_math_perc(self):
        self.instr.write('MATH PERC')

    # Set MATH to PFAIL
    def set_math_pfail(self):
        self.instr.write('MATH PFAIL')

    # Set MATH to RMS
    def set_math_rms(self):
        self.instr.write('MATH RMS')

    # Set MATH to SCALE
    def set_math_scale(self):
        self.instr.write('MATH SCALE')

    # Set MATH to STAT
    def set_math_stat(self):
        self.instr.write('MATH STAT')

    # Set MATH to CTHRM2K
    def set_math_cthrm2k(self):
        self.instr.write('MATH CTHRM2K')

    # Set MATH to CTHRM10K
    def set_math_cthrm10k(self):
        self.instr.write('MATH CTHRM10K')

    # Set MATH to FTHRM2K
    def set_math_fthrm2k(self):
        self.instr.write('MATH FTHRM2K')

    # Set MATH to FTHRM10K
    def set_math_fthrm10k(self):
        self.instr.write('MATH FTHRM10K')

    # Set MATH to CRTD85
    def set_math_crtd85(self):
        self.instr.write('MATH CRTD85')

    # Set MATH to CRTD92
    def set_math_crtd92(self):
        self.instr.write('MATH CRTD92')

    # Set MATH to FRTD85
    def set_math_frtd85(self):
        self.instr.write('MATH FRTD85')

    # Set MATH to FRTD92
    def set_math_frtd92(self):
        self.instr.write('MATH FRTD92')

    # Set the number of readings per trigger
    def set_nrdgs(self, num: int = 100):
        self.instr.write(f'NRDGS {num}')

    # Retrieve MATH DEGREE
    def get_math_degree(self) -> str:
        return self.instr.query('RMATH DEGREE')

    # Retrieve MATH LOWER
    def get_math_lower(self) -> str:
        return self.instr.query('RMATH LOWER')

    # Retrieve MATH MAX
    def get_math_max(self) -> str:
        return self.instr.query('RMATH MAX')

    # Retrieve MATH MEAN
    def get_math_mean(self) -> str:
        return self.instr.query('RMATH MEAN')

    # Retrieve MATH MIN
    def get_math_min(self) -> str:
        return self.instr.query('RMATH MIN')

    # Retrieve MATH NSAMP
    def get_math_nsamp(self) -> str:
        return self.instr.query('RMATH NSAMP')

    # Retrieve MATH OFFSET
    def get_math_offset(self) -> str:
        return self.instr.query('RMATH OFFSET')

    # Retrieve MATH PERC
    def get_math_perc(self) -> str:
        return self.instr.query('RMATH PERC')

    # Retrieve MATH REF
    def get_math_ref(self) -> str:
        return self.instr.query('RMATH REF')

    # Retrieve MATH RES
    def get_math_res(self) -> str:
        return self.instr.query('RMATH RES')

    # Retrieve MATH SCALE
    def get_math_scale(self) -> str:
        return self.instr.query('RMATH SCALE')

    # Retrieve MATH SDEV
    def get_math_sdev(self) -> str:
        return self.instr.query('RMATH SDEV')

    # Retrieve MATH UPPER
    def get_math_upper(self) -> str:
        return self.instr.query('RMATH UPPER')

    # Retrieve MATH HIRES
    def get_math_hires(self) -> str:
        return self.instr.query('RMATH HIRES')

    # Retrieve MATH PFAILNUM
    def get_math_pfailnum(self) -> str:
        return self.instr.query('RMATH PFAILNUM')

    # Set SETACV to ANA
    def set_setacv_ana(self):
        self.instr.write('SETACV ANA')

    # Set SETACV to RNDM
    def set_setacv_rndm(self):
        self.instr.write('SETACV RNDM')

    # Set SETACV to SYNC
    def set_setacv_sync(self):
        self.instr.write('SETACV SYNC')

    # Set the last reading into SMATH of DEGREE
    def set_smath_degree(self):
        self.instr.write('SMATH DEGREE')

    # Set the last reading into SMATH of LOWER
    def set_smath_lower(self):
        self.instr.write('SMATH LOWER')

    # Set the last reading into SMATH of MAX
    def set_smath_max(self):
        self.instr.write('SMATH MAX')

    # Set the last reading into SMATH of MEAN
    def set_smath_mean(self):
        self.instr.write('SMATH MEAN')

    # Set the last reading into SMATH of MIN
    def set_smath_min(self):
        self.instr.write('SMATH MIN')

    # Set the last reading into SMATH of NSAMP
    def set_smath_nsamp(self):
        self.instr.write('SMATH NSAMP')

    # Set the last reading into SMATH of OFFSET
    def set_smath_offset(self):
        self.instr.write('SMATH OFFSET')

    # Set the last reading into SMATH of PERC
    def set_smath_perc(self):
        self.instr.write('SMATH PERC')

    # Set the last reading into SMATH of REF
    def set_smath_ref(self):
        self.instr.write('SMATH REF')

    # Set the last reading into SMATH of RES
    def set_smath_res(self):
        self.instr.write('SMATH RES')

    # Set the last reading into SMATH of SCALE
    def set_smath_scale(self):
        self.instr.write('SMATH SCALE')

    # Set the last reading into SMATH of UPPER
    def set_smath_upper(self):
        self.instr.write('SMATH UPPER')

    # Set the last reading into SMATH of HIRES
    def set_smath_hires(self):
        self.instr.write('SMATH HIRES')

    # Set the last reading into SMATH of PFAILNUM
    def set_smath_pfailnum(self):
        self.instr.write('SMATH PFAILNUM')

    # Retrieve Reading
    def get_measurement(self) -> float:
        try:
            return float(self.instr.read())
        except:
            return -999999

    # Retrieve Readings
    def get_measurements(self, count: int = 5) -> list:
        readings = []
        result = []
        for _ in range(count):
            readings.append(self.instr.read())
        for num in readings:
            try:
                result.append(float(num))
            except:
                result.append(-9999)
        return result
