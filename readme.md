# IoT HoneyPot

## Supervisor:  
Misha Glazunov M.Glazunov@tudelft.nl

## Group members:
Adriaan de Vos - 4422643 - adriaan.devos@gmail.com  
Peter Elgar - 5396328 - p.w.j.elgar@student.tudelft.nl  
Suzanne Maquelin - 5402840 - s.l.maquelin@student.tudelft.nl  
Wouter Zonneveld - 4582861 - w.r.zonneveld@student.tudelft.nl  

## Requirements
- Docker>=19

## Repository Structure
`./iotpot/` folder contains the Python code for our IoT Honeypot.  
`./database/` folder contains Python scripts that we used to populate our MongoDB database with banners.  
`./qemu/ folder contains bash scripts that are related to qemu managing.  
`Dockerfile` is used to build and run the IoTHoneypot.

### IoTHoneypot Setup
On your host-pc:
- For building: ```docker build -t iotbox .```  
- For running: ```docker run -it iotbox```  

In the IoTHoneypot Docker Instance:
- To boot up the qemu instances, run ```./qemu/qemu-setup.sh```.  
- To run our IoTHoneypot server, move to `/iotpot/`  and run `python3 main.py`.

## Preparations for Development workspace
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

