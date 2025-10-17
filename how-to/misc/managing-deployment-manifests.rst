Managing deployment manifests
=============================

This page shows how to manage deployment manifests. For an overview of
manifests, see the :doc:`Deployment manifest </explanation/deployment-manifest>` page.

.. note::
   Looking to use a manifest from an edge deployment? Take a look at
   `Manifest for non-stable deployments <#manifest-for-non-stable-deployments-4>`__.

List manifests
--------------

To list all manifests, run the following command:

::

   sunbeam manifest list

Sample output:

================================ ===================
ID                               Applied Date
================================ ===================
c6a6d2ab47ac4c21308483e567d64b04 2024-02-05 12:17:59
e446b42859f461e690d66b4d233c1ear 2024-02-06 07:39:38
================================ ===================

Show a manifest
---------------

To view the content of a manifest, run the following command:

::

   sunbeam manifest show --id <manifest id>

Sample output:

.. code:: text

   software:
     charms:
       keystone-k8s:
         channel: 2024.1/candidate
       glance-k8s:
         channel: 2024.1/candidate

To get the latest manifest, use the keyword ``latest`` instead of the
manifest ID:

::

   sunbeam manifest show --id latest

Generate a manifest
-------------------

A manifest file can be generated using the below command:

::

   sunbeam manifest generate --manifest-file <output file>

The generated manifest will be written to ``<output file>``.

Manifest for non-stable deployments
-----------------------------------

Manifest files for the ``candidate`` and ``edge`` risks can be found in:

::

   /snap/openstack/current/etc/manifests/candidate|edge.yml

A manifest with complete channel information is needed to deploy on
candidate or edge channels.

Specify a manifest
------------------

A manifest is specified by means of the ``--manifest`` option. There are
three supported use cases.

Cluster bootstrap
~~~~~~~~~~~~~~~~~

To specify a manifest during the cluster bootstrap process:

::

   sunbeam cluster bootstrap [--role <control|compute|network|storage>] [--manifest <manifest file path>] [--accept-defaults]

Cluster refresh
~~~~~~~~~~~~~~~

To specify a manifest during a cluster refresh (update) process:

::

   sunbeam cluster refresh [--manifest <manifest file path>] [--clear-manifest] [--upgrade-release]

Only components managed via Terraform can be changed (bootstrap options
will be immutable at this point).

.. note::
   A manifest update must be accompanied by a complete manifest file
   (i.e. not a delta).

Feature enablement
~~~~~~~~~~~~~~~~~~

To specify a manifest during the enablement (or post-enablement) of a
feature:

::

   sunbeam enable [--manifest <manifest file path>] <feature> [<feature options>]

A post-enablement invocation implies a manifest update.

.. note::
   A manifest update must be accompanied by a complete manifest file
   (i.e. not a delta).
