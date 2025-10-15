# @depends: tutorial/snippets/get-started-with-openstack.task.sh

# [docs-view:enable-images-sync]
sunbeam enable images-sync
# [docs-view:enable-images-sync-end]

# [docs-exec:enable-images-sync]
sg snap_daemon 'sunbeam enable images-sync'
# [docs-exec:enable-images-sync-end]


# [docs-view:disable-images-sync]
sunbeam disable images-sync
# [docs-view:disable-images-sync-end]

# [docs-exec:disable-images-sync]
sg snap_daemon 'sunbeam disable images-sync'
# [docs-exec:disable-images-sync-end]
