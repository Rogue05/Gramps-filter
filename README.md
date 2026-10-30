# Gramps Event Add-ons

This repository provides two Gramps add-ons:

- **People with event ID** — a Person filter rule that finds all people
  referenced by an event ID, regardless of their event role.
- **Events by Role** — an alternate Events view that gives each standard and
  tree-specific custom event role its own column, including both people and
  families.

The Events by Role view shows one event per row. Participants in a role column
are separated by semicolons. The standard Events view remains available.

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
use the **Project base URL** instead. Select **People with event ID** and/or
**Events by Role** and install them. Restart Gramps to use the add-ons.

The filter rule is available in the People custom-filter editor under
**Event filters**. **Events by Role** appears as an alternate view mode in the
Events category.

If the addon is not visible, set the Addon Manager's status filter to **All
statuses**. For updates, refresh the project listing and install the offered
update.

### Manual installation

Alternatively, download either add-on's `.addon.tgz` package from the
`download/` folder for your Gramps version, then install it using the Addon
Manager. The plugin files can also be copied from the corresponding `source/`
subdirectory into the Gramps user plugins directory.

An empty or unknown ID matches no people. The rule matches every person
referencing the event, regardless of role.

## Development

The plugin sources are in `source/`. To regenerate the Addon Manager listings
and packages after changing either add-on, run:

```sh
python3 tools/build_addons.py
```

Compile-check the Python files with:

```sh
python3 -m py_compile \
  source/EventParticipantsById/EventParticipantsById.py \
  source/EventParticipantsById/EventParticipantsById.gpr.py \
  source/EventsByRole/EventsByRole.py \
  source/EventsByRole/EventsByRole.gpr.py \
  tools/build_addons.py
```

The runtime rule depends on Gramps and is intended to be loaded by Gramps'
Plugin Manager.

## License

This plugin is licensed under the GNU General Public License, version 2 or
(at your option) any later version. See [`LICENSE`](LICENSE).
