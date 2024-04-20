# rasp-pi-ipcam-server
[Phase I: Producer] This repository holds the code developed in partial fulfilment of online credit course "CS370 - OS" offered at Colorado State University Online for Spring 2024.

## Preface
This ReadMe file will highlight the objectives with precedence, setup instructions for first-time user and finally the step-by-step development progress for reference (also reflected in the commits).

## Objectives
The rasp-pi-ipcam-server is the producer/master/server of the Producer-Consumer Architectural Pattern on which this project is designed on. Following are it's objectives/features in order of import:

[1] Connect to the IP Camera of the Raspberry Pi (4B) and transmit h264 stream feed which is then exposed to network/internet via RTSP/UDP.

[2] Support continuous integration with codebase via "GitHub Actions", a CI-CD platform built between this repo and Raspberry Pi through SSH.

[3] Provide RPC API to clients (Consumer) 

[4] Provide REST API as web service (Internet).

[5] Implement security for all IP transmissions through encryption.

### Autorun:

```autorun 
./autorun.sh
```

### To setup the environment manually:

```setup 
./env-setup.sh
```
