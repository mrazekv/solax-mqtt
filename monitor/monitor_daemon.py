#!/usr/bin/env python3

from solaxcom import SolaxCom
from mqtt_local import MqttLocal
from exporter import Exporter
import sched, time  
import sys
import logging


if __name__=="__main__":
    solax = SolaxCom()
    mqtt = MqttLocal()    
    exporter = Exporter()

    def do_something(scheduler):
        # schedule the next call first
        scheduler.enter(60, 1, do_something, (scheduler,))
        logging.log(0, "Refresh")
        try:
            exporter.export_all(solax=solax, mqtt=mqtt)
        except Exception as e:
            logging.error("Solax failure:" + str(e), exc_info=e)
        # then do your stuff
    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(1, 1, do_something, (my_scheduler,))
    my_scheduler.run()
