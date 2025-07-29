CPU pinning
================

CPU pinning is the binding of specific processes to dedicated CPU cores. The ``isolcpus`` kernel command line parameter is one way of configuring isolated CPUs for the node. Once set, the system lists the isolated cores in :file:`/sys/devices/system/cpu/isolated` on a given node.

The Enhanced Performance Accelerator (EPA) Orchestrator leverages this information for CPU core allocation to the services. The **EPA Orchestrator** provides functionality to request isolated CPU cores for the purpose of CPU Pinning on a given node. The **EPA Orchestrator** is a snap which runs a daemon service `snap.epa-orchestrator.daemon.server` and exposes a Unix socket API for requesting CPU cores or listing the allocations. The **EPA Orchestrator** is designed to work seamlessly with other OpenStack services such as `openstack-hypervisor` through the socket connection.

This document explains the role and the design of the **EPA Orchestrator** within the Sunbeam OpenStack.

Architecture
------------

The EPA Orchestrator operates as a daemon service that:

* Runs as a snap service (`snap.epa-orchestrator.daemon.service`)
* Exposes a Unix socket API for communication
* Performs system introspection to get the isolated CPU configuration
* Performs allocation and deallocation of CPU cores to the services


Introspection
~~~~~~~~~~~~~

The orchestrator reads the system's isolated CPU configuration from :file:`/sys/devices/system/cpu/isolated` and manages allocations based on this information. When no isolated CPUs are configured, the orchestrator operates in a "no-op" mode.

Operational Modes
-----------------

**No CPU Pinning Required:**
No action is needed. EPA Orchestrator will operate in a "no-op" mode for allocations, but will not cause errors for monitoring or automation tools querying allocations.

**CPU Pinning Required:**
Ensure the ``isolcpus`` kernel parameter is set and that :file:`/sys/devices/system/cpu/isolated` lists the expected CPUs. Reboot the system if you change kernel parameters.
