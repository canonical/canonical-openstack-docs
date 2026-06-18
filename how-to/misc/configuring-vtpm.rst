Configuring vTPM
================

Overview
--------

Virtual Trusted Platform Module (vTPM) support allows OpenStack instances to
use an emulated TPM device.

Prerequisites
-------------

* Enable the :doc:`Vault </how-to/features/vault>` feature.
* Enable the :doc:`Secrets as a Service </how-to/features/secrets>` feature.
* Use an image that supports UEFI firmware.

Operations
----------

Configure a flavor and an image for vTPM usage.

Validate compute host support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List the TPM traits advertised by a compute host:

::

   COMPUTE_UUID=$(openstack resource provider list --name <COMPUTE_HOST> -f value -c uuid)
   openstack resource provider trait list $COMPUTE_UUID | grep SECURITY_TPM

The command should return the supported TPM versions:

::

   | COMPUTE_SECURITY_TPM_1_2 |
   | COMPUTE_SECURITY_TPM_2_0 |

Flavor properties
~~~~~~~~~~~~~~~~~

Configure a flavor with the TPM version and model to expose to the instance:

To set the properties on an existing flavor, run:

::

   openstack flavor set FLAVORNAME \
      --property hw:tpm_version=2.0 \
      --property hw:tpm_model=tpm-crb

To create a new flavor with the same properties, run:

::

   openstack flavor create FLAVORNAME \
      --ram RAM \
      --disk DISK \
      --vcpus VCPUS \
      --property hw:tpm_version=2.0 \
      --property hw:tpm_model=tpm-crb

.. note::

   The ``tpm-crb`` model is only compatible with TPM version ``2.0``.

Image properties
~~~~~~~~~~~~~~~~

Configure the image to use UEFI firmware:

::

   openstack image set --property hw_firmware_type=uefi IMAGENAME

Launch an instance
~~~~~~~~~~~~~~~~~~

Launch an instance using the flavor and image configured above:

::

   openstack server create \
      --flavor FLAVORNAME \
      --image IMAGENAME \
      --network NETWORK \
      SERVERNAME

Verify vTPM in the guest
~~~~~~~~~~~~~~~~~~~~~~~~

After the instance boots, log in to the guest and check for TPM devices:

::

   ls -l /dev/tpm*

The guest should show devices such as ``/dev/tpm0`` and ``/dev/tpmrm0``.

Limitations
-----------

* The image must use UEFI firmware.
* The ``tpm-crb`` model requires TPM version ``2.0``.

References
----------

For more information about vTPM in OpenStack, see the upstream Nova
documentation:

* `Emulated Trusted Platform Module`_
* `Extra Specs`_
* `Useful image properties`_

.. LINKS
.. _Emulated Trusted Platform Module: https://docs.openstack.org/nova/latest/admin/emulated-tpm.html
.. _Extra Specs: https://docs.openstack.org/nova/latest/configuration/extra-specs.html
.. _Useful image properties: https://docs.openstack.org/glance/latest/admin/useful-image-properties.html
