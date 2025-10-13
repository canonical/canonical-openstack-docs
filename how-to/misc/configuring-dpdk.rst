Configuring DPDK
================

Overview
--------

Open vSwitch (OVS) can be configured to use the `DPDK`_ (Data Plane Development
Kit) userspace datapath, achieving increased performance compared to the
standard OVS kernel datapath.

Prerequisites
-------------

Compatible network adapters and CPU architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please consult the `DPDK supported hardware page`_ to ensure that your CPU
architecture and network adapters are compatible with DPDK.

Isolated CPU cores
~~~~~~~~~~~~~~~~~~

Canonical Openstack users can specify the desired number of CPU cores that will
be allocated to DPDK. The cores will be distributed based on the NUMA location
of the network interfaces used with DPDK.

Use kernel command line parameters to preconfigure the necessary number of
isolated CPU cores and pay attention to the NUMA nodes:

::

	isolcpus=0-3,16-19

If hyperthreading is enabled, make sure to include the CPU siblings as well.

VT-d / IO-MMU
~~~~~~~~~~~~~

IO virtualization (for example Intel VT-d or AMD-V) must be enabled in
the system BIOS and then through kernel arguments, using the following:

::

	intel_iommu=on iommu=pt

Huge pages
~~~~~~~~~~

This feature requires 1GB huge pages to be preconfigured. For example, the
following kernel arguments may be used:

::

	default_hugepagesz=1G hugepagesz=1G hugepages=64

Openstack instances that leverage DPDK must request huge pages through
flavor extra specs:

::

	openstack flavor set m1.large --property hw:mem_page_size=large

Make sure that the flavor ram size is a multiple of the huge page size (1GB).

Instances configured to use huge pages will be connected to the DPDK datapath
through ``vhost-user`` interfaces, as opposed to the standard tap devices.
See the `Openstack DPDK documentation`_ for more details.

Network configuration
~~~~~~~~~~~~~~~~~~~~~

Physical network interfaces that leverage DPDK are expected to be connected to
OVS bridges, either directly or through bonds.

Make sure to configure the bridges using Netplan or MAAS before enabling DPDK.

Canonical Openstack will pivot the configuration from the system OVS
installation to the snap based OVS service. This requires a currently
`unreleased Netplan change`_.

At the same time, the DPDK devices will be persistently bound to the
configured DPDK-compatible driver (`vfio-pci` by default), at which point
the interfaces will no longer be visible to the host.

As such, the charm will remove the DPDK interfaces from the Netplan
configuration and move bond definitions to OVS.

::

	$ sudo /snap/bin/ovs-vsctl show
	53cdbac9-b6e4-40c5-8c12-71a874f3a606
	    Bridge br0
	        fail_mode: standalone
	        datapath_type: netdev
	        Port br0
	            Interface br0
	                type: internal
	        Port bond0
	            Interface dpdk-eth1
	                type: dpdk
	                options: {dpdk-devargs="0000:06:00.0"}
	            Interface dpdk-eth2
	                type: dpdk
	                options: {dpdk-devargs="0000:07:00.0"}

Snapd
~~~~~

``snapd`` 2.72 is required, providing the necessary snap permissions.

Manual mode
-----------

As mentioned in the previous section, network interfaces used with DPDK must
be connected to OVS bridges using Netplan:

::

	bridges:
	    br0:
	      macaddress: "00:16:3e:c0:43:a8"
	      mtu: 1500
	      interfaces:
	      - bond0
	      parameters:
	        forward-delay: "15"
	        stp: false
	      openvswitch: {}
	  bonds:
	    bond0:
	      macaddress: "00:16:3e:c0:43:a8"
	      mtu: 1500
	      interfaces:
	      - eth1
	      - eth2

DPDK can be configured using the following command:

::

	sunbeam configure dpdk

The user will need to specify which network interfaces are going to connected
to the DPDK datapath and the amount of system resources to allocate.

Example:

::

	$ sunbeam configure dpdk 
	Enable OVS DPDK data path, handling packets in userspace. It provides improved performance compared to 
	the standard OVS kernel data path. DPDK capable network interfaces are required.
	Enable and configure DPDK [y/n] (n): y
	Configuring DPDK physical interfaces.

	WARNING: the specified interfaces will be reconfigured to use a DPDK-compatible driver (vfio-pci by 
	default) and will no longer be visible to the host.
	Any bonds and bridges defined in MAAS/Netplan will be updated to use the new DPDK OVS port.

	DPDK candidate interfaces:
	* Intel Corporation Ethernet Controller X550 (eno2)
	* Mellanox Technologies MT27520 Family [ConnectX-3 Pro] (enp94s0)
	* Mellanox Technologies MT27520 Family [ConnectX-3 Pro] (enp94s0d1)
	Enable interface DPDK mode? Intel Corporation Ethernet Controller X550 (eno2) [y/n] (n): y
	Enable interface DPDK mode? Mellanox Technologies MT27520 Family [ConnectX-3 Pro] (enp94s0) [y/n] (n): y
	Enable interface DPDK mode? Mellanox Technologies MT27520 Family [ConnectX-3 Pro] (enp94s0d1) [y/n] 
	(n): y
	The specified number of cores will be allocated to OVS datapath processing, taking into account the 
	NUMA location of physical DPDK ports. Isolated cpu cores must be preconfigured using kernel parameters.
	The number of cores allocated to OVS datapath processing (2): 
	The specified number of cores will be allocated to OVS control plane processing, taking into account 
	the NUMA location of physical DPDK ports. Isolated cpu cores must be preconfigured using kernel 
	parameters.
	The number of cores allocated to OVS control plane processing (2): 
	The total amount of memory in MB to allocate from huge pages for OVS DPDK. The memory will be 
	distributed across NUMA nodes based on the location of the physical DPDK ports. Currently uses 1GB 
	pages, make sure to specify a multiple of 1024 and preallocate enough 1GB pages.
	The amount of memory in MB allocated to OVS from huge pages (2048): 2048
	The DPDK-compatible driver used for DPDK physical ports (vfio-pci):


MAAS mode
---------

Each MAAS network interface connected to the DPDK datapath must contain the
`neutron:dpdk` tag. Also, it should be connected to an OVS bridge defined in
MAAS, either directly or through a bond.

Apart from that, DPDK can be enabled and configured similarly to the
manual (local) mode.

Manifest configuration
----------------------

The DPDK settings can be provided through the Canonical Openstack manifest,
for example:

::

	core:
	  config:
	    dpdk:
	      enabled: true
	      control_plane_cores: 2
	      dataplane_cores: 2
	      memory: 2048
	      driver: vfio-pci
	      ports:
	        my-node.maas:
	          - eno3
	          - eno4

Openstack instances using DPDK
------------------------------

Openstack instances must be configured to use huge pages in order to leverage
DPDK.

::

	openstack flavor set m1.large --property hw:mem_page_size=large

The instances will then be connected to the DPDK datapath using ``vhost-user``
ports:

::

	$ sudo openstack-hypervisor.virsh dumpxml instance-0000000d | grep -i vhost -A 7
    <interface type='vhostuser'>
      <mac address='fa:16:3e:55:8d:e1'/>
      <source type='unix' path='/var/snap/openstack-hypervisor/common/run/libvirt/vhu90ab19fb-57' mode='server'/>
      <target dev='vhu90ab19fb-57'/>
      <model type='virtio'/>
      <alias name='net0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
    </interface>

	$ sudo openstack-hypervisor.ovs-vsctl show
	    Bridge br-int
	        fail_mode: secure
	        datapath_type: netdev
	        Port vhu90ab19fb-57
	            Interface vhu90ab19fb-57
	                type: dpdkvhostuserclient
	                options: {vhost-server-path="/var/snap/openstack-hypervisor/common/run/libvirt/vhu90ab19fb-57"}

Disabling DPDK
--------------

The DPDK feature may be disabled using the following command. Simply specify
"n" when prompted in order to disable DPDK.

::

	sunbeam configure dpdk

	Enable OVS DPDK data path, handling packets in userspace. It provides improved performance compared to
	the standard OVS kernel data path. DPDK capable network interfaces are required.
	Enable and configure DPDK [y/n] (y): n

By doing so, the OVS bridges will be set to use the standard system datapath
instead of ``netdev`` (DPDK).

Note that as part of the DPDK enablement, physical port configuration is moved
from Netplan to OVS and the interfaces are persistently bound to the DPDK
compatible driver (``vfio-pci`` by default) using ``driverctl``. Those steps
are not reverted automatically, the user may have to manually redefine
bonds and remove the driver overrides. Unbinding the ``vfio-pci`` driver may
require a host reboot.

At the same time, existing instances will continue to use ``vhost-user``
interfaces. Either rebuild or migrate those instances to reconfigure the
port attachments.


.. Links

.. _DPDK: https://www.dpdk.org
.. _DPDK supported hardware page: https://core.dpdk.org/supported/
.. _Openstack DPDK documentation: https://docs.openstack.org/neutron/latest/admin/config-ovs-dpdk.html
.. _unreleased Netplan change: https://github.com/canonical/netplan/pull/549
