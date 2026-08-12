DNS as a Service
================

This feature deploys `Designate`_, the OpenStack DNS service.

Enabling DNS
------------

To enable DNS, run the following command:

::

   sunbeam enable dns "<ns record>"

The openstack CLI can now be used to manage DNS. See the upstream
`Designate command-line interface documentation`_ for details.

Nameservers are specified with FQDNs separated by a space, each ending
with a dot, whose records point to the DNS instance managed by the
Designate service. It is assumed that your infrastructure DNS is
configured to redirect your nameserver records to the DNS service
address.

Disabling DNS
-------------

To disable DNS, run the following command:

::

   sunbeam disable dns

Fetching DNS service address
----------------------------

To fetch the DNS service address, run the following command:

::

   sunbeam dns address

Usage
-----

Users need the role ``member`` to be able to manage DNS zones and
records. A user has this role by default so all users have the ability
to manage DNS in their own project.

For example, create zone ``sunbeam.tld`` with:

::

   openstack zone create --email dnsmaster@sunbeam.tld sunbeam.tld.

   +----------------+--------------------------------------+
   | Field          | Value                                |
   +----------------+--------------------------------------+
   | action         | CREATE                               |
   | attributes     |                                      |
   | created_at     | 2023-10-11T20:25:52.000000           |
   | description    | None                                 |
   | email          | dnsmaster@sunbeam.tld                |
   | id             | f27cd25d-43ff-4205-84a4-79c524bd9652 |
   | masters        |                                      |
   | name           | sunbeam.tld.                         |
   | pool_id        | 794ccc2c-d751-44fe-b57f-8894c9f5c842 |
   | project_id     | b6cc0f4bf25c432785b4f7c91858304b     |
   | serial         | 1697055952                           |
   | shared         | False                                |
   | status         | PENDING                              |
   | transferred_at | None                                 |
   | ttl            | 3600                                 |
   | type           | PRIMARY                              |
   | updated_at     | None                                 |
   | version        | 1                                    |
   +----------------+--------------------------------------+

Retrieve the list of DNS zones - wait for the new zone to become
``ACTIVE``:

::

   openstack zone list

   +--------------------------------------+--------------+---------+------------+--------+--------+
   | id                                   | name         | type    |     serial | status | action |
   +--------------------------------------+--------------+---------+------------+--------+--------+
   | f27cd25d-43ff-4205-84a4-79c524bd9652 | sunbeam.tld. | PRIMARY | 1697055952 | ACTIVE | NONE   |
   +--------------------------------------+--------------+---------+------------+--------+--------+

Create the ``TXT`` record ``note.sunbeam.tld``:

::

   openstack recordset create --type TXT --record '"This is a record created in Sunbeam!"' sunbeam.tld. note

   +-------------+----------------------------------------+
   | Field       | Value                                  |
   +-------------+----------------------------------------+
   | action      | CREATE                                 |
   | created_at  | 2023-10-11T20:30:33.000000             |
   | description | None                                   |
   | id          | 40222abd-1624-42af-90ff-7fc212e99885   |
   | name        | note.sunbeam.tld.                      |
   | project_id  | b6cc0f4bf25c432785b4f7c91858304b       |
   | records     | "This is a record created in Sunbeam!" |
   | status      | PENDING                                |
   | ttl         | None                                   |
   | type        | TXT                                    |
   | updated_at  | None                                   |
   | version     | 1                                      |
   | zone_id     | f27cd25d-43ff-4205-84a4-79c524bd9652   |
   | zone_name   | sunbeam.tld.                           |
   +-------------+----------------------------------------+

Obtain the address of the DNS service with the ``sunbeam`` command:

::

   sunbeam dns address
   10.206.54.244

With the ``dig`` command, query the DNS service and verify that it
returns the newly-created ``TXT`` record:

::

   dig @10.206.54.244 +short TXT note.sunbeam.tld
   "This is a record created in Sunbeam!"


.. _Designate command-line interface documentation: https://docs.openstack.org/python-designateclient/latest/user/shell-v2.html
