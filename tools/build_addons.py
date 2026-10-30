#!/usr/bin/env python3
"""Build Gramps Addon Manager listings and packages for supported versions."""

import json
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSIONS = {
    "gramps52": "5.2",
    "gramps60": "6.0",
    "gramps61": "6.1",
}
LANGUAGES = ("da", "de", "en", "fi", "fr")
HELP_URL = "https://github.com/Rogue05/Gramps-filter"
ADDONS = (
    {
        "source": "EventParticipantsById",
        "package": "EventParticipantsById.addon.tgz",
        "id": "PeopleWithEventId",
        "name": "People with event ID",
        "type": 13,
        "description": (
            "Finds every person who participated in the event with the "
            "specified Gramps ID, regardless of their role."
        ),
        "files": (
            "EventParticipantsById.gpr.py",
            "EventParticipantsById.py",
            "README.md",
            "LICENSE",
        ),
    },
    {
        "source": "EventsByRole",
        "package": "EventsByRole.addon.tgz",
        "id": "eventsbyrole",
        "name": "Events by Role",
        "type": 8,
        "description": (
            "An Events view that displays participants in separate columns "
            "for each event role."
        ),
        "files": (
            "EventsByRole.gpr.py",
            "EventsByRole.py",
            "README.md",
            "LICENSE",
        ),
    },
)


def write_package(addon, output_path):
    """Create a .addon.tgz archive with the addon in its own top-level folder."""
    source = ROOT / "source" / addon["source"]
    with tarfile.open(output_path, "w:gz") as archive:
        for filename in addon["files"]:
            source_path = source / filename
            archive.add(source_path, arcname=f"{addon['source']}/{filename}")


def listing_entry(addon, gramps_version):
    """Return one Addon Manager listing record for the supported Gramps version."""
    return {
        "n": addon["name"],
        "i": addon["id"],
        "t": addon["type"],
        "d": addon["description"],
        "v": "1.0.0",
        "g": gramps_version,
        "s": 3,
        "z": addon["package"],
        "h": HELP_URL,
    }


def build_version(directory_name, gramps_version):
    """Write the version-specific download archive and listing files."""
    version_root = ROOT / directory_name
    download_dir = version_root / "download"
    listings_dir = version_root / "listings"
    download_dir.mkdir(parents=True, exist_ok=True)
    listings_dir.mkdir(parents=True, exist_ok=True)

    for addon in ADDONS:
        write_package(addon, download_dir / addon["package"])
    listing = [listing_entry(addon, gramps_version) for addon in ADDONS]
    for language in LANGUAGES:
        listing_path = listings_dir / f"addons-{language}.json"
        listing_path.write_text(
            json.dumps(listing, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )


def main():
    """Build listings and archives for every supported Gramps release."""
    for directory_name, gramps_version in VERSIONS.items():
        build_version(directory_name, gramps_version)
        print(f"Built {directory_name}/")


if __name__ == "__main__":
    main()
