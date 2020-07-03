# Build PIC firmware with MPLAB-X in a docker container
PIC firmware that is developed using MPLAB-X cannot always be built using a
headless build system. The purpose of this repo is to provide a docker image
which can be used to configure and build firmware that is configured using
MPLAB-X project files.

# Acknowledgements
This docker image and associated python build script is based of the original
docker image provided on docker hub by dataspeedinc here:
https://hub.docker.com/r/dataspeedinc/mplabx

It has been modified to support the XC8 compiler.

## Getting Started
This docker image is available on docker hub.
```
docker pull mpfitzpatrick/mplabx-build:latest
```

To build your firmware, add it as a volume to the docker container when it is run:
```
docker run --rm -v $PWD:/pic mpfitzpatrick/mplabx-build
```
