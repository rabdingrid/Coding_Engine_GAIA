#!/bin/bash
# Quick status check for PostgreSQL server

echo "🔍 Checking PostgreSQL Server Status..."
echo ""

STATUS=$(az postgres flexible-server show \
  --resource-group ai-ta-2 \
  --name ai-ta-ra-postgre \
  --query "{state:state, fqdn:fullyQualifiedDomainName}" \
  -o json 2>/dev/null)

if [ $? -eq 0 ]; then
    STATE=$(echo "$STATUS" | grep -o '"state": "[^"]*' | cut -d'"' -f4)
    FQDN=$(echo "$STATUS" | grep -o '"fqdn": "[^"]*' | cut -d'"' -f4)
    
    echo "Server: ai-ta-ra-postgre"
    echo "FQDN: $FQDN"
    echo "Status: $STATE"
    echo ""
    
    if [ "$STATE" = "Ready" ]; then
        echo "✅ Server is ready!"
    elif [ "$STATE" = "Provisioning" ]; then
        echo "⏳ Server is still provisioning (usually takes 5-10 minutes)"
    else
        echo "⚠️  Status: $STATE"
    fi
else
    echo "❌ Server not found or error checking status"
fi
