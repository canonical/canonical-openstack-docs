Stable release process
======================

This reference describes the stable release workflow for Canonical OpenStack components.
Each component (Rocks, Snaps, Charms, and the OpenStack snap) follows a structured release process with automated builds and manual promotion through release channels.

Quick reference
---------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Component
     - Build system
     - Build trigger
     - Build frequency
     - Promotion method
   * - Rocks
     - GitHub Actions
     - Commit to stable branch
     - On commit
     - Automatic on commit
   * - Snaps
     - Launchpad
     - Commit to stable branch
     - Every 5 hours (if changes)
     - Manual via Snap Store
   * - Charms
     - OpenDev CI
     - Commit to stable branch
     - On commit
     - Manual via Charmhub
   * - `OpenStack snap`_
     - Launchpad
     - Commit to stable branch
     - Every 5 hours (if changes)
     - Manual via Snap Store

Release channels
----------------

Components follow the Snap Store and Charmhub channel model with progressive promotion through risk levels:

edge
   Automated builds from stable branches. For development and early testing.

beta
   Builds promoted from edge after initial validation. For broader testing.

candidate
   Builds promoted from beta after extended testing. Release candidates for production.

stable
   Production-ready builds promoted from candidate after full validation.

Component specifications
-------------------------

Rocks
~~~~~

Overview
^^^^^^^^

Rocks are OCI images that provide the runtime environment for OpenStack services.
The rocks mono-repository maintains a stable branch from which new rocks are built and published to the registry.

Repository and registry
^^^^^^^^^^^^^^^^^^^^^^^

:Repository: https://github.com/canonical/ubuntu-openstack-rocks
:Registry: GitHub Container Registry (ghcr.io)
:Stable branch naming: ``stable/YYYY.N`` (e.g., ``stable/2024.1``)

Build automation
^^^^^^^^^^^^^^^^

:Build system: GitHub Actions
:Trigger: Commit to stable branch
:Frequency: On each commit
:Artifacts: OCI images published to ghcr.io

Release workflow
^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Stage
     - Description
   * - Backport
     - Changes are proposed to the stable branch via pull request
   * - Approval
     - Changes are reviewed and approved by maintainers
   * - Build
     - GitHub Actions automatically builds and publishes the rock to the registry

.. note::

   Rocks are not automatically re-assigned to charm versions. After a rock is published, the associated charms must be rebuilt and published to Charmhub to consume the new rock version.

Snaps
~~~~~

Overview
^^^^^^^^

Infrastructure snaps (OpenStack Hypervisor, MicroCeph, MicroOVN) provide the runtime components for Canonical OpenStack deployments.
Snaps are built automatically and published to the edge channel, then manually promoted through higher risk levels.

Repository and registry
^^^^^^^^^^^^^^^^^^^^^^^

:Build system: Launchpad
:Registry: Snap Store
:Stable branch naming: ``stable/YYYY.N`` (e.g., ``stable/2024.1``)

Component snaps:

- `OpenStack Hypervisor snap`_
- `MicroCeph snap`_
- `MicroOVN snap`_

Build automation
^^^^^^^^^^^^^^^^

:Build system: Launchpad
:Trigger: Commit to stable branch
:Frequency: Every 5 hours (if changes detected)
:Artifacts: Snap packages published to edge channel
:Build delay: Up to 5 hours

Release workflow
^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Stage
     - Description
   * - Backport
     - Changes are proposed to the stable branch
   * - Approval
     - Changes are reviewed and approved by maintainers
   * - Build
     - Launchpad builds the snap and publishes to edge channel (up to 5 hour delay)
   * - Testing (edge)
     - Snap is validated in the edge channel
   * - Promote to beta
     - Snap is manually promoted to beta channel after edge validation
   * - Testing (beta)
     - Snap is validated in the beta channel
   * - Promote to candidate
     - Snap is manually promoted to candidate channel after beta validation
   * - Testing (candidate)
     - Snap is validated in the candidate channel
   * - Promote to stable
     - Snap is manually promoted to stable channel after candidate validation

Charms
~~~~~~

Overview
^^^^^^^^

Canonical OpenStack deploy and manage OpenStack services on Kubernetes and Machine.
Charms are built automatically on each commit and published to the edge channel, then manually promoted.

Repository and registry
^^^^^^^^^^^^^^^^^^^^^^^

:Repository: https://opendev.org/openstack/sunbeam-charms
:Registry: Charmhub (https://charmhub.io)
:Build system: OpenDev CI
:Stable branch naming: ``stable/YYYY.N`` (e.g., ``stable/2024.1``)

Build automation
^^^^^^^^^^^^^^^^

:Build system: OpenDev CI
:Trigger: Commit to stable branch
:Frequency: On each commit
:Artifacts: Charms published to edge channel

Release workflow
^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Stage
     - Description
   * - Backport
     - Changes are proposed to the stable branch
   * - Approval
     - Changes are reviewed and approved by maintainers
   * - Build
     - OpenDev CI builds the charm and publishes to edge channel
   * - Testing (edge)
     - Charm is validated in the edge channel
   * - Promote to beta
     - Charm is manually promoted to beta channel after edge validation
   * - Testing (beta)
     - Charm is validated in the beta channel
   * - Promote to candidate
     - Charm is manually promoted to candidate channel after beta validation
   * - Testing (candidate)
     - Charm is validated in the candidate channel
   * - Promote to stable
     - Charm is manually promoted to stable channel after candidate validation

Release tools
^^^^^^^^^^^^^

For mass charm releases, use the `sunbeam-release tool`_.

OpenStack snap
~~~~~~~~~~~~~~

Overview
^^^^^^^^

The `OpenStack snap`_ is the primary entry point for deploying and managing Canonical OpenStack.
It integrates charms, rocks, and infrastructure snaps into a cohesive deployment tool.
This component drives most integration testing across the Canonical OpenStack ecosystem.

Repository and registry
^^^^^^^^^^^^^^^^^^^^^^^

:Repository: https://github.com/canonical/snap-openstack
:Registry: Snap Store
:Snap Store listing: https://snapcraft.io/openstack
:Build system: Launchpad
:Stable branch naming: ``stable/YYYY.N`` (e.g., ``stable/2024.1``)

Build automation
^^^^^^^^^^^^^^^^

:Build system: Launchpad
:Trigger: Commit to stable branch
:Frequency: Every 5 hours (if changes detected)
:Artifacts: Snap package published to edge channel
:Build delay: Up to 5 hours

Release workflow
^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Stage
     - Description
   * - Backport
     - Changes are proposed to the stable branch
   * - Approval
     - Changes are reviewed and approved by maintainers
   * - Build
     - Launchpad builds the snap and publishes to edge channel (up to 5 hour delay)
   * - Testing (edge)
     - Changes are validated in the edge channel
   * - Promote to beta
     - Snap is manually promoted to beta channel after edge validation
   * - Testing (beta)
     - Automated internal tests run at Canonical: smoke, regression, and scale tests
   * - Promote to candidate
     - Snap is manually promoted to candidate channel after beta validation
   * - Testing (candidate)
     - Final validation in candidate channel
   * - Promote to stable
     - Snap is manually promoted to stable channel after all tests pass

Testing specifications
^^^^^^^^^^^^^^^^^^^^^^

The OpenStack snap undergoes comprehensive automated testing:

Smoke tests
   Basic functionality validation of core OpenStack services

Regression tests
   Verification that existing functionality remains intact

Scale tests
   Performance and scalability validation under load

These automated tests run internally at Canonical before promotion to stable.
