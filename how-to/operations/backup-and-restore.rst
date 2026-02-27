Backup and Restore
==================

Overview
--------

Regular backups of the Sunbeam cluster are a critical component of any robust disaster recovery plan,
ensuring the resilience and continuity of the Canonical OpenStack Cluster deployment. Given that
the procedures described below primarily focus on backing up essential control-plane elements
including application data (MySQL, Vault), the Kubernetes control plane, Juju controller state,
and sunbeam-clusterd.

Unexpected hardware failures, human error, or data corruption can severely compromise the
control plane, leading to extended outages and potential data loss. By maintaining up-to-date
backups, administrators can significantly minimize recovery time objectives (RTO) and restore the
core management services necessary for operating the cloud infrastructure.


s3-integrator
-------------
The Sunbeam cluster, by default, utilizes ceph-rgw within MicroCeph, which provides S3-compatible
object storage capabilities. This built-in functionality can be used to create the S3 buckets
necessary for the backup procedures described here. While this is convenient for initial setup
and testing, it is recommended that for production environments, all critical backups be
stored in an S3-compatible service located outside of the Canonical OpenStack Cluster deployment
itself. Storing backups externally ensures resilience against catastrophic failures that could
affect the entire cloud environment, including the internal Ceph cluster.

For demonstration purposes, the backup procedures outlined in this document will utilize the internal
Ceph Rados Gateway (RGW) provided by the ceph-rgw charm.

.. code-block :: text

    juju switch openstack-machines
    juju exec -u microceph/leader -- microceph.radosgw-admin user create --uid my-user --display-name my-user
    {
        "user_id": "my-user",
        "display_name": "my-user",
        "email": "",
        "suspended": 0,
        "max_buckets": 1000,
        "subusers": [],
        "keys": [
            {
                "user": "my-user",
                "access_key": "<your-access-key>", # save this access key
                "secret_key": "<your-secret-key>", # save this secret key
                "active": true,
                "create_date": "2026-02-26T20:40:18.959341Z"
            }
        ],
    }

    # get the endpoint of the ceph-rgw service on openstack model
    juju switch openstack
    juju run traefik-rgw/leader show-external-endpoints
    Running operation 316 with 1 task
    - task 317 on unit-traefik-rgw-1

    Waiting for task 317...
    external-endpoints: '{"traefik-rgw": {"url": "http://<IP_RGW_SERVICE>"}}'

Install a tool like aws-cli or s3cmd and configure it with the access key and secret key obtained
from the previous command to interact with the S3 storage provided by ceph-rgw.

.. code-block :: text

    sudo snap install aws-cli --classic
    aws configure --profile ceph # fill the asked information
    aws --profile ceph --endpoint-url http:///<IP_RGW_SERVICE> s3api create-bucket --bucket mysql
    ...
    # repeat the previous command to create a bucket for each application you want to backup

Deploy one s3-integrator application for each application that needs s3-integration. E.g:

.. code-block :: text

    juju switch openstack
    juju deploy s3-integrator --model openstack mysql-s3-integrator
    juju relate mysql-s3-integrator mysql
    ...
    # deploy and relate for all necessary apps


Run the sync-s3-credentials action to configure the charm

.. code-block :: text

    juju run mysql-s3-integrator/leader sync-s3-credentials access-key=<ACCESS_KEY> secret-key=<SECRET_KEY>
    ...
    # do the same for all necessary apps

Configure the s3-integrator charm to use the correct bucket for each application
.. code-block :: text

    juju config mysql-s3-integrator bucket=mysql s3-uri-style=path endpoint=http:///<IP_RGW_SERVICE> path=mysql
    ...
    # do the same for all necessary apps

MySQL
-----

Requirements
~~~~~~~~~~~~
* A deployed MySQL K8s cluster
* Access to S3 storage
* Configured settings for S3 storage
* Units in active/idle
* Control-plane units paused to avoid usage of the cluster during **restore** procedure

Backup
~~~~~~
The backup procedure should be executed on secondary MySQL units to avoid impacting the performance
of the primary unit. To get a secondary unit, run the following command:

.. code-block :: text

    juju run mysql/leader get-cluster-status
    Running operation 196 with 1 task
    - task 197 on unit-mysql-2

    Waiting for task 197...
    status:
    clustername: cluster-1e57de179fb5edd8c4e6392a25473b96
    clusterrole: primary
    defaultreplicaset:
        name: default
        primary: mysql-2.mysql-endpoints.openstack.svc.cluster.local.:3306
        ssl: required
        status: ok
        statustext: cluster is online and can tolerate up to one failure.
        topology:
        mysql-0:
            address: mysql-0.mysql-endpoints.openstack.svc.cluster.local.:3306
            memberrole: secondary
            mode: r/o
            replicationlagfromimmediatesource: ""
            replicationlagfromoriginalsource: ""
            role: ha
            status: online
            version: 8.0.41
        mysql-1:
            address: mysql-1.mysql-endpoints.openstack.svc.cluster.local.:3306
            memberrole: secondary
            mode: r/o
            replicationlagfromimmediatesource: ""
            replicationlagfromoriginalsource: ""
            role: ha
            status: online
            version: 8.0.41
        mysql-2:
            address: mysql-2.mysql-endpoints.openstack.svc.cluster.local.:3306
            memberrole: primary
            mode: r/w
            role: ha
            status: online
            version: 8.0.41
        topologymode: single-primary
    domainname: cluster-set-1e57de179fb5edd8c4e6392a25473b96
    groupinformationsourcemember: mysql-2.mysql-endpoints.openstack.svc.cluster.local.:3306
    success: "True"

It's possible to see in this case that mysql/0 and mysql/1 are secondary and mysql/2 is primary.
So backups should be run on unit 0 or 1.

.. code-block :: text

    juju run glance-mysql/0 create-backup --wait 1m

Restore
~~~~~~~
To restore it is recommended to stop all control-plane services that might be using the database
before running the restore-backup action. This is to avoid any issues related to data corruption
or inconsistencies during the restore process.

At the moment, there isn't a charm action to stop all control-plane services at once, so it needs
to be done manually by running on all Openstack API services:
.. code-block :: text

    # get the container names of all OpenStack API services
    kubectl get pods -n openstack -o json | jq -r '
    .items[]
    | select(
        (.metadata.name | test("traefik|rabbitmq|mysql|modeloperator|ovn") | not)
        )
    | .metadata.name as $pod
    | .spec.containers[]
    | select(.name != "charm")
    | "\($pod) => \(.name)"
    '
    ...

    # get the pebble service names for all OpenStack API services
    for i in {0..2}; do kubectl -n openstack exec keystone-$i -c keystone -- pebble services; done
    # do the same for all necessary apps

    # stop the containers of all OpenStack API services
    for i in {0..2}; do kubectl -n openstack exec keystone-$i -c keystone -- pebble stop wsgi-keystone; done
    # do the same for all necessary apps

With all API services stopped, it's possible to run the restore-backup action on a MySQL unit.
Before that is necessary to scale down the MySQL cluster to 1 replica to ensure data consistency
during the restore process. See the `charmed MySQL documentation`_ for more details

.. code-block :: text

    juju scale-application mysql 1

Then, run the restore-backup action on the unit where you want to restore the backup. E.g:
.. code-block :: text

    juju run mysql/leader restore-backup backup-id=<backup-id>

After restoring all databases, it's necessary to resume the OpenStack services and scale again
the mysql units.

.. code-block :: text

    # start the containers of all OpenStack API services
    for i in {0..2}; do kubectl -n openstack exec keystone-$i -c keystone -- pebble start wsgi-keystone; done
    # do the same for all necessary apps

    juju scale-application mysql 3

In case you find mysql-routers on blocked state, it's necessary to re-launch them by running the following command:
.. code-block :: text

    juju scale-application keystone-mysql-router 0
    juju scale-application keystone-mysql-router 3


Vault
-----

Requirements
~~~~~~~~~~~~
* Have a Vault cluster enabled in Sunbeam.
* Units are in active idle state
* Configured settings for S3 storage
* Have saved your unseal keys and root-token in a secure location of your choice

Backup / Restore
~~~~~~~~~~~~~~~~
.. code-block :: text

    juju run vault/leader create-backup

    juju run vault/leader list-backups

    juju run vault/leader restore-backup backup-id=<backup-id>

K8s control plane backup
------------------------

Requirements
~~~~~~~~~~~~
* Have a `velero-operator`_ deployed
* Have the `infra-backup-operator`_ deployed
* Have access to S3 storage
* Configure s3-integrator

Backup
~~~~~~
.. code-block :: text

    juju run velero-operator/0 create-backup \
    target=infra-backup-operator:cluster-infra-backup

    juju run velero-operator/0 create-backup \
    target=infra-backup-operator:namespaced-infra-backup

Restore
~~~~~~~
.. code-block :: text

    # list the backups

    juju run velero-operator/0 list-backups

    backups:
    83503892-a24a-409b-b0df-553dcc2465ec:
        app: infra-backup-operator
        completion-timestamp: "2025-08-08T20:00:28Z"
        endpoint: cluster-infra-backup
        model: test-charm-9f0e8dda
        name: infra-backup-operator-cluster-infra-backup-pblz2
        phase: Completed
        start-timestamp: "2025-08-08T20:00:26Z"
    85662948-8e5e-4922-8e1c-c5568eafa6e7:
        app: infra-backup-operator
        completion-timestamp: "2025-08-07T18:42:13Z"
        endpoint: cluster-infra-backup
        model: test-charm-9f0e8dda
        name: infra-backup-operator-cluster-infra-backup-4bm7p
        phase: Completed
        start-timestamp: "2025-08-07T18:42:10Z"

    # restore the backups

    juju run velero-operator/0 restore backup-uid=85662948-8e5e-4922-8e1c-c5568eafa6e7

    juju run velero-operator/0 restore backup-uid=83503892-a24a-409b-b0df-553dcc2465ec

Juju
----

Backup
~~~~~~
.. code-block :: text

    # export all models
    juju export-bundle --model=cos --filename=cos-bundle.yaml
    juju export-bundle --model=openstack --filename=openstack-bundle.yaml
    ...

    # backup of controller
    juju create-backup --model=${CONTROLLERS_MODEL} --filename=juju-ctrl-backup.tar.gz

    # local client configuration
    tar -czf juju-credentials.tar.gz .local/share/juju/*

Restore
~~~~~~~
For restoring there is the `juju-restore`_ tool to help.


MAAS deployment access
----------------------

See the :doc:`Backup and Restore MAAS Deployment</how-to/misc/backup-and-restore-maas-deployment>` for details.

Sunbeam-clusterd
----------------

Backup
~~~~~~
It's recommended to create a backup of sunbeam-clusterd data by running the following command:

.. code-block :: text

    juju exec -a sunbeam-clusterd -- tar -cvf /home/ubuntu/backup.tar /var/snap/openstack/common/state/database

Note that the backup file is created in the home directory of the ubuntu user, so it needs to be
moved to a safe location after the backup is created.

Restore
~~~~~~~
If a unit has a corrupted database, it's possible to restore the backup by running the following command:

.. code-block :: text

    # stop the clusterd service before restoring the backup
    juju exec -a sunbeam-clusterd -- sudo systemctl stop snap.openstack.clusterd.service

    # remove snapshots and segments database files from the corrupted unit
    juju exec -u sunbeam-clusterd/{unit} -- rm /var/snap/openstack/common/state/database/snapshot*
    juju exec -u sunbeam-clusterd/{unit} -- rm /var/snap/openstack/common/state/database/000000*

    # restore the backup on the corrupted unit
    juju exec -u sunbeam-clusterd/{unit} -- tar -xvf /home/ubuntu/backup.tar -C /var/snap/openstack/common/state/database/

    # start the clusterd service after restoring the backup
    juju exec -a sunbeam-clusterd -- sudo systemctl start snap.openstack.clusterd.service

.. LINKS
.. _velero-operator: https://charmhub.io/velero-operator
.. _infra-backup-operator: https://charmhub.io/infra-backup-operator/docs/tutorial
.. _juju-restore: https://github.com/juju/juju-restore/
.. _charmed-mysql-documentation: https://canonical-charmed-mysql.readthedocs-hosted.com/how-to/back-up-and-restore/restore-a-backup/
