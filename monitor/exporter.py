import numpy as np
import csv
import os

#from solaxcom import X3HybridG4
from solax.units import Units
from solax.inverters import X3HybridG4

class Exporter:
    def __init__(self):
        # load input register file
        pass

    def export_all(self, solax, mqtt, verbose=False):
        solax.reload()
        for (name), j in X3HybridG4.response_decoder().items():
            if len(j) == 3:
                (id, unit_or_measurement, fn) = j
            else:
                (id, unit_or_measurement) = j
                fn = lambda x: x

            if type(id) is int:
                val =  solax.alld[id]
            else:
                ids, pack_fn = id
                val = pack_fn(*[solax.alld[i] for i in ids])

            if verbose:
                r_unit = "???"
                if isinstance(unit_or_measurement, Units):
                    r_unit = unit_or_measurement.value
                else:
                    r_unit = unit_or_measurement.unit.value
            
                print(name, " = ", fn(val), r_unit) #, unit.value)

            mqtt[name.replace(" ", "")] = fn(val)
