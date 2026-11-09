Configuring DPU
===============

Overview
--------

A Data Processing Unit (DPU), also known as an off-path SmartNIC, builds on
Single Root I/O Virtualization (SR-IOV): a single physical port (physical
function, or PF) is split into multiple virtual ports (virtual functions, or
VFs) that are passed through to OpenStack instances, bypassing the host network
stack to significantly improve performance while reducing host resource usage.

The DPU is enrolled in MAAS as its own machine and joins Sunbeam with the
``network`` role.

Prerequisites
-------------

* MAAS 3.8 or later.
* The DPU enrolled in MAAS with its custom boot image. See the `MAAS DPU
  deployment guide`_.
* The DPU image built with ``preserve_hostname: false`` in ``cloud.cfg``, so the
  DPU picks up the hostname configured in MAAS.

The DPU image includes the services required to enable hardware offload at boot.
No Sunbeam-side hardware offload configuration is required.

MAAS tags
---------

Tag each DPU machine in MAAS with:

* ``dpu-image-<name>`` — selects the boot image, where ``<name>`` is the MAAS
  boot resource holding the custom DPU image (for example
  ``dpu-image-bf-321-v2-ovs-hack``).
* A ``dpu`` tag carrying the required kernel options:

::

    {
      "name": "dpu",
      "kernel_opts": "text console=hvc0 console=ttyAMA0 earlycon=pl011,0x13010000 fixrtc net.ifnames=0 biosdevname=0 iommu.passthrough=1",
      "definition": ""
    }

The DPU machine must use the 24.04 kernel:

::

    "hwe_kernel": "hwe-24.04"
    "min_hwe_kernel": "hwe-24.04"

Operations
----------

Verify the VFs on the host
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The DPU VFs appear on the compute host paired with the DPU. On the compute host,
check the number of VFs configured for the DPU's Physical Function (PF)
interface:

::

    ifname=ens1f0np0
    cat /sys/class/net/${ifname}/device/sriov_numvfs

If none exist, create them:

::

    echo '4' | sudo tee /sys/class/net/${ifname}/device/sriov_numvfs

Confirm the VFs are present. They are reported as ``Virtual Function`` devices:

::

    $ sudo lshw -class net -businfo
    # output #
    Bus info          Device          Class          Description
    ============================================================
    pci@0000:41:00.0  ens1f0np0       network        MT43244 BlueField-3 integrated ConnectX-7 network controller
    pci@0000:41:00.1  ens1f1np1       network        MT43244 BlueField-3 integrated ConnectX-7 network controller
    pci@0000:41:00.3  ens1f0v0        network        ConnectX Family mlx5Gen Virtual Function
    pci@0000:41:00.4  ens1f0v1        network        ConnectX Family mlx5Gen Virtual Function
    pci@0000:41:00.5  ens1f0v2        network        ConnectX Family mlx5Gen Virtual Function
    pci@0000:41:00.6  ens1f0v3        network        ConnectX Family mlx5Gen Virtual Function

On the DPU machine, each host VF has a matching representor (``pf0vf0`` to
``pf0vf3``), through which the DPU handles the VF's traffic:

::

    $ sudo lshw -class net -businfo
    # output #
    Bus info          Device            Class      Description
    ==========================================================
    pci@0000:03:00.0  enp3s0f0np0       network    MT43244 BlueField-3 integrated ConnectX-7 network controller
    pci@0000:03:00.1  p1                network    MT43244 BlueField-3 integrated ConnectX-7 network controller
    pci@0000:03:00.0  pf0hpf            network    Ethernet interface
    pci@0000:03:00.1  pf1hpf            network    Ethernet interface
    pci@0000:03:00.0  pf0vf0            network    Ethernet interface
    pci@0000:03:00.0  pf0vf1            network    Ethernet interface
    pci@0000:03:00.0  pf0vf2            network    Ethernet interface
    pci@0000:03:00.0  pf0vf3            network    Ethernet interface

The representor interfaces also appear in ``ip -br a`` on the DPU machine:

::

    $ ip -br a
    # output #
    pf0hpf           UP             fe80::a876:f5ff:fe32:5467/64
    pf0vf0           UP             fe80::18e1:67ff:fe05:3f54/64
    pf0vf1           UP             fe80::a4fd:98ff:fe7f:2f77/64
    pf0vf2           UP             fe80::ecaf:b9ff:feb1:824/64
    pf0vf3           UP             fe80::7c5b:dfff:fee5:9276/64

Configure SR-IOV
~~~~~~~~~~~~~~~~~

Run SR-IOV configuration:

::

    sunbeam configure sriov

Sunbeam detects that the compute host is paired with a DPU and records the DPU
VFs as remote-managed devices, rather than performing regular SR-IOV
configuration. No extra flag is required.

See :doc:`configuring-sriov` for the general SR-IOV workflow.

Verify the Nova configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On the host, confirm the VFs were written to ``nova.conf`` with
``remote_managed`` set and a null physical network:

::

    sudo cat /var/snap/openstack-hypervisor/common/etc/nova/nova.conf
    # output #
    [pci]
    device_spec = {"address": "0000:41:00.3", "vendor_id": "15b3", "product_id": "101e", "physical_network": null, "remote_managed": "true"}
    device_spec = {"address": "0000:41:00.4", "vendor_id": "15b3", "product_id": "101e", "physical_network": null, "remote_managed": "true"}
    device_spec = {"address": "0000:41:00.5", "vendor_id": "15b3", "product_id": "101e", "physical_network": null, "remote_managed": "true"}
    device_spec = {"address": "0000:41:00.6", "vendor_id": "15b3", "product_id": "101e", "physical_network": null, "remote_managed": "true"}

Attaching a DPU VF to an instance
---------------------------------

Create a port with ``--vnic-type=remote-managed``:

::

    openstack port create --network demo-network --vnic-type=remote-managed sriov-dpu-port

Launch an instance with the port attached:

::

    openstack server create --flavor m1.tiny --image ubuntu \
      --nic net-id=demo-network --nic port-id=sriov-dpu-port dpu-demo

Confirm the instance is active:

::

    openstack server list
    # output #
    +--------------------------------------+------+--------+------------------------------------------+--------+---------+
    | ID                                   | Name | Status | Networks                                 | Image  | Flavor  |
    +--------------------------------------+------+--------+------------------------------------------+--------+---------+
    | 440727f5-6f39-4c59-b9f8-bd85ac88b3c9 | one  | ACTIVE | demo-network=192.168.0.246, 192.168.0.81 | ubuntu | m1.tiny |
    +--------------------------------------+------+--------+------------------------------------------+--------+---------+

Check the port status. The ``binding_vnic_type`` is ``remote-managed`` and the
binding profile records the DPU ``card_serial_number`` and the VF ``pci_slot``:

::

    openstack port show sriov-dpu-port
    # output #
    +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Field                   | Value                                                                                                                                                      |
    +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | admin_state_up          | UP                                                                                                                                                         |
    | allowed_address_pairs   |                                                                                                                                                            |
    | binding_host_id         | pc8a-rb3-n4.pc8a.canonical.com                                                                                                                             |
    | binding_profile         | capabilities='['rx', 'tx', 'sg', 'tso', 'gso', 'gro', 'rxvlan', 'txvlan', 'rxhash', 'rdma', 'txudptnl']', card_serial_number='53FV4AF0066',                |
    |                         | pci_slot='0000:41:00.6', pci_vendor_info='15b3:101e', pf_mac_address='b8:e9:24:3d:7d:3a', physical_network=, vf_num='3'                                    |
    | binding_vif_details     | bound_drivers.0='ovn', bridge_name='br-int', connectivity='l2', datapath_type='system', ovs_create_tap='False', port_filter='True'                         |
    | binding_vif_type        | ovs                                                                                                                                                        |
    | binding_vnic_type       | remote-managed                                                                                                                                             |
    | created_at              | 2026-08-21T05:32:49Z                                                                                                                                       |
    | data_plane_status       | None                                                                                                                                                       |
    | description             |                                                                                                                                                            |
    | device_id               | 440727f5-6f39-4c59-b9f8-bd85ac88b3c9                                                                                                                       |
    | device_owner            | compute:nova                                                                                                                                               |
    | device_profile          | None                                                                                                                                                       |
    | dns_assignment          | fqdn='one.cloud.sunbeam.internal.', hostname='one', ip_address='192.168.0.246'                                                                             |
    | dns_domain              |                                                                                                                                                            |
    | extra_dhcp_opts         |                                                                                                                                                            |
    | fixed_ips               | ip_address='192.168.0.246', subnet_id='39c18115-8791-4f8f-a790-ead9c32f5c0e'                                                                               |
    | hardware_offload_type   | None                                                                                                                                                       |
    | hints                   |                                                                                                                                                            |
    | id                      | d5f9199a-bd76-4511-b7e6-9cace5f3f1be                                                                                                                       |
    | ip_allocation           | immediate                                                                                                                                                  |
    | mac_address             | fa:16:3e:84:01:08                                                                                                                                          |
    | name                    | sriov-dpu-port                                                                                                                                             |
    | network_id              | 7c8fa3dd-db5f-4fe8-978a-721ac2076a94                                                                                                                       |
    | numa_affinity_policy    | None                                                                                                                                                       |
    | port_security_enabled   | True                                                                                                                                                       |
    | project_id              | ea4d34acbb1d48bbaa73e61a5737a410                                                                                                                           |
    | propagate_uplink_status | True                                                                                                                                                       |
    | resource_request        | None                                                                                                                                                       |
    | revision_number         | 17                                                                                                                                                         |
    | qos_network_policy_id   | None                                                                                                                                                       |
    | qos_policy_id           | None                                                                                                                                                       |
    | security_group_ids      | 713f18eb-6125-44e5-a356-d2eacb342054                                                                                                                       |
    | status                  | ACTIVE                                                                                                                                                     |
    | tags                    |                                                                                                                                                            |
    | trunk_details           | None                                                                                                                                                       |
    | trusted                 | None                                                                                                                                                       |
    | updated_at              | 2026-08-22T11:25:06Z                                                                                                                                       |
    +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------+

On the host, confirm that Nova has allocated the VF to the instance. Query the
``nova.pci_devices`` table on the ``mysql`` unit:

::

    $ juju ssh -m openstack --container mysql mysql/0 \
        mysql -e "SELECT address,status,instance_uuid,dev_type,parent_addr \
                  FROM nova.pci_devices \
                  WHERE address LIKE '0000:41:00.%' AND deleted=0 ORDER BY address;"
    # output #
    +--------------+-----------+--------------------------------------+----------+--------------+
    | address      | status    | instance_uuid                        | dev_type | parent_addr  |
    +--------------+-----------+--------------------------------------+----------+--------------+
    | 0000:41:00.3 | available | NULL                                 | type-VF  | 0000:41:00.0 |
    | 0000:41:00.4 | available | NULL                                 | type-VF  | 0000:41:00.0 |
    | 0000:41:00.5 | available | NULL                                 | type-VF  | 0000:41:00.0 |
    | 0000:41:00.6 | allocated | 440727f5-6f39-4c59-b9f8-bd85ac88b3c9 | type-VF  | 0000:41:00.0 |
    +--------------+-----------+--------------------------------------+----------+--------------+

Verify the Libvirt domain. The VF is passed through with the ``vfio`` driver:

::

    $ sudo openstack-hypervisor.virsh dumpxml instance-00000007 | grep "type='hostdev" -A 8
    <interface type='hostdev' managed='yes'>
      <mac address='fa:16:3e:84:01:08'/>
      <driver name='vfio'/>
      <source>
        <address type='pci' domain='0x0000' bus='0x41' slot='0x00' function='0x6'/>
      </source>
      <alias name='hostdev0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/>
    </interface>

Confirm that the port is bound to the DPU chassis, not the host. In the OVN
Southbound database, the DPU appears as its own chassis (identified by the
hostname baked into the image, for example ``packer-ubuntu``) and carries the
instance ``Port_Binding``:

::

    $ sudo microovn.ovn-sbctl show
    # output #
    Chassis pc8a-rb3-n3
        hostname: pc8a-rb3-n3.pc8a.canonical.com
        Encap geneve
            ip: "10.21.6.15"
            options: {csum="true"}
    Chassis pc8a-rb3-n2
        hostname: pc8a-rb3-n2.pc8a.canonical.com
        Encap geneve
            ip: "10.21.6.13"
            options: {csum="true"}
        Port_Binding cr-lrp-6a987857-08f4-49b2-a705-2241733e5746
    Chassis pc8a-rb3-n4
        hostname: pc8a-rb3-n4.pc8a.canonical.com
        Encap geneve
            ip: "10.21.6.14"
            options: {csum="true"}
        Port_Binding "202bc250-f366-499f-af9b-905d5f78fc05"
    Chassis packer-ubuntu
        hostname: packer-ubuntu
        Encap geneve
            ip: "10.21.6.20"
            options: {csum="true"}
        Port_Binding "d5f9199a-bd76-4511-b7e6-9cace5f3f1be"
        Port_Binding "49a9ad67-7357-4a09-8e76-ee953d43ae83"
    Chassis pc8a-rb3-n1
        hostname: pc8a-rb3-n1.pc8a.canonical.com
        Encap geneve
            ip: "10.21.6.10"
            options: {csum="true"}

The DPU chassis advertises its card serial number and acts as the gateway
(``ovn-cms-options``):

::

    $ sudo microovn.ovn-sbctl list chassis
    # output #
    _uuid               : 869088a7-339d-4b12-a274-e7d410f8cd4c
    encaps              : [4623e0dc-fc9d-49ed-ac76-653a9329a625]
    external_ids        : {}
    hostname            : packer-ubuntu
    name                : packer-ubuntu
    nb_cfg              : 0
    other_config        : {..., ovn-bridge-mappings="physnet1:br-ex", ovn-cms-options="card-serial-number=53FV4AF0066,enable-chassis-as-gw", ...}
    transport_zones     : []
    vtep_logical_switches: []

References
----------

* :doc:`configuring-sriov`
* `MAAS DPU deployment guide`_
* `MicroOVN DPU integration`_
* `Nova SmartNIC DPU configuration`_

.. LINKS
.. _MAAS DPU deployment guide: https://canonical.com/maas/docs/latest/how-to-guides/deploy-a-dpu-host-pair/
.. _MicroOVN DPU integration: https://ubuntu.com/docs/microovn/latest/reference/dpu/
.. _Nova SmartNIC DPU configuration: https://docs.openstack.org/neutron/latest/admin/ovn/smartnic_dpu.html
