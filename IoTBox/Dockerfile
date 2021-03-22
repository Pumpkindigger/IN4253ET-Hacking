FROM debian:latest

# Do installs
RUN apt-get update
RUN apt-get install --no-install-recommends -y qemu-system libvirt-clients libvirt-daemon-system virtinst # Install QEMU for virtualization, libvirt for configuration and management, virtinst for cli vm creation
RUN apt-get install bridge-utils libguestfs-tools genisoimage libosinfo-bin wget net-tools


# Download image openwrt for QEMU
RUN mkdir /qemu_images
RUN wget -P /qemu_images https://downloads.openwrt.org/releases/19.07.7/targets/x86/64/openwrt-19.07.7-x86-64-combined-ext4.img.gz
RUN gunzip /qemu_images/openwrt-19.07.7-x86-64-combined-ext4.img.gz

# Make bridge.conf file to allow bridge utilities for QEMU
RUN mkdir /etc/qemu
RUN echo "allow br0" >> /etc/qemu/bridge.conf

COPY setup.sh /setup.sh

# https://wiki.debian.org/KVM
# https://jamielinux.com/docs/libvirt-networking-handbook/
