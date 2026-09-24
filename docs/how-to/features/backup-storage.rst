Backup storage
==============

This feature deploys and configures s3-integrator applications for MySQL and
Vault in the ``openstack`` model. It prepares access to S3 storage; it does not
create backups or restore data.

Requirements
------------

* A deployed MySQL application and, optionally, Vault.
* An S3 bucket and endpoint accessible from the deployment.
* An access key and secret key with permission to use the bucket.

For production deployments, store backups outside the OpenStack cluster.

Enabling backup storage
-----------------------

The feature is experimental and uses the command name ``disaster-recovery``.
Unlock it before enabling:

.. code:: text

   sudo snap set openstack feature.disaster-recovery=true
   sunbeam enable disaster-recovery

See :doc:`/how-to/operations/manage-experimental-features` for details on feature
gates.

Sunbeam deploys one s3-integrator application for each eligible MySQL or Vault
application and relates it to that application. It uses the deployment's
single-MySQL or multi-MySQL configuration to select the MySQL applications.

For example, ``mysql`` uses ``mysql-s3-integrator``, ``keystone-mysql`` uses
``keystone-s3-integrator``, and ``vault`` uses ``vault-s3-integrator``.

Applications with an existing, externally managed S3 relation are skipped. Sunbeam
also skips an application if its expected integrator name is already in use by an
application it does not manage. Existing S3 configurations are not adopted or
overwritten.

Configuring S3
--------------

Answer ``y`` to ``Configure all s3-integrators?`` to configure the integrators
managed by the feature. Sunbeam prompts for:

* S3 bucket
* S3 path prefix (default: ``/``)
* S3 region (default: ``us-east-2``)
* S3 endpoint (default: ``https://s3.us-east-2.amazonaws.com``)
* S3 access key
* S3 secret key

The endpoint must begin with ``http://`` or ``https://``. Both credential prompts
hide the entered value. Sunbeam creates a Juju secret for each integrator and
grants that application access to it.

All managed integrators use the same bucket, endpoint, region, and credentials.
Sunbeam appends each target application name to the path prefix to separate its
backups. For example, a prefix of ``/cloud-backups`` produces
``/cloud-backups/keystone-mysql`` and ``/cloud-backups/vault``.

The default answer to the configuration prompt is ``n``. In this case, Sunbeam
deploys the integrators and relations without supplying S3 settings or
credentials. Configure them manually using the s3-integrator procedure in
:doc:`/how-to/operations/backup-and-restore`.

Check the application status after enabling:

.. code:: text

   juju status -m openstack

Enabling can complete while integrators are blocked pending configuration.
Resolve their status messages and verify the MySQL and Vault applications are
ready before following :doc:`/how-to/operations/backup-and-restore`.

Disabling backup storage
------------------------

To remove the integrations managed by this feature:

.. code:: text

   sunbeam disable disaster-recovery

This removes the managed s3-integrator applications, their relations, and the
Juju secrets created for their credentials. Externally managed S3 integrations
are left in place. The S3 bucket and stored backups are not deleted.

Applications whose integrations were removed need an S3 integration configured
again before they can back up or restore data. Reuse the original bucket and
application paths to access their existing backups.
