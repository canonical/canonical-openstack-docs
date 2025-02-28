Enterprise Requirements
=======================

Single-node
-----------

For single-node deployments the following minimum hardware specification
applies:

+-----------------------+-----------------------+-----------------------+
| Component             | Specification         | Notes                 |
+=======================+=======================+=======================+
| CPU                   | 4 core                | amd64 only            |
+-----------------------+-----------------------+-----------------------+
| RAM                   | 16 GiB                |                       |
+-----------------------+-----------------------+-----------------------+
| Root Disk             | 100 GiB of free space | SSD                   |
+-----------------------+-----------------------+-----------------------+
| Control plane network | 1 Gbps                | Mainly localhost only |
|                       |                       | networking so minimal |
|                       |                       | requirement           |
+-----------------------+-----------------------+-----------------------+
| External network      | 1 Gbps                | Optional - only       |
|                       |                       | required for remote   |
|                       |                       | access to instances   |
+-----------------------+-----------------------+-----------------------+
| Storage               | 1 x 100 GiB SSD       | Optional - only       |
|                       |                       | required for block    |
|                       |                       | storage service       |
+-----------------------+-----------------------+-----------------------+

.. note ::
    A single-node deployment has no resilience and has
    limited performance.

Multi-node
----------

For multi-node deployments the following minimum hardware specification
applies:

+-----------------------+-----------------------+-----------------------+
| Component             | Specification         | Notes                 |
+=======================+=======================+=======================+
| CPU                   | 16 core               | amd64 only            |
+-----------------------+-----------------------+-----------------------+
| RAM                   | 32 GiB                |                       |
+-----------------------+-----------------------+-----------------------+
| Root Disk             | 500 GiB of free space | SSD                   |
+-----------------------+-----------------------+-----------------------+
| Control plane network | 1 Gbps                | Supports east/west    |
| network               |                       | traffic               |
+-----------------------+-----------------------+-----------------------+
| External network      | 1 Gbps                | Supports north/south  |
|                       |                       | traffic               |
+-----------------------+-----------------------+-----------------------+
| Storage               | 1 x 500 GiB SSD       | Required for block    |
|                       |                       | storage and image     |
|                       |                       | services              |
+-----------------------+-----------------------+-----------------------+

.. note ::
    Three nodes are required for multi-node operation.

Role Based Minimum Memory Sizing
--------------------------------

For multi-node deployments the following minimum component memory sizing may be
used to size each node based on the roles it hosts within the deployment:

+-----------------+----------+---------+--------------+----------+--------+-----------------+
| Component       | Control  | Compute | Storage      | Sunbeam  | Client | Juju-Controller |
+=================+==========+=========+==============+==========+========+=================+
| Kubernetes      | 4 GiB    |         |              |          |        |                 |
+-----------------+----------+---------+--------------+----------+--------+-----------------+
| Ceph OSD        |          |         | 5GiB per OSD |          |        |                 |
+-----------------+----------+---------+--------------+----------+--------+-----------------+
| Ceph MON/MGR    |          |         | 2GiB         |          |        |                 |
+-----------------+----------+---------+--------------+----------+--------+-----------------+
| Ceph RGW        |          |         | 2GiB         |          |        |                 |
+-----------------+----------+---------+--------------+----------+--------+-----------------+
| Control Plane   | 10 GiB   | 1GiB    |              |          |        |                 |
+-----------------+----------+---------+--------------+----------+--------+-----------------+
| SunbeamD        |          |         |              | 4 GiB    |        |                 |
+-----------------+----------+---------+--------------+----------+--------+-----------------+
| Juju Controller |          |         |              |          |        | 4GiB            |
+-----------------+----------+---------+--------------+----------+--------+-----------------+
| Sunbeam Client  |          |         |              |          | 1 GiB  |                 |
+-----------------+----------+---------+--------------+----------+--------+-----------------+

.. note ::
    For Ceph components, the scale of the deployment will have an
    impact on the memory footprint for MON/MGR daemons (3 nodes) and more memory and
    cores may be needed per Ceph OSD if using NVMe drives instead of SSD of spinning
    disks.
