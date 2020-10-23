import base64
import json
import logging
import os
import pathlib
import requests

def authenticate_iam(base_url, client_id, scope, user_name, user_password):
    url = f"{base_url}/oauth/token"
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": client_id,
        "grant_type": "password",
        "username": user_name,
        "password": user_password,
        "scope": scope
    }
    response = requests.post(url=url, headers=headers, data=data)

    if response.ok:
        content = json.loads(response.content)
        token_type = content["token_type"]
        access_token = content["access_token"]
        return token_type + " " + access_token
    else:
        response.raise_for_status()
        return ""


def fetch_artifact_info(base_url, miniapp_id, miniapp_version_id, miniapp_asset_ids, iam_token):
    url = f"{base_url}/api/v1/mini-apps/{miniapp_id}/versions/{miniapp_version_id}/manifests/download"
    headers = {
        "Authorization": iam_token
    }
    params = {
        "assetIds": miniapp_asset_ids
    }
    response = requests.get(url=url, headers=headers, params=params)

    if response.ok:
        content = json.loads(response.content)
        assets = content["data"]
        for asset in assets:
            download_asset(asset["name"], asset["content"])
    else:
        response.raise_for_status()

def download_asset(name, content_url):
    response = requests.get(url=content_url)
    if response.ok:
        pathlib.Path('build/outputs').mkdir(parents=True, exist_ok=True)
        file = open(f"build/outputs/{name}", "wb+")
        print(pathlib.Path('build/outputs').absolute())
        file.write(response.content)
        file.close()
    else:
        response.raise_for_status()


def main():
    logging.basicConfig(level=logging.DEBUG)

    # iam_base_url = os.environ["IAM_BASE_URL"]
    # iam_client_id = os.environ["IAM_CLIENT_ID"]
    # iam_scope = os.environ["IAM_SCOPE"]
    # iam_user_email = os.environ["IAM_USER_EMAIL"]
    # iam_user_password = os.environ["IAM_USER_PASSWORD"]

    # token = authenticate_iam(
    #     iam_base_url,
    #     iam_client_id,
    #     iam_scope,
    #     iam_user_email,
    #     iam_user_password
    # )

    # terra_base_url = os.environ["TERRA_BASE_URL"]
    # miniapp_id = os.environ["MINIAPP_ID"]
    # miniapp_version_id = os.environ["MINIAPP_VERSION_ID"]
    # miniapp_asset_ids = os.environ["MINIAPP_ASSET_IDS"]

    # fetch_artifact_info(
    #     terra_base_url,
    #     miniapp_id,
    #     miniapp_version_id,
    #     miniapp_asset_ids,
    #     token
    # )

    download_asset('CallAppSDK', 'https://github.com/tungnx-teko/terra-external-packages-ios/releases/download/CallAppSDK/CallAppSDK.framework.zip')
    download_asset('call-app-sdk', 'https://github.com/tungnx-teko/terra-external-packages-ios/releases/download/CallAppSDK/call-app-sdk.json')


if __name__ == "__main__":
    main()
