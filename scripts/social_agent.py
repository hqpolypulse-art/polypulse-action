import os
import random
import sys
import requests
from requests_oauthlib import OAuth1

# Templates for autonomous daily technical & marketing tweets (<280 chars)
TWEETS = [
    (
        "🚀 Translating React & Next.js apps often breaks mobile UI layouts.\n\n"
        "PolyPulse runs headless Playwright audits in your GitHub CI/CD to catch "
        "overflows before production.\n\n"
        "📦 Marketplace: https://github.com/marketplace/actions/polypulse-ui-localization-qa\n"
        "#i18n #nextjs #buildinpublic"
    ),
    (
        "💡 Quick dev tip: German and French strings are typically 30% longer than English.\n\n"
        "Automate your i18n JSON sync and bounding-box overflow QA with PolyPulse GitHub Action.\n\n"
        "🌐 https://hqpolypulse-art.github.io/polypulse-action/\n"
        "#reactjs #webdev #localization"
    ),
    (
        "⚡ Stop manually inspecting localized screens.\n\n"
        "PolyPulse generates automated Pull Requests with AI-translated strings & layout QA visual reports.\n\n"
        "Try it on GitHub Marketplace:\n"
        "👉 https://github.com/marketplace/actions/polypulse-ui-localization-qa\n"
        "#githubactions #indiehackers #devops"
    ),
    (
        "🌐 Support RTL (Arabic/Hebrew) and global languages without clipping text on buttons.\n\n"
        "PolyPulse combines AI translation + visual viewport QA in a single GitHub Action.\n\n"
        "Check it out: https://hqpolypulse-art.github.io/polypulse-action/\n"
        "#frontend #programming #opensource"
    ),
    (
        "🛠️ Add automated UI Localization QA to your repository in under 2 minutes with PolyPulse:\n\n"
        "- Zero configuration overhead\n"
        "- Automated JSON sync\n"
        "- Layout bounding-box validation\n\n"
        "🔗 https://github.com/marketplace/actions/polypulse-ui-localization-qa\n"
        "#buildinpublic #SaaS"
    )
]

def post_tweet():
    api_key = os.environ.get("X_API_KEY")
    api_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")

    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("Error: Missing X API credentials in environment variables.")
        sys.exit(1)

    auth = OAuth1(api_key, api_secret, access_token, access_token_secret)
    tweet_text = random.choice(TWEETS)

    url = "https://api.twitter.com/2/tweets"
    payload = {"text": tweet_text}

    response = requests.post(url, auth=auth, json=payload)

    if response.status_code in [200, 201]:
        print("Tweet posted successfully!")
        print(response.json())
    else:
        print(f"Failed to post tweet: {response.status_code}")
        print(response.text)
        sys.exit(1)

if __name__ == "__main__":
    post_tweet()
