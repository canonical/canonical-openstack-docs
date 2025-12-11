Rating as a Service
===================

This feature deploys `CloudKitty`_ providing Canonical OpenStack with the ability bill 
based on resource usage

Enable the Rating service
-------------------------

To enable Rating, run the following command:

::

   sunbeam enable rating

The openstack CLI can now be used to manage Rating. See the upstream
`CloudKitty command-line interface documentation`_ for details.

Disable the Rating service
--------------------------

To disable Rating, run the following command:

::

   sunbeam disable rating

Usage
-----

Setting up of an example billing scenario
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To setup a scenario where the m1.tiny flavor is billed at 0.01 units of currency (based on example at `CloudKitty hashmap rating module`_):

Create a hashmap group with a descriptive name, and store its UUID in a variable for later

.. terminal::
   :input: openstack rating hashmap group create instance_uptime_flavor_id

   +---------------------------+--------------------------------------+
   | Name                      | Group ID                             |
   +---------------------------+--------------------------------------+
   | instance_uptime_flavor_id | d702c760-fb4b-456d-afb2-af5c0c9943ad |
   +---------------------------+--------------------------------------+

   GROUP_UUID=$(openstack rating hashmap group list -f value -c name -c group_id | grep ^instance_uptime_flavor_id | awk '{ print $2 }')


Create a hashmap service with a descriptive name, and store its UUID in a variable for later

.. terminal::
   :input: openstack rating hashmap service create instance
   
   +----------+--------------------------------------+
   | Name     | Service ID                           |
   +----------+--------------------------------------+
   | instance | e63eac22-bf4b-4013-986a-4240f6861b62 |
   +----------+--------------------------------------+
   
   SERVICE_UUID=$(openstack rating hashmap service list -f value -c name -c service_id | grep ^instance | awk '{ print $2 }')


Create a hashmap field for the service with a descriptive name, and store its UUID in a variable for later

.. terminal::
   :input: openstack rating hashmap field create $SERVICE_UUID flavor_id
   
   +-----------+--------------------------------------+--------------------------------------+
   | Name      | Field ID                             | Service ID                           |
   +-----------+--------------------------------------+--------------------------------------+
   | flavor_id | 107b7c1a-0b22-49b0-a10c-e4b05f5ccf04 | e63eac22-bf4b-4013-986a-4240f6861b62 |
   +-----------+--------------------------------------+--------------------------------------+
   
   FIELD_UUID=$(openstack rating hashmap field list $SERVICE_UUID -f value -c name -c field_id | grep ^flavor_id | awk '{ print $2 }')


Create a hashmap service with a descriptive name, and store its UUID in a variable for later

.. terminal::
   :input: openstack rating hashmap mapping create 0.01 --field-id $FIELD_UUID --value $(openstack flavor show m1.tiny -f value  -c id) -g $GROUP_UUID -t flat

   +----------------+----------------+----------------+------+----------------+------------+--------------------+------------+
   | Mapping ID     | Value          | Cost           | Type | Field ID       | Service ID | Group ID           | Project ID |
   +----------------+----------------+----------------+------+----------------+------------+--------------------+------------+
   | c55db7fd-3c5f- | 7cd5ef70-4532- | 0.010000000000 | flat | 107b7c1a-0b22- | None       | d702c760-fb4b-     | None       |
   | 4689-89a1-     | 4396-8ab8-     | 00000020816681 |      | 49b0-a10c-     |            | 456d-afb2-         |            |
   | c29ae3077f5c   | 7fe1bd780b43   | 71             |      | e4b05f5ccf04   |            | af5c0c9943ad       |            |
   +----------------+----------------+----------------+------+----------------+------------+--------------------+------------+



.. _CloudKitty: https://docs.openstack.org/cloudkitty/latest/
.. _CloudKitty command-line interface documentation: https://docs.openstack.org/cloudkitty/latest/admin/cli/index.html
.. _CloudKitty hashmap rating module: https://docs.openstack.org/cloudkitty/latest/user/rating/hashmap.html
