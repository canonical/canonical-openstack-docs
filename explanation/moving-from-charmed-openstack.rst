Moving from Charmed Openstack
=============================

`Charmed Openstack`_ is the name of the previous solution that allowed
deploying and managing Openstack clouds using Juju charms.

It has been redesigned from scratch and evolved into what is now Canonical
Openstack (Sunbeam).

Since Charmed Openstack will be discontinued, existing users are expected to
migrate to Canonical Openstack. In place upgrades are not possible at the
moment, as such a "lift-and-shift" approach will be used.

Canonical Openstack may be deployed alongside Charmed Openstack, evacuating
compute nodes one by one and adding them to the new deployment.

In the following sections we'll describe the procedure of moving various
Openstack resources.

Identity
--------

Start by redefining identity resources such as domains, projects, users and
roles on the destination cloud. Application credentials and unified limits
may also need to be recreated.

Moving Keystone database entries directly requires compatible database schemas.
Furthermore, it must be handled very carefully in order to avoid overwriting
Canonical Openstack project and service definitions.

Images
------

Use ``openstack image show`` to retrieve the Glance image details such as disk
format, flavor requirements or other custom properties.

The images may be downloaded locally using ``openstack image save --file $path``
and then pushed to the destination cloud through ``openstack image create --file $path``.

For convenience, consider using a `clouds.yaml`_ file containing the credentials
of both source and destination clouds and specify the ``--os-cloud`` parameter
to ``openstack`` commands to select the desired cloud.

Block storage
-------------

Redefine volume types if necessary and pay attention to the existing extra specs.

The backend agnostic approach of migrating Cinder volumes between clouds
consists in:

* upload the volume to Glance: ``openstack image create --volume $volumeID``
* download the image: ``openstack image save --file $path``
* upload the image to the new cloud: ``openstack image create --file $path``
* recreate the volume on the destination: ``openstack volume create --image $image``

At the time of writing, Ceph is the only Cinder backend supported by Canonical
Openstack. With external storage such as a SAN, it may be possible to simply
import the volumes on the target cloud, without performing data migrations.

The ``os-brick`` library may also be used to attach the source and target
volumes locally and then perform the data transfer, thus avoiding the need
to upload images to Glance. However, this is outside the scope of this document.

Network resources
-----------------

Before being able to migrate instances, the following network resources need
to be recreated:

* networks
* subnets
* routers
* security groups
* load balancers
* manually created ports
* floating IPs

When creating ports, fixed IPs and MAC addresses may be explicitly requested
if required by the workload.

Compute instances
-----------------

The compute instances are among the last resources to be moved. Migrate all
the necessary images, networks, volumes and projects first. Recreate
Nova flavors if needed.

If the instance state is not important, simply recreate the instances on
the target cloud using the same specifications (image, network, volumes,
security groups, etc).

To preserve the previous state, start by uploading the instance to Glance
using `openstack server image create`. Download the image locally and then
push it to the destination cloud. Make sure to pass all the original image
properties.

Commercial migration solutions
------------------------------

`Coriolis`_ is a commercial solution developed by Cloudbase Solutions that
can be used to migrate virtual machines and other resources between various
types of clouds.

`Coriolis`_ can greatly simplify the migration between Charmed Openstack
and Canonical Openstack, reducing or even completely eliminating downtime.

.. Links

.. _clouds.yaml: https://docs.openstack.org/python-openstackclient/latest/configuration/index.html#clouds-yaml
.. _Charmed Openstack: https://docs.openstack.org/charm-guide/latest/
.. _Coriolis: https://cloudbase.it/coriolis/
