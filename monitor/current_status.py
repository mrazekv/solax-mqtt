#!/usr/bin/env python3
from solaxcom import SolaxCom
from mqtt_local import MqttLocal
from exporter import Exporter
import yaml
import pathlib
import os


if __name__=="__main__":

    top_path = pathlib.Path(__file__).parent.resolve()
    config = yaml.load(open(os.path.join(top_path, "config.yaml")).read(), Loader=yaml.FullLoader)

    solax = SolaxCom(config["solax"]["address"], config["solax"]["sn"])
    mqtt = MqttLocal(**config["mqtt"])    
    exporter = Exporter()
    exporter.export_all(solax=solax, mqtt=mqtt, verbose=True)