Use the EPA orchestrator
========================

The snap `epa-orchestrator` provides NUMA-aware CPU cores and huge pages allocation functionality, and this guide explains how to configure and manage the EPA orchestrator to optimize resource allocation for OpenStack workloads.


System configuration requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before using the EPA orchestrator, ensure that the following kernel command line parameters are configured. For MAAS deployments, configure these via the MAAS UI for each node. For single node deployments, configure them manually on the node.
 
For detailed instructions on setting kernel boot parameters via the CLI, refer to the
`MAAS documentation on machine customization <https://canonical.com/maas/docs/about-machine-customization#p-17465-kernel-boot-options>`_.

For **single-node deployments**, configure these parameters manually on the node.

1. **CPU isolation**: Reserve dedicated CPU cores for EPA workloads by setting the ``isolcpus`` kernel parameter.
2. **Huge pages**: Enable large memory pages by setting parameters such as ``default_hugepagesz``, ``hugepagesz``, and ``hugepages`` (for example, to configure 16 × 1 GB huge pages).


Snap interface
--------------

To enable communication between the EPA orchestrator and other snaps (like ``openstack-hypervisor``), you need to connect the `epa-info` interface.

Manual connection
~~~~~~~~~~~~~~~~~

This is required until the ``epa-orchestrator`` charm is published to the stable channel and the ownership is transferred to Canonical.

Connect the interface using:

.. code-block:: bash

   sudo snap connect openstack-hypervisor:epa-info epa-orchestrator:epa-info

Verify the connection
~~~~~~~~~~~~~~~~~~~~~

Check that the connection is established:

.. code-block:: bash

   snap connections

Example output:

.. code-block:: text

   Interface        Plug                              Slot                    Notes
   content[epa-info]      openstack-hypervisor:epa-info               epa-orchestrator:epa-info  manual
   network-bind           epa-orchestrator:network-bind               :network-bind     

The `manual` status indicates the connection was manually established and is active.

Request resource allocation
---------------------------

Use the socket API to request and manage CPU pinning and huge pages allocation for your services. Connect to the ``epa.sock`` socket and send JSON-based requests using the following APIs: CPU core allocation (``allocate_cores``), NUMA-aware core allocation (``allocate_numa_cores``), listing allocations (``list_allocations``), memory allocation information (``get_memory_info``), and huge pages allocation (``allocate_hugepages``). The orchestrator returns JSON responses containing the allocated resources, including CPU ranges and huge pages assignments, along with information about remaining available resources.

Verify the EPA orchestrator status
-----------------------------------

To verify that the EPA orchestrator is properly installed and running, use the `juju status` command. A successful deployment should show the `epa-orchestrator` application in an active state.

Example output:

.. code-block:: text

   Model  Controller           Cloud/Region         Version  SLA          Timestamp  
   example-model     localhost-localhost  localhost/localhost  3.6.8    unsupported  11:24:48Z  
   
   App               Version  Status  Scale  Charm             Channel  Rev  Exposed  Message  
   epa-orchestrator           active      1  epa-orchestrator             0  no       
   sunbeam-machine            active      1  sunbeam-machine              0  no       
   
   Unit                   Workload  Agent  Machine  Public address  Ports  Message  
   sunbeam-machine/0*     active    idle   0        10.28.254.92           
     epa-orchestrator/0*  active    idle            10.28.254.92           
   
   Machine  State    Address       Inst id        Base          AZ  Message  
   0        started  10.28.254.92  juju-ea75f5-0  ubuntu@24.04      Running