#!/usr/bin/env python3
"""
Add repository description to Bell-Prep on GitHub
Run this script to update your repository description
"""

import subprocess
import sys

def add_repo_description_via_cli():
    """Add description using GitHub CLI (gh)"""
    description = "Production-grade procurement automation system for Bell Textron with SAP Ariba integration, ITAR compliance, and AS9100 certification tracking"
    
    try:
        print("Adding description to Bell-Prep repository...")
        result = subprocess.run([
            "gh", "repo", "edit", 
            "akabbas/Bell-Prep", 
            "--description", description,
            "--visibility", "public"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Description added successfully!")
            print(f"\nDescription: {description}")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ GitHub CLI (gh) not found. Please install it from https://cli.github.com/")
        return False

def add_repo_description_via_api():
    """Add description using GitHub REST API"""
    try:
        import requests
    except ImportError:
        print("❌ requests library not found. Install with: pip install requests")
        return False
    
    # Note: This requires GITHUB_TOKEN environment variable to be set
    import os
    token = os.environ.get('GITHUB_TOKEN')
    
    if not token:
        print("❌ GITHUB_TOKEN environment variable not set")
        print("   Set it with: export GITHUB_TOKEN='your_github_token'")
        print("   Get a token from: https://github.com/settings/tokens")
        return False
    
    description = "Production-grade procurement automation system for Bell Textron with SAP Ariba integration, ITAR compliance, and AS9100 certification tracking"
    
    url = "https://api.github.com/repos/akabbas/Bell-Prep"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "description": description
    }
    
    try:
        print("Adding description via GitHub API...")
        response = requests.patch(url, headers=headers, json=data)
        
        if response.status_code == 200:
            print("✅ Description added successfully!")
            print(f"\nDescription: {description}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.json())
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("Bell-Prep Repository Description Setup")
    print("=" * 70)
    print()
    
    # Try CLI first (preferred method)
    if add_repo_description_via_cli():
        sys.exit(0)
    
    print()
    print("Trying GitHub API method...")
    if add_repo_description_via_api():
        sys.exit(0)
    
    print()
    print("=" * 70)
    print("Manual Setup Instructions:")
    print("=" * 70)
    print("1. Go to: https://github.com/akabbas/Bell-Prep")
    print("2. Click the gear icon (⚙️) next to 'About' on the right sidebar")
    print("3. Enter this description:")
    print()
    print("   Production-grade procurement automation system for Bell Textron")
    print("   with SAP Ariba integration, ITAR compliance, and AS9100")
    print("   certification tracking")
    print()
    print("4. Click 'Save'")
    print()
    sys.exit(1)


