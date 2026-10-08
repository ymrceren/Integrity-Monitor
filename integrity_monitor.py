
import hashlib
import json
from pathlib import Path

BASELINE_FILE = Path("baseline.json")
MONITOR_DIR = Path("monitored_files")


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(4096)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


def scan_files():
    file_hashes = {}

    for file_path in MONITOR_DIR.rglob("*"):
        if file_path.is_file():
            relative_path = str(file_path.relative_to(MONITOR_DIR))
            file_hashes[relative_path] = calculate_hash(file_path)

    return file_hashes


def save_baseline():
    hashes = scan_files()

    BASELINE_FILE.write_text(
        json.dumps(hashes, indent=4),
        encoding="utf-8"
    )

    print(f"Baseline saved for {len(hashes)} file(s).")


def check_integrity():
    if not BASELINE_FILE.exists():
        print("No baseline found. Create one first.")
        return

    original_hashes = json.loads(
        BASELINE_FILE.read_text(encoding="utf-8")
    )

    current_hashes = scan_files()

    added = current_hashes.keys() - original_hashes.keys()
    removed = original_hashes.keys() - current_hashes.keys()

    modified = [
        name
        for name in original_hashes.keys() & current_hashes.keys()
        if original_hashes[name] != current_hashes[name]
    ]

    print("\n=== Integrity Report ===")

    if not added and not removed and not modified:
        print("No changes detected.")
        return

    for name in sorted(added):
        print(f"[ADDED] {name}")

    for name in sorted(removed):
        print(f"[REMOVED] {name}")

    for name in sorted(modified):
        print(f"[MODIFIED] {name}")


def main():
    MONITOR_DIR.mkdir(exist_ok=True)

    print("=== File Integrity Monitor ===")
    print("1. Create baseline")
    print("2. Check integrity")

    choice = input("Select an option (1/2): ").strip()

    if choice == "1":
        save_baseline()
    elif choice == "2":
        check_integrity()
    else:
        print("Invalid option. Please select 1 or 2.")


if __name__ == "__main__":
    main()