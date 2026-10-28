# @depends: tutorial/snippets/get-started-with-openstack.task.sh

# [docs-view:enable-loadbalancer]
sunbeam enable loadbalancer
# [docs-view:enable-loadbalancer-end]

# [docs-exec:enable-loadbalancer]
sg snap_daemon 'sunbeam enable loadbalancer'
# [docs-exec:enable-loadbalancer-end]

# [docs-view:disable-loadbalancer]
sunbeam disable loadbalancer
# [docs-view:disable-loadbalancer-end]

# [docs-exec:disable-loadbalancer]
sg snap_daemon 'sunbeam disable loadbalancer'
# [docs-exec:disable-loadbalancer-end]
