EPA Orchestrator
================================

The EPA Orchestrator is a snap which runs a daemon service `snap.epa-orchestrator.daemon.server` and exposes a Unix socket API for requesting cpu cores or listing the allocations.

* **Why am I am unable to connect to epa-orchestrator daemon socket?**

Check if the epa-orchestrator snap is running

.. code-block:: bash

        sudo snap list

If epa-orchestrator snap is not running then make sure that epa-orchestrator unit is `active`

.. code-block:: bash
        
        juju status


* **Why am I seeing zero allocations?**
  Check if `/sys/devices/system/cpu/isolated` is empty on the node. This means isolCPUs are not configured on the node.

* **Why does `allocate_cores` action on epa-orchestrator returns an error?**
  Allocation is only possible when isolated CPUs are configured. Set the appropriate kernel parameters and reboot if needed.

* **How do I verify isolated CPUs?**
  Run the following command on the node:
  
  .. code-block:: bash
  
     cat /sys/devices/system/cpu/isolated
  
  If the output is empty, no CPUs are isolated.