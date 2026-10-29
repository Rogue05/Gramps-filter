# People with Event ID (Gramps filter rule)

A Gramps custom Person filter rule that finds **all people referenced by one
event**, irrespective of their event role (Primary, Witness, Godparent, etc.).

Enter the event's exact **Gramps ID** (for example, `E0012`). The rule resolves
that ID once at the start of a filter run and matches people whose event
references point to that event. It does not match by event type, description,
or internal database handle. An empty or unknown ID matches no people.

## Install with the Addon Manager

The repository provides Addon Manager listings and `.addon.tgz` packages for
Gramps 5.2, 6.0, and 6.1, following the versioned project layout used by the
[Emyoulation curated Gramps plug-ins](https://github.com/emyoulation/CuratedGrampsPlugins).

### Project URLs

Use the URL for your Gramps version:

| Gramps version | Project base URL (`Where to check`) | Listing URL (`Projects` tab) |
| --- | --- | --- |
| 5.2 | `https://raw.githubusercontent.com/Rogue05/Gramps-filter/main/gramps52` | `https://raw.githubusercontent.com/Rogue05/Gramps-filter/main/gramps52/listings/addons-en.json` |
| 6.0 | `https://raw.githubusercontent.com/Rogue05/Gramps-filter/main/gramps60` | `https://raw.githubusercontent.com/Rogue05/Gramps-filter/main/gramps60/listings/addons-en.json` |
| 6.1 | `https://raw.githubusercontent.com/Rogue05/Gramps-filter/main/gramps61` | `https://raw.githubusercontent.com/Rogue05/Gramps-filter/main/gramps61/listings/addons-en.json` |

In the Addon Manager **Projects** tab, add the matching **Listing URL** and
refresh the list. If configuring the older **Where to check** project setting,
use the **Project base URL** instead. Select **People with event ID** and
install it. Restart Gramps, then find the rule in the People custom filter
editor under **Event filters**.

If the addon is not visible, set the Addon Manager's status filter to **All
statuses**. For updates, refresh the project listing and install the offered
update.

### Manual installation

Alternatively, download `EventParticipantsById.addon.tgz` from the `download/`
folder for your Gramps version, then install that package using the Addon
Manager. The two plugin files can also be copied from
`source/EventParticipantsById/` into the Gramps user plugins directory.

An empty or unknown ID matches no people. The rule matches every person
referencing the event, regardless of role.

## Development

The plugin source is in `source/EventParticipantsById/`. To regenerate the
Addon Manager listings and packages after changing it, run:

```sh
python3 tools/build_addons.py
```

Compile-check the Python files with:

```sh
python3 -m py_compile source/EventParticipantsById/EventParticipantsById.py \
  source/EventParticipantsById/EventParticipantsById.gpr.py tools/build_addons.py
```

The runtime rule depends on Gramps and is intended to be loaded by Gramps'
Plugin Manager.

## License

This plugin is licensed under the GNU General Public License, version 2 or
(at your option) any later version. See [`LICENSE`](LICENSE).
