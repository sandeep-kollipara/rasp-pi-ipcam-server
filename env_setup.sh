sudo apt install python3-venv
python3 -m venv venviron
source .venviron/bin/activate
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install python-picamera python3-picamera
sudo apt install -y python3-libcamera python3-kms++
sudo apt install -y python3-prctl libatlas-base-dev ffmpeg libopenjp2-7 python3-pip
sudo apt-get install python3-opencv
python3 -m pip install imutils
#pip3 install numpy --upgrade
NOGUI=1 pip3 install picamera2
sudo pip install picamera
#pip3 install imutils
#python -m pip install -r requirements_addl.txt
