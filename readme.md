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

## Folder Structure
`./database/` folder contains scripts that we used to populate our MongoDB database with banners.  
`./iotpot/` folder contains the code for our IoT Honeypot.  
`qemu-setup.sh` is used to start the qemu instances within docker.  
`Dockerfile` is used to build and configure the docker instance.

### Shodan
Username: 2GgLivbNtbRqE5Sr\
Password: TLuekis2Qx9UVWEp

### IoTBOX Setup
First, ensure you have a working docker v19> installation. Resources we used:
- docker.com
- https://www.digitalocean.com/community/questions/how-to-fix-docker-got-permission-denied-while-trying-to-connect-to-the-docker-daemon-socket

Then, run the following commands:  
For building this image (once): ```docker build -t iotbox .```  
For running an instance: ```docker run -it iotbox```  

To set up the qemu instances, run ```./qemu-setup.sh``` in the docker container.  
To run our IoT Honey pot, move to `/iotpot/`  and run `python3 main.py`.

[comment]: <> (TODO add a description for setting up tuntap on Mac)
