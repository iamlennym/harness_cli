import requests
import json
import sys
import os
import time
from dotenv import load_dotenv


#	---------------------------------------------------------------------------------
#	Config variables required
#	---------------------------------------------------------------------------------
pipeline_name = "devBootstrap"
account_id = "6_vVHzo9Qeu9fXvj-AcbCQ"
org_id = "SE_Sandbox"
project_id = "Len_Sandbox"

# Headers (needed for authentication)
headers = {
	"Content-Type": "application/yaml",
	"x-api-key": None
}

# Define the API endpoint URL
api_url = f"https://app.harness.io/gateway/pipeline/api/pipeline/execute/{pipeline_name}?accountIdentifier={account_id}&orgIdentifier={org_id}&projectIdentifier={project_id}&moduleType=CI"
deploy_url = f"https://app.harness.io/ng/account/{account_id}/cd/orgs/{org_id}/projects/{project_id}/pipelines/{pipeline_name}/deployments/"
deploy_url_suffix = "/pipeline?storeType=INLINE"


# Define the YAML payload template as a string
yaml_payload_template = """
pipeline:
  identifier: devBootstrap
  variables:
    - name: APPLICATION_NAME
      type: String
      value: {}
"""

# Initialize an empty dictionary to store responses
status_dict = {}

def printProgress(plan_execution_uuid):
	# Define the API endpoint URL
	status_url = f"https://app.harness.io/pipeline/api/pipelines/execution/{plan_execution_uuid}?accountIdentifier={account_id}&orgIdentifier={org_id}&projectIdentifier={project_id}"
	run_success = False

	print ("Status:")
	while True:
		try:
			# Make the GET request with the raw YAML payload
			response = requests.get(status_url, headers=headers)

			# Check if the request was successful (status code 200)
			if response.status_code == 200:
				# Parse the JSON response
				data = response.json()
				pl_status = data['data']['pipelineExecutionSummary']['status']
				# print (f"Status : {pl_status}")

				# Access the layoutNodeMap and print the status of each element
				layout_node_map = data.get("data", {}).get("pipelineExecutionSummary", {}).get("layoutNodeMap", {})
				for node_id, node_info in layout_node_map.items():
					status = node_info.get("status", "Unknown")
					name = node_info.get("name", "Unknown")

					if run_success:
						# print(f"Checking Stage: {name}, Status: {status}")
						if status == 'Running' or status == "Success":
							stage_status = f"{name}-{status}"
							if stage_status not in status_dict:
								status_dict[stage_status] = True
								print(f"Stage: {name}, Status: {status}")

					if status == "Success":
						stage_status = f"{name}-{status}"
						if stage_status not in status_dict:
							status_dict[stage_status] = True
							print(f"Stage: {name}, Status: {status}")

				# Check if the pipeline is done
				if pl_status == "Success":
					print (f"Done...")
					break
			else:
				print("Error: Request failed with status code", response.status_code)

		except requests.exceptions.RequestException as e:
			print("Error: Request exception -", str(e))
		except json.JSONDecodeError as e:
			print("Error: JSON decoding error -", str(e))

		# Sleep for a while before polling again (e.g., every 5 seconds)
		time.sleep(5)


#	---------------------------------------------------------------------------------
#	Main script starts here
#	---------------------------------------------------------------------------------

# Load variables from the .env file
load_dotenv()
api_key = os.getenv("API_KEY")
if api_key is None:
    print("API_KEY environment variable missing")
    sys.exit(1) 

headers["x-api-key"] = api_key

# Check if at least one command-line argument is provided
if len(sys.argv) < 2:
    print("Usage: python3 onboard.py <new application name> (all lowercase, no spaces)")
    sys.exit(1)  # Exit with an error code

yaml_payload = yaml_payload_template.format(sys.argv[1])
#	print (f"apiurl : {api_url}\n")

try:
	# Make the POST request with the raw YAML payload
	response = requests.post(api_url, data=yaml_payload, headers=headers)

	# Check if the request was successful (status code 200)
	if response.status_code == 200:
		# Parse the JSON response
		data = response.json()
		status = data['status']
		plan_execution_uuid = data['data']['planExecution']['uuid']

		if status == "SUCCESS":
			print ("Onboarding pipeline started...")
			print ("Pipeline URL:")
			print(f"{deploy_url}{plan_execution_uuid}{deploy_url_suffix}")
			printProgress(plan_execution_uuid)
		else:
			print("Onboarding unsuccesful.")

	else:
		print("Error: Request failed with status code", response.status_code)

except requests.exceptions.RequestException as e:
	print("Error: Request exception -", str(e))
except json.JSONDecodeError as e:
	print("Error: JSON decoding error -", str(e))
