Stable release process
======================

Key Steps at Each Stage
-----------------------

Rocks
+++++

Currently, the rocks are published directly to the registry when a modification is made.
The Rocks mono-repository is maintains a stable branch from which new rocks are built and published.

The process is as follows:

* **backport**: A backport is proposed to the stable branch.
* **approval**: The change is reviewed and approved.
* **build**: A GitHub action automatically builds and publishes the rock to the registry.

.. note::

    A rock is not automatically re-assigned to a charm version, the associated charms must be re-built and published to the charm store.

Snaps
+++++

Snaps are automatically built every 5 hours when there are changes and published to the related edge channel. Promotion to stable channels is done manually after validation.

The process is as follows:

* **backport**: A backport is proposed to the stable branch
* **approval**: The change is reviewed and approved.
* **build**: Launchpad builds the snap and publishes it to the edge channel. (There might be a delay of up to 5 hours)
* **testing**: The snap is tested in the edge channel.
* **promote**:
    * If the snap passes testing, it is promoted to the beta channel.
    * If the snap passes testing in the beta channel, it is promoted to the candidate channel.
    * If the snap passes testing in the candidate channel, it is promoted to the stable channel.

Charms
++++++

Charms are automatically built and published to the charm store on each and every commit.

The process is as follows:

* **backport**: A change is proposed to be backported to the stable branch.
* **approval**: The change is reviewed and approved.
* **build**: OpenDev CI builds the charm and publishes to the edge channel.
* **testing**: The charm is tested in the edge channel.
* **promote**:
    * If the charm passes testing, it is promoted to the beta channel.
    * If the charm passes testing in the beta channel, it is promoted to the candidate channel.
    * If the charm passes testing in the candidate channel, it is promoted to the stable channel.

To mass release charms, the following tool is used: `sunbeam-release <https://github.com/openstack-charmers/sunbeam-release>`_.

OpenStack Snap
++++++++++++++

.. note::

        The OpenStack snap is the main entry point for users to deploy and manage Canonical OpenStack. It integrates various components, including charms and payloads.
        It is the central piece driving most of the testing of the many pieces composing Canonical OpenStack.

The OpenStack snap is built and published to the snap store every 5 hours when there are changes, and it is promoted to stable channels manually after validation.

The process is as follows:

* **backport**: A change is proposed to be backported to the stable branch.
* **approval**: The change is reviewed and approved.
* **testing**: The change is tested in the edge channel.
* **promote**:
    * If the change passes testing, it is promoted to the beta channel.
    * If the change passes testing in the beta channel, it is promoted to the candidate channel.
    * There are automated internal tests run internally at Canonical to validate: smoke, regression and scale tests.
    * If the change passes all tests, it is promoted to the stable channel.
