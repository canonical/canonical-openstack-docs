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
     - On existing deployments, when a control node becomes unavailable, API
       requests may fail intermittently for up to 5 minutes. Starting from
       **rev998**, new deployments reduce this window to 60 seconds. Existing
       clusters will continue to have this issue due to a `k8s charm limitation
       <https://charmhub.io/k8s/configurations#kube-apiserver-extra-args>`_
       because the k8s charm only applies ``kube-apiserver-extra-args`` at
       bootstrap.