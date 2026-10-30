#
# Gramps - a GTK+/GNOME based genealogy program
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#

"""An Events-category view that separates participants into role columns."""

from gramps.gen.const import GRAMPS_LOCALE as glocale
from gramps.gen.display.name import displayer as name_displayer
from gramps.gen.config import config
from gramps.gen.lib import EventRoleType
from gramps.gen.utils.db import family_name
from gramps.gen.utils.lru import LRU
from gramps.gui.views.listview import ListView, TEXT
from gramps.gui.views.treemodels.eventmodel import EventModel
from gramps.gui.views.treemodels.flatbasemodel import FlatBaseModel
from gramps.plugins.view.eventview import (
    EventBookmarks,
    EventSidebarFilter,
    EventView,
)

_ = glocale.translation.sgettext


def get_role_columns(db):
    """Return every standard and tree-specific custom role, in stable order."""
    roles = []
    seen = set()

    for value in sorted(EventRoleType._I2EMAP):
        if value == EventRoleType._CUSTOM:
            continue
        role = EventRoleType(value)
        role_key = role.xml_str()
        if role_key and role_key not in seen:
            roles.append((role_key, str(role)))
            seen.add(role_key)

    try:
        custom_roles = db.get_event_roles()
    except AttributeError:
        custom_roles = []

    for role_key in sorted(custom_roles, key=glocale.sort_key):
        if role_key and role_key not in seen:
            roles.append((role_key, role_key))
            seen.add(role_key)

    return roles


class EventsByRoleModel(EventModel):
    """Event model with one participant-name column for each role."""

    def __init__(
        self,
        db,
        uistate,
        role_keys,
        scol=0,
        order=None,
        search=None,
        skip=set(),
        sort_map=None,
    ):
        from gi.repository import Gtk

        if order is None:
            order = Gtk.SortType.ASCENDING

        self.role_keys = tuple(role_keys)
        self.role_cache = LRU(config.get("interface.treemodel-cache-size"))
        self.gen_cursor = db.get_event_cursor
        self.map = db.get_raw_event_data
        self.fmap = [
            self.column_description,
            self.column_id,
            self.column_type,
            self.column_date,
            self.column_place,
            self.column_private,
            self.column_tags,
            self.column_change,
        ]
        self.fmap.extend(
            lambda data, role_key=role_key: self.column_role_participants(
                data, role_key
            )
            for role_key in self.role_keys
        )
        self.fmap.append(self.column_tag_color)

        self.smap = [
            self.column_description,
            self.column_id,
            self.column_type,
            self.sort_date,
            self.column_place,
            self.column_private,
            self.column_tags,
            self.sort_change,
        ]
        self.smap.extend(
            lambda data, role_key=role_key: self.column_role_participants(
                data, role_key
            )
            for role_key in self.role_keys
        )
        self.smap.append(self.column_tag_color)

        FlatBaseModel.__init__(
            self,
            db,
            uistate,
            scol,
            order,
            search=search,
            skip=skip,
            sort_map=sort_map,
        )

    def color_column(self):
        """Return the hidden tag-color model column."""
        return len(self.fmap) - 1

    def column_role_participants(self, data, role_key):
        """Return sorted, joined participant names for one role and event."""
        if data.handle not in self.role_cache:
            self.role_cache[data.handle] = self._participants_by_role(data.handle)
        participants = self.role_cache[data.handle]
        return participants.get(role_key, "")

    def update_row_by_handle(self, handle):
        """Invalidate participant data when an event row is refreshed."""
        if handle in self.role_cache:
            del self.role_cache[handle]
        super().update_row_by_handle(handle)

    def _participants_by_role(self, event_handle):
        """Build the per-event role-to-participant display mapping."""
        by_role = {}
        for class_name, handle in self.db.find_backlink_handles(
            event_handle, include_classes=["Person", "Family"]
        ):
            if class_name == "Person":
                participant = self.db.get_person_from_handle(handle)
                if participant is None:
                    continue
                name = name_displayer.display(participant)
            else:
                participant = self.db.get_family_from_handle(handle)
                if participant is None:
                    continue
                name = family_name(participant, self.db)

            for event_ref in participant.get_event_ref_list():
                if event_ref.ref == event_handle:
                    role_key = event_ref.get_role().xml_str()
                    by_role.setdefault(role_key, {})[(class_name, handle)] = name

        return {
            role_key: "; ".join(sorted(names.values(), key=glocale.sort_key))
            for role_key, names in by_role.items()
        }

    def destroy(self):
        """Release role data cached by this model."""
        self.role_cache = None
        super().destroy()


class EventsByRoleView(EventView):
    """Alternate Events view showing participants grouped by event role."""

    def __init__(self, pdata, dbstate, uistate, nav_group=0):
        self.roles = get_role_columns(dbstate.db)
        self.role_keys = tuple(role_key for role_key, _label in self.roles)
        self.COLUMNS = list(EventView.COLUMNS[:8]) + [
            (label, TEXT, None) for _role_key, label in self.roles
        ]

        self.CONFIGSETTINGS = self._column_config_settings()

        signal_map = {
            "event-add": self.row_add,
            "event-update": self.row_update,
            "event-delete": self.row_delete,
            "event-rebuild": self.object_build,
            "person-update": self.person_update,
            "person-add": self.person_update,
            "person-delete": self.object_build,
            "family-update": self.family_update,
            "family-add": self.family_update,
            "family-delete": self.object_build,
            "place-update": self.related_update,
        }

        ListView.__init__(
            self,
            _("Events by Role"),
            pdata,
            dbstate,
            uistate,
            self._make_model,
            signal_map,
            EventBookmarks,
            nav_group,
            multiple=True,
            filter_class=EventSidebarFilter,
        )

        if self._config.get("columns.rolekeys") != list(self.role_keys):
            self._reset_column_config()

        uistate.connect("nameformat-changed", self.build_tree)
        uistate.connect("placeformat-changed", self.build_tree)
        self.additional_uis.append(self.additional_ui)

    def _column_config_settings(self):
        """Return defaults for the current set of dynamic role columns."""
        indexes = list(range(len(self.COLUMNS)))
        sizes = [150, 80, 110, 140, 150, 35, 140, 120] + [160] * len(self.roles)
        return (
            ("columns.visible", indexes),
            ("columns.rank", indexes),
            ("columns.size", sizes),
            ("columns.rolekeys", list(self.role_keys)),
        )

    def _make_model(
        self,
        db,
        model_uistate,
        scol=0,
        order=None,
        search=None,
        skip=set(),
        sort_map=None,
    ):
        """Create a model using the view's current role columns."""
        return EventsByRoleModel(
            db,
            model_uistate,
            self.role_keys,
            scol=scol,
            order=order,
            search=search,
            skip=skip,
            sort_map=sort_map,
        )

    def _reset_column_config(self):
        """Reset stored column ordering if the role set has changed."""
        settings = dict(
            (name, value) for name, value in self._column_config_settings()
        )
        for name, value in settings.items():
            self._config.set(name, value)

    def _refresh_role_columns(self):
        """Rebuild the view if custom roles were added or removed."""
        roles = get_role_columns(self.dbstate.db)
        role_keys = tuple(role_key for role_key, _label in roles)
        if role_keys == self.role_keys:
            return False

        self.roles = roles
        self.role_keys = role_keys
        self.COLUMNS = list(EventView.COLUMNS[:8]) + [
            (label, TEXT, None) for _role_key, label in roles
        ]
        self._reset_column_config()
        self.dirty = True
        if self.active:
            self.build_tree(preserve_col=False)
        return True

    def person_update(self, handle_list):
        """Refresh role columns and affected events after person changes."""
        if not self._refresh_role_columns():
            EventView.person_update(self, handle_list)

    def family_update(self, handle_list):
        """Refresh role columns and affected events after family changes."""
        if not self._refresh_role_columns():
            EventView.family_update(self, handle_list)

    def get_config_name(self):
        """Keep this view's column settings separate from the standard view."""
        return __name__
