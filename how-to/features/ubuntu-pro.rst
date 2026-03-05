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
