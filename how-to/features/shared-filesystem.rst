Shared Filesystems as a Service
===============================

This feature deploys `Manila`_, the OpenStack Shared Filesystems service.
It enables the user to create NFS Shared Filesystems on the Ceph storage
backend.


Enabling Shared Filesystems
---------------------------

This feature requires the storage role. To enable this feature, run the
following command:

::

   sunbeam enable shared-filesystem

The following commands would have to be run on the storage nodes:

::

   sudo microceph.ceph mgr module enable microceph
   sudo microceph.ceph orch set backend microceph

The openstack CLI can now be used to create and manage CephFS NFS Shared
Filesystems. See the upstream `Manila CLI`_ documentation for details.

Disabling Shared Filesystems
----------------------------

To disable this feature, run the following command:

::

   sunbeam disable shared-filesystem

Usage
-----

Administrators need to create a share type suitable for CephFS NFS share:

::

   openstack share type create cephfsnfstype false

   +----------------------+--------------------------------------+
   | Field                | Value                                |
   +----------------------+--------------------------------------+
   | id                   | 8fa7d7ff-16de-44c4-97c2-627b608970bd |
   | name                 | cephfsnfstype                        |
   | visibility           | public                               |
   | is_default           | False                                |
   | required_extra_specs | driver_handles_share_servers : False |
   | optional_extra_specs |                                      |
   | description          | None                                 |
   +----------------------+--------------------------------------+

   openstack share type set cephfsnfstype --extra-specs vendor_name=Ceph storage_protocol=NFS

Shares can then be created with the following command:

::

   openstack share create --share-type cephfsnfstype --name cephnfsshare1 nfs 1

   +---------------------------------------+--------------------------------------+
   | Field                                 | Value                                |
   +---------------------------------------+--------------------------------------+
   | access_rules_status                   | active                               |
   | availability_zone                     | None                                 |
   | create_share_from_snapshot_support    | False                                |
   | created_at                            | 2025-08-18T07:19:04.825882           |
   | description                           | None                                 |
   | has_replicas                          | False                                |
   | host                                  |                                      |
   | id                                    | 9ad6e4f1-26c2-47b0-944a-957c973e8260 |
   | is_public                             | False                                |
   | is_soft_deleted                       | False                                |
   | metadata                              | {}                                   |
   | mount_snapshot_support                | False                                |
   | name                                  | cephnfsshare2                        |
   | progress                              | None                                 |
   | project_id                            | 59e4d08bafeb42a2987d0dd7ef477764     |
   | replication_type                      | None                                 |
   | revert_to_snapshot_support            | False                                |
   | scheduled_to_be_deleted_at            | None                                 |
   | share_group_id                        | None                                 |
   | share_network_id                      | None                                 |
   | share_proto                           | NFS                                  |
   | share_server_id                       | None                                 |
   | share_type                            | 89a7c4c9-9f01-4051-a1f2-407c63387e68 |
   | share_type_name                       | cephfsnfstype                        |
   | size                                  | 1                                    |
   | snapshot_id                           | None                                 |
   | snapshot_support                      | False                                |
   | source_backup_id                      | None                                 |
   | source_share_group_snapshot_member_id | None                                 |
   | status                                | creating                             |
   | task_state                            | None                                 |
   | user_id                               | 03ed09d378be484cade24f5731bb820d     |
   | volume_type                           | cephfsnfstype                        |
   +---------------------------------------+--------------------------------------+



The created share should be available:

::

   openstack share list

   +--------------------------------------+---------------+------+-------------+-----------+-----------+-----------------+--------------------------------+-------------------+
   | ID                                   | Name          | Size | Share Proto | Status    | Is Public | Share Type Name | Host                           | Availability Zone |
   +--------------------------------------+---------------+------+-------------+-----------+-----------+-----------------+--------------------------------+-------------------+
   | 5c156c74-43bf-432b-af2e-bddc82f5c6f9 | cephnfsshare1 |    1 | NFS         | available | False     | cephfsnfstype   | manila-cephfs-0@cephnfs#cephfs | nova              |
   +--------------------------------------+---------------+------+-------------+-----------+-----------+-----------------+--------------------------------+-------------------+

Note the export location of the share:

::

   openstack share export location list cephnfsshare1

   +--------------------------------------+------------------------------------------------------------------------------------------------------------+-----------+
   | ID                                   | Path                                                                                                       | Preferred |
   +--------------------------------------+------------------------------------------------------------------------------------------------------------+-----------+
   | 96f2ae5a-7fdf-4457-a65d-6b8579635dd0 | 192.168.137.10:/volumes/_nogroup/5692f246-d3d0-4567-81a6-3f590d1957a4/aa0c7383-b5e1-48ab-984c-15b6219c48e7 | True      |
   +--------------------------------------+------------------------------------------------------------------------------------------------------------+-----------+

The export location of the share contains the bind IP address of the NFS
Ganesha server and the path to be mounted.
