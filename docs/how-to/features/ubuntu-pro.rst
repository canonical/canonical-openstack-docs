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

The feature deploys the ``ubuntu-pro`` charm to every machine in the
deployment. Release 2026.1.0 deployed the ``ubuntu-advantage`` charm instead.
To move a deployment from ``ubuntu-advantage`` to ``ubuntu-pro`` when you
upgrade to 2026.1.1, see :ref:`ubuntu-pro-move-charm`.

Enabling Ubuntu Pro
-------------------

To enable Ubuntu Pro support, run the following command with an
attachment token associated with your subscription:

::

   sunbeam enable pro <pro token>

The command deploys the ``ubuntu-pro`` charm and attaches every machine to the
subscription. It fails if a machine cannot attach, for example because the
token is not valid, and shows the error returned by the ``pro attach``
command. Run ``sunbeam enable pro`` again with a valid token, or disable Ubuntu
Pro.

Disabling Ubuntu Pro
--------------------

To disable Ubuntu Pro support, run the following command:

::

   sunbeam disable pro

The command first detaches every machine from the Ubuntu Pro subscription,
then removes the ``ubuntu-pro`` application. Detaching disables the Ubuntu Pro
services on each machine, such as Livepatch and the ESM repositories.

.. _ubuntu-pro-disable-failed:

If disabling fails
~~~~~~~~~~~~~~~~~~

If a machine does not detach within ten minutes, the command fails and keeps
the ``ubuntu-pro`` application. The error names the units that did not detach
and their status, for example:

::

   Error: Timed out after 600 seconds waiting for ubuntu-pro units: ubuntu-pro/3
   (unknown: agent lost, see 'juju show-status-log ubuntu-pro/3'). ubuntu-pro was
   not removed.

The token stays empty, so no machine is attached to the subscription again
unless you run ``sunbeam enable pro``. Depending on the status of each unit listed, do one of
the following:

* **The Juju agent is down** (``agent lost``): start the agent again, for
  example by bringing the machine back online. The unit then detaches the
  machine. Run ``sunbeam disable pro`` again.

* **The unit is in error** (``hook failed: "config-changed"``): fix the cause
  shown in ``juju debug-log -m openstack-machines --include <unit>``. Then
  retry the failed hook with ``juju resolve``, which detaches the machine, and
  run ``sunbeam disable pro`` again:

  ::

     juju resolve -m openstack-machines <unit>
     sunbeam disable pro

* **The cause cannot be fixed**: detach the machine manually, remove the
  application with Juju, and run ``sunbeam disable pro`` again to finish the
  removal. On each machine listed, run:

  ::

     sudo pro detach --assume-yes

  Then, from the Sunbeam client node:

  ::

     juju remove-application -m openstack-machines ubuntu-pro --force --no-wait
     sunbeam disable pro

To keep Ubuntu Pro instead, run ``sunbeam enable pro <pro token>``. The
command attaches the detached machines to the subscription again.

.. _ubuntu-pro-move-charm:

Moving from the ubuntu-advantage charm
--------------------------------------

Deployments that enabled Ubuntu Pro on 2026.1.0 run the ``ubuntu-advantage``
charm. When you upgrade to 2026.1.1, there is no in-place upgrade from
``ubuntu-advantage`` to ``ubuntu-pro``. Refreshing the ``openstack`` snap leaves the
``ubuntu-advantage`` charm in place, and ``sunbeam cluster refresh`` only
refreshes it to the latest revision in its current channel.

To check which charm a deployment runs:

::

   juju status -m openstack-machines ubuntu-pro --format json | jq -r '.applications["ubuntu-pro"]["charm-name"]'

.. warning::
   Do not run ``sunbeam enable pro`` on a deployment that still runs
   ``ubuntu-advantage`` without disabling Ubuntu Pro first. The command
   replaces the charm, but it does not detach the machines, and it does not
   relate the new ``ubuntu-pro`` application to them. The machines stay
   attached to the Ubuntu Pro subscription with no charm managing them, and
   the ``ubuntu-pro`` application has no units and an ``unknown`` status.

   To recover, run ``sunbeam enable pro <pro token>`` again. The second run
   relates the application to the machines, and the ``ubuntu-pro`` charm
   takes over their attachment. Then check the units as in the last step
   below.

If the output is ``ubuntu-advantage``, move to the ``ubuntu-pro`` charm by
disabling Ubuntu Pro and enabling it again, in this order:

#. Refresh the ``openstack`` snap to 2026.1.1, as described in
   :doc:`Cluster upgrades </how-to/operations/cluster-upgrades>`. Disabling
   Ubuntu Pro with an older snap removes the charm without detaching the
   machines.

#. Disable Ubuntu Pro:

   ::

      sunbeam disable pro

   If the command fails, see :ref:`ubuntu-pro-disable-failed`.

#. Check that each machine is detached from the subscription. On every node,
   the following command returns ``false``:

   ::

      sudo pro status --format json | jq .attached

#. Enable Ubuntu Pro again with your token:

   ::

      sunbeam enable pro <pro token>

#. Check that the deployment now runs the ``ubuntu-pro`` charm, using the
   command above, and that every node has an ``ubuntu-pro`` unit in the
   ``active`` status:

   ::

      juju status -m openstack-machines ubuntu-pro --relations

   Also check that ``pro status`` shows the expected services on every node.

.. note::
   Between the disable and enable steps, the machines have no Ubuntu Pro
   services: Livepatch is disabled and the ESM repositories are removed. Plan
   the change for a maintenance window and run the enable step straight after
   the disable step.

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
