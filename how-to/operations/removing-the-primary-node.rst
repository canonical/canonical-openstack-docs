Removing the primary node
#########################

Removing the primary node refers to the removal of the first (bootstrap) node in the cluster and is only applicable when using the manual bare metal provider.

If the deployment consists of multiple nodes then remove all non-primary nodes before removing the primary node. Refer to the :doc:`Scaling the cluster in</how-to/operations/scaling-the-cluster-in>` section of this documentation for exact instructions on how to do that.

Remove components from the machine
++++++++++++++++++++++++++++++++++

.. warning ::

   Removing the primary node will destroy the entire Canonical OpenStack deployment.

Software components now need to be removed from the primary node. Perform all the below steps on the primary node.

Remove the Juju models:

.. code-block :: text

   juju destroy-model --destroy-storage --no-prompt --force --no-wait openstack
   juju destroy-model --destroy-storage --no-prompt --force --no-wait admin/openstack-machines

Remove the Juju controller:

.. code-block :: text

   juju destroy-controller --no-prompt --destroy-storage  --force --no-wait localhost-localhost

Remove the Juju agent:

.. code-block :: text

   sudo /sbin/remove-juju-services

Remove the ``juju`` snap:

.. code-block :: text

   sudo snap remove --purge juju

Remove Juju configuration:

.. code-block :: text

   rm -rf ~/.local/share/juju
   sudo rm -rf /var/lib/juju/dqlite
   sudo rm -rf /var/lib/juju/system-identity
   sudo rm -rf /var/lib/juju/bootstrap-params

Remove the ``openstack-hypervisor`` and ``openstack`` snaps:

.. code-block :: text

   sudo snap remove --purge openstack-hypervisor
   sudo snap remove --purge openstack

Remove ``openstack`` snap configuration:

.. code-block :: text

   rm -rf ~/.local/share/openstack

Remove the ``k8s`` snap:

.. code-block :: text

   sudo snap remove --purge k8s

Remove the ``microovn`` snap:

.. code-block :: text

   sudo snap remove --purge microovn

.. note ::

   The above steps can take a few minutes to complete.

Remove the disk(s) used by MicroCeph on this node:

.. code-block :: text

   sudo microceph disk list
   sudo microceph disk remove --bypass-safety-checks <OSD on this node>

.. note ::

   ``sudo microceph disk list`` may list the un-partitioned disks on the system. These can be ignored.

Remove the ``microceph`` snap:

.. code-block :: text

   sudo snap remove --purge microceph

If required clean the disk(s) identified in the earlier command:

.. warning ::

   The ``dd`` command will result in the permanent erasure of data. It is vital that you have specified the correct disk path to avoid unintended data loss.

.. code-block :: text

   sudo dd if=/dev/zero of=PATH bs=4M count=10

``PATH`` is a path to the disk being cleaned.

Clear the remaining network configuration with a reboot:

.. code-block :: text

   sudo reboot
