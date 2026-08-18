# @depends: tutorial/snippets/get-started-with-openstack.task.sh

# [docs-view:enable-orchestration]
sunbeam enable orchestration
# [docs-view:enable-orchestration-end]

# [docs-exec:enable-orchestration]
sg snap_daemon 'sunbeam enable orchestration'
# [docs-exec:enable-orchestration-end]


# [docs-view:disable-orchestration]
sunbeam disable orchestration
# [docs-view:disable-orchestration-end]

# [docs-exec:disable-orchestration]
sg snap_daemon 'sunbeam disable orchestration'
# [docs-exec:disable-orchestration-end]
