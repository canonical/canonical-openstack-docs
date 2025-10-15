CPU pinning and huge pages
==========================

The Enhanced Performance Accelerator (EPA) orchestrator provides resource allocation for CPU pinning and huge pages within Sunbeam OpenStack. The EPA orchestrator is a snap that runs a daemon service `snap.epa-orchestrator.daemon.server` and exposes a Unix socket API for resource allocation, introspection, and management. The EPA orchestrator is designed to work seamlessly with other OpenStack services such as `openstack-hypervisor` through the socket connection.

This document explains the role and design of the EPA orchestrator within Sunbeam OpenStack.

CPU pinning
-----------

CPU pinning is the binding of specific processes to dedicated CPU cores. The ``isolcpus`` kernel command line parameter is one way of configuring isolated CPUs for the node (e.g., ``isolcpus=0-3``). Once set, the system lists the isolated cores in :file:`/sys/devices/system/cpu/isolated` on a given node.

The EPA orchestrator leverages this information for CPU core allocation to services, providing functionality to request isolated CPU cores for CPU pinning on a given node.

Huge pages
----------

Huge pages are configured via kernel command line parameters: ``default_hugepagesz``, ``hugepagesz``, and ``hugepages`` (e.g., ``default_hugepagesz=1G hugepagesz=1G hugepages=16``).

The EPA orchestrator provides NUMA-aware CPU cores and huge pages allocation, allowing services to request and manage cores and huge pages allocations across NUMA nodes.

Architecture
------------

The EPA orchestrator operates as a daemon service that:

* Runs as a snap service (`snap.epa-orchestrator.daemon.service`)
* Exposes a ``epa.sock`` Unix socket API for communication
* Performs system introspection to discover isolated CPU configuration and NUMA huge pages information
* Serves service requests to allocate CPU cores and huge pages allocations

Introspection
~~~~~~~~~~~~~

The orchestrator performs system introspection for both CPU and memory resources:

* **CPU introspection**: Reads the system's isolated CPU configuration from :file:`/sys/devices/system/cpu/isolated` and manages allocations based on this information. When no isolated CPUs are configured, the orchestrator operates in a "no-op" mode for CPU allocations.
* **Huge pages introspection**: Reads NUMA huge pages information from the system and provides NUMA-aware huge pages allocation.

Operational modes
-----------------

The EPA orchestrator supports different operational modes based on the configured resources:

**No CPU pinning or huge pages Required:**
No action is needed. EPA orchestrator will operate in a "no-op" mode for allocations, but will not cause errors for monitoring or automation tools querying allocations.

**CPU pinning required:**
Ensure the ``isolcpus`` kernel parameter is set and that :file:`/sys/devices/system/cpu/isolated` lists the expected CPUs. Reboot the system if you change kernel parameters.

**Huge pages required:**
Configure the ``default_hugepagesz``, ``hugepagesz``, and ``hugepages`` kernel parameters. The EPA orchestrator will introspect NUMA huge pages configuration and track allocations per service and per NUMA node. Reboot the system if you change kernel parameters.
