Multi-region deployments
========================

OpenStack deployments can span across multiple regions while sharing only the
identity (Keystone) and dashboard (Horizon) services.

Commonly used with large deployments, the OpenStack region concept is
quite flexible. These may be geographically distinct locations, providing
regional level fault tolerance.

Alternatively, regions can exist within the same physical site, used to
partition a large cluster and distribute load among critical components like
databases or message brokers.

Region controllers
------------------

To accommodate multi-region environments, Canonical OpenStack defines the
region controller role, which is mutually exclusive with all other roles.

Region controllers will only run the shared services, such as Keystone and
Horizon.

In local mode, a region controller may be bootstrapped like so:

::

	sunbeam cluster bootstrap --role region_controller

For high availability, additional region controllers can be added using
the standard procedure. First, obtain a cluster join token:

::

	sunbeam cluster add $fqdn

Then use the token to join the new region controller node:

::

	sunbeam cluster join --role region_controller $token

Secondary regions
-----------------

The secondary regions are distinct Canonical Openstack deployments, using
separate Kubernetes clusters and Juju controllers.

Shared services such as Keystone and Horizon will be omitted from secondary
regions. These services will be provided by the region controllers and
consumed through cross-controller Juju relations.

In order to access the region controller, each secondary region node will
need a token obtained from the region controllers:

::

	sunbeam cluster add-secondary-region-node $fqdn

The token must then be passed to the bootstrap command:

::

	sunbeam cluster bootstrap \
    	--role control,compute,storage --region-controller-token=$token

During bootstrap, make sure to specify a region name other than the one of the
region controller.

A region controller token is also required when joining secondary region nodes.
This means that the join operation requires two tokens: one from the region
controller and one from an existing member of the secondary region.

::

	sunbeam --verbose cluster join --role control,compute,storage \
    	--region-controller-token $region_ctrl_token $same_region_token

Juju cross-controller relations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For the time being, the Juju Terraform provider does not support
`cross-controller relations`_. As such, these relations must be manually
defined.

::

	controller="sunbeam-controller-region-controller"
	# Usually the region controller fqdn
	owner="$ownerFqdn"

	# Run the following when Sunbeam reaches the following phase:
	# ⠼ Deploying OpenStack Control Plane to Kubernetes (this may take a while) ... waiting for services to come online (14/18)
	juju switch openstack

	juju consume $controller:$owner/openstack.keystone-credentials
	juju consume $controller:$owner/openstack.keystone-endpoints
	juju consume $controller:$owner/openstack.keystone-ops
	juju consume $controller:$owner/openstack.cert-distributor

	juju integrate keystone-endpoints cinder:identity-service
	juju integrate keystone-endpoints glance:identity-service
	juju integrate keystone-endpoints neutron:identity-service
	juju integrate keystone-endpoints nova:identity-service
	juju integrate keystone-endpoints placement:identity-service

	# Run the following once Sunbeam reaches the following phase:
	# ⠸ Deploying OpenStack Hypervisor ...
	juju switch admin/openstack-machines

	juju consume $controller:$owner/openstack.keystone-credentials
	juju integrate keystone-credentials openstack-hypervisor:identity-credentials


.. Links

.. _cross-controller relations: https://github.com/juju/terraform-provider-juju/issues/805
