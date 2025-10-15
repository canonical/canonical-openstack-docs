Configuring GPU Passthrough
===========================

Overview
--------

The GPU passthrough allows full access and direct control of physical GPU
device in guests. The guests should have the corresponding drivers to use
the devices.

.. _gpu_passthrough_prerequisites:

Prerequisites
-------------

1. Enable the VT-d settings in BIOS.

2. Add the following kernel parameters.

::

    intel_iommu=on amd_iommu=on

Manual mode
-----------

Canonical Openstack will determine if there are any GPU devices. `PCI device
classes`_ of type Display Controller (0x03) and Processing Accelerators (0x1200)
are filtered as GPU devices. The devices are automatically added to `Nova PCI 
whitelist`_ and no user intervention is required.

Maas mode
---------

Maas mode works similar to Manual mode and the detected GPU devices are added
to `Nova PCI whitelist`_ with no user intervention.

Ensure that MAAS is configured to apply the necessary kernel parameters.

Manifest configuration
----------------------

Arbitrary PCI devices may be whitelisted through the Canonical Openstack manifest.

Example:

::

    pci:
      device_specs:
        - address: "0000:4b:00.0"
          vendor_id: "10de"
          product_id: "1db4"
      excluded_devices:
        r740-dc1-ceph.maas:
          - "0000:19:00.0"
          - "0000:19:00.1"
          - "0000:1b:00.1"
          - "0000:5e:00.0"
      aliases:
        - vendor_id: "10de"
          product_id: "1db4"
          device_type: type-PCI
          name: "nvidia-gpu"

The device spec filters are highly flexible and can contain PCI address wildcards
or PCI vendor/product IDs. See the `Nova device spec reference`_ for more details.

The device whitelist will be applied to all the compute nodes. If needed, use
the exclusion list to define per-node lists of devices that should not be
exposed to Openstack instances.

Configured `PCI device aliases`_ may be requested through Nova flavor extra specs.

Attaching GPUs to Openstack instances
-------------------------------------------

Create a flavor with pci_passthrough:alias property.

In the below example, the property is set on an existing flavor.

::

    openstack flavor set m1.tiny --property "pci_passthrough:alias"="nvidia-gpu:1"

Launch a demo instance:

::

    sunbeam launch --name test

Verify the Libvirt domain:

::

    $ sudo openstack-hypervisor.virsh dumpxml instance-00000001 | grep "hostdev mode='subsystem' type='pci'" -A 7
    <hostdev mode='subsystem' type='pci' managed='yes'>
      <driver name='vfio'/>
      <source>
        <address domain='0x0000' bus='0x41' slot='0x00' function='0x0'/>
      </source>
      <alias name='hostdev0'/>
      <address type='pci' domain='0x0000' bus='0x04' slot='0x00' function='0x0'/>
    </hostdev>


Verify the PCI device in the guest:

::

    $ ssh -i /home/ubuntu/snap/openstack/x1/sunbeam ubuntu@172.16.2.115 sudo lspci -nn
    ...
    ...
    04:00.0 3D controller [0302]: NVIDIA Corporation GV100GL [Tesla V100 PCIe 16GB] [10de:1db4] (rev a1)
    ...
    ...

Above example shows the passthrough device Nvidia 3D controller in the guest.

.. Links

.. _Nova PCI whitelist: https://docs.openstack.org/nova/latest/admin/pci-passthrough.html
.. _Nova device spec reference: https://docs.openstack.org/nova/latest/configuration/config.html#pci.device_spec
.. _PCI device aliases: https://docs.openstack.org/nova/latest/configuration/config.html#pci.alias
.. _PCI device classes: https://admin.pci-ids.ucw.cz/read/PD/
