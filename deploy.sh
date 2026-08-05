#!/usr/bin/env bash
# Deploy this Flask app to the Azure Web App "ese-impact" (resource group "Impact").
#
# Usage:
#   ./deploy.sh
#
# Requires: Azure CLI (az) logged in with access to the "Impact" resource group.
set -euo pipefail

RESOURCE_GROUP="Impact"
APP_NAME="ese-impact"
ZIP_PATH="/tmp/ese-impact.zip"

cd "$(dirname "$0")"

rm -f "$ZIP_PATH"
zip -r "$ZIP_PATH" . \
	-x ".git/*" \
	-x ".venv/*" \
	-x "venv/*" \
	-x "tests/*" \
	-x "*.pyc" \
	-x "__pycache__/*" \
	-x "*/__pycache__/*" \
	> /dev/null

echo "Deploying $ZIP_PATH to $APP_NAME (resource group $RESOURCE_GROUP)..."
az webapp deployment source config-zip \
	--resource-group "$RESOURCE_GROUP" \
	--name "$APP_NAME" \
	--src "$ZIP_PATH"

rm -f "$ZIP_PATH"
echo "Deployment complete: https://${APP_NAME}.azurewebsites.net"
