Enable Network Role for Canonical Openstack
===========================================


This how-to guide provides all necessary information to deploy dedicated network nodes in your
`Canonical OpenStack`_ deployment with Sunbeam.

Overview
--------

By default, Sunbeam deploys OpenStack with combined control and compute nodes, where networking
services run alongside compute workloads. The network role allows you to deploy dedicated network
nodes that handle all networking functions separately.

Network nodes run MicroOVN and the OpenStack network agents (deployed as a subordinate charm
co-located with MicroOVN), providing:

* OVN chassis functionality for overlay networking
* Gateway services for North-South traffic
* External network connectivity for instances
* Remote connectivity for bare-metal instances when Ironic is enabled

.. important ::

   Network and compute roles are **mutually exclusive**. A node cannot be both a compute node
   and a network node at the same time. This design ensures clear separation of concerns between
   compute and network traffic processing.

Bootstrap with network role
===========================

When creating a new Sunbeam cluster, you can designate the bootstrap node as a network node
instead of the default compute node.

Bootstrap the cluster
---------------------

To bootstrap a new cluster with the network role, execute the following command:

::

   sunbeam cluster bootstrap --role network

The ``--role network`` flag designates this node as a network node instead of the default compute
node. The ``control`` role is implicitly added during bootstrap.

When prompted, answer the interactive questions. The prompts are the same as a standard bootstrap
operation. Refer to the :doc:`Interactive configuration prompts</reference/interactive-configuration-prompts>`
section for detailed descriptions.

Configure network nodes
=======================

After bootstrapping or joining nodes with the network role, you must configure the network
services on each network node.

Run the configure command
-------------------------

On any cluster member, execute the following command:

::

   sunbeam configure deployment

The configure deployment command will detect nodes with the network role and prompt for
network-specific configuration.

.. important ::

   For Network nodes, the configure deployment command will select automatically the remote access
   option for VM access.

Interactive prompts
-------------------

When configuring a network node, you will be prompted for the following information:

::

   External network's interface:

This is the name of the network interface that will be used for external network connectivity.
This interface will be added to the external bridge, and will be used to configure MicroOVN.

.. important ::

   The interface must not be configured with an IP address, as MicroOVN will manage the addressing based on the external network configuration.

Related how-to guides
---------------------

Now that Canonical OpenStack is installed, you might want to check out the following how-to guides:

:doc:`Using the OpenStack dashboard </how-to/misc/using-the-openstack-dashboard>`
:doc:`Using the OpenStack client </how-to/misc/using-the-openstack-cli>`
:doc:`Scaling the cluster out </how-to/operations/scaling-the-cluster-out>`

