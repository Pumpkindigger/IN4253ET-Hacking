#!/bin/bash

case "$1" in
    0) rm /qemu_images/openwrt-19.07.7-x86-64-combined-ext4_copy.img && cp /qemu_images/openwrt-19.07.7-x86-64-combined-ext4.img /qemu_images/openwrt-19.07.7-x86-64-combined-ext4_copy.img && qemu-system-x86_64 -drive format=raw,file=/qemu_images/openwrt-19.07.7-x86-64-combined-ext4_copy.img -daemonize -serial telnet:localhost:4321,server,nowait && echo "0";;
    1) rm /qemu_images/openwrt-19.07.7-malta-be-vmlinux-initramfs_copy.elf && cp /qemu_images/openwrt-19.07.7-malta-be-vmlinux-initramfs.elf /qemu_images/openwrt-19.07.7-malta-be-vmlinux-initramfs_copy.elf && qemu-system-mips -kernel /qemu_images/openwrt-19.07.7-malta-be-vmlinux-initramfs_copy.elf -daemonize -serial telnet:localhost:4322,server,nowait && echo "1";;
    2) rm /qemu_images/openwrt-19.07.7-armvirt-64-Image-initramfs_copy && cp /qemu_images/openwrt-19.07.7-armvirt-64-Image-initramfs /qemu_images/openwrt-19.07.7-armvirt-64-Image-initramfs_copy && qemu-system-aarch64 -m 1024 -smp 2 -cpu cortex-a57 -M virt -kernel /qemu_images/openwrt-19.07.7-armvirt-64-Image-initramfs_copy -daemonize -serial telnet:localhost:4323,server,nowait && echo "2";;
esac
