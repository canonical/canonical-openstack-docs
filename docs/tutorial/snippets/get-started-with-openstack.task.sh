# [docs-view:installation]
sudo snap install openstack
# [docs-view:installation-end]

# [docs-exec:installation]
sudo snap install openstack
# [docs-exec:installation-end]


# [docs-view:prepare-node-script]
sunbeam prepare-node-script --bootstrap | bash -x && newgrp snap_daemon
# [docs-view:prepare-node-script-end]

# [docs-exec:prepare-node-script]
sunbeam prepare-node-script --bootstrap | bash -x
# [docs-exec:prepare-node-script-end]


# [docs-view:bootstrap]
sunbeam cluster bootstrap --accept-defaults --role control,compute,storage
# [docs-view:bootstrap-end]

# [docs-exec:bootstrap]
sg snap_daemon 'sunbeam cluster bootstrap --accept-defaults --role control,compute'
# [docs-exec:bootstrap-end]


# [docs-view:configure]
sunbeam configure --accept-defaults --openrc demo-openrc
# [docs-view:configure-end]

# [docs-exec:configure]
sg snap_daemon 'sunbeam configure --accept-defaults --openrc demo-openrc'
# [docs-exec:configure-end]


# [docs-view:launch]
sunbeam launch ubuntu --name test
# [docs-view:launch-end]

# [docs-exec:launch]
sg snap_daemon 'sunbeam launch ubuntu --name test'
# [docs-exec:launch-end]


# [docs-view:ssh]
ssh -i /home/ubuntu/.config/openstack/sunbeam ubuntu@10.20.20.200
# [docs-view:ssh-end]
