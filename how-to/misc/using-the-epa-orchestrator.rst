Using the EPA Orchestrator
==========================

This feature provides CPU core allocation functionality for CPU pinning through the EPA Orchestrator service.

Prerequisites
-------------

Before using EPA Orchestrator, ensure that:

1. CPU isolation is configured via the `isolcpus` kernel command line parameter (if CPU pinning is required)
   
   - For MAAS, this can be done via MAAS UI for each node.
   - For single node, this should be done manually on the node.
2. The target service has the appropriate plug to connect to the `epa-info` slot
3. The `sunbeam-machine` charm is deployed which will install the `epa-orchestrator` charm as a subordinate charm. The `epa-orchestrator` charm will install the `epa-orchestrator` snap and configure the `epa-info` interface.

Setting Up Socket Communication
-------------------------------

To enable communication between EPA Orchestrator and other snaps (like `openstack-hypervisor`), you need to connect the `epa-info` interface.

**Manual Connection**

This is required until the `epa-orchestrator` charm is published to stable channel and the ownership is transferred to Canonical.

Connect the interface using:

.. code-block:: bash

   sudo snap connect openstack-hypervisor:epa-info epa-orchestrator:epa-info

**Verifying the Connection**

Check that the connection is established:

.. code-block:: bash

   snap connections

Example output:

.. code-block:: text

   Interface        Plug                              Slot                    Notes
   content[epa-info]      openstack-hypervisor:epa-info               epa-orchestrator:epa-info  manual
   network-bind           epa-orchestrator:network-bind               :network-bind     

The `manual` status indicates the connection was manually established and is active.

Allocating CPU Cores
--------------------

To request CPU cores for your service:

1. **Connect to the EPA Orchestrator socket**
2. **Send an allocation request** with your desired number of cores
3. **Process the response** to get your allocated CPU ranges

Request Types
-------------

There are two types of requests supported by the **EPA Orchestrator**. These are defined by the parameter `action` in the request payload. The services can connect to the daemon socket and send JSON requests.

Allocate Cores Payload
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
    "version": "1.0",
    "service_name": "my-service",
    "action": "allocate_cores",
    "cores_requested": n
   }

Where n = {0, 1, 2, 3..,n}. `0` means the maximum available isolated cores. The current heuristics only allocate 80% of the available isolcpus cores unless the service requests the exact number of cores `n` in the request.

List allocations Payload
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
    "version": "1.0",
    "service_name": "any-service",
    "action": "list_allocations"
   }

Usage Examples
--------------

Scenario I: Node with no isolcpus configured
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Request:**

.. code-block:: json

   {
    "version": "1.0",
    "service_name": "my-service",
    "action": "allocate_cores",
    "cores_requested": 2
   }

**Response:**

.. code-block:: json

   {
    "version": "1.0",
    "error": "No Isolated CPUs configured"
   }

* This error means allocation is not possible because no CPUs are isolated.
* If CPU pinning is required, check your kernel boot parameters and system configuration.

Scenario II: Allocate Cores with n = 0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Request:**

.. code-block:: json

   {
    "version": "1.0",
    "service_name": "my-service",
    "action": "allocate_cores",
    "cores_requested": 0
   }

**Response:**

.. code-block:: json

   {
    "version": "1.0",
    "service_name": "my-service",
    "cores_requested": 0,
    "cores_allocated": 134,
    "allocated_cores": "0-133",
    "shared_cpus": "134-149",
    "total_available_cpus": 150,
    "remaining_available_cpus": 16
   }

* When `cores_requested` is 0, EPA Orchestrator will allocate 80% of the isolcpus cores and make sure that the remain 20% do not exceed more than 16 cores.

Scenario III: Allocate Cores with n = 4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Request:**

.. code-block:: json

   {
    "version": "1.0",
    "service_name": "my-service",
    "action": "allocate_cores",
    "cores_requested": 4
   }

**Response:**

.. code-block:: json

   {
    "version": "1.0",
    "service_name": "my-service",
    "cores_requested": 4,
    "cores_allocated": 4,
    "allocated_cores": "0-3",
    "shared_cpus": "4-19",
    "total_available_cpus": 20,
    "remaining_available_cpus": 16
   }

* Successfully allocates exactly the requested number of cores.
* Returns the allocated CPU ranges and remaining shared CPUs.

Scenario IV: Allocate Cores (Insufficient CPUs Available)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Request:**

.. code-block:: json

   {
    "version": "1.0",
    "service_name": "my-service",
    "action": "allocate_cores",
    "cores_requested": 25
   }

**Response:**

.. code-block:: json

   {
    "version": "1.0",
    "error": "Insufficient CPUs available. Requested: 25, Available: 20"
   }

* Error occurs when more cores are requested than available in the isolated CPU set.
* The error message includes both the requested and available counts.

Scenario V: List Allocations (With Existing Allocations)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Request:**

.. code-block:: json

   {
    "version": "1.0",
    "service_name": "any-service",
    "action": "list_allocations"
   }

**Response:**

.. code-block:: json

   {
    "version": "1.0",
    "total_allocations": 2,
    "total_allocated_cpus": 6,
    "total_available_cpus": 20,
    "remaining_available_cpus": 14,
    "allocations": [
      {
        "service_name": "service-1",
        "allocated_cores": "0-3",
        "cores_count": 4
      },
      {
        "service_name": "service-2",
        "allocated_cores": "4-5",
        "cores_count": 2
      }
    ]
   }

* Shows current allocation state when services have been allocated cores.
* `total_allocations` counts the number of services with allocations.
* `total_allocated_cpus` is the sum of all allocated cores across services.
* `remaining_available_cpus` is the difference between total and allocated.

Verifying EPA Orchestrator Status
---------------------------------

To verify that the EPA Orchestrator is properly installed and running, use the `juju status` command. A successful deployment should show the `epa-orchestrator` application in an active state.

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

The `*` indicates the primary unit for the application. When you see this status, the EPA Orchestrator is ready to handle CPU core allocation requests.