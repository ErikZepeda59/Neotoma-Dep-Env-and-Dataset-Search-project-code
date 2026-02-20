import requests
import time
import os
import json
from collections import defaultdict

def load_existing_env_data(filepath="depositional_env_index.json"):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(" JSON file is malformed. Starting fresh.")
                return {}
    return {}

BASE_DATASETS_URL = "https://api.neotomadb.org/v2.0/data/datasets"
BASE_DOWNLOAD_URL = "https://api.neotomadb.org/v2.0/data/downloads/"
LIMIT = 10000

# def existing_ids_set(path="depositional_env_index.json"):
#     """Flatten IDs already saved so we can skip them while collecting."""
#     data = load_existing_env_data(path)
#     seen = set()
#     for arr in data.values():
#         for dsid in arr:
#             try:
#                 seen.add(int(dsid))
#             except Exception:
#                 seen.add(dsid)
#     return seen

def get_first_dataset_ids():
    print("Fetching dataset IDs with pagination...")
    ids = []

    # seen_global = existing_ids_set()
    # seen_this_run = set()

    offset = 0
    batch_size = 500
    max_records = 100000  # cap how many records we loop through total

    while offset < max_records and len(ids) < LIMIT:
        url = f"{BASE_DATASETS_URL}?offset={offset}&limit={batch_size}"
        response = requests.get(url)
        data = response.json()

        print(f" Batch at offset {offset}")

        if "data" not in data:
            print(" 'data' key not found. Stopping.")
            break

        batch_data = data["data"]
        if not batch_data:
            print(" No more data returned. Stopping.")
            break

        for entry in batch_data:
            datasets = entry.get("site", {}).get("datasets", [])
            for ds in datasets:
                if "datasetid" in ds and len(ids) < LIMIT:
                    ids.append(ds["datasetid"])


        offset += batch_size
        time.sleep(0.25)  # Respect rate limits

    print(f" Got {len(ids)} dataset IDs.")
    return ids

def build_env_index(dataset_ids):
    print(" Fetching detailed data and building index...")
    env_dict = defaultdict(list)
    existing_data = load_existing_env_data()
    print(f" Loaded {len(existing_data)} existing depositional environments.")

    for i, dsid in enumerate(dataset_ids):
        dsid_str = str(dsid)
        # Skip if already in existing JSON
        already_in_file = any(dsid in existing_data.get(env, []) for env in existing_data)
        if already_in_file:
            print(f"{i+1}/{len(dataset_ids)}: {dsid} ⏭️ Already in JSON, skipping.")
            continue

        url = f"{BASE_DATASETS_URL}/{dsid}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f" Skipping dataset {dsid} (bad response)")
            continue

        try:
            data = response.json()

            if "data" not in data:
                print(f"{i+1}/{len(dataset_ids)}: {dsid} - No 'data' key.")
                print(json.dumps(data, indent=2))
                continue

            if not data["data"]:
                print(f"{i+1}/{len(dataset_ids)}: {dsid} - 'data' is an empty list.")
                print(json.dumps(data, indent=2))
                continue

            item = data["data"][0] 

            env_raw = item.get("site", {}).get("collectionunit", {}).get("depositionalenvironment")
            env = (env_raw or "unknown").strip().lower()

            if env:
                env_dict[env].append(dsid)
                print(f"{i+1}/{len(dataset_ids)}: {dsid} → {env}")
            else:
                print(f"{i+1}/{len(dataset_ids)}: {dsid} 🔵 Empty depositional environment string")

            time.sleep(0.25)

        except Exception as e:
            print(f"{i+1}/{len(dataset_ids)}: {dsid}  Error: {e}")
            continue

    # Merge with existing data
    for env, dsids in env_dict.items():
        existing_data.setdefault(env, [])
        for d in dsids:
            if d not in existing_data[env]:
                existing_data[env].append(d)

    return existing_data

def save_to_json(env_dict):
    with open("depositional_env_index.json", "w") as f:
        json.dump(env_dict, f, indent=2)
    print(" Saved to depositional_env_index.json")

def print_summary(env_dict):
    print("\n Environment counts:")
    for env, ids in env_dict.items():
        print(f"{env}: {len(ids)}")

def count_ids_in_json(path="depositional_env_index.json"):
    data = load_existing_env_data(path)
    all_ids = set()
    for arr in data.values():
        for dsid in arr:
            try:
                all_ids.add(int(dsid))
            except Exception:
                all_ids.add(dsid)
    return len(all_ids)

# def get_total_datasets():
#     url = f"{BASE_DATASETS_URL}?limit=1"
#     resp = requests.get(url)
#     data = resp.json()
#     return data.get("total", None)



def main():
    ids = get_first_dataset_ids()
    env_dict = build_env_index(ids)
    save_to_json(env_dict)
    print_summary(env_dict)

if __name__ == "__main__":
    main()

have = count_ids_in_json()
print(f"\n Progress: {have} datasets saved (couldn't fetch total)")