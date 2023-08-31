from solax.inverter import Inverter
from solax.units import Total, Units
from solax.inverters import X3HybridG4
import requests
import yaml

class SolaxCom:
    def __init__(self, solax_address, solax_sn):
        self.solax_address = solax_address
        self.solax_sn = solax_sn
        self.reload()

    def reload(self):
        r = requests.post(f"http://{self.solax_address}" , data=f"optType=ReadRealTimeData&pwd={self.solax_sn}")
        r.raise_for_status()
        d = r.json()
        self.alld = d["Data"]

    def __getitem__(self, i):
        if i < 0 or i >= len(self.alld):
            raise(Exception(f"SOLAX: Unknown address 0x{i:04x} while max is 0x{len(self.alld):04x}"))
        return self.alld[i]


if __name__ == "__main__":
    import requests
    
    config = yaml.load(open("config.yaml").read(), Loader=yaml.BaseLoader)

    s = SolaxCom(config["solax"]["address"], config["solax"]["sn"])

    print("Read {0:d} (0x{0:04x}) short integers".format(len(s.alld)))
    for (name), j in X3HybridG4.response_decoder().items():
        if len(j) == 3:
            (id, unit_or_measurement, fn) = j
        else:
            (id, unit) = j
            fn = lambda x: x

        if type(id) is int:
            val =  s.alld[id]
        else:
            ids, pack_fn = id
            val = pack_fn(*[s.alld[i] for i in ids])

        r_unit = "???"
        if isinstance(unit_or_measurement, Units):
            r_unit = unit_or_measurement.value
        else:
            r_unit = unit_or_measurement.unit.value
        
        print(name, " = ", fn(val), r_unit) #, unit.value)

