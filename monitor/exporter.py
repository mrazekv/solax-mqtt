import numpy as np
import csv
import os

class Exporter:
    def __init__(self, filename = "regs.csv"):
        # load input register file
        self.registers = []
        dd = os.path.dirname(__file__)

        with open(os.path.join(dd, filename),"r") as fconf:
            csv_conv = csv.reader(fconf, delimiter=",")
            for row in csv_conv:
                if len(row) != 8:
                    print("## skipping ", row)
                    continue
                self.registers.append(row)

    def export_all(self, solax, mqtt, verbose=False):
        solax.reload()
        for row in self.registers:    
            address, name, _, note, scale, unit, dtype, length = row
            if "+" in address:
                rval = 0
                for a in  address.split("+"):
                    v = solax[int(a, 0)]
                    rval = (rval << 16) |  v



            else:
                rval = solax[int(address, 0)]
            val = rval

            val = np.array(val).astype(dtype).item()

            if scale:
                val *= float(scale)
            if verbose:
                print(name, " = ", val, unit)
            mqtt[name] = val
