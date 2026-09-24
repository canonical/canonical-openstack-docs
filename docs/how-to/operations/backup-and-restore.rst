Backup and Restore
==================

Overview
--------

Sunbeam provides commands to back up, list backups, and restore MySQL and Vault
data in an existing deployment. These commands operate on applications in the
``openstack`` model. They do not back up virtual machine disks, volumes, or the
entire cluster.

Separate procedures for Kubernetes, Juju, deployment access, and sunbeam-clusterd
are described below.


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

Install a tool like ``aws-cli`` or ``s3cmd`` and configure it with the access key and secret key
obtained from the previous command to interact with the S3 storage provided by ceph-rgw.

.. code-block :: text

    sudo snap install aws-cli --classic
    aws configure --profile ceph # fill the asked information
    aws --profile ceph --endpoint-url http://<IP_RGW_SERVICE> s3api create-bucket --bucket mysql
    ...
    # repeat the previous command to create a bucket for each application you want to backup

Deploy one s3-integrator application for each application that needs s3-integration. E.g:

.. code-block :: text

    juju switch openstack
    juju deploy s3-integrator --model openstack mysql-s3-integrator
    juju integrate mysql-s3-integrator mysql
    ...
    # deploy and integrate for all necessary apps


Run the sync-s3-credentials action to configure the charm

.. code-block :: text

    juju run mysql-s3-integrator/leader sync-s3-credentials access-key=<ACCESS_KEY> secret-key=<SECRET_KEY>
    ...
    # do the same for all necessary apps

Configure the s3-integrator charm to use the correct bucket for each application

.. code-block :: text

    juju config mysql-s3-integrator bucket=mysql s3-uri-style=path endpoint=http://<IP_RGW_SERVICE> path=mysql
    ...
    # do the same for all necessary apps

MySQL and Vault
---------------

Requirements
~~~~~~~~~~~~

* MySQL and Vault applications to be backed up are in active/idle state.
* Each application has an s3-integrator relation and working S3 configuration.
  Follow the setup above for each MySQL application and for Vault, when enabled.
* For MySQL restore, the related OpenStack API charms provide ``pause`` and
  ``resume`` actions.
* For Vault restore, retain the unseal keys and root token that were in use when
  the backup was created. See :doc:`/how-to/features/vault`.

Backup
~~~~~~

Create backups of the MySQL and Vault applications:

.. code-block :: text

    sunbeam backup

Sunbeam selects a secondary MySQL unit when available and the Vault leader unit.
Backups run concurrently. The command reports a backup ID and status for each
application and writes a YAML manifest to the path shown in its output.

Check that every expected application has a successful backup. Applications that
fail readiness checks are skipped; Sunbeam asks whether to continue with the
remaining applications.

.. note::

   Concurrent backups reduce the time between application backups but do not
   guarantee a consistent snapshot across databases. Restoring backups taken at
   different times can leave inconsistent references between OpenStack services.

List backups
~~~~~~~~~~~~

List the backup IDs available in the configured S3 storage:

.. code-block :: text

    sunbeam list-backups

The command displays the inventory for each application and writes a YAML
inventory manifest to the path shown in its output. Both manifests contain
backup metadata, not the backed-up data. They are not inputs to the restore
command.

Restore
~~~~~~~

Schedule a maintenance window. Restoring MySQL interrupts the related OpenStack
API services and replaces database contents with the selected backup state.

Restore each application from its latest successful backup:

.. code-block :: text

    sunbeam restore

Review the inventory and confirm the restore. Sunbeam warns before proceeding
with missing or failed backups. A partial restore can leave inconsistent data
between services.

For each MySQL application, Sunbeam pauses the related API services, scales its
routers to zero units and MySQL to one unit, and restores the backup. It then
restores the original unit counts and resumes the API services. Vault is restored
through its charm's ``restore-backup`` action.

To restore MySQL to a point in time, specify a UTC timestamp:

.. code-block :: text

    sunbeam restore --restore-to-time "YYYY-MM-DD HH:MM:SS"

This requires a MySQL charm supporting point-in-time recovery and backup data
covering the requested time. See the `charmed MySQL documentation`_. Vault does
not support point-in-time recovery; Sunbeam warns and restores its latest backup
instead.

After restoring Vault, unseal it and authorize the charm using the keys and root
token from the time of the backup. Follow :doc:`/how-to/features/vault` and the
`Vault restore documentation`_.

Check application status and verify that the restored data is accessible through
the affected OpenStack services:

.. code-block :: text

    juju status -m openstack

If MySQL reports ``Move restored cluster to another S3 repository``, create a new
bucket and update the corresponding integrator. For example:

.. code-block :: text

    juju config -m openstack mysql-s3-integrator bucket=<NEW_BUCKET_NAME>

Command options
~~~~~~~~~~~~~~~

Use ``--timeout <seconds>`` to change the wait time for backup, listing, or restore
operations. The default is 1800 seconds. For example:

.. code-block :: text

    sunbeam backup --timeout 3600

The backup and restore commands accept ``--no-prompt`` for unattended use. This
also accepts prompts to continue after applications have been skipped; check
the reported applications and results.

The ``--force`` option allows backup or restore to proceed despite application
health concerns. For MySQL backup, it also allows use of the leader when cluster
health cannot be verified. It does not bypass the S3 relation requirement and
may result in a backup containing stale data.

Failed operations
~~~~~~~~~~~~~~~~~

Backup and restore return ``0`` when all attempted operations succeed, ``1`` for
partial failure, and ``2`` when all attempted operations fail. Listing returns
``2`` if any application's inventory cannot be retrieved. Validation errors and
cancelled prompts also return nonzero exit codes. Check warnings for applications
skipped before the operation; a zero exit code does not prove they were included.

If restore fails, Sunbeam attempts to restore MySQL and router unit counts and
resume the related API services. This does not undo changes to database contents.
Recovery failures are reported separately.

Inspect the reported error and Juju status before retrying. A timeout does not
establish whether the charm action completed. Check for paused services, missing
router units, sealed Vault units, and MySQL status messages before starting
another restore.

Other components
----------------

The following procedures are separate from the Sunbeam backup and restore
commands.

K8s control plane backup
~~~~~~~~~~~~~~~~~~~~~~~~

Requirements
^^^^^^^^^^^^
* Have a `velero-operator`_ deployed
* Have the `infra-backup-operator`_ deployed
* Have access to S3 storage
* Configure s3-integrator

Backup
^^^^^^
.. code-block :: text

    juju run velero-operator/0 create-backup \
    target=infra-backup-operator:cluster-infra-backup

    juju run velero-operator/0 create-backup \
    target=infra-backup-operator:namespaced-infra-backup

Restore
^^^^^^^
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
~~~~

Backup
^^^^^^
.. code-block :: text

    # export all models
    juju export-bundle --model=cos --filename=cos-bundle.yaml
    juju export-bundle --model=openstack --filename=openstack-bundle.yaml
    ...

    # backup of controller
    juju create-backup --model=${CONTROLLERS_MODEL} --filename=juju-ctrl-backup.tar.gz

    # local client configuration
    tar -czf juju-credentials.tar.gz ~/.local/share/juju/*

Restore
^^^^^^^
For restoring there is the `juju-restore`_ tool to help.


MAAS deployment access
~~~~~~~~~~~~~~~~~~~~~~

See the :doc:`Backup and Restore MAAS Deployment</how-to/misc/backup-and-restore-maas-deployment>` for details.

Sunbeam-clusterd
~~~~~~~~~~~~~~~~

Backup
^^^^^^
It's recommended to create a backup of sunbeam-clusterd data by running the following command:

.. code-block :: text

    juju exec -a sunbeam-clusterd -- tar -cvf /home/ubuntu/backup.tar /var/snap/openstack/common/state/database

Note that the backup file is created in the home directory of the ubuntu user, so it needs to be
moved to a safe location after the backup is created.

Restore
^^^^^^^
If a unit has a corrupted database, it's possible to restore the backup by running the following command:

.. code-block :: text

    # stop the clusterd service before restoring the backup
    juju exec -a sunbeam-clusterd -- sudo systemctl stop snap.openstack.clusterd.service

    # remove snapshots and segments database files from the corrupted unit
    juju exec -u sunbeam-clusterd/{unit} -- rm /var/snap/openstack/common/state/database/snapshot*
    juju exec -u sunbeam-clusterd/{unit} -- rm /var/snap/openstack/common/state/database/000000*

    # restore the backup on the corrupted unit
    juju exec -u sunbeam-clusterd/{unit} -- tar -xvf /home/ubuntu/backup.tar -C /

    # start the clusterd service after restoring the backup
    juju exec -a sunbeam-clusterd -- sudo systemctl start snap.openstack.clusterd.service

.. LINKS
.. _velero-operator: https://charmhub.io/velero-operator
.. _infra-backup-operator: https://charmhub.io/infra-backup-operator/docs/tutorial
.. _juju-restore: https://github.com/juju/juju-restore/
.. _charmed mysql documentation: https://canonical-charmed-mysql.readthedocs-hosted.com/8.0/how-to/back-up-and-restore/restore-a-backup/
.. _Vault restore documentation: https://canonical-vault-charms.readthedocs-hosted.com/en/latest/how-to/restore_backup/
