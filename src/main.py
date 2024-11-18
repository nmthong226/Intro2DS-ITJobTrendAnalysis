import requests

def get_access_token(client_id, client_secret):
    """
    Get access token from LinkedIn using client credentials.
    
    Args:
        client_id (str): Your LinkedIn application's client ID.
        client_secret (str): Your LinkedIn application's client secret.

    Returns:
        str: The access token.
    """
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    # Send the POST request to get the access token
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print(f"Access token received: {access_token}")
        return access_token
    else:
        print(f"Failed to get access token: {response.status_code}, {response.text}")
        return None

def fetch_job_posts(access_token):
    """
    Fetch job posts from LinkedIn API using the provided access token.
    
    Args:
        access_token (str): The access token obtained from LinkedIn API.
    
    Returns:
        list: A list of job posts fetched from LinkedIn.
    """
    url = "https://api.linkedin.com/v2/jobs"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Connection": "Keep-Alive"
    }

    # Send GET request to fetch job posts
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        job_posts = response.json()
        print("Job posts fetched successfully.")
        return job_posts
    else:
        print(f"Failed to fetch job posts: {response.status_code}, {response.text}")
        return None

def main():
    # Your LinkedIn credentials (replace with actual values)
    client_id = ""
    client_secret = ""

    # Step 1: Get the access token
    access_token = get_access_token(client_id, client_secret)

    if access_token:
        # Step 2: Fetch job posts using the access token
        job_posts = fetch_job_posts(access_token)

        if job_posts:
            # Process job posts (for demonstration purposes, we just print the results)
            print(job_posts)
        else:
            print("No job posts found.")
    else:
        print("Unable to retrieve access token.")

if __name__ == "__main__":
    main()
