#chmod 700 env_setup.sh
#./env_setup.sh
# Module 3 camera supports HDR mode:
v4l2-ctl --set-ctrl wide_dynamic_range=1 -d /dev/v4l-subdev0
python3 main.py
