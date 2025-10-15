# @depends: tutorial/snippets/get-started-with-openstack.task.sh

# [docs-view:enable-observability-external]
sunbeam enable observability external CONTROLLER GRAFANA_DASHBOARD_OFFER_URL PROMETHEUS_RECEIVE_REMOTE_WRITE_OFFER_URL LOKI_LOGGING_OFFER_URL
# [docs-view:enable-observability-external-end]


# [docs-view:disable-observability-external]
sunbeam disable observability external
# [docs-view:disable-observability-external-end]


# [docs-view:enable-observability-embedded]
sunbeam enable observability embedded
# [docs-view:enable-observability-embedded-end]

# [docs-exec:enable-observability-embedded]
sg snap_daemon 'sunbeam enable observability embedded'
# [docs-exec:enable-observability-embedded-end]


# [docs-view:disable-observability-embedded]
sunbeam disable observability embedded
# [docs-view:disable-observability-embedded-end]

# [docs-exec:disable-observability-embedded]
sg snap_daemon 'sunbeam disable observability embedded'
# [docs-exec:disable-observability-embedded-end]


# [docs-view:observability-dashboard-url]
sunbeam observability dashboard-url
# [docs-view:observability-dashboard-url-end]