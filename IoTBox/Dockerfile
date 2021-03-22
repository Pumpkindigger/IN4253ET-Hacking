FROM debian:latest

# Do installs
RUN apt-get update && apt-get install -y qemu qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils libguestfs-tools  genisoimage  virtinst  libosinfo-bin  virt-manager  wget uml-utilities  net-tools



# Download image openwrt for QEMU
RUN mkdir /qemu_images
RUN wget -P /qemu_images https://downloads.openwrt.org/releases/19.07.7/targets/x86/64/openwrt-19.07.7-x86-64-combined-ext4.img.gz
RUN gunzip /qemu_images/openwrt-19.07.7-x86-64-combined-ext4.img.gz

# Make bridge.conf file to allow bridge utilities for QEMU
RUN mkdir /etc/qemu
RUN echo "allow br0" >> /etc/qemu/bridge.conf

COPY setup.sh /setup.sh
