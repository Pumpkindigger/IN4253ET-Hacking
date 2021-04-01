FROM debian:latest

# Do installs
RUN apt-get update
RUN apt-get install --no-install-recommends -y qemu-system libvirt-clients libvirt-daemon-system virtinst libguestfs-tools telnet # Install QEMU for virtualization, libvirt for configuration and management, virtinst for cli vm creation, libguestsfs for accessing images, telnet for establishing connection to the VMs.
RUN apt-get install -y bridge-utils libosinfo-bin wget net-tools
RUN apt-get install qemu-efi-aarch64

# Download image x86 openwrt for QEMU
RUN mkdir /qemu_images
RUN wget -P /qemu_images https://downloads.openwrt.org/releases/19.07.7/targets/x86/64/openwrt-19.07.7-x86-64-combined-ext4.img.gz
RUN gunzip /qemu_images/openwrt-19.07.7-x86-64-combined-ext4.img.gz

# Download mips openwrt
RUN wget -P /qemu_images https://downloads.openwrt.org/releases/19.07.7/targets/malta/be/openwrt-19.07.7-malta-be-vmlinux-initramfs.elf

# Download arm image
RUN wget -P /qemu_images https://downloads.openwrt.org/releases/19.07.7/targets/armvirt/64/openwrt-19.07.7-armvirt-64-Image-initramfs

# Make bridge.conf file to allow bridge utilities for QEMU
RUN mkdir /etc/qemu
RUN echo "allow br0" >> /etc/qemu/bridge.conf

# Add qemu startup script
COPY qemu-setup.sh /qemu-setup.sh
RUN chmod +x /qemu-setup.sh

# Add iotpot to docker instance
RUN mkdir /iotpot
COPY ./iotpot/ /iotpot/

# https://wiki.debian.org/KVM
# https://jamielinux.com/docs/libvirt-networking-handbook/