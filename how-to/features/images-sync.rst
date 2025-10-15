Images Sync
===========

This feature deploys OpenStack Images Sync, a tool for importing
images from a SimpleStreams source to the OpenStack Glance image service.

.. note::
   This feature is currently only supported in channel ``2024.1/edge`` of the
   **openstack** snap.

Enable Images Sync
------------------

To enable Images Sync, run the following command:

.. literalinclude:: ../snippets/images-sync.task.sh
   :language: bash
   :start-after: [docs-view:enable-images-sync]
   :end-before:  [docs-view:enable-images-sync-end]

Disable Images Sync
-------------------

To disable Images Sync, run the following command:

.. literalinclude:: ../snippets/images-sync.task.sh
   :language: bash
   :start-after: [docs-view:disable-images-sync]
   :end-before:  [docs-view:disable-images-sync-end]

.. caution::
   **Caution**: Disabling Images Sync will **not** remove images that have been
   previously imported from the Glance image service.

Usage
-----

Users need the role ``reader`` to list images.

To list images added by the Images Sync feature, run the following
command:

::

   openstack image list | grep auto-sync/

Sample output:

::

   | 200df230-0983-4cd8-9d14-97327664f77b | auto-sync/ubuntu-focal-20.04-amd64-server-20240513-disk1.img   | active |
   | 1935961b-e646-4f0d-a796-8c653308f790 | auto-sync/ubuntu-jammy-22.04-amd64-server-20240514-disk1.img   | active |
   | 62be8807-f068-4317-9552-c1357fa8d962 | auto-sync/ubuntu-noble-24.04-amd64-server-20240523.1-disk1.img | active |

The feature downloads images for the three most recent LTS releases.
