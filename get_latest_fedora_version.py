import json
import re
import sys
from urllib.request import Request, urlopen

# Official URL provided by the Fedora Infrastructure team
URL = "https://fedoraproject.org/releases.json"

# Set a custom user agent to be respectful of Fedora's infrastructure
REQ_HEADERS = {"User-Agent": "FedoraVersionChecker/1.0 (Python script)"}


def get_latest_stable_fedora():
    try:
        # Fetch data from the Fedora Project releases endpoint
        req = Request(URL, headers=REQ_HEADERS)
        with urlopen(req) as response:
            if response.status != 200:
                print(
                    f"Error: Unable to reach Fedora servers (Status: {response.status})"
                )
                sys.exit(1)
            data = json.loads(response.read().decode("utf-8"))

        # Extract only numeric stable versions (e.g., '44', '45')
        # This filters out string values or test labels like "rawhide"
        stable_versions = []
        for release in data:
            version_str = str(release.get("version", ""))
            if re.match(r"^\d+$", version_str):
                stable_versions.append(int(version_str))

        if not stable_versions:
            print("Error: No stable versions found in the JSON file.")
            sys.exit(1)

        # The maximum numeric version represents the latest stable release
        return max(stable_versions)

    except Exception as e:
        print(f"An error occurred while parsing the release data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    latest_version = get_latest_stable_fedora()
    print(f"Latest Stable Fedora Release: {latest_version}")