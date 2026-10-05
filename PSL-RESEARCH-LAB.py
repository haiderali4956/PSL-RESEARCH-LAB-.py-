import os
import json
from pathlib import Path
from datetime import datetime

data_folder = Path("data")
reports_folder = data_folder / "reports"
matches_file = data_folder / "matches.json"
config_file = data_folder / "config.json"
log_file = data_folder / "activity_log.json"

default_config = {
    "project name": "PSL Research Lab",
    "version": "2.0",
    "seed": 42,
    "max overs": 20,
    "max wickets": 10
}


def js_dump(path, upcoming_data):
    # pehle temp file mai likhte hain taa ke file kabhi adhi na rahe
    temp_path = str(path) + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(upcoming_data, f, indent=4, ensure_ascii=False)
    os.replace(temp_path, path)


def js_load(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{path}.corrupt_{stamp}.bak"
        os.replace(path, backup_path)
        print(f'{path} corrupt thi, backup ban gya : {backup_path}')
        return default


def folders_check():
    os.makedirs(data_folder, exist_ok=True)
    reports_folder.mkdir(parents=True, exist_ok=True)
    for path, default in ((config_file, default_config), (matches_file, []), (log_file, [])):
        data = js_load(path, default)
        js_dump(path, data)
    print('Data folder ready. | Reports folder ready. | Configuration loaded. | Matches JSON ready. | Activity log ready.')


def matches_load():
    return js_load(matches_file, [])


def matches_save(upcoming_list):
    js_dump(matches_file, upcoming_list)
    print('matches.json updated.')


def log_add(action, details):
    log = js_load(log_file, [])
    log.append({
        "time": datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
        "action": action,
        "details": details
    })
    js_dump(log_file, log)


def unique_id(prefix, upcoming_list):
    base = datetime.now().strftime(f"{prefix}_%Y%m%d_%H%M%S")
    used = [m["match id"] for m in upcoming_list]
    new_id = base
    count = 1
    while new_id in used:
        count += 1
        new_id = f"{base}_{count:02d}"
    return new_id
