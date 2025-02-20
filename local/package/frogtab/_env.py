from pathlib import Path
import sys
import os
import shutil
import subprocess

def config_path() -> Path:
    if os.getenv("FROGTAB_CONFIG_FILE"):
        config_path = Path(os.getenv("FROGTAB_CONFIG_FILE"))
    else:
        config_path = Path("Frogtab_config.json")
    if not config_path.is_file():
        try_migrate_legacy_config(config_path)
    return config_path

def try_migrate_legacy_config(target_config_path: Path) -> None:
    if not Path("config.py").is_file() or Path("migrated").exists():
        return
    # Move config.py to a dedicated subdir of the working dir
    shutil.copytree(Path(__file__).parent / "legacy", "migrated")
    shutil.move("config.py", "migrated")
    # Read config.py and create a JSON file
    config_path = Path("migrated") / "Frogtab_config.json"
    subprocess.run([
        "python",
        Path("migrated") / "migrate_config.py",
        config_path
    ])
    # Copy the JSON file to the correct location
    if config_path.is_file():
        shutil.copy(config_path, target_config_path)

def tick() -> str:
    display_tick = "✓"
    if use_color():
        return f"\033[32m{display_tick}\033[0m"  # Make it green
    else:
        return display_tick

def url(port: int) -> str:
    display_url = f"http://localhost:{port}"
    if use_color():
        return f"\033[96m{display_url}\033[0m"  # Make it bright cyan
    else:
        return display_url

def error() -> str:
    display_error = "Error:"
    if use_color():
        return f"\033[1;31m{display_error}\033[0m"  # Make it bold and red
    else:
        return display_error

def use_color() -> bool:
    return os.isatty(sys.stdout.fileno()) and not os.getenv("NO_COLOR")

def end() -> str:
    if os.isatty(sys.stdout.fileno()):
        return "\n"
    else:
        return ""

def task_or_exit() -> str:
    task = ""
    if os.isatty(sys.stdin.fileno()):
        print("Add a task to your inbox:")
        try:
            task = input("> ")
        except KeyboardInterrupt:
            sys.exit(130)
        except EOFError:
            print()
            sys.exit(2)
    else:
        task = sys.stdin.read()
    if not task:
        sys.exit(2)
    return task