"""A Python Pulumi program"""

import pulumi

import pulumi_proxmoxve as proxmox
import os

proxmox_provider = proxmox.Provider(
    resource_name="pxprovider",
    endpoint=os.getenv("PX_ENDPOINT"),
    api_token=os.getenv("PX_TOKEN"),
    insecure=bool(os.getenv("PX_INSECURE","false"))
)
test_machine = proxmox.vm.VirtualMachine(
    opts=pulumi.ResourceOptions(provider=proxmox_provider),
    resource_name="tm1",
    node_name="tokio",
    clone=proxmox.vm.VirtualMachineCloneArgs(
            node_name="tokio",
            vm_id=6000,
            full=True
        ),
    cpu=proxmox.vm.VirtualMachineCpuArgs(
        cores=2,
        sockets=1
    ),
    disks=[
        proxmox.vm.VirtualMachineDiskArgs(
            interface="scsi0",
            datastore_id="vmpool",
            size=20,
            file_format="raw"
        )
    ],
    memory=proxmox.vm.VirtualMachineMemoryArgs(
        dedicated=2048
    ),
    initialization=proxmox.vm.VirtualMachineInitializationArgs(
        datastore_id="vmpool",
        dns=proxmox.vm.VirtualMachineInitializationDnsArgs(
            domain="",
            servers=["192.168.178.1"]
        ),
        ip_configs=[
            proxmox.vm.VirtualMachineInitializationIpConfigArgs(
                ipv4=proxmox.vm.VirtualMachineInitializationIpConfigIpv4Args(
                    address="192.168.178.240/24",
                    gateway="192.168.178.1"
                ),
            )
        ],
        user_account=proxmox.vm.VirtualMachineInitializationUserAccountArgs(
            username="proxmox",
            password="test1234",
            keys=["ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEzurqIvWE9mkV6zL5n6q+oHvn5pG/HNFsXTmvYpzUGJ"]
        )
    )
)