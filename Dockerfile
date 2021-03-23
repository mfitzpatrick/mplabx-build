# Create a docker image for building PIC firmware using XC8 2.31 and MPLABX 5.30

FROM ubuntu:18.04

# AWS APT mirrors
RUN sed -i 's+http://security.ubuntu.com/+http://archive.ubuntu.com/+g' /etc/apt/sources.list \
 && sed -i 's+http://archive.ubuntu.com/+http://us-east-1.ec2.archive.ubuntu.com/+g' /etc/apt/sources.list \
 && apt update \
 && rm -rf /var/lib/apt/lists/*

# Install git and ssh
RUN apt update \
 && apt install -y git ssh-client \
 && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN dpkg --add-architecture i386 \
 && apt update \
 && apt install -y --no-install-recommends curl libc6:i386 \
        libx11-6:i386 libxext6:i386 libstdc++6:i386 libexpat1:i386 \
        libxext6 libxrender1 libxtst6 libgtk2.0-0 make unzip \
 && rm -rf /var/lib/apt/lists/*

# Install python modules
RUN apt update \
 && apt install -y python-pip python-setuptools \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --upgrade pip
RUN pip install glob2

# Download and install XC8 compiler
RUN curl -fSL -A "Mozilla/4.0" -o /tmp/xc8.run "http://ww1.microchip.com/downloads/en/DeviceDoc/xc8-v2.31-full-install-linux-x64-installer.run" \
    && chmod a+x /tmp/xc8.run \
    && /tmp/xc8.run --mode unattended --unattendedmodeui none \
        --netservername localhost --LicenseType FreeMode --prefix /opt/microchip/xc8/v2.31 \
    && rm /tmp/xc8.run

ENV PATH="/opt/microchip/xc8/v2.31/bin:${PATH}"
ENV DFP_DIR="/root/.mchp_packs"

# Download and install MPLAB X IDE
# Use url: http://www.microchip.com/mplabx-ide-linux-installer to get the latest version
RUN curl -fSL -A "Mozilla/4.0" -o /tmp/mplabx-installer.tar "http://ww1.microchip.com/downloads/en/DeviceDoc/MPLABX-v5.45-linux-installer.tar" \
 && tar xf /tmp/mplabx-installer.tar && rm /tmp/mplabx-installer.tar \
 && USER=root ./*-installer.sh --nox11 \
    -- --unattendedmodeui none --mode unattended \
 && rm ./*-installer.sh


#Use URL packs.download.microchip.com to get the latest version
RUN curl -fSL -A "Mozilla/4.0" -o /tmp/packs-installer "http://packs.download.microchip.com/Microchip.PIC16F1xxxx_DFP.1.6.143.atpack" \
 && mkdir /root/.mchp_packs \
 && unzip /tmp/packs-installer -d /root/.mchp_packs/. \
 && rm /tmp/packs-installer

# Add MPLABX build scripts
ADD mplabxBuildProject.py /usr/bin

RUN ln -s -f /usr/bin/mplabxBuildProject.py /usr/bin/mplabx-build-project
