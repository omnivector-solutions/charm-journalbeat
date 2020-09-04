#!/usr/bin/python3
"""FilebeatCharm."""
from elastic_ops_manager import ElasticOpsManager
from beats_requires import BeatsRequires
from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus

class JournalbeatCharm(CharmBase):
    """Filebeat charm."""
    stored = StoredState()

    def __init__(self, *args):
        """Initialize charm, configure states, and events to observe."""
        super().__init__(*args)
        self.filebeat_requires = BeatsRequires(self, "beats")
        self._elastic_ops_manager = ElasticOpsManager("journalbeat")
        self.stored.set_default(
            endpoint_address=None,
        )

        event_handler_bindings = {
            self.on.install: self._on_install,
            self.on.start: self._on_start,

        }
        for event, handler in event_handler_bindings.items():
            self.framework.observe(event, handler)

    def _on_install(self, event):
        resource = self.model.resources.fetch('elastic-resource')
        self._elastic_ops_manager.install(resource)
        self.unit.status = ActiveStatus("Journalbeat installed")

    def _on_start(self, event):
        self._elastic_ops_manager.start_elastic_service()
        self.unit.status = ActiveStatus("Journalbeat available")


if __name__ == "__main__":
    main(JournalbeatCharm)
