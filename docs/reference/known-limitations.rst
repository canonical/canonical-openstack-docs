.. _Known limitations:

Known limitations
=================

This document describes the known limitations of the Sunbeam project.


.. list-table::
   :widths: 20 15 55
   :header-rows: 1

   * - Issue
     - Bug Number
     - Meaning
   * - Intermittent API failures when a control node is down on existing deployments
     - | `LP #2150551 <https://bugs.launchpad.net/snap-openstack/+bug/2150551>`_
       | `k8s-operator #930 <https://github.com/canonical/k8s-operator/issues/930>`_
     - Clusters bootstrapped with ``snap-openstack`` versions earlier than 
       **rev998** will continue to experience intermittent API failures (for up 
       to 5 minutes) when a control node becomes unavailable. A known 
       `k8s charm limitation <https://charmhub.io/k8s/configurations#kube-apiserver-extra-args>`_ 
       restricts updates on active deployments, meaning this issue cannot be 
       fixed on clusters deployed prior to this revision.