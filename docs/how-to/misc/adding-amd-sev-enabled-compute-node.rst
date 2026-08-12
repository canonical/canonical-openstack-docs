Adding AMD SEV enabled Compute Node
===================================

Secure Encrypted Virtualization is a technology from AMD enabling encryption of guest memory.
OpenStack provides support to make use of this technology and deploy trusted guests.
Refer `Admin guide <https://docs.openstack.org/nova/latest/admin/sev.html>`_ for more information.

In Canonical OpenStack, AMD SEV enabled compute nodes can be added using the :doc:`cluster scale out procedure </how-to/operations/scaling-the-cluster-out>` by adding compute role to the node.
Canonical OpenStack auto detects the compute node if the node is AMD SEV enabled or not.

For AMD SEV enabled compute nodes, sufficient memory need to be reserved for the host since SEV enabled guests memory pages are pinned in RAM.
To set the reserved memory for the host, update manifest with the following configuration for openstack-hypervisor charm.

::

    core:
      config:
        software:
          charms:
            openstack-hypervisor:
              config:
                reserved-host-memory-mb-for-sev: 8192


For manual bare metal provider, pass the updated manifest in join command

::

    cat TOKEN_FILE | sunbeam cluster join --manifest MANIFEST_FILE --role ROLES -

For MAAS provider, pass the updated manifest in deploy command

::

    sunbeam cluster deploy --manifest MANIFEST_FILE

The configuration will be applied only on AMD SEV enabled compute nodes.

Operations
----------

Once the cloud is deployed, Operator need to do the following operations

Flavor properties
~~~~~~~~~~~~~~~~~

Create or set flavors with the property `hw:mem_encryption=true`.

To create new flavor with the above property, run the command

::

    openstack flavor create FLAVORNAME --ram RAM --disk DISK --vcpus VCPUS --property hw:mem_encryption=true

To set property on existing flavor, run the command

::

    openstack flavor set --property hw:mem_encryption=true FLAVORNAME

Flavors created by `sunbeam configure` ending with `-sev` have already the property added.


Image properties
~~~~~~~~~~~~~~~~

Create or set images with the property `hw_firmware_type=uefi`

To create new image with the above property, run the command

::

    openstack image create --disk-format FORMAT --container-format CFORMAT --file IMAGEFILE --property hw_firmware_type=uefi IMAGENAME

To set property on existing image, run the command

::

    openstack image set --property hw_firmware_type=uefi IMAGENAME

The :doc:`Images Sync Feature </how-to/features/images-sync>` will add the property `hw_firmware_type=uefi` by default when importing images.

Launch instance
~~~~~~~~~~~~~~~

To launch an SEV encrypted instance, use the flavor and images set with the above properties.

Limitations
-----------

* Live migration is not supported for AMD SEV enabled guests.
