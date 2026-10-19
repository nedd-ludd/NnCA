from pathlib import Path
from zipfile import ZipFile
import sqlite3

from icalendar import Calendar


PROJECT_DIR = Path(__file__).resolve().parent

DATABASE_PATH = PROJECT_DIR / "data" / "calendar.db"
IMPORT_DIR = PROJECT_DIR / "data" / "imports"


def import_calendar():
    # Find the Nextcloud export.
    exports = list(IMPORT_DIR.glob("*.nextcloud_export"))

    if len(exports) != 1:
        raise RuntimeError(
            f"Expected exactly one Nextcloud export, found {len(exports)}"
        )

    # Read the calendar from the ZIP archive.
    with ZipFile(exports[0]) as archive:
        ics_data = archive.read("dav/calendars/personal.data")

    calendar = Calendar.from_ical(ics_data)

    events = [
        component
        for component in calendar.walk()
        if component.name == "VEVENT"
    ]

    # Connect to our existing SQLite database.
    if not DATABASE_PATH.is_file():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}. Run init_db.py first."
        )
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON;")

        # Create the calendar record if it does not already exist.
        existing = connection.execute(
            "SELECT id FROM calendars WHERE name = ?",
            ("Personal",)
        ).fetchone()

        if existing:
            calendar_id = existing[0]
            print(f"Existing calendar found (ID: {calendar_id})")
        else:
            cursor = connection.execute(
                """
                INSERT INTO calendars (name, timezone)
                VALUES (?, ?)
                """,
                ("Personal", "Europe/London")
            )
            calendar_id = cursor.lastrowid
            print(f"Created Personal calendar (ID: {calendar_id})")

        # TEST: Import only the first event.
        event = events[0]

        uid = str(event["UID"])
        summary = str(event.get("SUMMARY", ""))
        start = event.decoded("DTSTART")
        end = event.decoded("DTEND")

        # Preserve the original VEVENT component.
        original_ics = event.to_ical().decode("utf-8")

        # Convert timezone-aware datetimes to UTC timestamps.
        from datetime import timezone

        start_utc = int(start.astimezone(timezone.utc).timestamp())
        end_utc = int(end.astimezone(timezone.utc).timestamp())

        cursor = connection.execute(
            """
            INSERT OR IGNORE INTO events (
                calendar_id,
                uid,
                summary,
                time_kind,
                start_value,
                end_value,
                timezone,
                original_ics
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                calendar_id,
                uid,
                summary,
                "ZONED",
                start.isoformat(),
                end.isoformat(),
                str(start.tzinfo),
                original_ics
            )
        )

        if cursor.rowcount == 1:
            print(f"Imported test event: {summary}")
        else:
            print(f"Test event already exists: {summary}")
        tables = connection.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'"
        ).fetchone()[0]

        print(f"Connected to: {DATABASE_PATH.name}")
        print(f"Database tables found: {tables}")
        print(f"Events ready to import: {len(events)}")

    




if __name__ == "__main__":
    import_calendar()
