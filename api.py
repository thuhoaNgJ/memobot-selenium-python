import requests

BASE_URL = "https://sohoa.memobot.io/authen"

def login(username, password):
    """Perform login and return access token"""
    url = f"{BASE_URL}/api/v1/auth/login"
    headers = {"Content-Type": "application/json"}
    payload = {
        "username": username,
        "password": password
    }

    response = requests.post(url, json=payload, headers=headers)
 
    print("Response Status Code:", response.status_code)
    print("Raw Response Text:", response.text) 

    # Try parsing JSON safely
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        print("❌ ERROR: Response is not valid JSON!")
        return None

    # Extract token
    access_token = response_json.get("data", {}).get("accessToken")
    return access_token

# Example usage
username = "your_username"
password = "your_password"
access_token = login(username, password)

# Print Access Token
if access_token:
    print("Access Token:", access_token)
else:
    print("❌ Login failed. Check API response above.")
