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

Open source migration solution
------------------------------

`sunbeam-migrate`_ is an open source tool that was specifically developed
to facilitate the migration to Sunbeam.

The tool is designed with simplicity and versatility in mind, relying only on
public OpenStack APIs. As such, it can migrate between different OpenStack
distributions and even different releases.

It models resource hierarchies and ownership, which are automatically
handled during the migration process.

Commercial migration solution
-----------------------------

`Coriolis`_ is a commercial solution developed by Cloudbase Solutions that
can be used to migrate virtual machines and other resources between various
types of clouds.

`Coriolis`_ can greatly simplify the migration between Charmed Openstack
and Canonical Openstack, reducing or even completely eliminating downtime.

.. Links

.. _clouds.yaml: https://docs.openstack.org/python-openstackclient/latest/configuration/index.html#clouds-yaml
.. _Charmed Openstack: https://docs.openstack.org/charm-guide/latest/
.. _Coriolis: https://cloudbase.it/coriolis/
.. _sunbeam-migrate: https://sunbeam-migrate.readthedocs.io/en/latest/
