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
This docker image is available on github container registry.
```
docker pull ghcr.io/mfitzpatrick/mplabx-build:<tag name>
```

To build your firmware, add it as a volume to the docker container when it is run:
```
docker run --rm -v $PWD:/pic mpfitzpatrick/mplabx-build
```

# Releases
Docker Hub has recently changed its policy and stopped automated builds linked to open-source
repositories from working by default. For simplicity, this has now been moved over to Github
Container Registry. Follow the link to the github repository, and search for updated images
in the releases section.

