:orphan:

Containers as a Service
=======================

This feature deploys `Magnum`_, the OpenStack CaaS service.

Enabling CaaS
-------------

To enable CaaS, run the following command:

::

   sunbeam enable caas

Use the OpenStack CLI to manage container infrastructures. See the
upstream `Magnum`_ documentation for details.

.. note::
   The :doc:`secrets` and :doc:`orchestration` features are dependencies of the CaaS
   feature. Make sure to enable them.

When using the CaaS feature in conjunction with the :doc:`load-balancer` feature, you
are subject to the same limitations as the latter feature. In particular, the OVN provider
only supports the ``SOURCE_IP_PORT`` load balancing algorithm.

Configuring CaaS
----------------

To configure the cloud for CaaS usage, run the following command:

::

   sunbeam configure caas

Disabling CaaS
--------------

To disable CaaS, run the following command:

::

   sunbeam disable caas

Usage
-----

Create a cluster template using the following command:

::

   openstack coe cluster template \
      create k8s-cluster-template-ovn \
      --image fedora-coreos-38 \
      --keypair sunbeam \
      --external-network external-network \
      --flavor m1.small \
      --docker-volume-size 15 \
      --master-lb-enabled \
      --labels octavia_provider=ovn \
      --labels octavia_lb_algorithm=SOURCE_IP_PORT \
      --network-driver flannel \
      --coe kubernetes

Sample output:

.. terminal::
   :user: ubuntu
   :host: sunbeam01
   :dir: ~
   :input: openstack coe cluster template
      create k8s-cluster-template-ovn
      --image fedora-coreos-38
      --keypair sunbeam
      --external-network external-network
      --flavor m1.small
      --docker-volume-size 15
      --master-lb-enabled
      --labels octavia_provider=ovn
      --labels octavia_lb_algorithm=SOURCE_IP_PORT
      --network-driver flannel
      --coe kubernetes


   Request to create cluster template k8s-cluster-template-ovn accepted
   +-----------------------+-----------------------------------------------------------------------+
   | Field                 | Value                                                                 |
   +-----------------------+-----------------------------------------------------------------------+
   | insecure_registry     | -                                                                     |
   | labels                | {'octavia_provider': 'ovn', 'octavia_lb_algorithm': 'SOURCE_IP_PORT'} |
   | updated_at            | -                                                                     |
   | floating_ip_enabled   | True                                                                  |
   | fixed_subnet          | -                                                                     |
   | master_flavor_id      | -                                                                     |
   | uuid                  | 4d675c2b-c4e6-4877-a949-987195125fbc                                  |
   | no_proxy              | -                                                                     |
   | https_proxy           | -                                                                     |
   | tls_disabled          | False                                                                 |
   | keypair_id            | sunbeam                                                               |
   | public                | False                                                                 |
   | http_proxy            | -                                                                     |
   | docker_volume_size    | 15                                                                    |
   | server_type           | vm                                                                    |
   | external_network_id   | external-network                                                      |
   | cluster_distro        | fedora-coreos                                                         |
   | image_id              | fedora-coreos-38                                                      |
   | volume_driver         | -                                                                     |
   | registry_enabled      | False                                                                 |
   | docker_storage_driver | overlay2                                                              |
   | apiserver_port        | -                                                                     |
   | name                  | k8s-cluster-template-ovn                                              |
   | created_at            | 2023-10-16T09:45:24.751362+00:00                                      |
   | network_driver        | flannel                                                               |
   | fixed_network         | -                                                                     |
   | coe                   | kubernetes                                                            |
   | flavor_id             | m1.small                                                              |
   | master_lb_enabled     | True                                                                  |
   | dns_nameserver        | 8.8.8.8                                                               |
   | hidden                | False                                                                 |
   | tags                  | -                                                                     |
   +-----------------------+-----------------------------------------------------------------------+

Create a Kubernetes cluster using the following command:

::

   openstack coe cluster create --cluster-template k8s-cluster-template-ovn --node-count 1 --timeout 60 sunbeam-k8s-ovn

Sample output:

::

   Request to create cluster 27eba31c-66a5-4efe-8373-49dd186567e6 accepted

Check cluster list status using the following command:

::

   openstack coe cluster list

   +--------------------------------------+-----------------+---------+------------+--------------+-----------------+---------------+
   | uuid                                 | name            | keypair | node_count | master_count | status          | health_status |
   +--------------------------------------+-----------------+---------+------------+--------------+-----------------+---------------+
   | 27eba31c-66a5-4efe-8373-49dd186567e6 | sunbeam-k8s-ovn | sunbeam |          1 |            1 | CREATE_COMPLETE | HEALTHY       |
   +--------------------------------------+-----------------+---------+------------+--------------+-----------------+---------------+

.. note::
   You may need to wait a few minutes before the cluster is ready.

Check cluster status using the following command:

::

   openstack coe cluster show sunbeam-k8s-ovn

   +----------------------+---------------------------------------------------------------------------------------------------------------------------+
   | Field                | Value                                                                                                                     |
   +----------------------+---------------------------------------------------------------------------------------------------------------------------+
   | status               | CREATE_COMPLETE                                                                                                           |
   | health_status        | HEALTHY                                                                                                                   |
   | cluster_template_id  | 4d675c2b-c4e6-4877-a949-987195125fbc                                                                                      |
   | node_addresses       | ['10.20.20.227']                                                                                                          |
   | uuid                 | 27eba31c-66a5-4efe-8373-49dd186567e6                                                                                      |
   | stack_id             | a4221337-395e-4328-a878-de3f08a29bb2                                                                                      |
   | status_reason        | None                                                                                                                      |
   | created_at           | 2023-10-16T11:11:37+00:00                                                                                                 |
   | updated_at           | 2023-10-16T11:18:24+00:00                                                                                                 |
   | coe_version          | v1.18.16                                                                                                                  |
   | labels               | {'octavia_provider': 'ovn', 'octavia_lb_algorithm': 'SOURCE_IP_PORT'}                                                     |
   | labels_overridden    | {}                                                                                                                        |
   | labels_skipped       | {}                                                                                                                        |
   | labels_added         | {}                                                                                                                        |
   | fixed_network        | None                                                                                                                      |
   | fixed_subnet         | None                                                                                                                      |
   | floating_ip_enabled  | True                                                                                                                      |
   | faults               |                                                                                                                           |
   | keypair              | sunbeam                                                                                                                   |
   | api_address          | https://10.20.20.215:6443                                                                                                 |
   | master_addresses     | ['10.20.20.52']                                                                                                           |
   | master_lb_enabled    | True                                                                                                                      |
   | create_timeout       | 60                                                                                                                        |
   | node_count           | 1                                                                                                                         |
   | discovery_url        | https://discovery.etcd.io/e98c17817a572118135f4cfa60397792                                                                |
   | docker_volume_size   | 15                                                                                                                        |
   | master_count         | 1                                                                                                                         |
   | container_version    | 1.12.6                                                                                                                    |
   | name                 | sunbeam-k8s-ovn                                                                                                           |
   | master_flavor_id     | None                                                                                                                      |
   | flavor_id            | m1.small                                                                                                                  |
   | health_status_reason | {'sunbeam-k8s-ovn-fvwzbaayuols-master-0.Ready': 'True', 'sunbeam-k8s-ovn-fvwzbaayuols-node-0.Ready': 'True', 'api': 'ok'} |
   | project_id           | cf669675a9784b84805a5aa42afb21fe                                                                                          |
   +----------------------+---------------------------------------------------------------------------------------------------------------------------+

Access your Kubernetes cluster using the following commands:

::

   mkdir config-dir
   openstack coe cluster config sunbeam-k8s-ovn --dir config-dir/
   export KUBECONFIG=/home/ubuntu/config-dir/config
   kubectl get pods -A

   NAMESPACE     NAME                                         READY   STATUS    RESTARTS   AGE
   kube-system   coredns-56448757b9-km7qj                     1/1     Running   0          4m43s
   kube-system   coredns-56448757b9-w46cq                     1/1     Running   0          4m43s
   kube-system   dashboard-metrics-scraper-67f57ff746-6phd6   1/1     Running   0          4m40s
   kube-system   k8s-keystone-auth-4sqx8                      1/1     Running   0          4m39s
   kube-system   kube-dns-autoscaler-6d5b5dc777-wbt4w         1/1     Running   0          4m42s
   kube-system   kube-flannel-ds-c8dqt                        1/1     Running   0          2m44s
   kube-system   kube-flannel-ds-t5kc8                        1/1     Running   0          4m42s
   kube-system   kubernetes-dashboard-7b88d986b4-2qgm5        1/1     Running   0          4m40s
   kube-system   magnum-metrics-server-6c4c77844b-p2ws4       1/1     Running   0          4m34s
   kube-system   npd-h7xsg                                    1/1     Running   0          2m23s
   kube-system   openstack-cloud-controller-manager-j8l4l     1/1     Running   0          4m43s
