Manage experimental features
============================

Overview
--------

Canonical OpenStack supports experimental features that are not enabled
by default. These features are controlled through feature gates, which
allow operators to opt in to functionality that is still under active
development or not yet considered production-ready.

Use the commands documented here to discover available feature gates and
to enable or disable them.

List feature gates
------------------

Feature gates group one or more related features under a common flag.
To list all available feature gates:

.. code:: text

   sunbeam list-feature-gates

Example output:

::

                                   Feature Gates
   +---------------------------+-----------------+-------------------+----------+
   | Gate Key                  | Type            | Name              | Unlocked |
   +===========================+=================+===================+==========+
   | feature.baremetal         | feature         | baremetal         |          |
   +---------------------------+-----------------+-------------------+----------+
   | feature.microovn-sdn      | feature-gate    | microovn-sdn      |          |
   +---------------------------+-----------------+-------------------+----------+
   | feature.multi-region      | feature-gate    | multi-region      |          |
   +---------------------------+-----------------+-------------------+----------+
   | feature.shared-filesystem | feature         | shared-filesystem |          |
   +---------------------------+-----------------+-------------------+----------+
   | feature.storage.dellsc    | storage-backend | dellsc            |          |
   +---------------------------+-----------------+-------------------+----------+
   | feature.storage.hitachi   | storage-backend | hitachi           |          |
   +---------------------------+-----------------+-------------------+----------+

The output lists each gate's key (used with ``snap set``), its type, and name.
The **Unlocked** column is set when the feature gate has been enabled by setting
its key to ``true`` via ``sudo snap set openstack``.

Enable an experimental feature
-------------------------------

To enable an experimental feature, set its corresponding snap
configuration option to ``true``:

.. code:: text

   sudo snap set openstack feature.<feature-name>=true

Replace ``<feature-name>`` with the gate key of the feature you want to
enable. For example, to enable the ``multi-region`` feature gate:

.. code:: text

   sudo snap set openstack feature.multi-region=true

.. note::

   Experimental features may change or be removed in future releases.
   Enable them only in environments where instability is acceptable.

Disable an experimental feature
--------------------------------

To disable a previously enabled experimental feature:

.. code:: text

   sudo snap set openstack feature.<feature-name>=false
