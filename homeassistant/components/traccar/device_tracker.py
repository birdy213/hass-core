"""Support for Traccar device tracking."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from . import DOMAIN, TRACKER_UPDATE
from .const import (
    ATTR_ACCURACY,
    ATTR_ALTITUDE,
    ATTR_BATTERY,
    ATTR_BEARING,
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
    ATTR_SPEED,
    EVENT_ALARM,
    EVENT_ALL_EVENTS,
    EVENT_COMMAND_RESULT,
    EVENT_DEVICE_FUEL_DROP,
    EVENT_DEVICE_MOVING,
    EVENT_DEVICE_OFFLINE,
    EVENT_DEVICE_ONLINE,
    EVENT_DEVICE_OVERSPEED,
    EVENT_DEVICE_STOPPED,
    EVENT_DEVICE_UNKNOWN,
    EVENT_DRIVER_CHANGED,
    EVENT_GEOFENCE_ENTER,
    EVENT_GEOFENCE_EXIT,
    EVENT_IGNITION_OFF,
    EVENT_IGNITION_ON,
    EVENT_MAINTENANCE,
    EVENT_TEXT_MESSAGE,
)

_LOGGER = logging.getLogger(__name__)

DEFAULT_SCAN_INTERVAL = timedelta(seconds=30)
SCAN_INTERVAL = DEFAULT_SCAN_INTERVAL

EVENTS = [
    EVENT_DEVICE_MOVING,
    EVENT_COMMAND_RESULT,
    EVENT_DEVICE_FUEL_DROP,
    EVENT_GEOFENCE_ENTER,
    EVENT_DEVICE_OFFLINE,
    EVENT_DRIVER_CHANGED,
    EVENT_GEOFENCE_EXIT,
    EVENT_DEVICE_OVERSPEED,
    EVENT_DEVICE_ONLINE,
    EVENT_DEVICE_STOPPED,
    EVENT_MAINTENANCE,
    EVENT_ALARM,
    EVENT_TEXT_MESSAGE,
    EVENT_DEVICE_UNKNOWN,
    EVENT_IGNITION_OFF,
    EVENT_IGNITION_ON,
    EVENT_ALL_EVENTS,
]


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Configure a dispatcher connection based on a config entry."""

    @callback
    def _receive_data(device, latitude, longitude, battery, accuracy, attrs):
        """Receive set location."""
        if device in hass.data[DOMAIN]["devices"]:
            return

        hass.data[DOMAIN]["devices"].add(device)

        async_add_entities(
            [TraccarEntity(device, latitude, longitude, battery, accuracy, attrs)]
        )

    hass.data[DOMAIN]["unsub_device_tracker"][entry.entry_id] = (
        async_dispatcher_connect(hass, TRACKER_UPDATE, _receive_data)
    )

    # Restore previously loaded devices
    dev_reg = dr.async_get(hass)
    dev_ids = {
        identifier[1]
        for device in dev_reg.devices.get_devices_for_config_entry_id(entry.entry_id)
        for identifier in device.identifiers
    }
    if not dev_ids:
        return

    entities = []
    for dev_id in dev_ids:
        hass.data[DOMAIN]["devices"].add(dev_id)
        entity = TraccarEntity(dev_id, None, None, None, None, None)
        entities.append(entity)

    async_add_entities(entities)


class TraccarEntity(TrackerEntity, RestoreEntity):
    """Represent a tracked device."""

    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device, latitude, longitude, battery, accuracy, attributes):
        """Set up Traccar entity."""
        self._accuracy = accuracy
        self._attributes = attributes
        self._name = device
        self._battery = battery
        self._latitude = latitude
        self._longitude = longitude
        self._unsub_dispatcher = None
        self._unique_id = device

    @property
    def battery_level(self):
        """Return battery value of the device."""
        return self._battery

    @property
    def extra_state_attributes(self):
        """Return device specific attributes."""
        return self._attributes

    @property
    def latitude(self):
        """Return latitude value of the device."""
        return self._latitude

    @property
    def longitude(self):
        """Return longitude value of the device."""
        return self._longitude

    @property
    def location_accuracy(self):
        """Return the gps accuracy of the device."""
        return self._accuracy

    @property
    def unique_id(self):
        """Return the unique ID."""
        return self._unique_id

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            name=self._name,
            identifiers={(DOMAIN, self._unique_id)},
        )

    @property
    def source_type(self) -> SourceType:
        """Return the source type, eg gps or router, of the device."""
        return SourceType.GPS

    async def async_added_to_hass(self) -> None:
        """Register state update callback."""
        await super().async_added_to_hass()
        self._unsub_dispatcher = async_dispatcher_connect(
            self.hass, TRACKER_UPDATE, self._async_receive_data
        )

        # don't restore if we got created with data
        if self._latitude is not None or self._longitude is not None:
            return

        if (state := await self.async_get_last_state()) is None:
            self._latitude = None
            self._longitude = None
            self._accuracy = None
            self._attributes = {
                ATTR_ALTITUDE: None,
                ATTR_BEARING: None,
                ATTR_SPEED: None,
            }
            self._battery = None
            return

        attr = state.attributes
        self._latitude = attr.get(ATTR_LATITUDE)
        self._longitude = attr.get(ATTR_LONGITUDE)
        self._accuracy = attr.get(ATTR_ACCURACY)
        self._attributes = {
            ATTR_ALTITUDE: attr.get(ATTR_ALTITUDE),
            ATTR_BEARING: attr.get(ATTR_BEARING),
            ATTR_SPEED: attr.get(ATTR_SPEED),
        }
        self._battery = attr.get(ATTR_BATTERY)

    async def async_will_remove_from_hass(self) -> None:
        """Clean up after entity before removal."""
        await super().async_will_remove_from_hass()
        self._unsub_dispatcher()

    @callback
    def _async_receive_data(
        self, device, latitude, longitude, battery, accuracy, attributes
    ):
        """Mark the device as seen."""
        if device != self._name:
            return

        self._latitude = latitude
        self._longitude = longitude
        self._battery = battery
        self._accuracy = accuracy
        self._attributes.update(attributes)
        self.async_write_ha_state()
