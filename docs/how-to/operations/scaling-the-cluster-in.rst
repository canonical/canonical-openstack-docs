Scaling the cluster in
######################

Canonical OpenStack scales in, meaning that you can remove machines from the cluster if you no longer need them.

Scaling the cluster in using the manual bare metal provider
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The following section provides instructions on scaling the cluster in with the manual bare metal provider.

These instructions apply to all node types but the primary node. For instruction on the latter, refer to :doc:`Removing the primary node</how-to/operations/removing-the-primary-node>` section of this documentation.

Remove the machine from the cluster
-----------------------------------

To remove the machine from the cluster, execute the ``sunbeam cluster remove`` command on the primary node:

.. code-block :: text

   sunbeam cluster remove FQDN

``FQDN`` is a fully qualified domain name (FQDN) of the machine being removed.

For example, to remove the *cloud-2* machine from the :doc:`Example physical configuration</reference/example-physical-configuration>` section, execute the following command:

.. code-block :: text

   sunbeam cluster remove cloud-2.example.com

Remove components from the machine
----------------------------------

Software components now need to be removed from the target node. Perform all the below steps on the target node.

Remove the Juju agent:

.. code-block :: text

   sudo /sbin/remove-juju-services

Remove the ``juju`` snap:

.. code-block :: text

   sudo snap remove --purge juju

Remove Juju configuration:

.. code-block :: text

   rm -rf ~/.local/share/juju

Remove the ``openstack-hypervisor`` and ``openstack`` snaps:

.. code-block :: text

   sudo snap remove --purge openstack-hypervisor
   sudo snap remove --purge openstack

Remove ``openstack`` snap configuration:

.. code-block :: text

   rm -rf ~/.local/share/openstack

Remove the ``k8s`` snap:

.. code-block :: text

   sudo k8s remove-node
   sudo snap remove --purge k8s

.. note ::

   The above steps can take a few minutes to complete.

Remove the disk(s) used by MicroCeph on this node:

.. code-block :: text

   sudo microceph disk list
   sudo microceph disk remove <OSD on this node>

Remove the ``microceph`` snap:

.. code-block :: text

   sudo microceph disk list
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

Scaling the cluster in using Canonical MAAS
++++++++++++++++++++++++++++++++++++++++++++

The following section provides instructions on scaling the cluster out with Canonical MAAS.

Coming soon.

.. TODO: To be updated once https://warthogs.atlassian.net/browse/OPEN-2688 is implemented.

