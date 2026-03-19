Use the EPA orchestrator
========================

The Enhanced Performance Accelerator (EPA) orchestrator provides resource allocation for CPU pinning and huge pages within Sunbeam OpenStack.

System configuration requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use the EPA orchestrator, the host system must be preconfigured with the following kernel parameters:

1. **CPU isolation**: Reserve dedicated CPU cores for EPA workloads by setting the ``isolcpus`` kernel parameter.
2. **Huge pages**: Enable large memory pages by setting parameters such as ``default_hugepagesz``, ``hugepagesz``, and ``hugepages`` (for example, to configure 16 × 1 GB huge pages).

For MAAS deployments, configure these via the MAAS UI/CLI for each node.
For detailed instructions on setting kernel boot parameters via the CLI, refer to the
`MAAS documentation on machine customization <https://canonical.com/maas/docs/about-machine-customization#p-17465-kernel-boot-options>`_.

For **single-node deployments**, configure these parameters manually on the node and reboot the machine.