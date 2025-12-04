#!/bin/bash
# Add your laptop IP to Azure PostgreSQL firewall

echo "🔍 Getting your IP address..."
MY_IP=$(curl -s https://api.ipify.org)
echo "Your IP: $MY_IP"
echo ""

read -p "Enter your name (for firewall rule name): " NAME

if [ -z "$NAME" ]; then
    NAME="TeamMember"
fi

RULE_NAME="Allow_${NAME// /_}"

echo ""
echo "🔒 Adding firewall rule: $RULE_NAME"
echo "IP: $MY_IP"
echo ""

az postgres flexible-server firewall-rule create \
  --resource-group ai-ta-2 \
  --name ai-ta-ra-postgre \
  --rule-name "$RULE_NAME" \
  --start-ip-address "$MY_IP" \
  --end-ip-address "$MY_IP" \
  --yes

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Your IP has been added to firewall!"
    echo ""
    echo "📋 Connection details:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Server: ai-ta-ra-postgre.postgres.database.azure.com"
    echo "Database: railway"
    echo "Username: postgresadmin"
    echo "Password: 5oXcNX59QmEl7zmV3DbjemkiJ"
    echo "SSL: Required"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🧪 Test connection:"
    echo "psql \"postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require\" -c \"SELECT version();\""
else
    echo ""
    echo "❌ Failed to add IP. Please check:"
    echo "  1. Azure CLI is installed and logged in"
    echo "  2. You have permissions to modify firewall"
    echo "  3. Contact team lead if issues persist"
fi

