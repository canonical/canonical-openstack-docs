Enable and deploy a gated storage backend
=========================================

Use this procedure to unlock a gated in-tree storage backend in the CLI and
then deploy it. For general information about feature gates, see
:doc:`Manage experimental features </how-to/operations/manage-experimental-features>`.

.. note::

   Pure Storage is generally available and does not require a feature gate.
   Add it directly with ``sunbeam storage add purestorage ...``.

List the available feature gates
--------------------------------

List the gates that are available in your deployment:

.. code:: text

   sunbeam list-feature-gates

Identify the gate key for the storage backend that you want to deploy. Current
gated in-tree storage backends use keys such as
``feature.storage.dellsc`` and ``feature.storage.hitachi``.

Enable the storage backend gate
-------------------------------

Unlock the backend by setting its feature gate to ``true``:

.. code:: text

   sudo snap set openstack feature.storage.<backend>=true

Replace ``<backend>`` with the storage backend name, for example
``dellsc`` or ``hitachi``.

.. note::

   Unlocking the gate makes the backend visible in the CLI. It does not deploy
   the backend.

Verify that the backend is unlocked
-----------------------------------

Run the feature gate command again and confirm that the **Unlocked** column is
set for your storage backend:

.. code:: text

   sunbeam list-feature-gates

If the backend does not appear immediately in the CLI, start a new command
invocation and check again.

In local multi-node deployments, gate changes propagate automatically across
nodes in roughly 5 to 10 seconds. In MAAS deployments, you may need to run the
same ``snap set`` command on each node even though the gate state is still
stored in the cluster database.

Review the backend options in the CLI
---------------------------------------

After the gate is unlocked, confirm that the backend is now exposed by
the storage commands:

.. code:: text

   sunbeam storage add --help

or:

.. code:: text

   sunbeam storage options <backend>

Use ``sunbeam storage options <backend>`` to review the configuration fields
required by the backend before you create its YAML configuration file.

Deploy the backend
------------------

Add the backend by using the backend type, an instance name, and a backend
configuration file:

.. code:: text

   sunbeam storage add <backend> <name> --config-file <backend>.yaml

For example, to deploy a Hitachi backend:

.. code:: text

   sunbeam storage add hitachi hitachi-prod --config-file hitachi.yaml

Verify the deployment
---------------------

List deployed storage backends and confirm that the new backend is present:

.. code:: text

   sunbeam storage list

Once deployed, the backend remains managed separately from the feature gate
state.
