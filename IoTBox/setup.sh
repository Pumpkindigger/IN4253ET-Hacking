# Create bridge
brctl addbr br0

# Make sure everything is up
ip link set dev br0 up

# Start X86 QEMU instance
qemu-system-x86_64 -drive format=raw,file=/qemu_images/openwrt-19.07.7-x86-64-combined-ext4.img -net nic -net bridge,br=br0 -daemonize -serial telnet:localhost:4321,server,nowait;

# Start mips QEMU instance
qemu-system-mips -kernel /qemu_images/openwrt-19.07.7-malta-be-vmlinux-initramfs.elf -net nic -net bridge,br=br0 -daemonize -serial telnet:localhost:4322,server,nowait;

# Start ARM QEMU instance
qemu-system-aarch64 -m 1024 -smp 2 -cpu cortex-a57 -M virt -kernel /qemu_images/openwrt-19.07.7-armvirt-64-Image-initramfs -net nic -net bridge,br=br0 -daemonize -serial telnet:localhost:4323,server,nowait;

