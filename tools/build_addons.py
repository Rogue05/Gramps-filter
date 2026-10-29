#!/usr/bin/env python3
"""Build Gramps Addon Manager listings and packages for supported versions."""

import json
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "EventParticipantsById"
VERSIONS = {
    "gramps52": "5.2",
    "gramps60": "6.0",
    "gramps61": "6.1",
}
LANGUAGES = ("da", "de", "en", "fi", "fr")
PACKAGE_NAME = "EventParticipantsById.addon.tgz"
PLUGIN_ID = "PeopleWithEventId"
PLUGIN_NAME = "People with event ID"
DESCRIPTION = (
    "Finds every person who participated in the event with the specified "
    "Gramps ID, regardless of their role."
)
HELP_URL = "https://github.com/Rogue05/Gramps-filter"
PACKAGE_FILES = (
    "EventParticipantsById.gpr.py",
    "EventParticipantsById.py",
    "README.md",
    "LICENSE",
)


def write_package(output_path):
    """Create a .addon.tgz archive with the addon in its own top-level folder."""
    with tarfile.open(output_path, "w:gz") as archive:
        for filename in PACKAGE_FILES:
            source_path = SOURCE / filename
            archive.add(source_path, arcname=f"EventParticipantsById/{filename}")


def listing_entry(gramps_version):
    """Return one Addon Manager listing record for the supported Gramps version."""
    return {
        "n": PLUGIN_NAME,
        "i": PLUGIN_ID,
        "t": 13,
        "d": DESCRIPTION,
        "v": "1.0.0",
        "g": gramps_version,
        "s": 3,
        "z": PACKAGE_NAME,
        "h": HELP_URL,
    }


def build_version(directory_name, gramps_version):
    """Write the version-specific download archive and listing files."""
    version_root = ROOT / directory_name
    download_dir = version_root / "download"
    listings_dir = version_root / "listings"
    download_dir.mkdir(parents=True, exist_ok=True)
    listings_dir.mkdir(parents=True, exist_ok=True)

    write_package(download_dir / PACKAGE_NAME)
    listing = [listing_entry(gramps_version)]
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
