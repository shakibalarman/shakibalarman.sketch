import os
import json
import subprocess
import sys
import time
from datetime import datetime, timedelta

# ============================================
# GitHub Contribution Graph Hack
#
# Created by Aononto Jahan
# GitHub: https://github.com/aonontojahan
#
# If you like this project, give it a ⭐
# ============================================

PATTERN_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "pattern.json"))
FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "info.txt"))

COMMITS_PER_PIXEL = 5   # lighter than darkest green


# -------------------------------
# Loading Animation (3 seconds)
# -------------------------------
def loading_animation(duration=3):
    animation = "|/-\\"
    end_time = time.time() + duration
    i = 0

    sys.stdout.write("\nInitializing GitHub Pattern Committer ")
    sys.stdout.flush()

    while time.time() < end_time:
        sys.stdout.write(animation[i % len(animation)])
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("\b")
        i += 1

    print("☑️")


# -------------------------------
# Credit Banner (Start)
# -------------------------------
def show_start_credit():
    print(r"""
          
┏┓• ┓┏  ┓   ┏┓        •   ┓   ┓ 
┃┓┓╋┣┫┓┏┣┓  ┃ ┏┓┏┳┓┏┳┓┓╋  ┃ ┏┓┣┓
┗┛┗┗┛┗┗┻┗┛  ┗┛┗┛┛┗┗┛┗┗┗┗  ┗┛┗┻┗┛                       

Created by Shakib Al Arman
GitHub: https://github.com/shakibalarman
----------------------------------------
""")


# -------------------------------
# Credit Banner (End)
# -------------------------------
def show_end_credit():
    print(r"""
          
┳┳┓┳┏┓┏┓┳┏┓┳┓  ┏┓┏┓┏┓┏┓┏┓┳┓  ╻
┃┃┃┃┗┓┗┓┃┃┃┃┃  ┃┃┣┫┗┓┗┓┣ ┃┃  ┃
┛ ┗┻┗┛┗┛┻┗┛┛┗  ┣┛┛┗┗┛┗┛┗┛┻┛  •
                                                        

☑️ History Has Been Rewritten.  
☑️ The Timeline Has Changed.
☑️ Success! Pretend This Was Hard.           

----------------------------------------
⭐ If you like this project, give it a star on GitHub!
👉 https://github.com/shakibalarman

Made with ❤️  by Shakib Al Arman
----------------------------------------
""")



# -------------------------------
# Git Commit (FIXED)
# -------------------------------
def git_commit(message, commit_date):
    subprocess.run(["git", "add", FILE_PATH], check=True)

    env = os.environ.copy()
    date_str = commit_date.strftime("%Y-%m-%dT12:00:00")

    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str

    subprocess.run(
        [
            "git",
            "commit",
            "--allow-empty",   # ✅ FIX: allows commit even if no file changes
            "-m",
            message,
            "--date",
            date_str
        ],
        env=env,
        check=True
    )

    print(f"{message} successful ✔️")
    print(f"{message} successful ✔️")


def git_push():
    try:
        subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True)
        print("✅ Pushed to origin/main successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Push failed (code {e.returncode}).")
        print("💡 Check: git status, auth (token?), upstream.")
        print("💡 Manual: git push origin main")
        print("💡 Auth help: https://github.com/settings/tokens")


def ensure_git_repo():
    """Initialize git repo if it doesn't exist."""
    try:
        subprocess.check_output(["git", "rev-parse", "--git-dir"], stderr=subprocess.DEVNULL)
        print("✅ Git repository already exists.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ No git repository found. Initializing...")
        subprocess.run(["git", "init"], check=True)
        print("✅ Initialized new git repository.")
        print("💡 Tip: Set remote with: git remote add origin <your-repo-url>")

def ensure_git_remote():
    """Ensure origin remote exists, prompt user if missing."""
    try:
        result = subprocess.check_output(["git", "remote"], stderr=subprocess.DEVNULL, text=True)
        if "origin" not in result:
            print("⚠️ No 'origin' remote found. Setting up...")
            repo_url = input("Enter GitHub repo URL (e.g. https://github.com/user/repo.git): ").strip()
            if repo_url:
                subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
                print("✅ Added origin remote.")
            else:
                print("❌ No URL provided. Push skipped later.")
                return False
        else:
            print("✅ Origin remote already configured.")
        return True
    except subprocess.CalledProcessError:
        print("❌ Git remote check failed.")
        return False


def load_pattern():
    if not os.path.exists(PATTERN_FILE):
        print(f"⚠️ {PATTERN_FILE} missing. Creating default pattern...")
        default_pattern = [
            "3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3",
            " 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 ",
            "3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3",
            " 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 ",
            "3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3",
            " 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 ",
            "3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3"
        ]
        with open(PATTERN_FILE, "w") as f:
            json.dump(default_pattern, f)
    try:
        with open(PATTERN_FILE, "r") as f:
            pattern = json.load(f)
        if not isinstance(pattern, list) or len(pattern) != 7:
            raise ValueError("Invalid pattern format: must be 7 weekly rows")
        print(f"✅ Loaded pattern: {sum(sum(1 for c in row if c != ' ') for row in pattern)} pixels")
        return pattern
    except Exception as e:
        raise ValueError(f"Failed to load/create pattern: {e}")


def first_sunday(year):
    d = datetime(year, 1, 1)
    while d.weekday() != 6:  # Sunday
        d += timedelta(days=1)
    return d


def make_commits_from_pattern(year):
    pattern = load_pattern()
    ensure_git_repo()
    if ensure_git_remote():
        print("🚀 Ready for commits and push.")
    else:
        print("⚠️ Remote issue - commits will run but push may fail.")
    start_date = first_sunday(year)

    for row_idx, row in enumerate(pattern):
        for col_idx, char in enumerate(row):
            if char == " ":
                continue  # empty pixel

            commit_date = start_date + timedelta(
                weeks=col_idx,
                days=row_idx
            )

            for i in range(1, COMMITS_PER_PIXEL + 1):
                msg = f"{commit_date.date()} pixel commit {i}"

                with open(FILE_PATH, "w") as f:
                    f.write(msg)

                git_commit(msg, commit_date)

    git_push()


# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    loading_animation(3)
    show_start_credit()

    year = int(input("👉 Enter year to draw pattern 📆 ➤ "))
    make_commits_from_pattern(year)

    show_end_credit()
