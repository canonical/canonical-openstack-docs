Use the EPA orchestrator
==========================

The snap `epa-orchestrator` provides CPU core allocation functionality for CPU pinning through the EPA orchestrator service.

Prerequisites
-------------

Before using EPA orchestrator, ensure that:

1. CPU isolation is configured via the ``isolcpus`` kernel command line parameter (if CPU pinning is required)
   
   - For MAAS, this can be done via MAAS UI for each node.
   - For single node, this should be done manually on the node.
2. The target service has the appropriate plug to connect to the ``epa-info`` slot
3. The ``sunbeam-machine`` charm, which will install the ``epa-orchestrator`` charm as a subordinate charm, is deployed.

Set up socket communication
-------------------------------

To enable communication between the EPA orchestrator and other snaps (like ``openstack-hypervisor``), you need to connect the `epa-info` interface.

Manual Connection
~~~~~~~~~~~~~~~~~

This is required until the ``epa-orchestrator`` charm is published to stable channel and the ownership is transferred to Canonical.

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

EPA socket API
--------------------

To request CPU cores for your service, use the EPA Socket API.

1. **Connect to the EPA orchestrator socket**
2. **Send an allocation request** with your desired number of cores
3. **Process the response** to get your allocated CPU ranges

Verify EPA orchestrator status
---------------------------------

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

In this example:

* **Model**: Shows the current Juju model (`example-model`)
* **App**: The `epa-orchestrator` application is listed with status `active`
* **Unit**: The `epa-orchestrator/0*` unit shows `active` workload and `idle` agent status
* **Machine**: The unit is deployed on machine `0` which is in `started` state

The ``*`` indicates the primary unit for the application. When you see this status, the EPA Orchestrator is ready to handle CPU core allocation requests.