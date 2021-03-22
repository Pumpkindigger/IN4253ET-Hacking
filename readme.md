# IoT HoneyPot

## Supervisor:  
Misha Glazunov M.Glazunov@tudelft.nl

## Group members:
Adriaan de Vos - 4422643 - adriaan.devos@gmail.com  
Peter Elgar - 5396328 - p.w.j.elgar@student.tudelft.nl  
Suzanne Maquelin - 5402840 - s.l.maquelin@student.tudelft.nl  
Wouter Zonneveld - 4582861 - w.r.zonneveld@student.tudelft.nl  

## Preparations
Requirements:
- Python3.8
- Python3 pip
- Python3 venv

Creation of virtual environment and installing dependencies
```shell
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

## Usage
`server.py` is our IoT Honeypot  
`client.pt` is used to test and create telnet connections

### Shodan
Username: 2GgLivbNtbRqE5Sr\
Password: TLuekis2Qx9UVWEp

### IoTBOX
Setting up IoTBOX:  
First navigate to the folder containing the Dockerfile, and run this command.  
```docker build -t iotbox .```  
```docker run -d -it --cap-add=NET_ADMIN --name Lab --device=/dev/net/tun iotbox```  

[comment]: <> (TODO add a description for getting and running the .sh file)
[comment]: <> (TODO add a description for setting up tuntap on Mac)