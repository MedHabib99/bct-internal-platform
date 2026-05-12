# Quick script to verify we have all needed files - run after manual creation
import os

apps = ['generalinfo', 'partners', 'news', 'events']
files = ['__init__.py', 'apps.py', 'models.py', 'admin.py', 'views.py', 'urls.py', 'tests.py', 'migrations/__init__.py']

print("Checking app structure...")
for app in apps:
    print(f"\n{app}:")
    for file in files:
        path = os.path.join(app, file)
        exists = os.path.exists(path)
        status = "✓" if exists else "✗"
        print(f"  {status} {file}")

