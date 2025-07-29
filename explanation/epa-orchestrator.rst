CPU Pinning
================

Introduction
------------

CPU pinning is the binding of specific processes to dedicated CPU cores. The `isolcpus` kernel command line parameter is one way of configured isolated CPUs for the node. Once set, the system lists the isolated cores at `/sys/devices/system/cpu/isolated` on a given node.

The Enhanced Performance Accelerator (EPA) Orchestrator leverages this information for cpu cores allocation to the services. The **EPA Orchestrator** provides functionality to request isolated CPU cores for the purpose of CPU Pinning on a given node. The **EPA Orchestrator** is a snap which runs a daemon service `snap.epa-orchestrator.daemon.server` and exposes a Unix socket API for requesting cpu cores or listing the allocations. The **EPA Orchestrator** is designed to work seamlessly with other openstack services such as `openstack-hypervisor` through the socket connection.
The **EPA Orchestrator** is designed to work seamlessly with other openstack services such as `openstack-hypervisor` through the socket connection.

This document explains how the **EPA Orchestrator** can be used for CPU pinning of services within the Sunbeam Openstack.

Architecture
------------

The EPA Orchestrator operates as a daemon service that:

* Runs as a snap service (`snap.epa-orchestrator.daemon.service`)
* Exposes a Unix socket API for communication
* Performs system introspection to get the isolated CPU configuration
* Manages CPU core allocations based on isolated CPU configuration
* Integrates with OpenStack services through socket connections
* Provides allocation tracking and management capabilities
* Caches the allocation for a given service for a given node


Introspection
~~~~~~~~~~~~~

The orchestrator reads the system's isolated CPU configuration from `/sys/devices/system/cpu/isolated` and manages allocations based on this information. When no isolated CPUs are configured, the orchestrator operates in a "no-op" mode, allowing monitoring and automation tools to query allocations without errors.

Heuristics
~~~~~~~~~~~~~

- If a service requests the maximum number of cores without specifying an exact amount (i.e., "cores_requested": 0), the epa-orchestrator allocates 80% of the total isolCPUs to the service, leaving the remaining 20% unallocated, with the 20% number capped at a maximum of 16 cores.
- If a service requests a specific number of cores (i.e., "cores_requested": 8), the epa-orchestrator allocates the requested number of cores to the service.

Operational Modes
-----------------

**No CPU Pinning Required:**
No action is needed. EPA Orchestrator will operate in a "no-op" mode for allocations, but will not cause errors for monitoring or automation tools querying allocations.

**CPU Pinning Required:**
Ensure the `isolcpus` kernel parameter is set and that `/sys/devices/system/cpu/isolated` lists the expected CPUs. Reboot the system if you change kernel parameters.
