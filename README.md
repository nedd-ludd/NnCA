# NnCA
Local AI Hosting and Calendar Assistant

## INTRODUCTION

## PACKAGES
icalendar

## CONTENTS

Steps
Initial research
Watched Youtube vid
Planned to build without VRAM
Slowly bought components as could afford

Approach - Keep notes throughout the project, treat everything as a learning exercise. Consistently push to github and manage version.

## BUILD COSTS / EQUIPMENT

The initial AI rig uses the Ryzen 9 7900X's integrated graphics. A dedicated GPU has not yet been purchased and is excluded from the total.

| Component | Description | Condition | Supplier | Cost (£) |
|---|---|---|---|---:|
| Case | Tonysa DIY Computer Motherboard Case Rack, Open Frame ATX | New | Amazon | £46.49 |
| CPU Cooler | Thermalright Phantom Spirit 120 SE CPU Air Cooler | New | Amazon | £29.09 |
| PSU | Corsair CX750 80 PLUS Bronze 750W Power Supply | Used | Amazon | £48.49 |
| CPU | AMD Ryzen 9 7900X, 12 Cores / 24 Threads, Integrated Radeon Graphics | New | Amazon | £291.00 |
| Motherboard | Gigabyte B650 EAGLE AX AM5 Motherboard | New | Amazon | £119.19 |
| RAM | Kingston FURY Beast RGB 32GB (2 × 16GB), 6000MT/s | New | CCL Online | £178.94 |
| Storage | Kingston NV2 250GB M.2 NVMe PCIe 4.0 SSD | New | eBay | £40.00 |
| Power Switch | LED Power Button Switch Extension Cable | New | eBay | £4.94 |
| Dedicated GPU / VRAM | Not yet purchased | — | — | Excluded |
| **Total (without dedicated GPU)** | | | | **£758.14** |

18/10/2026
Investigated last bits of componants and ordered
Installed Ubuntu server LTS on flash drive ready for boot
Exported personal nextcloud to machine for review
Looked at RFC RFC 5545

19/10/2026
File and version management, created git repo, pulled, pushed back readme with build costs to check
Environment tasks, gitignore, venv for python, hello world with test.py file
DB:
- Verify SQLite workd in env
```
python -c "import sys, sqlite3; print('Python:', sys.executable); print('SQLite:', sqlite3.sqlite_version)"
```


### Initial Calendar Database Development

The calendar assistant uses **SQLite** as its local database, with Python providing the interface for database operations and, eventually, AI function calling.

| File | Purpose |
|---|---|
| `schema.sql` | Defines the database structure: tables, columns, relationships, constraints and indexes. |
| `init_db.py` | Reads and executes `schema.sql` to initialise the database. |
| `data/calendar.db` | The actual SQLite database containing calendar records. Excluded from Git. |
| `calendar_crud.py` *(planned)* | Python functions for creating, reading, updating and deleting calendar records. |

I can then Import my calenda from nextcloud to see what matches and what doesnt

