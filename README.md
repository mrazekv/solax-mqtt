# Solax to MQTT monitor

# Principle
This tool monitors the status of Solax system over local network (without cloud, but Solax Cloud may be used). 
It was tested with Solax X3-G4 Hybrid. However it uses `solax` package and can be further extended for different tool.

# Usage
## Installation
The scripts has some requirements. It can be run on arbitrary Linux system such as Raspberry Pi.
It uses Python 3 langugage. For the requirements installation use
```bash
sudo pip -r requirements.txt
```

Note that root grants are required for running as a service

Copy config file and fill your details
```bash
cp monitor/config.default.yaml monitor/config.yaml
```

It will be needed to input IP address of Solax Pocket Wifi and grants to some MQTT server (local or public).

## Simple monitoring (once)
Just run 
```monitor/current_status.py```

and you should get all information from the inverter. These data are also exported to the MQTT server.

## Running as a service
Firstly, create service file with a valid path using this script.
```bash
cat > monitor/solax-monitor.service << EOF
[Unit]
Description=Solax Monitor
After=multi-user.target
[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 `pwd`/monitor/monitor_daemon.py
[Install]
WantedBy=multi-user.target
EOF
```
Then enable the service.
```bash
sudo ln monitor/solax-monitor.service /etc/systemd/system/solax-monitor.service
sudo systemctl daemon-reload
sudo systemctl enable solax-monitor.service 
# Created symlink /etc/systemd/system/multi-user.target.wants/solax-monitor.service → /etc/systemd/system/solax-monitor.service.
sudo service solax-monitor start
```

The monitor regularly (once per minute) exports the state of the inverter to MQTT.

# Usage for load balancing and reporting
The data from MQTT can be used for example as an input to nodered or exported to influxdb to be shown in grafana.

To join them together a simple combination can be used as in this [example](nodered_solax.json)
![solax](nodered_solax.png)

These data can be exported to InfluxDB or used for controlling RaspberryPi Relay as shown [here](nodered_control.json)

![control](nodered_control.png)


# Possible improvements
## Selection of different type of Inverter
Just change the inverter in [monitor/solaxcom.py](monitor/solaxcom.py) file.

## Controlling of Export
With a new version of Pocket Wifi, Modbus TCP is also enabled. You can add listenting on the MQTT and controlling the valid place in memory. Note that number of writing in the memory is limited!