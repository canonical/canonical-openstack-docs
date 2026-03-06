Deploy a Pure Storage backend
=============================

Overview
--------

Use this procedure to deploy a Pure Storage backend for Cinder. The backend is
deployed as the ``cinder-volume-purestorage`` charm.

Requirements
------------

You will need:

* a bootstrapped Canonical OpenStack deployment with storage capability already
  in place
* network connectivity from the storage nodes to the Pure Storage array
* a valid Pure Storage API token
* a backend instance name that satisfies Juju application naming rules,
  for example ``pure-prod``

Inspect the available options
-----------------------------

If you want to review the supported configuration keys before deploying the
backend, run:

.. code-block:: text

   sunbeam storage options purestorage

Create the backend configuration
--------------------------------

You can provide the backend settings in a YAML file or pass the equivalent CLI
options directly to the deployment command. The required keys are ``san-ip``
and ``pure-api-token``.

For example, create a file named ``purestorage.yaml`` with the following
content:

.. code-block:: yaml

   san-ip: 192.0.2.10
   pure-api-token: 01234567-89ab-cdef-0123-456789abcdef
   protocol: iscsi
   volume-backend-name: pure-iscsi
   backend-availability-zone: az1
   pure-iscsi-cidr: 192.0.2.0/24

Set ``protocol`` to ``iscsi``, ``fc``, or ``nvme`` to match your deployment.
For NVMe/TCP deployments, you can also set ``pure-nvme-cidr`` and
``pure-nvme-transport``. Only ``tcp`` is supported for
``pure-nvme-transport``.

Deploy the backend
------------------

Deploy the backend with the backend type (``purestorage``), a
Juju-compatible backend instance name, and the configuration file:

.. code-block:: text

   sunbeam storage add purestorage pure-prod --config-file purestorage.yaml

If you prefer not to use a file, pass the equivalent options directly on the
command line.

Verify the backend
------------------

Check that the backend has been added:

.. code-block:: text

   sunbeam storage list

To inspect the deployed backend in more detail, run:

.. code-block:: text

   sunbeam storage show pure-prod
