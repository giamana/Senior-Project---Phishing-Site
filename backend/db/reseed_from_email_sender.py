import shutil
import os
from datetime import datetime

here = os.path.dirname(__file__)
DB = os.path.join(here, 'database.db')
if not os.path.exists(DB):
    raise SystemExit(f"Database not found: {DB}")

bak = os.path.join(here, f"database.db.reseed_from_module.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak")
shutil.copy2(DB, bak)
print(f"Backup created: {bak}")

import sqlite3
con = sqlite3.connect(DB)
cur = con.cursor()
cur.execute('DELETE FROM email_templates;')
con.commit()
print('Cleared email_templates table.')
con.close()

# Import and run the module's seeder
import importlib
email_sender = importlib.import_module('backend.db.email_sender')
# Call the function that inserts templates
email_sender.add_default_email_templates()

print('Re-seeded email_templates using backend.db.email_sender.add_default_email_templates()')
