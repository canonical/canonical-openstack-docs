API auditing
============

Canonical OpenStack automatically enables auditing for most OpenStack API
services, leveraging the `Keystone audit middleware <https://docs.openstack.org/keystonemiddleware/latest/audit.html>`_.

The audit events are logged in `CADF <https://www.dmtf.org/standards/cadf>`_
format using the `pyCADF <https://docs.openstack.org/pycadf/latest/>`_ library.

.. list-table:: API service support matrix
   :header-rows: 1

   * - Service name
     - CADF auditing supported
   * - Aodh
     - ✓
   * - Barbican
     - ✓
   * - Ceilometer
     - ✓
   * - Cinder
     - ✓
   * - Designate
     - ✓
   * - Glance
     - ✓
   * - Gnocchi
     - X
   * - Heat
     - ✓
   * - Keystone
     - ✓
   * - Magnum
     - ✓
   * - Masakari
     - ✓
   * - Neutron
     - ✓
   * - Octavia
     - ✓
   * - Placement
     - X
   * - Watcher
     - X

All the API requests and responses that reach the `audit`
`api-paste filter <https://docs.pylonsproject.org/projects/pastedeploy>`_.
will be logged.

.. note::

    Some requests may be rejected by other filters, for example due to an
    invalid token. No CADF event will be emitted in this case.

Sample
------

The audit middleware will log one notification for the observed request and
another for the corresponding reply.

The records include information such as:

* initiator credentials and address
* target endpoint
* request path and action
* request outcome
* request id, which can be used to correlate logs


.. code:: text

    $ sudo k8s kubectl logs -n openstack pod/nova-0 \
        --container nova-api --since 5m | grep oslo.messaging.notification.audit

    2025-06-12T09:45:55.775Z [wsgi-nova-api] 2025-06-12 09:45:55.775335 2025-06-12 09:45:55.774 80 INFO oslo.messaging.notification.audit.http.request [None req-4cf54a26-26b3-4cd3-9442-2630480563b4 1c6dfb96f6ad40cab32a5add1daef45e 123e60b3cd024672b6dfdd0b6db8c32d - - 756f65bca3e74610aed6fffb0cc771c3 756f65bca3e74610aed6fffb0cc771c3] {"message_id": "31f1874a-91ea-4822-84a2-b82570afdc44", "publisher_id": "mod_wsgi", "event_type": "audit.http.request", "priority": "INFO", "payload": {"typeURI": "http://schemas.dmtf.org/cloud/audit/1.0/event", "eventType": "activity", "id": "d7853699-5d1c-5bea-9fe0-815616e40ee0", "eventTime": "2025-06-12T09:45:55.774005+0000", "action": "read/list", "outcome": "pending", "observer": {"id": "target"}, "initiator": {"id": "1c6dfb96f6ad40cab32a5add1daef45e", "typeURI": "service/security/account/user", "name": "admin", "credential": {"token": "***", "identity_status": "Confirmed"}, "host": {"address": "10.1.0.179", "agent": "openstacksdk/3.0.0 keystoneauth1/5.6.0 python-requests/2.31.0 CPython/3.12.3"}, "project_id": "123e60b3cd024672b6dfdd0b6db8c32d", "request_id": "req-4cf54a26-26b3-4cd3-9442-2630480563b4"}, "target": {"id": "nova", "typeURI": "service/compute/servers/detail", "name": "nova", "addresses": [{"url": "http://10.152.183.37:8774/v2.1", "name": "admin"}, {"url": "http://10.7.66.204:80/openstack-nova/v2.1", "name": "private"}, {"url": "http://10.7.66.205:80/openstack-nova/v2.1", "name": "public"}]}, "requestPath": "/openstack-nova/v2.1/servers/detail?deleted=False", "tags": ["correlation_id?value=79a738d0-b97d-556e-9efe-d99536267d1e"]}, "timestamp": "2025-06-12 09:45:55.774487"}

    2025-06-12T09:45:56.184Z [wsgi-nova-api] 2025-06-12 09:45:56.184431 2025-06-12 09:45:56.184 80 INFO oslo.messaging.notification.audit.http.response [None req-4cf54a26-26b3-4cd3-9442-2630480563b4 1c6dfb96f6ad40cab32a5add1daef45e 123e60b3cd024672b6dfdd0b6db8c32d - - 756f65bca3e74610aed6fffb0cc771c3 756f65bca3e74610aed6fffb0cc771c3] {"message_id": "1ecdd560-e881-4038-ba27-2a74cf322872", "publisher_id": "mod_wsgi", "event_type": "audit.http.response", "priority": "INFO", "payload": {"typeURI": "http://schemas.dmtf.org/cloud/audit/1.0/event", "eventType": "activity", "id": "d7853699-5d1c-5bea-9fe0-815616e40ee0", "eventTime": "2025-06-12T09:45:55.774005+0000", "action": "read/list", "outcome": "success", "observer": {"id": "target"}, "initiator": {"id": "1c6dfb96f6ad40cab32a5add1daef45e", "typeURI": "service/security/account/user", "name": "admin", "credential": {"token": "***", "identity_status": "Confirmed"}, "host": {"address": "10.1.0.179", "agent": "openstacksdk/3.0.0 keystoneauth1/5.6.0 python-requests/2.31.0 CPython/3.12.3"}, "project_id": "123e60b3cd024672b6dfdd0b6db8c32d", "request_id": "req-4cf54a26-26b3-4cd3-9442-2630480563b4"}, "target": {"id": "nova", "typeURI": "service/compute/servers/detail", "name": "nova", "addresses": [{"url": "http://10.152.183.37:8774/v2.1", "name": "admin"}, {"url": "http://10.7.66.204:80/openstack-nova/v2.1", "name": "private"}, {"url": "http://10.7.66.205:80/openstack-nova/v2.1", "name": "public"}]}, "requestPath": "/openstack-nova/v2.1/servers/detail?deleted=False", "tags": ["correlation_id?value=79a738d0-b97d-556e-9efe-d99536267d1e"], "reason": {"reasonType": "HTTP", "reasonCode": "200"}, "reporterchain": [{"role": "modifier", "reporterTime": "2025-06-12T09:45:56.183492+0000", "reporter": {"id": "target"}}]}, "timestamp": "2025-06-12 09:45:56.183889"}


Keystone does not use the audit middleware, but instead will log one
notification for each successful create, modify or delete operation.

Again, the notification will contain the initiator details along with the
requested action.

.. code:: text

    $ sudo k8s kubectl logs -n openstack pod/keystone-0 \
        --container keystone --since 5m | grep oslo.messaging.notification

    2025-06-17T10:23:40.242Z [wsgi-keystone] 2025-06-17 10:23:40.242100 2025-06-17 10:23:40.241 1329 INFO oslo.messaging.notification.identity.user.updated [None req-6cf138c4-c390-40e9-92a7-63091d538fcf f28f7f5a711941af99f5a09a42699dc6 c386d8fed6694aa78b6a2d42d2d04348 - - e2f3d227a8db47a1a9204cbe8bc7758c e2f3d227a8db47a1a9204cbe8bc7758c] {"message_id": "e585b0b6-42b2-4423-947a-b5987796dd1e", "publisher_id": "identity.keystone-0", "event_type": "identity.user.updated", "priority": "INFO", "payload": {"typeURI": "http://schemas.dmtf.org/cloud/audit/1.0/event", "eventType": "activity", "id": "0b349407-5549-51bf-adff-e3c484740c0a", "eventTime": "2025-06-17T10:23:40.204955+0000", "action": "updated.user", "outcome": "success", "observer": {"id": "41393a82908d4d59ae36032d92569fd7", "typeURI": "service/security"}, "initiator": {"id": "f28f7f5a711941af99f5a09a42699dc6", "typeURI": "service/security/account/user", "host": {"address": "10.1.0.197", "agent": "python-keystoneclient"}, "user_id": "f28f7f5a711941af99f5a09a42699dc6", "project_id": "c386d8fed6694aa78b6a2d42d2d04348", "request_id": "req-6cf138c4-c390-40e9-92a7-63091d538fcf", "username": "admin"}, "target": {"id": "da9429a6cda54340b9a8652423c21d0a", "typeURI": "data/security/account/user"}, "resource_info": "da9429a6cda54340b9a8652423c21d0a"}, "timestamp": "2025-06-17 10:23:40.241660"}
