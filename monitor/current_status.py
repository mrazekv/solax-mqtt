#!/usr/bin/env python3
from solaxcom import SolaxCom
from mqtt_local import MqttLocal
from exporter import Exporter


if __name__=="__main__":
    solax = SolaxCom()
    mqtt = MqttLocal()    
    exporter = Exporter()
    exporter.export_all(solax=solax, mqtt=mqtt, verbose=True)