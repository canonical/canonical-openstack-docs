API auditing
============

Canonical OpenStack automatically enables auditing for most OpenStack API
services, leveraging the `Keystone audit middleware <https://docs.openstack.org/keystonemiddleware/latest/audit.html>`_.

The audit events are logged in `CADF <https://www.dmtf.org/standards/cadf>`_
format using the `pyCADF <https://docs.openstack.org/pycadf/latest/>`_ library.

.. note::

    Some OpenStack services no longer support api-paste pipelines,
    namely Keystone, Placement and Watcher.

    Keystone emits CADF notifications using `oslo_messaging` but only for
    successful create, update, or delete operations. The `log` notification
    driver will be enabled by default, while the optional `messagingv2` driver
    can be enabled through the Canonical OpenStack `telemetry` feature.

    Furthermore, Gnocchi auditing currently requires debug logging.

The `audit` filter leverages environment variables set by the `authtoken`
middleware and is usually placed close to the end of the
`api-paste pipeline <https://docs.pylonsproject.org/projects/pastedeploy>`_.

.. code:: text

    [composite:openstack_compute_api_v21]
    use = call:nova.api.auth:pipeline_factory_v21
    keystone = cors http_proxy_to_wsgi compute_req_id faultwrap request_log sizelimit osprofiler authtoken keystonecontext audit osapi_compute_app_v21

All the API requests and responses that reach the `audit` filter will be logged.

.. note::

    Some requests may be rejected by other filters, for example due to an
    invalid token. No CADF event will be emitted in this case.

Sample
------

.. code:: text

    $ sudo k8s kubectl logs -n openstack pod/nova-0 \
        --container nova-api --since 5m | grep audit

    2025-06-12T09:45:55.775Z [wsgi-nova-api] 2025-06-12 09:45:55.775335 2025-06-12 09:45:55.774 80 INFO oslo.messaging.notification.audit.http.request [None req-4cf54a26-26b3-4cd3-9442-2630480563b4 1c6dfb96f6ad40cab32a5add1daef45e 123e60b3cd024672b6dfdd0b6db8c32d - - 756f65bca3e74610aed6fffb0cc771c3 756f65bca3e74610aed6fffb0cc771c3] {"message_id": "31f1874a-91ea-4822-84a2-b82570afdc44", "publisher_id": "mod_wsgi", "event_type": "audit.http.request", "priority": "INFO", "payload": {"typeURI": "http://schemas.dmtf.org/cloud/audit/1.0/event", "eventType": "activity", "id": "d7853699-5d1c-5bea-9fe0-815616e40ee0", "eventTime": "2025-06-12T09:45:55.774005+0000", "action": "read/list", "outcome": "pending", "observer": {"id": "target"}, "initiator": {"id": "1c6dfb96f6ad40cab32a5add1daef45e", "typeURI": "service/security/account/user", "name": "admin", "credential": {"token": "***", "identity_status": "Confirmed"}, "host": {"address": "10.1.0.179", "agent": "openstacksdk/3.0.0 keystoneauth1/5.6.0 python-requests/2.31.0 CPython/3.12.3"}, "project_id": "123e60b3cd024672b6dfdd0b6db8c32d", "request_id": "req-4cf54a26-26b3-4cd3-9442-2630480563b4"}, "target": {"id": "nova", "typeURI": "service/compute/servers/detail", "name": "nova", "addresses": [{"url": "http://10.152.183.37:8774/v2.1", "name": "admin"}, {"url": "http://10.7.66.204:80/openstack-nova/v2.1", "name": "private"}, {"url": "http://10.7.66.205:80/openstack-nova/v2.1", "name": "public"}]}, "requestPath": "/openstack-nova/v2.1/servers/detail?deleted=False", "tags": ["correlation_id?value=79a738d0-b97d-556e-9efe-d99536267d1e"]}, "timestamp": "2025-06-12 09:45:55.774487"}\x1b[00m

    2025-06-12T09:45:56.184Z [wsgi-nova-api] 2025-06-12 09:45:56.184431 2025-06-12 09:45:56.184 80 INFO oslo.messaging.notification.audit.http.response [None req-4cf54a26-26b3-4cd3-9442-2630480563b4 1c6dfb96f6ad40cab32a5add1daef45e 123e60b3cd024672b6dfdd0b6db8c32d - - 756f65bca3e74610aed6fffb0cc771c3 756f65bca3e74610aed6fffb0cc771c3] {"message_id": "1ecdd560-e881-4038-ba27-2a74cf322872", "publisher_id": "mod_wsgi", "event_type": "audit.http.response", "priority": "INFO", "payload": {"typeURI": "http://schemas.dmtf.org/cloud/audit/1.0/event", "eventType": "activity", "id": "d7853699-5d1c-5bea-9fe0-815616e40ee0", "eventTime": "2025-06-12T09:45:55.774005+0000", "action": "read/list", "outcome": "success", "observer": {"id": "target"}, "initiator": {"id": "1c6dfb96f6ad40cab32a5add1daef45e", "typeURI": "service/security/account/user", "name": "admin", "credential": {"token": "***", "identity_status": "Confirmed"}, "host": {"address": "10.1.0.179", "agent": "openstacksdk/3.0.0 keystoneauth1/5.6.0 python-requests/2.31.0 CPython/3.12.3"}, "project_id": "123e60b3cd024672b6dfdd0b6db8c32d", "request_id": "req-4cf54a26-26b3-4cd3-9442-2630480563b4"}, "target": {"id": "nova", "typeURI": "service/compute/servers/detail", "name": "nova", "addresses": [{"url": "http://10.152.183.37:8774/v2.1", "name": "admin"}, {"url": "http://10.7.66.204:80/openstack-nova/v2.1", "name": "private"}, {"url": "http://10.7.66.205:80/openstack-nova/v2.1", "name": "public"}]}, "requestPath": "/openstack-nova/v2.1/servers/detail?deleted=False", "tags": ["correlation_id?value=79a738d0-b97d-556e-9efe-d99536267d1e"], "reason": {"reasonType": "HTTP", "reasonCode": "200"}, "reporterchain": [{"role": "modifier", "reporterTime": "2025-06-12T09:45:56.183492+0000", "reporter": {"id": "target"}}]}, "timestamp": "2025-06-12 09:45:56.183889"}\x1b[00m
