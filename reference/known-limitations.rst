.. _Known limitations:

Known limitations
=================

This document describes the known limitations of the Sunbeam project.


.. list-table::
   :widths: 20 15 55
   :header-rows: 1

   * - Issue
     - Bug Number
     - Meaning
   * - **Cold migration is not supported**
     - `2082056 <https://bugs.launchpad.net/snap-openstack/+bug/2082056>`__
     - Cold migration of VMs is not supported. This means that if a VM is running on a host, it cannot be moved to another host while being shutdown. Current workaround is to use live migration. This also means resizing instances is not supported.
