"""
Auto-Sync to Render Cloud
Rural Opportunity Connect - Automated Continuous Deployment Monitor

Monitors the repository for local changes (HTML templates, Python files, CSS/JS static assets).
When changes are detected:
  1. Debounces saves (waits 5 seconds for editing to finish)
  2. Runs git add -A
  3. Creates an automated timestamped commit
  4. Pushes to GitHub origin/main
  5. Render automatically deploys the update to:
     https://rural-opportunity-connect.onrender.com/
"""

import subprocess
import time
import sys
import os
from datetime import datetime

# Determine repository root
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
RENDER_URL = "https://rural-opportunity-connect.onrender.com/"
CHECK_INTERVAL_SECONDS = 5
DEBOUNCE_SECONDS = 5

def run_git(args):
    """Executes a git command inside the repository and returns (returncode, stdout, stderr)."""
    try:
        proc = subprocess.run(
            ["git"] + args,
            cwd=REPO_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def get_changed_files():
    """Returns list of changed files from git status porcelain."""
    code, out, err = run_git(["status", "--porcelain"])
    if code != 0:
        return []
    lines = [line.strip() for line in out.splitlines() if line.strip()]
    return lines

def sync_now(reason="Manual sync"):
    """Performs an immediate commit and push to GitHub."""
    changed = get_changed_files()
    if not changed:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Everything is already up-to-date. No changes detected.")
        print(f"Live website link: {RENDER_URL}\n")
        return False

    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Detected {len(changed)} changed file(s):")
    for f in changed[:10]:
        print(f"   * {f}")
    if len(changed) > 10:
        print(f"   * ... and {len(changed) - 10} more files")

    print("\nStaging changes (git add -A)...")
    run_git(["add", "-A"])

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = ", ".join([f.split()[-1] for f in changed[:3]])
    if len(changed) > 3:
        summary += f" and {len(changed) - 3} others"
    commit_msg = f"Auto-update: {summary} [{now_str}]"

    print(f"Creating commit: '{commit_msg}'...")
    code, out, err = run_git(["commit", "-m", commit_msg])
    if code != 0 and "nothing to commit" not in out.lower():
        print(f"[WARN] Commit message: {out or err}")

    print("Pushing to GitHub (origin/main)...")
    code, out, err = run_git(["push", "origin", "main"])
    if code == 0:
        print("=" * 65)
        print(" SUCCESS: Code pushed to GitHub origin/main!")
        print(f" Render is automatically rebuilding and updating:")
        print(f" >>> {RENDER_URL} <<<")
        print(" Your updates will be visible live in ~1-3 minutes.")
        print("=" * 65 + "\n")
        return True
    else:
        print(f"[ERROR] Failed to push to GitHub: {err}")
        print("Will retry on next detection cycle.\n")
        return False

def watch_loop():
    """Continuously monitors for file updates and automatically deploys."""
    print("=" * 65)
    print("  RURAL OPPORTUNITY CONNECT - AUTOMATIC CLOUD SYNC MONITOR")
    print("=" * 65)
    print(f" Repository: {REPO_DIR}")
    print(f" Target Link: {RENDER_URL}")
    print(f" Check Interval: {CHECK_INTERVAL_SECONDS}s | Debounce: {DEBOUNCE_SECONDS}s")
    print("\n Watching for file changes (Ctrl+C to stop)...")
    print(" Whenever you save any file, it will automatically push to Render!\n")

    while True:
        try:
            changed = get_changed_files()
            if changed:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Change detected in {len(changed)} file(s).")
                print(f"Waiting {DEBOUNCE_SECONDS}s for all file saves to complete...")
                time.sleep(DEBOUNCE_SECONDS)
                sync_now(reason="File change detected")
            
            time.sleep(CHECK_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print("\nAuto-sync monitor stopped by user.")
            break
        except Exception as e:
            print(f"[ERROR] Watcher error: {e}")
            time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    if "--now" in sys.argv or "--sync-now" in sys.argv:
        sync_now()
    else:
        watch_loop()
