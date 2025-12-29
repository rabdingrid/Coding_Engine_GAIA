#!/bin/bash
# Quick Redis Status Check Script

echo "🔍 Checking Redis Status..."
echo ""

STATUS=$(az redis show --name ai-ta-ra-redis --resource-group ai-ta-2 --query provisioningState -o tsv 2>&1)

if [ "$STATUS" = "Succeeded" ]; then
    echo "✅ Redis is READY!"
    echo ""
    echo "📋 Connection Details:"
    az redis show --name ai-ta-ra-redis --resource-group ai-ta-2 \
        --query "{hostname:hostName,sslPort:sslPort,redisVersion:redisVersion}" -o json
    echo ""
    echo "🔑 Access Keys are available!"
    echo ""
    echo "You can now use Redis. See REDIS_DEVELOPER_GUIDE.md for integration instructions."
else
    echo "⏳ Status: $STATUS"
    echo ""
    echo "Redis is still being created. Please wait a bit more."
    echo ""
    echo "Check again in a few minutes by running:"
    echo "  ./check-redis-status.sh"
    echo ""
    echo "Or manually:"
    echo "  az redis show --name ai-ta-ra-redis --resource-group ai-ta-2 --query provisioningState"
fi




