import os
import json
import requests

GITHUB_USER = "imdeepthakkar"
FOLLOWERS_FILE = "followers.json"

def get_current_followers():
    url = f"https://api.github.com/users/{GITHUB_USER}/followers"
    followers = []
    page = 1
    
    while True:
        response = requests.get(f"{url}?per_page=100&page={page}")
        response.raise_for_status()
        data = response.json()
        if not data:
            break
        followers.extend([user['login'] for user in data])
        page += 1
        
    return followers

def get_saved_followers():
    if os.path.exists(FOLLOWERS_FILE):
        with open(FOLLOWERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_followers(followers):
    with open(FOLLOWERS_FILE, "w") as f:
        json.dump(followers, f, indent=2)

def main():
    current_followers = get_current_followers()
    saved_followers = get_saved_followers()
    
    new_followers = [f for f in current_followers if f not in saved_followers]
    
    if new_followers:
        print(f"Found {len(new_followers)} new followers!")
        
        # Write the issue content to a markdown file
        body = "Great news! The following users recently followed you on GitHub:\\n\\n"
        for user in new_followers:
            body += f"- [@{user}](https://github.com/{user})\\n"
            
        with open("new_followers_issue.md", "w") as f:
            f.write(body)
    else:
        print("No new followers found.")
        
    # Always update the saved file
    if set(current_followers) != set(saved_followers):
        save_followers(current_followers)
        print("Updated followers.json")

if __name__ == "__main__":
    main()
