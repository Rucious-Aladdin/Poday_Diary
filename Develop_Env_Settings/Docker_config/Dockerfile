# Base image with Ubuntu 22.04
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages including KVM
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    openjdk-11-jdk \
    lib32stdc++6 \
    lib32z1 \
    libc6-i386 \
    libx11-6 \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    mesa-utils \
    libglu1-mesa \
    libpulse0 \
    libxcb1 \
    libx11-xcb1 \
    libxrender1 \
    libxi6 \
    libxtst6 \
    libnss3 \
    libxrandr2 \
    libxfixes3 \
    libxdamage1 \
    libfontconfig1 \
    libglvnd0 \
    libegl1 \
    libgles2 \
    libglx0 \
    libgl1 \
    qemu-kvm \
    kmod \
    net-tools\
    iperf3 \
    locales \
    iputils-ping \
    vim \
    && apt-get clean

# can using korean fonts
RUN locale-gen ko_KR.UTF-8

# Download and install Android Studio
RUN wget https://redirector.gvt1.com/edgedl/android/studio/ide-zips/2022.1.1.20/android-studio-2022.1.1.20-linux.tar.gz \
    -O /tmp/android-studio.tar.gz \
    && mkdir -p /opt/android-studio \
    && tar -xvzf /tmp/android-studio.tar.gz -C /opt/android-studio --strip-components=1 \
    && rm /tmp/android-studio.tar.gz

# Set environment variables for Android Studio
ENV ANDROID_HOME /opt/android-studio
ENV PATH $ANDROID_HOME/bin:$PATH

# Set GTK and Java environment variables for better font rendering
ENV _JAVA_OPTIONS='-Dawt.useSystemAAFontSettings=on -Dswing.aatext=true'
ENV JAVA_FONTS=/usr/share/fonts/truetype/dejavu

# Regenerate font cache
RUN fc-cache -f -v

# Entry point to start Android Studio
ENTRYPOINT ["/opt/android-studio/bin/studio.sh"]

