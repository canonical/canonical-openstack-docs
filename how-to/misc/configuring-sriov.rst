Configuring SR-IOV
==================

Overview
--------

The Single Root I/O Virtualization (SR-IOV) specification allows splitting
a single physical port (called physical function or PF) into multiple virtual
ports known as virtual functions or VFs.

VFs as well as PFs can be assigned to Openstack instances, bypassing the
host network stack and significantly improving performance while reducing
host resource usage.

Hardware offloading, also known as switchdev mode, is a mechanism that
enables Open vSwitch (OVS) flows to be offloaded directly to the Virtual
Function (VF). This approach combines the performance advantages of SR-IOV
with the flexibility of OVS, allowing VFs to be added to the OVS bridge. As
a result, it supports the full OVN stack and facilitates overlay tenant
networks that rely on tunneling protocols such as VXLAN or Geneve.

.. _sriov_prerequisites:

Prerequisites
-------------

1. Make sure that the network adapters support SR-IOV and optionally the
hardware offloading feature.

2. Enable the SR-IOV and VT-d settings in BIOS.

3. Add the following kernel parameters, allowing VFs to be exposed to virtual
machines.

::

    intel_iommu=on iommu=pt pci=realloc pci=assign-busses

4. Optional: enable switchdev mode.

In this example, we are configuring a Mellanox ConnectX-6 device. Please
check your vendor documentation for other network adapter models.

::

    ifname=enp3s0f0np0
    pciaddr=0000:02:00.0
    sudo devlink dev eswitch set pci/${pciaddr} mode switchdev
    sudo ethtool -K $ifname hw-tc-offload on

Verify that hardware offloading is enabled:

::

    sudo devlink dev eswitch show pci/${pciaddr}
    # output #
    pci/0000:03:00.0: mode switchdev inline-mode none encap-mode basic

::

    sudo ethtool -k $ifname | grep hw-tc-offload
    # output #
    hw-tc-offload: on

5. Initialize the desired number of VFs

::

    echo '4' | sudo tee /sys/class/net/${ifname}/device/sriov_numvfs

This setting can be added to the Netplan configuration in order to survive reboots:

::

    enp3s0f0np0:
      virtual-function-count: 4
      embedded-switch-mode: "switchdev"


Verify that the VFs were created successfully:

::

    $ sudo lshw -class net -businfo
    # output #
    Bus info          Device          Class          Description
    ============================================================
    pci@0000:04:00.0  enp3s0f0np0     network        MT2892 Family [ConnectX-6 Dx]
    pci@0000:04:00.1  enp3s0f1np1     network        MT2892 Family [ConnectX-6 Dx]
    pci@0000:04:00.2  enp4s0f0v0      network        ConnectX Family mlx5Gen Virtual Function
    pci@0000:04:00.3  enp4s0f0v1      network        ConnectX Family mlx5Gen Virtual Function
    pci@0000:04:00.4  enp4s0f0v2      network        ConnectX Family mlx5Gen Virtual Function
    pci@0000:04:00.5  enp4s0f0v3      network        ConnectX Family mlx5Gen Virtual Function
    pci@0000:01:00.0  eno1            network        82599ES 10-Gigabit SFI/SFP+ Network Connection
    pci@0000:01:00.1  eno2            network        82599ES 10-Gigabit SFI/SFP+ Network Connection
    pci@0000:08:00.0  eno3            network        I350 Gigabit Network Connection
    pci@0000:08:00.1  eno4            network        I350 Gigabit Network Connection
    pci@0000:82:00.0  enp130s0f0      network        Ethernet 10G 2P X520 Adapter
    pci@0000:82:00.1  enp130s0f1      network        Ethernet 10G 2P X520 Adapter
    pci@0000:04:00.0  enp4s0f0r0      network        Ethernet interface
    pci@0000:04:00.0  enp4s0f0r1      network        Ethernet interface
    pci@0000:04:00.0  enp4s0f0r2      network        Ethernet interface
    pci@0000:04:00.0  enp4s0f0r3      network        Ethernet interface


If hardware offloading is enabled, additional `representor functions`_ may be
automatically created for each VF.

6. Ensure that you're using ``snapd`` 2.71 or later.

Manual mode
-----------

Canonical Openstack will determine if there are any SR-IOV capable
network devices.

If so, the user will be asked to specify which SR-IOV devices should be
exposed to Openstack tenants and the name of the corresponding Neutron
physical network, also known as physnet.

No physnet should be specified when using hardware offloading and overlay
networks such as VXLAN or Geneve.

Example:

:: 

    sunbeam cluster bootstrap --role control,compute
    # output #
    # ...
    Configure SR-IOV? [y/n] (n): y
    Found the following SR-IOV capable devices:
      [ ] Mellanox Technologies MT2892 Family [ConnectX-6 Dx] (enp3s0f0np0) [physnet: None]
      [ ] Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (eno1) [physnet: None]
      [ ] Mellanox Technologies MT2892 Family [ConnectX-6 Dx] (enp3s0f1np1) [physnet: None]
      [ ] Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (eno2) [physnet: None]
      [ ] Intel Corporation Ethernet 10G 2P X520 Adapter (enp130s0f0) [physnet: None]
      [ ] Intel Corporation Ethernet 10G 2P X520 Adapter (enp130s0f1) [physnet: None]
    Add network adapter to PCI whitelist? Mellanox Technologies MT2892 Family [ConnectX-6 Dx] (enp3s0f0np0) [y/n] (n): y
    Specify the physical network for Mellanox Technologies MT2892 Family [ConnectX-6 Dx] (enp3s0f0np0) or pass 'no-physnet' if using hardware offloading with overlay networks: no-physnet
    Add network adapter to PCI whitelist? Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (eno1) [y/n] (n): 
    Add network adapter to PCI whitelist? Mellanox Technologies MT2892 Family [ConnectX-6 Dx] (enp3s0f1np1) [y/n] (n): 
    Add network adapter to PCI whitelist? Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (eno2) [y/n] (n): 
    Add network adapter to PCI whitelist? Intel Corporation Ethernet 10G 2P X520 Adapter (enp130s0f0) [y/n] (n): 
    Add network adapter to PCI whitelist? Intel Corporation Ethernet 10G 2P X520 Adapter (enp130s0f1) [y/n] (n):

All the VFs that belong to the specified SR-IOV PFs will be added to the
`Nova PCI whitelist`_, in addition to the devices that may have been specified
in the :ref:`manifest file<sriov_manifest>`.

The ``openstack-hypervisor`` snap determines if the specified adapters support
hardware offloading. If not, it will configure the `Neutron SR-IOV agent`_ to
handle these ports.

The SR-IOV configuration may be subsequently modified using the following command:

::

    sunbeam configure sriov

MAAS mode
---------

When deploying Canonical Openstack in MAAS mode, set one of the following network
interface tags to expose SR-IOV adapters:

::

    sriov:<physnet>
    sriov:no-physnet

Use Curtin scripts to prepare the prerequisite SR-IOV configuration as described
in the :ref:`previous section<sriov_prerequisites>`. Also ensure that MAAS is configured
to apply the necessary kernel parameters.

Similarly to manual mode, the SR-IOV configuration can be modified using the
following command:

::

    sunbeam configure sriov

.. _sriov_manifest:

Manifest configuration
----------------------

Arbitrary PCI devices may be whitelisted through the Canonical Openstack manifest.
Apart from SR-IOV network adapters, this can also include vGPUs or FPGAs.

Example:

::

    pci:
      device_specs:
        - address: "0000:1b:00.0"
          vendor_id: "8086"
          product_id: "1563"
          physical_network: "physnet1"
      excluded_devices:
        r740-dc1-ceph.maas:
          - "0000:19:00.0"
          - "0000:19:00.1"
          - "0000:1b:00.1"
          - "0000:5e:00.0"
      aliases:
        - vendor_id: "8086"
          product_id: "1563"
          device_type: type-PF
          name: "intel-pf"

The device spec filters are highly flexible and can contain PCI address wildcards
or PCI vendor/product IDs. See the `Nova device spec reference`_ for more details.

The device whitelist will be applied to all the compute nodes. If needed, use
the exclusion list to define per-node lists of devices that should not be
exposed to Openstack instances.

Configured `PCI device aliases`_ may be requested through Nova flavor extra specs.

Attaching SR-IOV VFs to Openstack instances
-------------------------------------------

Launch a demo instance:

::

    sunbeam launch --name test

Create a port with ``--vnic-type=direct``:

::

    openstack port create --network demo-network --vnic-type=direct direct-port

Attach the port:

::

    openstack server add port test direct-port

Check the port status:

::

    openstack port show direct-port
    # output #
    +-------------------------+----------------------------------------------------------------------------------+
    | Field                   | Value                                                                            |
    +-------------------------+----------------------------------------------------------------------------------+
    | admin_state_up          | UP                                                                               |
    | allowed_address_pairs   |                                                                                  |
    | binding_host_id         | None                                                                             |
    | binding_profile         | None                                                                             |
    | binding_vif_details     | None                                                                             |
    | binding_vif_type        | None                                                                             |
    | binding_vnic_type       | direct                                                                           |
    | created_at              | 2025-07-29T09:37:26Z                                                             |
    | data_plane_status       | None                                                                             |
    | description             |                                                                                  |
    | device_id               | 1dd2e5a2-011c-4ab2-abb0-b21ee6b355a8                                             |
    | device_owner            | compute:nova                                                                     |
    | device_profile          | None                                                                             |
    | dns_assignment          | fqdn='test.cloud.sunbeam.internal.', hostname='test', ip_address='192.168.0.227' |
    | dns_domain              |                                                                                  |
    | dns_name                | test                                                                             |
    | extra_dhcp_opts         |                                                                                  |
    | fixed_ips               | ip_address='192.168.0.227', subnet_id='782b4f8b-0f05-4725-98e6-1519d44f3458'     |
    | hardware_offload_type   | None                                                                             |
    | hints                   |                                                                                  |
    | id                      | c240b03c-014d-4901-89a0-876f72c94aaf                                             |
    | ip_allocation           | immediate                                                                        |
    | mac_address             | fa:16:3e:66:b9:b2                                                                |
    | name                    | direct-port                                                                      |
    | network_id              | 578cb555-0972-4177-9739-85d29bd67ff1                                             |
    | numa_affinity_policy    | None                                                                             |
    | port_security_enabled   | True                                                                             |
    | project_id              | d081abb7eebc4279a8e8ca7ddcf7ecae                                                 |
    | propagate_uplink_status | True                                                                             |
    | resource_request        | None                                                                             |
    | revision_number         | 41                                                                               |
    | qos_network_policy_id   | None                                                                             |
    | qos_policy_id           | None                                                                             |
    | security_group_ids      | 5362283f-56e2-443a-a952-bfbdf18cfb06                                             |
    | status                  | ACTIVE                                                                           |
    | tags                    |                                                                                  |
    | trunk_details           | None                                                                             |
    | updated_at              | 2025-07-29T10:12:33Z                                                             |
    +-------------------------+----------------------------------------------------------------------------------+

Verify the Libvirt domain:

::

    $ sudo openstack-hypervisor.virsh dumpxml instance-00000001 | grep "type='hostdev" -A 8
    <interface type='hostdev' managed='yes'>
      <mac address='fa:16:3e:66:b9:b2'/>
      <driver name='vfio'/>
      <source>
        <address type='pci' domain='0x0000' bus='0x02' slot='0x00' function='0x5'/>
      </source>
      <alias name='hostdev0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x08' function='0x0'/>
    </interface>


If hardware offloading is available, the device will be added to the ``br-int``
bridge:

::

    sudo openstack-hypervisor.ovs-vsctl show
    # output #
    f9b527db-207c-453d-bcda-482610541462
        Bridge br-ex
            datapath_type: system
            Port br-ex
                Interface br-ex
                    type: internal
            Port patch-provnet-4cb61b1f-86a8-4c50-956a-04d8358ce055-to-br-int
                Interface patch-provnet-4cb61b1f-86a8-4c50-956a-04d8358ce055-to-br-int
                    type: patch
                    options: {peer=patch-br-int-to-provnet-4cb61b1f-86a8-4c50-956a-04d8358ce055}
        Bridge br-int
            fail_mode: secure
            datapath_type: system
            Port enp2s0f0r3
                Interface enp2s0f0r3
            Port tap578cb555-00
                Interface tap578cb555-00
            Port br-int
                Interface br-int
                    type: internal
            Port patch-br-int-to-provnet-4cb61b1f-86a8-4c50-956a-04d8358ce055
                Interface patch-br-int-to-provnet-4cb61b1f-86a8-4c50-956a-04d8358ce055
                    type: patch
                    options: {peer=patch-provnet-4cb61b1f-86a8-4c50-956a-04d8358ce055-to-br-int}
            Port tapdcf0ee2d-f8
                Interface tapdcf0ee2d-f8
        ovs_version: "3.5.0"

Disabling SR-IOV
----------------

The same command may also be used to disable the SR-IOV functionality.
Specify "n" for each interface that should no longer be used with SR-IOV.

::

    sunbeam configure sriov

    Found the following SR-IOV capable devices:
      [ ] Intel Corporation Ethernet Controller X550 (eno1) [physnet: None]
      [X] Intel Corporation Ethernet Controller X550 (eno2) [physnet: physnet1]
      [ ] Mellanox Technologies MT27520 Family [ConnectX-3 Pro] (enp94s0) [physnet: None]
    Add network adapter to PCI whitelist? Intel Corporation Ethernet Controller X550 (eno1)  [y/n] (n): n
    Add network adapter to PCI whitelist? Intel Corporation Ethernet Controller X550 (eno2)  [y/n] (y): n
    Add network adapter to PCI whitelist? Mellanox Technologies MT27520 Family [ConnectX-3 Pro] (enp94s0)  [y/n] (n): n

Existing instances will not be modified, consider removing VF attachments
manually to avoid subsequent port binding failures.


.. Links

.. _representor functions: https://docs.kernel.org/networking/representors.html
.. _Nova PCI whitelist: https://docs.openstack.org/nova/latest/admin/pci-passthrough.html
.. _Neutron SR-IOV agent: https://docs.openstack.org/neutron/latest/admin/config-sriov.html#enable-neutron-sriov-nic-agent-compute
.. _Nova device spec reference: https://docs.openstack.org/nova/latest/configuration/config.html#pci.device_spec
.. _PCI device aliases: https://docs.openstack.org/nova/latest/configuration/config.html#pci.alias