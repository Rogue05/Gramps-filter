# People with Event ID (Gramps filter rule)

A Gramps custom Person filter rule that finds **all people referenced by one
event**, irrespective of their event role (Primary, Witness, Godparent, etc.).

Enter the event's exact **Gramps ID** (for example, `E0012`). The rule resolves
that ID once at the start of a filter run and matches people whose event
references point to that event. It does not match by event type, description,
or internal database handle. An empty or unknown ID matches no people.

## Install

The plugin is registered for Gramps 5.2, 6.0, and 6.1.

1. Clone or download this repository:

   ```sh
   git clone https://github.com/Rogue05/Gramps-filter.git
   ```

2. In Gramps, open **Edit → Preferences → Folders** and find the configured
   **User plugins** directory. Copy both `EventParticipantsById.py` and
   `EventParticipantsById.gpr.py` from the cloned repository into that
   directory (keep the two files together; do not copy the `.git` directory).
3. Restart Gramps so its Plugin Manager discovers the rule.
4. In the People view, create or edit a custom filter. Add **People with event
   ID** from **Event filters**, and enter the event's exact Gramps ID.

To update, pull the latest repository changes, copy the two plugin files into
the User plugins directory again, and restart Gramps.

An empty or unknown ID matches no people. The rule matches every person
referencing that event, regardless of their event role.

## Development

This repository is the plugin source. Compile-check the Python files with:

```sh
python3 -m py_compile EventParticipantsById.py EventParticipantsById.gpr.py
```

The runtime rule depends on Gramps and is intended to be loaded by Gramps'
Plugin Manager.

## License

This plugin is licensed under the GNU General Public License, version 2 or
(at your option) any later version. See [`LICENSE`](LICENSE).
