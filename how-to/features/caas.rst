Containers as a Service
=======================

This feature deploys `Magnum`_, the OpenStack CaaS service. Only
`Magnum CAPI Helm driver <https://docs.openstack.org/magnum-capi-helm/latest/>`_ is supported.
This feature enables user to deploy `Canonical Kubernetes`_ on OpenStack infrastructure.

Enabling CaaS
-------------

To enable CaaS, run the following command:

.. literalinclude:: ../snippets/caas.task.sh
   :language: bash
   :start-after: [docs-view:enable-caas]
   :end-before:  [docs-view:enable-caas-end]

Use the OpenStack CLI to manage container infrastructures. See the
upstream `Magnum`_ documentation for details.

.. note::
   The :doc:`secrets` and :doc:`load-balancer` features are dependencies of the CaaS
   feature. Make sure to enable them.

When using the CaaS feature in conjunction with the :doc:`load-balancer` feature, you
are subject to the same limitations as the latter feature. In particular, the OVN provider
only supports the ``SOURCE_IP_PORT`` load balancing algorithm.

Disabling CaaS
--------------

To disable CaaS, run the following command:

.. literalinclude:: ../snippets/caas.task.sh
   :language: bash
   :start-after: [docs-view:disable-caas]
   :end-before:  [docs-view:disable-caas-end]

Usage
-----

Pre-requisites
~~~~~~~~~~~~~~

1. Set the following properties on the image that will be used to deploy instances

   * os-distro to ubuntu
   * kube-version to workload cluster kubernetes version

::

   openstack image set IMAGE --os-distro ubuntu --property kube_version=v1.32.8

2. Ensure to add role `member` and `load-balancer_member` to the user as specified in
   :doc:`load-balancer`

Create a kubernetes cluster
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a cluster template using the following command:

::

   openstack coe cluster template \
      create ck8s-cluster-template-ovn \
      --image ubuntu \
      --external-network external-network \
      --flavor m1.medium \
      --master-flavor m1.medium \
      --master-lb-enabled \
      --labels octavia_provider=ovn \
      --labels octavia_lb_algorithm=SOURCE_IP_PORT \
      --network-driver cilium \
      --coe kubernetes

Sample output:

.. terminal::
   :user: ubuntu
   :host: sunbeam01
   :dir: ~
   :input: openstack coe cluster template
      create ck8s-cluster-template-ovn \
      --image ubuntu \
      --external-network external-network \
      --flavor m1.medium \
      --master-flavor m1.medium \
      --master-lb-enabled \
      --labels octavia_provider=ovn \
      --labels octavia_lb_algorithm=SOURCE_IP_PORT \
      --network-driver cilium \
      --coe kubernetes

   Request to create cluster template ck8s-cluster-template-ovn accepted
   +-----------------------+-----------------------------------------------------------------------+
   | Field                 | Value                                                                 |
   +-----------------------+-----------------------------------------------------------------------+
   | insecure_registry     | -                                                                     |
   | labels                | {'octavia_provider': 'ovn', 'octavia_lb_algorithm': 'SOURCE_IP_PORT'} |
   | updated_at            | -                                                                     |
   | floating_ip_enabled   | True                                                                  |
   | fixed_subnet          | -                                                                     |
   | master_flavor_id      | m1.medium                                                             |
   | uuid                  | 1a3550d1-f493-449e-804f-7e1010cb1cf1                                  |
   | no_proxy              | -                                                                     |
   | https_proxy           | -                                                                     |
   | tls_disabled          | False                                                                 |
   | keypair_id            | -                                                                     |
   | public                | False                                                                 |
   | http_proxy            | -                                                                     |
   | docker_volume_size    | -                                                                     |
   | server_type           | vm                                                                    |
   | external_network_id   | external-network                                                      |
   | cluster_distro        | ubuntu                                                                |
   | image_id              | ubuntu                                                                |
   | volume_driver         | -                                                                     |
   | registry_enabled      | False                                                                 |
   | docker_storage_driver | overlay2                                                              |
   | apiserver_port        | -                                                                     |
   | name                  | ck8s-cluster-template-ovn                                             |
   | created_at            | 2025-09-25T05:04:00.227248+00:00                                      |
   | network_driver        | cilium                                                                |
   | fixed_network         | -                                                                     |
   | coe                   | kubernetes                                                            |
   | flavor_id             | m1.medium                                                             |
   | master_lb_enabled     | True                                                                  |
   | dns_nameserver        | 8.8.8.8                                                               |
   | project_id            | 82c3eedc4a3646ef8777cf0d17a3ab32                                      |
   | hidden                | False                                                                 |
   | tags                  | -                                                                     |
   +-----------------------+-----------------------------------------------------------------------+

Create a Kubernetes cluster using the following command:

::

   openstack coe cluster create --cluster-template CLUSTER_TEMPLATE_UUID --master-count 3 --node-count 3 --timeout 900 sunbeam-ck8s-ovn

Sample output:

::

   Request to create cluster fc5724ae-aef8-4c89-aef8-78bc41f54325 accepted

Check cluster list status using the following command:

::

   openstack coe cluster list

   +--------------------------------------+------------------+---------+------------+--------------+-----------------+---------------+
   | uuid                                 | name             | keypair | node_count | master_count | status          | health_status |
   +--------------------------------------+------------------+---------+------------+--------------+-----------------+---------------+
   | fc5724ae-aef8-4c89-aef8-78bc41f54325 | sunbeam-ck8s-ovn | None    |          3 |            3 | CREATE_COMPLETE | HEALTHY       |
   +--------------------------------------+------------------+---------+------------+--------------+-----------------+---------------+

.. note::
   You may need to wait a few minutes before the cluster is ready.

Check cluster status using the following command:

::

   openstack coe cluster show CLUSTER_UUID

   +----------------------+------------------------------------------------------------------------------------------------+
   | Field                | Value                                                                                          |
   +----------------------+------------------------------------------------------------------------------------------------+
   | status               | CREATE_COMPLETE                                                                                |
   | health_status        | HEALTHY                                                                                        |
   | cluster_template_id  | 1a3550d1-f493-449e-804f-7e1010cb1cf1                                                           |
   | node_addresses       | []                                                                                             |
   | uuid                 | fc5724ae-aef8-4c89-aef8-78bc41f54325                                                           |
   | stack_id             | sunbeam-ck8s-ovn-sei7c6sxbikj                                                                  |
   | status_reason        | None                                                                                           |
   | created_at           | 2025-09-25T05:18:52+00:00                                                                      |
   | updated_at           | 2025-09-25T05:28:52+00:00                                                                      |
   | coe_version          | v1.32.8                                                                                        |
   | labels               | {'octavia_provider': 'ovn', 'octavia_lb_algorithm': 'SOURCE_IP_PORT'}                          |
   | labels_overridden    | {}                                                                                             |
   | labels_skipped       | {}                                                                                             |
   | labels_added         | {}                                                                                             |
   | fixed_network        | None                                                                                           |
   | fixed_subnet         | None                                                                                           |
   | floating_ip_enabled  | True                                                                                           |
   | faults               |                                                                                                |
   | keypair              | None                                                                                           |
   | api_address          | https://172.16.2.247:6443                                                                      |
   | master_addresses     | []                                                                                             |
   | master_lb_enabled    | True                                                                                           |
   | create_timeout       | 900                                                                                            |
   | node_count           | 3                                                                                              |
   | discovery_url        | None                                                                                           |
   | docker_volume_size   | None                                                                                           |
   | master_count         | 3                                                                                              |
   | container_version    | None                                                                                           |
   | name                 | sunbeam-ck8s-ovn                                                                               |
   | master_flavor_id     | m1.medium                                                                                      |
   | flavor_id            | m1.medium                                                                                      |
   | health_status_reason | {'cluster': 'Ready', 'infrastructure': 'Ready', 'controlplane': 'Ready', 'nodegroup': 'Ready'} |
   | project_id           | 82c3eedc4a3646ef8777cf0d17a3ab32                                                               |
   +----------------------+------------------------------------------------------------------------------------------------+

Access your Kubernetes cluster using the following commands:

::

   mkdir config-dir
   openstack coe cluster config sunbeam-k8s-ovn --dir config-dir/
   export KUBECONFIG=/home/ubuntu/config-dir/config
   sudo -E k8s kubectl get pods -A

   NAMESPACE              NAME                                                              READY   STATUS    RESTARTS   AGE
   kube-system            cilium-7c98r                                                      1/1     Running   0          21m
   kube-system            cilium-lk2w9                                                      1/1     Running   0          21m
   kube-system            cilium-operator-6fb79c547b-h8ds7                                  1/1     Running   0          24m
   kube-system            cilium-p5wz7                                                      1/1     Running   0          24m
   kube-system            cilium-pmcj8                                                      1/1     Running   0          19m
   kube-system            cilium-tz5sj                                                      1/1     Running   0          21m
   kube-system            cilium-vs6m5                                                      1/1     Running   0          21m
   kube-system            ck-storage-rawfile-csi-controller-0                               2/2     Running   0          25m
   kube-system            ck-storage-rawfile-csi-node-6bn6l                                 4/4     Running   0          21m
   kube-system            ck-storage-rawfile-csi-node-7gndg                                 4/4     Running   0          21m
   kube-system            ck-storage-rawfile-csi-node-cjgtk                                 4/4     Running   0          21m
   kube-system            ck-storage-rawfile-csi-node-fl8fs                                 4/4     Running   0          25m
   kube-system            ck-storage-rawfile-csi-node-hc4pj                                 4/4     Running   0          19m
   kube-system            ck-storage-rawfile-csi-node-zrn5z                                 4/4     Running   0          21m
   kube-system            coredns-fc9c778db-fzrdf                                           1/1     Running   0          25m
   kube-system            k8sd-proxy-g7xvc                                                  1/1     Running   0          20m
   kube-system            k8sd-proxy-jqxp5                                                  1/1     Running   0          20m
   kube-system            k8sd-proxy-k7bv2                                                  1/1     Running   0          18m
   kube-system            k8sd-proxy-qwzr2                                                  1/1     Running   0          20m
   kube-system            k8sd-proxy-v2jqt                                                  1/1     Running   0          23m
   kube-system            k8sd-proxy-vv6t2                                                  1/1     Running   0          21m
   kube-system            metrics-server-8694c96fb7-hkfk6                                   1/1     Running   0          25m
   kubernetes-dashboard   kubernetes-dashboard-1758777722-api-574545d7f4-69bcx              1/1     Running   0          24m
   kubernetes-dashboard   kubernetes-dashboard-1758777722-auth-7b949ccdd9-d54tv             1/1     Running   0          24m
   kubernetes-dashboard   kubernetes-dashboard-1758777722-kong-58bc8dc74b-gl5n2             1/1     Running   0          24m
   kubernetes-dashboard   kubernetes-dashboard-1758777722-metrics-scraper-75cd94bbc-2tnq6   1/1     Running   0          24m
   kubernetes-dashboard   kubernetes-dashboard-1758777722-web-5866567c7d-cp6dg              1/1     Running   0          24m
   metallb-system         metallb-controller-7f647445fc-5ztvp                               1/1     Running   0          25m
   metallb-system         metallb-speaker-8jdfv                                             1/1     Running   0          20m
   metallb-system         metallb-speaker-bqwv2                                             1/1     Running   0          18m
   metallb-system         metallb-speaker-gx5j6                                             1/1     Running   0          21m
   metallb-system         metallb-speaker-s2gg9                                             1/1     Running   0          20m
   metallb-system         metallb-speaker-vjfrf                                             1/1     Running   0          20m
   metallb-system         metallb-speaker-zfv27                                             1/1     Running   0          23m
   openstack-system       openstack-cinder-csi-controllerplugin-5944b6858f-6wx82            6/6     Running   0          24m
   openstack-system       openstack-cinder-csi-nodeplugin-2gsb5                             3/3     Running   0          21m
   openstack-system       openstack-cinder-csi-nodeplugin-2m4gb                             3/3     Running   0          19m
   openstack-system       openstack-cinder-csi-nodeplugin-bzvcv                             3/3     Running   0          21m
   openstack-system       openstack-cinder-csi-nodeplugin-cbl9r                             3/3     Running   0          24m
   openstack-system       openstack-cinder-csi-nodeplugin-jnx2z                             3/3     Running   0          21m
   openstack-system       openstack-cinder-csi-nodeplugin-wwhx6                             3/3     Running   0          21m
   openstack-system       openstack-cloud-controller-manager-6w8v2                          1/1     Running   0          20m
   openstack-system       openstack-cloud-controller-manager-sh2zr                          1/1     Running   0          24m
   openstack-system       openstack-cloud-controller-manager-vbnlt                          1/1     Running   0          18m

Currently the command `openstack coe cluster config` is not returning proper kubeconfig.
As a workaround, get the kubeconfig using clusterctl

::

   curl -L https://github.com/kubernetes-sigs/cluster-api/releases/download/v1.10.5/clusterctl-linux-amd64 -o clusterctl
   sudo install -o root -g root -m 0755 clusterctl /usr/local/bin/clusterctl
   sudo k8s config > kubeconfig
   KUBECONFIG=kubeconfig clusterctl get kubeconfig --namespace magnum-<PROJECT_ID> <CLUSTER_STACK_ID> > config-dir/config

Replace PROJECT_ID and CLUSTER_STACK_ID from the output values in `openstack coe cluster show`.


Enable Autoscaling
~~~~~~~~~~~~~~~~~~

To enable Autoscaling feature, the cluster template should have the following labels

::

   --labels auto_scaling_enabled=True
   --labels min_node_count=3
   --labels max_node_count=5

.. note::
   The value for --node-count in `openstack coe cluster create` command should be in the range [min_node_count ... max_node_count]


Enable Keystone authentication and authorization webhook for Workload Kubernetes Cluster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable `Keystone authentication and authorization feature <https://github.com/kubernetes/cloud-provider-openstack/blob/master/docs/keystone-auth/using-keystone-webhook-authenticator-and-authorizer.md>`__, the cluster template should have the following label

::

   --labels keystone_auth_enabled=True

Existing cluster can be upgraded to enable keystone auth by running the following command

.. terminal::
   :user: ubuntu
   :host: sunbeam01
   :dir: ~
   :input: openstack coe cluster upgrade CLUSTER_UUID NEW_CLUSTER_TEMPLATE_UUID

   Request to upgrade cluster fc5724ae-aef8-4c89-aef8-78bc41f54325 has been accepted.

.. note::
   You may need to wait a few minutes before the cluster is ready.

To verify if keystone-auth is enabled or not, run the following command

::

   sudo -E k8s kubectl -n kube-system get po -l app.kubernetes.io/name=k8s-keystone-auth

   NAME                                 READY   STATUS    RESTARTS   AGE
   k8s-keystone-auth-1758780472-7qkbc   1/1     Running   0          7m56s
   k8s-keystone-auth-1758780472-kwlzj   1/1     Running   0          2m46s
   k8s-keystone-auth-1758780472-wprwk   1/1     Running   0          6m21s

The default keystone-k8s auth policy is specified `here <https://github.com/catalyst-cloud/capi-plugin-helm-charts/blob/main/charts/k8s-keystone-auth/values.yaml#L80>`__.
For custom policies, User need to manually update the config map `k8s-keystone-auth-policy`
in kube-system namespace and recycle the k8s-keystone-auth pods.


Setup a Kubernetes cluster in a proxy environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To setup a kubernetes cluster in a proxy environment, set the following parameters
in `openstack coe cluster template create` command

::

    --http-proxy <>
    --https-proxy <>
    --no-proxy <>


Delete a Cluster
~~~~~~~~~~~~~~~~

Delete the kubernetes cluster using the following command:

::

   openstack coe cluster delete CLUSTER_UUID

.. note::
   Cluster deletion fails as ingress is enabled in Canonical Kubernetes CAPI
   deployment but ingress is not supported in Magnum CAPI Helm driver.
   As a workaround, delete the loadbalancer using the following command:
   `openstack loadbalancer delete kube_service_<CLUSTER_STACK_ID>_kube-system_cilium-ingress --cascade`

Limitations:
------------

* Only `Cilium` network driver is supported.
* Enabling monitoring feature via label `monitoring_enabled` is not supported.
* Enabling Registry mirrors is not supported in Magnum CAPI Helm driver.



