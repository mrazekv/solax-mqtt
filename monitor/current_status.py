#!/usr/bin/env python3
from solaxcom import SolaxCom
from mqtt_local import MqttLocal
from exporter import Exporter
import yaml

if __name__=="__main__":

    config = yaml.load(open("config.yaml").read(), Loader=yaml.FullLoader)

    solax = SolaxCom(config["solax"]["address"], config["solax"]["sn"])
    mqtt = MqttLocal(**config["mqtt"])    
    exporter = Exporter()
    exporter.export_all(solax=solax, mqtt=mqtt, verbose=True)