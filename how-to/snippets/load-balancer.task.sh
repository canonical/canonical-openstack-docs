# @depends: tutorial/snippets/get-started-with-openstack.task.sh

# [docs-view:enable-load-balancer]
sunbeam enable load-balancer
# [docs-view:enable-load-balancer-end]

# [docs-exec:enable-load-balancer]
sg snap_daemon 'sunbeam enable load-balancer'
# [docs-exec:enable-load-balancer-end]

# [docs-view:disable-load-balancer]
sunbeam disable load-balancer
# [docs-view:disable-load-balancer-end]

# [docs-exec:disable-load-balancer]
sg snap_daemon 'sunbeam disable load-balancer'
# [docs-exec:disable-load-balancer-end]
