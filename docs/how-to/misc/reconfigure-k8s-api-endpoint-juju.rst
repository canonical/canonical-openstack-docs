Reconfigure the Kubernetes API endpoint in Juju
===============================================

Overview
--------

A known limitation of Canonical OpenStack today is that the Juju Controller
(the service responsible for orchestrating the deployment of Canonical
OpenStack) only communicates with a single Kubernetes API address.

Canonical Kubernetes does not setup load balancing in front of the Kubernetes API.
This means that if the node the Juju Controller is communicating with is
removed, Juju will not be able to communicate with the Kubernetes
cluster anymore.

There are plans to setup load balancing and a highly available IP
address to provide more robust access to the Kubernetes API service from
Juju in the future.

If you need the Juju controller to communicate to an alternative
:code:`kube-api` server you can update the endpoint in the Juju controller to
point to a different :code:`kube-api` server.

In the following example the deployment name is ``sbcloud01`` -
controller and cloud names are built from this name.

Pre-requisites
--------------

Ensure that the Juju client is logged in to the Juju controller:

.. code:: bash

   $ sunbeam utils juju-login
   Juju re-login complete.

Create a new cloud configuration
--------------------------------

Create a new cloud configuration file ``sbcloud01-k8s.yaml`` with the
new endpoint address:

.. code:: yaml

   clouds:
     sbcloud01-k8s:
       type: kubernetes
       auth-types: [oauth2, clientcertificate]
       endpoint: https://10.4.2.3:16443 # <- new endpoint
       regions:
         localhost:
           endpoint: https://10.4.2.3:16443 # <- new endpoint

Update the controller cloud configuration
-----------------------------------------

.. code:: bash

   $ juju update-cloud --controller sbcloud01-controller sbcloud01-k8s -f sbcloud01-k8s.yaml
   Cloud "sbcloud01-k8s" updated on controller "sbcloud01-controller" using provided file.

If an incorrect Kubernetes API endpoint is configured error messages
will be present in the ``openstack`` model debug log:

::

   $ juju debug-log -m openstack
