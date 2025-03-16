# Python Script for Cleaning Up and Formatting JSON for Graph API

### Overview

Once JSON data is retrieved, it needs to be cleaned and formatted before uploading it to SharePoint via Microsoft Graph API. The following Python script automates this process.

**Python Script**
```python
import requests
import json
import re

# Base API URL
API_BASE_URL = "https://api.digitalarchives.wa.gov/api/retention-schedules/"

# Function to determine which schedule to pull from
def get_schedule_id():
	"""Prompt user or determine which retention schedule ID to use."""
	schedules = {
		"CORE": 3,
		"Law Enforcement": 5,
		"Public Utilities": 7
	}
	print("Available Retention Schedules:")
	for name, id in schedules.items():
		print(f"{name}: {id}")
	choice = input("Enter the name of the retention schedule to pull: ").strip()
	return schedules.get(choice, 3) # Default to CORE if not found

SCHEDULE_ID = get_schedule_id()
API_URL = f"{API_BASE_URL}{SCHEDULE_ID}"
OUTPUT_FILE = "purview_retention_labels.json"

# Function to extract and format the display name
def extract_display_name(name):
	"""
	- Extracts only the first line from the name field
	- Removes leading/trailing whitespace
	- Removes invalid characters per Microsoft Purview requirements
	- Truncates to 64 characters max
	"""
	if not name:
		return "Default_Label"
	cleaned_name = name.split("\r\n")[0].strip()
	cleaned_name = re.sub(r"[\\%&<>|?:;/*,\x00\x08\x0B\x0C\x0E-\x1F]", "", cleaned_name) # Remove invalid characters
	return cleaned_name[:64] # Truncate to 64 characters

# Function to convert retention period from text to days
def convert_retention_to_days(retention_text):
	match = re.search(r"(\d+) year", retention_text)
	if match:
		return int(match.group(1)) * 365 # Convert years to days
	match = re.search(r"(\d+) month", retention_text)
	if match:
		return int(match.group(1)) * 30 # Convert months to days
	match = re.search(r"(\d+) day", retention_text)
	if match:
		return int(match.group(1)) # Keep as days
	return -1 # Default to indefinite retention

# Function to determine the disposition action
def determine_disposition_action(retention_text):
	if "Destroy" in retention_text:
		return "delete"
	if "Review" in retention_text:
		return "startDispositionReview"
	return "none" # Default if action is unclear

# Function to format multi-line descriptions
def format_description(text):
	"""Ensures multi-line formatting remains intact and replaces en dashes"""
	return text.replace("\u2013", "-").replace("\r", "").strip()

# Step 1: Fetch latest retention schedule JSON
response = requests.get(API_URL)
if response.status_code != 200:
	print(f"Failed to fetch data: {response.status_code}")
	exit()

data = response.json()

# Step 2: Extract retention schedule details
schedule = data.get("returnValue", {})
local_schedules = schedule.get("localSchedules", [])

# Step 3: Prepare transformed data for Microsoft Purview
purview_labels = []

for record in local_schedules:
	# Only process active retention labels
	if not record.get("isActive", False):
		continue

	# Extract category information
	category_name = record.get("category", {}).get("categoryName", "Uncategorized")

	# Extract citation details if available
	citation_text = record.get("citation", "")

	label = {
		"displayName": extract_display_name(record["seriesTitleDescription"]),
		"descriptionForUsers": format_description(record["seriesTitleDescription"]),
		"descriptionForAdmins": format_description(record["primaryCopyRetention"]),
		"retentionTrigger": "dateCreated",
		"retentionDuration": {"@odata.type": "#microsoft.graph.security.retentionDurationInDays", "days": convert_retention_to_days(record["primaryCopyRetention"])},
		"actionAfterRetentionPeriod": determine_disposition_action(record["primaryCopyRetention"]),
		"isRecordLabel": bool(record.get("archival", False)),
		"behaviorDuringRetentionPeriod": "retain", # Ensuring this is explicitly defined
		"filePlanDescriptors": {
			"category": {
				"name": category_name
			},
			"citation": {
				"name": schedule.get("scheduleName", "CORE (Local Government Common Records Retention Schedule)"),
				"url": "https://www.sos.wa.gov/archives/recordsmanagement/local-government-records-retention-schedules---alphabetical-list.aspx"
			}
		}
	}

	purview_labels.append(label)

# Step 4: Save transformed data to a new JSON file
with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
	json.dump(purview_labels, outfile, indent=4)

print(f"Transformed data saved to {OUTPUT_FILE}")
```

### Updated Core Principles for Applying Retention Policies

1. **Selective Retention Policy Application**
    - Only apply the specific labels that are needed at a given time.
    - Implement a step to select which retention policy to push to Purview via Graph API.
2. **Structured Preparation Before Purview Integration**
    - Add items to Purview _only_ after establishing a Document Library.
    - Configure the Document Library with Document Sets and all relevant metadata required for Purview.
3. **Automated Labeling**
    - Utilize automation to auto-label documents based on predefined metadata and configurations.

## Appendix E: Example JSON Ready for Graph API
