import logging
from ops.framework import (
    EventBase,
    EventSource,
    Object,
    ObjectEvents,
    StoredState,
)

logger = logging.getLogger()


class EndpointAvailableEvent(EventBase):
    """Emitted when a node joins the elasticsearch cluster."""


class ElasticEvents(ObjectEvents):
    """Interface events."""

    endpoint_available = EventSource(EndpointAvailableEvent)


class BeatsRequires(ObjectEvents):
    """Peer relation interface for elasticsearch."""

    on = ElasticEvents()

    def __init__(self, charm, relation_name):
        """Handle relation events."""
        super().__init__(charm, relation_name)

        self.charm = charm
        event_handler_bindings = {
            charm.on[relation_name].relation_created:
            self._on_relation_created,

            charm.on[relation_name].relation_joined:
            self._on_relation_joined,

            charm.on[relation_name].relation_changed:
            self._on_relation_changed,

            charm.on[relation_name].relation_departed:
            self._on_relation_departed,

            charm.on[relation_name].relation_broken:
            self._on_relation_broken,
        }
        for event, handler in event_handler_bindings.items():
            self.framework.observe(event, handler)

    def _on_relation_created(self, event):
        logger.debug("################ LOGGING RELATION CREATED ####################")

    def _on_relation_joined(self, event):
        logger.debug("################ LOGGING RELATION JOINED ####################")

    def _on_relation_changed(self, event):
        logger.debug("################ LOGGING RELATION CHANGED ####################")
        port = event.relation.data[event.unit].get('port', None)
        host = event.relation.data[event.unit].get('ingress-address')
        self.charm.stored.output_address = f'http://{host}:{port}'
        self.on.endpoint_available.emit()

    def _on_relation_departed(self, event):
        logger.debug("################ LOGGING RELATION DEPARTED ####################")

    def _on_relation_broken(self, event):
        logger.debug("################ LOGGING RELATION BROKEN ####################")
