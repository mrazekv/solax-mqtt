from pyModbusTCP.client import ModbusClient

class SolaxCom:
    def __init__(self):
        # TCP auto connect on first modbus request
        self.c = ModbusClient(host="192.168.1.105", port=502, unit_id=1, auto_open=True)
        self.reload()

    def reload(self):
        max_address = 0x0120 # including this number
        # read all data in batch
        self.alld = []
        read_size = 16
        for i in range(0,max_address + 1, read_size):
            rs = read_size
            if i + rs > max_address:
                rs =  max_address - i + 1

            resp = self.c.read_input_registers(i, rs)
            if not resp:
                raise(Exception(f"SOLAX: Bad read from address 0x{i:04x}"))
            #print(i, len(resp), read_size, rs)
            self.alld += resp
    def __getitem__(self, i):
        if i < 0 or i >= len(self.alld):
            raise(Exception(f"SOLAX: Unknown address 0x{i:04x} while max is 0x{len(self.alld):04x}"))
        return self.alld[i]
