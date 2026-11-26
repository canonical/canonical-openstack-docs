Ubuntu Pro
==========

Overview
--------

This feature enables `Ubuntu Pro <https://ubuntu.com/pro>`__ support for
Canonical OpenStack. Ubuntu Pro provides additional benefits such as Livepatch
and extended security support periods for Ubuntu LTS.

Ubuntu Pro is free for `limited personal
usage <https://ubuntu.com/pro/dashboard>`__ or subscriptions can be
`purchased for commercial support <https://ubuntu.com/pro/subscribe>`__.

Enabling Ubuntu Pro
-------------------

To enable Ubuntu Pro support, run the following command with an
attachment token associated with your subscription:

::

   sunbeam enable pro <pro token>

Disabling Ubuntu Pro
--------------------

To disable Ubuntu Pro support, run the following command:

::

   sunbeam disable pro

.. _ubuntu-pro-move-from-ubuntu-advantage:

Moving from the ubuntu-advantage charm
--------------------------------------

Earlier versions of Canonical OpenStack deploy Ubuntu Pro support with the
``ubuntu-advantage`` charm. This charm is deprecated, and current versions
deploy the ``ubuntu-pro`` charm instead. Both use the Juju application name
``ubuntu-pro``.

There is no in-place upgrade from ``ubuntu-advantage`` to ``ubuntu-pro``.
Refreshing the ``openstack`` snap and running ``sunbeam cluster refresh`` keeps
the existing ``ubuntu-advantage`` charm. To move to the ``ubuntu-pro`` charm,
disable the feature and then enable it again.

To check which charm is deployed, run:

::

   juju status -m openstack-machines ubuntu-pro

The ``Charm`` column shows ``ubuntu-advantage`` or ``ubuntu-pro``.

If it shows ``ubuntu-advantage``, first refresh the ``openstack`` snap to the
new version. Then disable the feature:

::

   sunbeam disable pro

This command detaches every machine from the Ubuntu Pro subscription before it
removes the application. Then enable the feature again with your token:

::

   sunbeam enable pro <pro token>

If a manifest sets options for this feature under the ``ubuntu-advantage``
charm key, rename the key to ``ubuntu-pro`` before you run these commands.

.. warning::

   Do not run ``sunbeam enable pro`` again without disabling the feature
   first. The command replaces the application but does not relate the new
   one to the machines, so no ``ubuntu-pro`` units are deployed, and the
   command still reports success.

Between ``sunbeam disable pro`` and ``sunbeam enable pro``, the machines are
not attached to Ubuntu Pro, so services such as ESM and Livepatch are not
active.

Usage
-----

To check the Ubuntu Pro status on any node in the Canonical OpenStack
deployment login to the node and use the ``pro`` command to validate the
subscription attachment and enabled services:

::

   pro status

Example output is:

::

   SERVICE          ENTITLED  STATUS    DESCRIPTION
   esm-apps         yes       enabled   Expanded Security Maintenance for Applications
   esm-infra        yes       enabled   Expanded Security Maintenance for Infrastructure
   livepatch        yes       disabled  Canonical Livepatch service
   realtime-kernel* yes       disabled  Ubuntu kernel with PREEMPT_RT patches integrated
   usg              yes       disabled  Security compliance and audit tools

    * Service has variants

   For a list of all Ubuntu Pro services and variants, run 'pro status --all'
   Enable services with: pro enable <service>

        Account: microstack@ubuntu.com
   Subscription: Ubuntu Pro - free personal subscription
