API auditing
============

Canonical OpenStack automatically enables auditing for most OpenStack API
services, leveraging the `Keystone audit middleware <https://docs.openstack.org/keystonemiddleware/latest/audit.html>`_.

The audit events are logged in `CADF <https://www.dmtf.org/standards/cadf>`_
format using the `pyCADF <https://docs.openstack.org/pycadf/latest/>`_ library.

.. note::
    Some OpenStack services no longer support api-paste pipelines. In case of
    Keystone, a separate service consumes the audit events over AMQP.

Sample
------

.. code:: text

    $ sudo k8s kubectl logs -n openstack pod/nova-0 \
        --container nova-api --since 5m | grep audit

    2025-06-06T09:17:12.817Z [wsgi-nova-api] 2025-06-06 09:17:12.817458 2025-06-06 09:17:12.816 52 INFO oslo.messaging.notification.audit.http.request [None req-aa97f465-2ff8-4cbd-b514-dd754ac57d49 eb92e7ec3ae6444091b36747d772c121 48bf6ac494944933932ecbd0719b4a57 - - 447a34e794e44eeb9dd4a0087e21f016 447a34e794e44eeb9dd4a0087e21f016] {"message_id": "d5f0290f-f425-4974-a2e3-90dda0791fc7", "publisher_id": "mod_wsgi", "event_type": "audit.http.request", "priority": "INFO", "payload": {"typeURI": "http://schemas.dmtf.org/cloud/audit/1.0/event", "eventType": "activity", "id": "d6d4e8b2-b8fb-53ba-9fcd-062d51807de4", "eventTime": "2025-06-06T09:17:12.814943+0000", "action": "read/list", "outcome": "pending", "observer": {"id": "target"}, "initiator": {"id": "eb92e7ec3ae6444091b36747d772c121", "typeURI": "service/security/account/user", "name": "admin", "credential": {"token": "***", "identity_status": "Confirmed"}, "host": {"address": "10.1.0.184", "agent": "openstacksdk/3.0.0 keystoneauth1/5.6.0 python-requests/2.31.0 CPython/3.12.3"}, "project_id": "48bf6ac494944933932ecbd0719b4a57", "request_id": "req-aa97f465-2ff8-4cbd-b514-dd754ac57d49"}, "target": {"id": "nova", "typeURI": "service/compute/servers/detail", "name": "nova", "addresses": [{"url": "http://10.152.183.216:8774/v2.1", "name": "admin"}, {"url": "http://13.13.14.205:80/zaza-d3fa69a52d6a-nova/v2.1", "name": "private"}, {"url": "http://13.13.14.205:80/zaza-d3fa69a52d6a-nova/v2.1", "name": "public"}]}, "requestPath": "/zaza-d3fa69a52d6a-nova/v2.1/servers/detail?deleted=False", "tags": ["correlation_id?value=b8cd809e-a85d-5a9c-9d59-09be00a16a6d"]}, "timestamp": "2025-06-06 09:17:12.815965"}
