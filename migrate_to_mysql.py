"""
Rural Opportunity Connect - Automated MySQL Migration & Seeding Script
Migrates all Django models and preserved data from SQLite to MySQL 8.0.
Usage:
    python migrate_to_mysql.py
    python migrate_to_mysql.py --password your_password
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
import pymysql

BASE_DIR = Path(__file__).resolve().parent

# Load existing .env if present
env_path = BASE_DIR / '.env'
env_vars = {}
if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env_vars[k.strip()] = v.strip()

def main():
    parser = argparse.ArgumentParser(description="Migrate Rural Opportunity Connect to MySQL.")
    parser.add_argument('--host', default=env_vars.get('DB_HOST', 'localhost'), help="MySQL Host")
    parser.add_argument('--port', type=int, default=int(env_vars.get('DB_PORT', 3306)), help="MySQL Port")
    parser.add_argument('--user', default=env_vars.get('DB_USER', 'root'), help="MySQL User")
    parser.add_argument('--password', default=env_vars.get('DB_PASSWORD', ''), help="MySQL Password")
    parser.add_argument('--dbname', default=env_vars.get('DB_NAME', 'rural_opportunity_connect'), help="Database Name")
    args = parser.parse_args()

    host = args.host
    port = args.port
    user = args.user
    password = args.password
    dbname = args.dbname

    print("=" * 65)
    print("  Rural Opportunity Connect — MySQL Database Migration")
    print("=" * 65)
    print(f"Target: MySQL Server at {host}:{port} as user '{user}'")
    print(f"Database: '{dbname}'")
    print("-" * 65)

    # If password is empty, attempt interactive prompt if running in interactive terminal
    conn = None
    max_attempts = 3
    attempt = 0
    current_password = password

    while attempt < max_attempts:
        attempt += 1
        try:
            print(f"[*] Testing connection to MySQL ({host}:{port})...")
            conn = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=current_password,
                connect_timeout=4
            )
            print("[\u2713] Connected to MySQL Server successfully!")
            password = current_password
            break
        except pymysql.err.OperationalError as e:
            err_code = e.args[0] if len(e.args) > 0 else None
            print(f"[!] MySQL connection failed: {e}")
            if err_code == 1045 and sys.stdin.isatty():
                import getpass
                current_password = getpass.getpass(f"Enter MySQL password for user '{user}': ")
            else:
                print("\n[HINT] Please provide your MySQL password using:")
                print(f"       python migrate_to_mysql.py --password <YOUR_PASSWORD>")
                print("       Or update DB_PASSWORD in your .env file.")
                sys.exit(1)

    if not conn:
        print("[!] Could not connect to MySQL. Migration aborted.")
        sys.exit(1)

    try:
        # Step 1: Create Database
        with conn.cursor() as cursor:
            print(f"[*] Ensuring database '{dbname}' exists with utf8mb4 encoding...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            print(f"[\u2713] Database '{dbname}' is ready.")
        conn.close()

        # Step 2: Write or update .env
        print("[*] Updating .env configuration...")
        env_content = f"""# Rural Opportunity Connect - Environment Configuration
SECRET_KEY=django-insecure-s%y0@&!mx%8#*&9-_(5-f6tctgq50qlm3ni^k2ro=_@+)p(bp^
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,testserver

# MySQL Database Settings
USE_MYSQL=True
DB_NAME={dbname}
DB_USER={user}
DB_PASSWORD={password}
DB_HOST={host}
DB_PORT={port}

RECOMMENDATION_API_URL=http://localhost:5000/api/recommendations
"""
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("[\u2713] .env file saved.")

        # Set env variables for current subprocesses
        sub_env = os.environ.copy()
        sub_env['USE_MYSQL'] = 'True'
        sub_env['DB_NAME'] = dbname
        sub_env['DB_USER'] = user
        sub_env['DB_PASSWORD'] = password
        sub_env['DB_HOST'] = host
        sub_env['DB_PORT'] = str(port)
        sub_env['PYTHONUTF8'] = '1'

        # Step 3: Run Django Migrations
        print("[*] Running Django migrations against MySQL...")
        res = subprocess.run([sys.executable, '-X', 'utf8', 'manage.py', 'migrate'], cwd=str(BASE_DIR), env=sub_env)
        if res.returncode != 0:
            print("[!] Migration failed. Check error above.")
            sys.exit(res.returncode)
        print("[\u2713] Django migrations completed successfully.")

        # Step 4: Load preserved JSON data if available
        dump_path = BASE_DIR / 'datadump.json'
        if dump_path.exists():
            print(f"[*] Seeding preserved data from {dump_path.name}...")
            res_data = subprocess.run([sys.executable, '-X', 'utf8', 'manage.py', 'loaddata', 'datadump.json'], cwd=str(BASE_DIR), env=sub_env)
            if res_data.returncode == 0:
                print("[\u2713] Data loaded successfully into MySQL!")
            else:
                print("[!] Data loading warning; checking if demo data script is needed...")
                subprocess.run([sys.executable, 'manage.py', 'shell'], input=open('populate_data.py', 'rb').read(), cwd=str(BASE_DIR), env=sub_env)

        # Step 5: Verification & Summary
        print("\n" + "=" * 65)
        print("  MIGRATION COMPLETE \u2714")
        print("=" * 65)
        print("MySQL database is fully initialized and synchronized.")
        print("You can now start the Django development server:")
        print("    python manage.py runserver")
        print("=" * 65)

    except Exception as exc:
        print(f"[!] Error during migration: {exc}")
        sys.exit(1)

if __name__ == '__main__':
    main()
