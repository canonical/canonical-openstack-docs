Object Storage
==============

The object storage service providing Swift and S3 endpoints is enabled
automatically as soon as there are storage nodes in a cluster.

The object storage endpoints can be retrieved using ``openstack``
client. See :doc:`Using OpenStack CLI </how-to/misc/using-the-openstack-cli>` on how to use OpenStack
CLI.

Run the below command to get s3 endpoint:

::

   openstack endpoint list --service s3 --interface public

Sample output of the above command:

::

   +----------------------------------+-----------+--------------+--------------+---------+-----------+--------------------+
   | ID                               | Region    | Service Name | Service Type | Enabled | Interface | URL                |
   +----------------------------------+-----------+--------------+--------------+---------+-----------+--------------------+
   | 74c9adaa7041422692a1f55adf0a65eb | RegionOne | s3           | s3           | True    | public    | http://10.20.21.10 |
   +----------------------------------+-----------+--------------+--------------+---------+-----------+--------------------+

Run the below command to get swift endpoint:

::

   openstack endpoint list --service swift --interface public

Sample output of the above command:

::

   +----------------------------------+-----------+--------------+--------------+---------+-----------+-------------------------------------------------+
   | ID                               | Region    | Service Name | Service Type | Enabled | Interface | URL                                             |
   +----------------------------------+-----------+--------------+--------------+---------+-----------+-------------------------------------------------+
   | d30b885de04b4b1090d2c7d05d4c6562 | RegionOne | swift        | object-store | True    | public    | http://10.20.21.10/swift/v1/AUTH_$(project_id)s |
   +----------------------------------+-----------+--------------+--------------+---------+-----------+-------------------------------------------------+

Usage
-----

To access using the swift protocol, users can use the ``openstack``
client.

Create a Swift container using command:

::

   openstack container create foo

Sample output:

::

   +---------------------------------------+-----------+--------------------------------------------------+
   | account                               | container | x-trans-id                                       |
   +---------------------------------------+-----------+--------------------------------------------------+
   | AUTH_75a27eb3202d4fcda251647d1d78af2c | foo       | tx0000045042a8694f86bc4-0066877b39-121b1-default |
   +---------------------------------------+-----------+--------------------------------------------------+ 

List containers using command:

::

   openstack container list

Sample output:

::

   +------+
   | Name |
   +------+
   | foo  |
   +------+

Upload an object in the container using command:

::

   openstack object create foo test.txt --name test

Sample output:

::

   +--------+-----------+----------------------------------+
   | object | container | etag                             |
   +--------+-----------+----------------------------------+
   | test   | foo       | d8e8fca2dc0f896fd7cb4cb0031ba249 |
   +--------+-----------+----------------------------------+

List the objects in the container using command:

::

   openstack object list foo

Sample output:

::

   +------+
   | Name |
   +------+
   | test |
   +------+

Delete an object from container using command:

::

   openstack object delete foo test

Delete a container using command:

::

   openstack container delete foo
