Instance Recovery
=================

Each compute node runs a Consul agent which periodically performs a TCP health check against the network interface card (NIC). Consul server on the control node detects the unreachable consul agent periodically. If the NIC is down, the following actions are taken on the affected node:

- Instances are shut down gracefully.
- The ``nova-compute`` service is disabled.

Masakari checks the status from the Consul server and triggers the recovery. Refer to the recovery matrix in the :doc:`Instance Recovery how-to </how-to/features/instance-recovery>` for when recovery is triggered and whether instances needs to be evacuated.