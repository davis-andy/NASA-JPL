"""
All the functions that are exposed to Eel are in this file.
Thought it would be cleaner on a separate file than to clutter the main.py file.
"""

import eel

# Global functions
from backend.globals.instruments import set_instrs, get_instrs
from backend.globals.indysoft import indy_login, instr_model, instr_serial, temp_data
from backend.globals.settings import set_user_settings, set_user_password, get_user_settings, get_user_setting, \
    get_user_password, set_bench_configs, get_bench_configs, set_ip, get_nics, change_ip, main_logger


# MUX Card Functions
from backend.daq.settings import daq_software_notes, daq_save_uut_specs, daq_set_uut_specs, daq_get_type_e, \
    daq_get_type_j, daq_get_type_k, daq_get_type_t, daq_show_setup, daq_test_setup, daq_check_stds, \
    daq_get_stds_loaded, mainframe, UUT, TC_SIMULATOR, daq_get_temp_settle, daq_excel_info, tests_screen, \
    daq_setup_standards, daq_get_type_e_acceptance, daq_get_type_j_acceptance, daq_get_type_k_acceptance, \
    daq_get_type_t_acceptance, daq_initial_excel_save, daq_get_state, daq_stop_tests, daq_set_std_specs, \
    daq_save_std_specs, daq_ending_excel_save, daq_get_final_acceptance, daq_reset_final_acceptance, \
    daq_open_report_path, daq_logger
from backend.daq.tests.type_e import daq_run_type_e, daq_run_type_e_params, daq_setup_type_e
from backend.daq.tests.type_j import daq_run_type_j, daq_run_type_j_params, daq_setup_type_j
from backend.daq.tests.type_k import daq_run_type_k, daq_run_type_k_params, daq_setup_type_k
from backend.daq.tests.type_t import daq_run_type_t, daq_run_type_t_params, daq_setup_type_t
