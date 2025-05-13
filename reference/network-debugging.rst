Network debugging
=================

This page presents a collection of techniques for interrogating your
cloud’s virtual networking system (OVN). Whether prompted by sheer
interest or by necessity (an issue has arisen), this page will assist
you in looking into the internals of your cloud’s networking layer.

.. note::
   This page was inspired by `upstream OVN documentation <https://docs.ovn.org/en/latest/tutorials/ovn-openstack.html>`__.
   Many OVN troubleshooting techniques can be applied equally to a Sunbeam environment.

Contents:

-  `Accessing OVN databases <#heading--accessing-ovn-databases>`__
-  `Querying OVN databases <#heading--accessing-ovn-databases>`__
-  `Capturing and tracing an ingress
   packet <#heading--capturing-and-tracing-an-ingress-packet>`__
-  `Resolving OpenFlow port
   numbers <#heading--resolving-openflow-port-numbers>`__

.. raw:: html

   <h2 id="heading--accessing-ovn-databases">

Accessing OVN databases

.. raw:: html

   </h2>

There are four containers in each :code:`ovn-chassis` pod:

-  Northd
-  Northbound database
-  Southbound database
-  the charm itself

These containers can each be accessed with Juju over SSH. Once
connected, start a Bash shell and create aliases for accessing the OVN
tooling:

For the Northbound DB container:

::

   juju ssh -m openstack --container ovn-nb-db-server ovn-central/0

Set up aliases:

.. code:: text

   bash
   alias ovn-nbctl='ovn-nbctl --db=ssl:127.0.0.1:6641 -c /etc/ovn/cert_host -p /etc/ovn/key_host -C /etc/ovn/ovn-central.crt'

For the Southbound DB container:

::

   juju ssh -m openstack --container ovn-sb-db-server ovn-central/0

Set up aliases:

.. code:: text

   bash
   alias ovn-sbctl='ovn-sbctl --db=ssl:127.0.0.1:6642 -c /etc/ovn/cert_host -p /etc/ovn/key_host -C /etc/ovn/ovn-central.crt'

.. raw:: html

   <h2 id="heading--querying-ovn-databases">

Querying OVN databases

.. raw:: html

   </h2>

Assuming that all the defaults for a single-node install were used and
``sunbeam launch`` was used to create a guest, then there will be a
demo-network, external-network, demo-router, and a guest.

These are some of the entities that are present from an OpenStack
perspective:

.. code:: text

   openstack server list --all-projects
   +--------------------------------------+-----------+--------+-------------------------------------------+--------+---------+
   | ID                                   | Name      | Status | Networks                                  | Image  | Flavor  |
   +--------------------------------------+-----------+--------+-------------------------------------------+--------+---------+
   | 6c446cb5-4934-401a-917d-e3bc215c0b64 | rapid-owl | ACTIVE | demo-network=10.20.20.138, 192.168.122.83 | ubuntu | m1.tiny |
   +--------------------------------------+-----------+--------+-------------------------------------------+--------+---------+

   openstack network list
   +--------------------------------------+------------------+--------------------------------------+
   | ID                                   | Name             | Subnets                              |
   +--------------------------------------+------------------+--------------------------------------+
   | 3f9bc3b1-2520-4658-85f0-545a69e8b06a | demo-network     | 17e394f9-e12c-4f31-a269-62ddf3308fc8 |
   | 856fe9e3-60bf-4177-bb8b-831f68bb55c0 | external-network | 14c63eaf-eeb7-476d-a99d-0a05f6a674f8 |
   +--------------------------------------+------------------+--------------------------------------+

   openstack subnet list
   +--------------------------------------+-----------------+--------------------------------------+------------------+
   | ID                                   | Name            | Network                              | Subnet           |
   +--------------------------------------+-----------------+--------------------------------------+------------------+
   | 14c63eaf-eeb7-476d-a99d-0a05f6a674f8 | external-subnet | 856fe9e3-60bf-4177-bb8b-831f68bb55c0 | 10.20.20.0/24    |
   | 17e394f9-e12c-4f31-a269-62ddf3308fc8 | demo-subnet     | 3f9bc3b1-2520-4658-85f0-545a69e8b06a | 192.168.122.0/24 |
   +--------------------------------------+-----------------+--------------------------------------+------------------+

   openstack router list
   +--------------------------------------+-------------+--------+-------+----------------------------------+
   | ID                                   | Name        | Status | State | Project                          |
   +--------------------------------------+-------------+--------+-------+----------------------------------+
   | 5c300bae-bf1f-4773-ac98-1d71c23e1bc7 | demo-router | ACTIVE | UP    | b8c896d15bb247448edd2d97f7d99f1f |
   +--------------------------------------+-------------+--------+-------+----------------------------------+

   openstack port list
   +--------------------------------------+------+-------------------+-------------------------------------------------------------------------------+--------+
   | ID                                   | Name | MAC Address       | Fixed IP Addresses                                                            | Status |
   +--------------------------------------+------+-------------------+-------------------------------------------------------------------------------+--------+
   | 418c3e5d-87fa-467c-b1c1-b9832fa1e752 |      | fa:16:3e:09:d4:a6 | ip_address='192.168.122.2', subnet_id='17e394f9-e12c-4f31-a269-62ddf3308fc8'  | DOWN   |
   | 56a18b9e-07d4-4249-b28b-b6446961a587 |      | fa:16:3e:23:60:97 | ip_address='10.20.20.239', subnet_id='14c63eaf-eeb7-476d-a99d-0a05f6a674f8'   | ACTIVE |
   | 98835e99-8ab5-4cd3-8b17-207e15538c03 |      | fa:16:3e:2d:6e:82 |                                                                               | DOWN   |
   | ae7b9a8e-48e8-4c3a-9ef0-710ccba00776 |      | fa:16:3e:70:93:8c | ip_address='192.168.122.1', subnet_id='17e394f9-e12c-4f31-a269-62ddf3308fc8'  | ACTIVE |
   | cd9f7cce-77cb-4fae-ae1c-94964248d8d5 |      | fa:16:3e:00:53:35 | ip_address='10.20.20.138', subnet_id='14c63eaf-eeb7-476d-a99d-0a05f6a674f8'   | N/A    |
   | d8174cec-c5ae-4bd0-abb4-9420c3b87e76 |      | fa:16:3e:dd:8f:4d | ip_address='192.168.122.83', subnet_id='17e394f9-e12c-4f31-a269-62ddf3308fc8' | ACTIVE |
   +--------------------------------------+------+-------------------+-------------------------------------------------------------------------------+--------+

To make the structure in OVN more readable, it helps to label the above
ports. Firstly, there are clearly two ports related to the ``rapid-owl``
guest:

.. code:: text

   openstack port set --name rapid-owl-internal d8174cec-c5ae-4bd0-abb4-9420c3b87e76
   openstack port set --name rapid-owl-floating cd9f7cce-77cb-4fae-ae1c-94964248d8d5

Similarly, there are two ports connected to the ``demo-router``:

.. code:: text

   openstack port set --name demo-router-internal ae7b9a8e-48e8-4c3a-9ef0-710ccba00776
   openstack port set --name demo-router-floating 56a18b9e-07d4-4249-b28b-b6446961a587

This leaves two ports unaccounted for. By showing the details of these
ports, we see that they are used internally for guest metadata:

.. code:: text

   openstack port show -c device_id -c device_owner -c network_id 418c3e5d-87fa-467c-b1c1-b9832fa1e752
   +--------------+----------------------------------------------+
   | Field        | Value                                        |
   +--------------+----------------------------------------------+
   | device_id    | ovnmeta-3f9bc3b1-2520-4658-85f0-545a69e8b06a |
   | device_owner | network:distributed                          |
   | network_id   | 3f9bc3b1-2520-4658-85f0-545a69e8b06a         |
   +--------------+----------------------------------------------+

   openstack port show -c device_id -c device_owner -c network_id 98835e99-8ab5-4cd3-8b17-207e15538c03
   +--------------+----------------------------------------------+
   | Field        | Value                                        |
   +--------------+----------------------------------------------+
   | device_id    | ovnmeta-856fe9e3-60bf-4177-bb8b-831f68bb55c0 |
   | device_owner | network:distributed                          |
   | network_id   | 856fe9e3-60bf-4177-bb8b-831f68bb55c0         |
   +--------------+----------------------------------------------+

.. note::
   The two metadata ports are marked as down and each of the guests floating IP
   ports is in a ``N/A`` state. In both cases, this is normal and not an
   indication of any kind of problem.

These entities are reflected in the configuration of the Northbound DB.

.. code:: text

   ovn-nbctl show
   switch 7fd2fe36-74b6-41a4-9005-d521d2a9a0fd (neutron-3f9bc3b1-2520-4658-85f0-545a69e8b06a) (aka demo-network)
       port d8174cec-c5ae-4bd0-abb4-9420c3b87e76 (aka rapid-owl-internal)
           addresses: ["fa:16:3e:dd:8f:4d 192.168.122.83"]
       port 418c3e5d-87fa-467c-b1c1-b9832fa1e752
           type: localport
           addresses: ["fa:16:3e:09:d4:a6 192.168.122.2"]
       port ae7b9a8e-48e8-4c3a-9ef0-710ccba00776 (aka demo-router-internal)
           type: router
           router-port: lrp-ae7b9a8e-48e8-4c3a-9ef0-710ccba00776
   switch 31f5c4f7-725b-4313-86a5-2b5c47d4f03a (neutron-856fe9e3-60bf-4177-bb8b-831f68bb55c0) (aka external-network)
       port 98835e99-8ab5-4cd3-8b17-207e15538c03
           type: localport
           addresses: ["fa:16:3e:2d:6e:82"]
       port 56a18b9e-07d4-4249-b28b-b6446961a587 (aka demo-router-floating)
           type: router
           router-port: lrp-56a18b9e-07d4-4249-b28b-b6446961a587
       port provnet-f5363a0a-8963-4271-a844-e545ba5f931b
           type: localnet
           addresses: ["unknown"]
   router 1a6ddfff-8a1e-45a6-bdf8-6f13e7c5d8f9 (neutron-5c300bae-bf1f-4773-ac98-1d71c23e1bc7) (aka demo-router)
       port lrp-ae7b9a8e-48e8-4c3a-9ef0-710ccba00776
           mac: "fa:16:3e:70:93:8c"
           networks: ["192.168.122.1/24"]
       port lrp-56a18b9e-07d4-4249-b28b-b6446961a587
           mac: "fa:16:3e:23:60:97"
           networks: ["10.20.20.239/24"]
           gateway chassis: [microk8s06.maas]
       nat aba8126c-612d-4de5-9445-6aacb813714a
           external ip: "10.20.20.138"
           logical ip: "192.168.122.83"
           type: "dnat_and_snat"
       nat cf7cfd04-ebfa-4407-b14e-1d43f999e233
           external ip: "10.20.20.239"
           logical ip: "192.168.122.0/24"
           type: "snat"

Over in the Southbound DB, the chassis for this deployment can be
examined:

.. code:: text

   ovn-sbctl show
   Chassis microk8s06.maas
       hostname: microk8s06.maas
       Encap geneve
           ip: "10.177.200.18"
           options: {csum="true"}
       Port_Binding "d8174cec-c5ae-4bd0-abb4-9420c3b87e76"
       Port_Binding cr-lrp-56a18b9e-07d4-4249-b28b-b6446961a587

The flows can also be listed:

.. code:: text

   ovn-sbctl lflow-list
   ...

.. raw:: html

   <h2 id="heading--capturing-and-tracing-an-ingress-packet">

Capturing and tracing an ingress packet

.. raw:: html

   </h2>

The example below captures and then traces an ICMP echo request packet
destined for a guest. The first step is to capture an echo request
packet. The code:`tcpdump` command can be used for this. In this example,
there is a single-node install with access to the guests available from
the installation node. The guests floating IP address is
**10.20.20.138**. The routes on the box show that traffic for this
subnet will be routed to **br-ex**.

.. code:: text

   ip route | grep '10.20.20.0/24'
   10.20.20.0/24 dev br-ex proto kernel scope link src 10.20.20.1

Listen on the br-ex interface, filter for echo request packets (an ICMP
code of 8), and store the captured packets in a file for later usage:

Window 1:

.. code:: text

   sudo tcpdump -i br-ex "icmp[0] == 8" -w ping.pcap

Window 2:

.. code:: text

   ping -c3 10.20.20.138

The **ping.pcap** file should now contain the echo requests generated by
the ping command. To use these with the OVS trace utility the packet capture
file needs to be converted. The utility for doing this is called
code:`ovs-pcap`. At the time of writing, this command is included in the
openstack-hypervisor snap but is not exposed. However it can still be
used:

.. code:: text

   /snap/openstack-hypervisor/current/usr/bin/ovs-pcap ping.pcap > ping.hex

The :code:`ping.hex` file will contain three entries corresponding to each
of the echo requests. For this example only the first is needed.

.. code:: text

   IN_PORT="br-ex"
   BRIDGE="br-ex"
   PACKET=$(head -1 ping.hex)
   sudo openstack-hypervisor.ovs-appctl ofproto/trace $BRIDGE in_port="$IN_PORT" $PACKET

If all is well the last rule in the output should end with:

.. code:: text

   ...
   65. reg15=0x3,metadata=0x2, priority 100, cookie 0x3d326af3
       output:2

This shows that the packet was sent out of OpenFlow port number 2. This
corresponds to the intended guest (See “Resolving OpenFlow port numbers”
below).

Tracing a hypothetical ingress packet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, a guest launched in the demo project will respond to an echo
request.

.. code:: text

   ping -q -c3 10.20.20.138
   PING 10.20.20.138 (10.20.20.138) 56(84) bytes of data.

   --- 10.20.20.138 ping statistics ---
   3 packets transmitted, 3 received, 0% packet loss, time 2045ms
   rtt min/avg/max/mdev = 0.351/0.472/0.692/0.155 ms

This request can be simulated using :code:`ovs-appctl`. Sunbeam installs this
utility as part of the openstack-hypervisor snap and can be accessed via
:code:`openstack-hypervisor.ovs-appctl`:

.. code:: text

   sudo openstack-hypervisor.ovs-appctl --help
   ovs-appctl, for querying and controlling Open vSwitch daemon
   ...

To simulate the echo request above, some information needs to be
gathered. Since the packet enters ovs via the br-ex bridge the first
step is to gather the MAC and IP address of the bridge:

.. code:: text

   ip address show  br-ex
   48: br-ex: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default qlen 1000
       link/ether 46:fc:d8:8d:05:49 brd ff:ff:ff:ff:ff:ff
       inet 10.20.20.1/24 scope global br-ex
          valid_lft forever preferred_lft forever
       inet6 fe80::44fc:d8ff:fe8d:549/64 scope link
          valid_lft forever preferred_lft forever

   BR_EX_MAC="46:fc:d8:8d:05:49"
   BR_EX_IP="10.20.20.1"

OpenFlow assigns each port a number so the next step is to find what
number has been assigned to the br-ex port on the br-ex bridge:

.. code:: text

   sudo openstack-hypervisor.ovs-vsctl get Interface br-ex ofport
   65534
   PORT_BR_EX=65534

Next, gather data about the destination of the request. The IP address
that was pinged earlier was 10.20.20.138:

.. code:: text

   GUEST_FLOATING_IP="10.20.20.138"

The demo-router is going to handle this traffic so the destination MAC
address in this case is actually the MAC address of the demo-routers
port on the external network:

.. code:: text

   openstack port list --router demo-router
   +--------------------------------------+----------------------+-------------------+------------------------------------------------------------------------------+--------+
   | ID                                   | Name                 | MAC Address       | Fixed IP Addresses                                                           | Status |
   +--------------------------------------+----------------------+-------------------+------------------------------------------------------------------------------+--------+
   | 56a18b9e-07d4-4249-b28b-b6446961a587 | demo-router-floating | fa:16:3e:23:60:97 | ip_address='10.20.20.239', subnet_id='14c63eaf-eeb7-476d-a99d-0a05f6a674f8'  | ACTIVE |
   | ae7b9a8e-48e8-4c3a-9ef0-710ccba00776 | demo-router-internal | fa:16:3e:70:93:8c | ip_address='192.168.122.1', subnet_id='17e394f9-e12c-4f31-a269-62ddf3308fc8' | ACTIVE |
   +--------------------------------------+----------------------+-------------------+------------------------------------------------------------------------------+--------+

   ROUTER_EXT_MAC="fa:16:3e:23:60:97"

Since this is going to trace a single packet, information about the type
of packet is needed. In this case, it is the echo request which is part
of the ping. An IPv4 ICMP echo request has an :code:`icmp_type` of 8 and a code
of 0. Lastly, :code:`nw_ttl` needs to be set to accommodate the number of hops
needed. In this case 64 is a reasonable value.

Putting this all together:

.. code:: text

   sudo openstack-hypervisor.ovs-appctl ofproto/trace \
      br-ex \
      icmp,\
      in_port=$PORT_BR_EX,\
      dl_src=$BR_EX_MAC,\
      dl_dst=$ROUTER_EXT_MAC,\
      nw_src=$BR_EX_IP,\
      nw_dst=$GUEST_FLOATING_IP,\
      nw_ttl=64,\
      icmp_type=8,\
      icmp_code=0

This produces a large amount of output - details of how the packet is
traversing the OpenFlow rules - but the important piece is at the end:

.. code:: text

   ...
   65. reg15=0x3,metadata=0x2, priority 100, cookie 0x3d326af3
       output:2

This shows that the packet was sent out of OpenFlow port number 2. This
corresponds to the intended guest (see “Resolving OpenFlow port numbers”
below).

Finally, delete the security group rule that is permitting ICMP traffic
and check that the trace command now drops the traffic.

.. code:: text

   openstack security group list --project demo
   +--------------------------------------+---------+------------------------+----------------------------------+------+
   | ID                                   | Name    | Description            | Project                          | Tags |
   +--------------------------------------+---------+------------------------+----------------------------------+------+
   | 00aed662-f303-47fa-82a7-86cde90a4ee1 | default | Default security group | b8c896d15bb247448edd2d97f7d99f1f | []   |
   +--------------------------------------+---------+------------------------+----------------------------------+------+

   openstack security group rule list --ingress --protocol icmp 00aed662-f303-47fa-82a7-86cde90a4ee1
   +--------------------------------------+-------------+-----------+-----------+------------+-----------+-----------------------+----------------------+
   | ID                                   | IP Protocol | Ethertype | IP Range  | Port Range | Direction | Remote Security Group | Remote Address Group |
   +--------------------------------------+-------------+-----------+-----------+------------+-----------+-----------------------+----------------------+
   | 33237298-6052-45d9-9a7e-1fee0a7587b7 | icmp        | IPv4      | 0.0.0.0/0 |            | ingress   | None                  | None                 |
   +--------------------------------------+-------------+-----------+-----------+------------+-----------+-----------------------+----------------------+

   openstack security group rule delete 33237298-6052-45d9-9a7e-1fee0a7587b7

This time the trace command ends with:

.. code:: text

   ...
   44. ip,reg0=0x200/0x200,reg15=0x3,metadata=0x2, priority 2001, cookie 0x5eeee244
       drop

.. raw:: html

   <h2 id="heading--resolving-openflow-port-numbers">

Resolving OpenFlow port numbers

.. raw:: html

   </h2>

When looking at OpenFlow rules or tracing a packet, the ports are given
numbers. These are the OpenFlow port numbers. For example, to find what
port 2 corresponds to:

.. code:: text

   sudo openstack-hypervisor.ovs-vsctl find interface ofport=2 | grep -E "^name"
   name                : tapd8174cec-c5

Often the first part of the corresponding port’s UUID is included in the
name of the device. This enables it to be traced back:

.. code:: text

   openstack port list | grep d8174cec-c5
   | d8174cec-c5ae-4bd0-abb4-9420c3b87e76 | rapid-owl-internal   | fa:16:3e:dd:8f:4d | ip_address='192.168.122.83', subnet_id='17e394f9-e12c-4f31-a269-62ddf3308fc8' | ACTIVE |
