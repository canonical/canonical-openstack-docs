Using an existing Juju controller
=================================

Canonical OpenStack can use an existing Juju controller during bootstrap
instead of deploying a Juju controller within the Canonical OpenStack
deployment.

This allows operators to make use of an existing Juju controller that
could be used to control many Juju deployments of different types of
services - including multiple Canonical OpenStack deployments!

Register the Juju controller
----------------------------

:doc:`Register an existing Juju controller </how-to/misc/manage-external-juju-controllers>`
in Sunbeam.

.. note::
   Ensure a dedicated user is created in the external Juju controller and has
   ``superuser`` permissions granted on this controller.

Bootstrap with registered Juju controller
-----------------------------------------

Use the option ``--controller`` with the bootstrap command to make use
of the previously registered Juju controller.

In local mode the roles for the machine still need to be provided during
bootstrap:

::

   sunbeam cluster bootstrap --role compute,storage,control \
       --accept-defaults --controller prod-controller-01

In MAAS mode the roles are determined by tags on the machines being
deployed, so the roles option is not used:

::

   sunbeam cluster bootstrap --controller prod-controller-01

Example external Juju configuration
-----------------------------------

An external Juju controller can be bootstrapped on top of a LXD cluster, for example, running
across the same machines that are used in the Canonical OpenStack deployment.

Please refer to the :doc:`Bootstrap highly available Juju controller on top of a LXD cluster </how-to/misc/bootstrap-highly-available-juju-controller-on-top-of-a-lxd-cluster>` section of this documentation for a detailed procedure on how to accomplish this goal.
