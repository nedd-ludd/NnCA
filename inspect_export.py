#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2026-10-19
"""
from zipfile import ZipFile
from icalendar import Calendar
from pathlib import Path
import os
from collections import Counter
from datetime import date, datetime
marker = 'marker'


PROJECT_DIR = Path(__file__).resolve().parent
IMPORT_DIR = PROJECT_DIR / "data" / "imports"

# Locate the Nextcloud export without relying on its exact filename.
exports = list(IMPORT_DIR.glob("*.nextcloud_export"))

if len(exports) != 1:
    raise RuntimeError(
        f"Expected exactly one Nextcloud export, found {len(exports)}"
    )

with ZipFile(exports[0]) as archive:
    ics_data = archive.read("dav/calendars/personal.data")

calendar = Calendar.from_ical(ics_data)

events = [
    component
    for component in calendar.walk()
    if component.name == "VEVENT"
]

print(f"Export: {exports[0].name}")
print(f"Calendar events: {len(events)}")

if events:
    print(f"First event UID: {events[0].get('UID')}")

if events:
    event = events[0]

    print("Summary:", event.get("SUMMARY"))
    print("UID:", event.get("UID"))
    print("Start:", event.decoded("DTSTART"))
    print("End:", event.decoded("DTEND")
          if event.get("DTEND") else "Not specified")
    print("Recurrence rule:", event.get("RRULE"))


date_types = Counter()

for event in events:
    start = event.decoded("DTSTART")

    if isinstance(start, datetime):
        if start.tzinfo is not None:
            date_types["Timezone-aware datetime"] += 1
        else:
            date_types["Floating datetime"] += 1
    elif isinstance(start, date):
        date_types["All-day date"] += 1

print("\nEvent start formats:")
for kind, count in date_types.items():
    print(f"{kind}: {count}")

print(f"Total: {sum(date_types.values())}")


end_types = Counter()

for event in events:
    if event.get("DTEND") is not None:
        end_types["DTEND"] += 1
    elif event.get("DURATION") is not None:
        end_types["DURATION"] += 1
    else:
        end_types["Neither"] += 1

print("\nEvent end formats:")
for kind, count in end_types.items():
    print(f"{kind}: {count}")

print(f"Total: {sum(end_types.values())}")

uid_counts = Counter(str(event["UID"]) for event in events)

duplicate_uids = {
    uid: count
    for uid, count in uid_counts.items()
    if count > 1
}

print("\nUID inspection:")
print(f"Total event components: {len(events)}")
print(f"Unique UIDs: {len(uid_counts)}")
print(f"UIDs appearing more than once: {len(duplicate_uids)}")
print(
    f"Components with RECURRENCE-ID: {sum(1 for event in events if event.get('RECURRENCE-ID') is not None)}")
