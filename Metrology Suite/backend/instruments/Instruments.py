from backend.globals.settings import RESOURCE_MANAGER


class Instr:
    keysight_opts = ['HEWLETT-PACKARD', 'AGILENT']

    # Initialize with resource
    def __init__(self, resource):
        self.instr = RESOURCE_MANAGER.open_resource(resource)
        self.instr.write_termination = '\n'
        self.instr.read_termination = '\n'

    # Close connection
    def close(self):
        self.instr.close()

    # Reset instrument
    def reset(self):
        self.instr.write('*RST')

    # Clear instrument
    def clear(self):
        self.instr.write('*CLS')

    # Retrieve instrument ID
    def get_id(self) -> str:
        return self.instr.query('*IDN?')

    # Retrieve instrument Information
    def get_info(self) -> str:
        idn = self.instr.query('*IDN?')
        idn_list = idn.split(',')

        manu = idn_list[0].capitalize()
        model = idn_list[1]

        if ' ' in manu:
            manu = manu.split()[0]

        if ' ' in model:
            model = model.split()[1]

        return f'{manu} {model}'

    # Retrieve instrument Serial number
    def get_serial(self) -> str:
        idn = self.instr.query('*IDN?')
        idn_list = idn.split(',')

        return idn_list[2]
