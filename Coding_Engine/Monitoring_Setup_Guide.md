# Azure Monitoring & Alerting Setup Guide

## 💰 Cost Breakdown

### **Azure Monitor Pricing:**

| Feature | Free Tier | Paid Tier |
|---------|-----------|-----------|
| **Metrics** | ✅ First 10 metrics FREE | $0.10 per metric/month |
| **Alerts** | ✅ First 10 alerts FREE | $0.10 per alert/month |
| **Log Analytics** | ✅ First 5GB/month FREE | $2.30 per GB |
| **Application Insights** | ✅ First 5GB/month FREE | $2.30 per GB |
| **Dashboards** | ✅ Unlimited FREE | FREE |

**For your use case:**
- Metrics: ~5 metrics = **FREE**
- Alerts: ~8 alerts = **FREE**
- Logs: ~2GB/month = **FREE**
- **Total Cost: $0/month** ✅

---

## 🔔 Notification Channels

### **Available Options:**

1. ✅ **Email** - FREE, built-in
2. ✅ **SMS** - $0.15 per SMS
3. ✅ **Slack** - FREE via webhook
4. ✅ **Microsoft Teams** - FREE via webhook
5. ✅ **Azure Mobile App** - FREE push notifications
6. ✅ **Webhook** - FREE (custom integrations)
7. ✅ **Logic Apps** - $0.000025 per action (almost free)

---

## 📧 Setup: Email Notifications

### **Step 1: Create Action Group**

```bash
# Create action group with email
az monitor action-group create \
  --name "CodingEngineAlerts" \
  --resource-group ai-ta-2 \
  --short-name "CodeAlert" \
  --email-receiver \
    name="AdminEmail" \
    email-address="rabdin@griddynamics.com" \
    use-common-alert-schema=true
```

**Via Azure Portal:**
1. Go to **Azure Monitor** → **Alerts** → **Action groups**
2. Click **+ Create**
3. **Basics:**
   - Name: `CodingEngineAlerts`
   - Display name: `CodeAlert`
4. **Notifications:**
   - Type: **Email/SMS/Push/Voice**
   - Name: `AdminEmail`
   - Email: `rabdin@griddynamics.com`
   - ✅ Enable common alert schema
5. Click **Review + create**

---

## 💬 Setup: Slack Notifications

### **Step 1: Create Slack Incoming Webhook**

1. Go to your Slack workspace
2. Navigate to **Apps** → **Incoming Webhooks**
3. Click **Add to Slack**
4. Choose channel (e.g., `#coding-engine-alerts`)
5. Click **Add Incoming WebHooks integration**
6. Copy the **Webhook URL** (looks like: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXX`)

### **Step 2: Add Slack to Action Group**

```bash
# Add webhook to action group
az monitor action-group update \
  --name "CodingEngineAlerts" \
  --resource-group ai-ta-2 \
  --add-action \
    webhook \
    name="SlackWebhook" \
    service-uri="https://hooks.slack.com/services/YOUR/WEBHOOK/URL" \
    use-common-alert-schema=true
```

**Via Azure Portal:**
1. Go to **Action groups** → `CodingEngineAlerts`
2. Click **Edit**
3. **Actions** tab:
   - Type: **Webhook**
   - Name: `SlackWebhook`
   - URI: `https://hooks.slack.com/services/YOUR/WEBHOOK/URL`
   - ✅ Enable common alert schema
4. Click **Save**

---

## 🚨 Critical Alerts Setup

### **Alert 1: High Cost (Daily Budget Exceeded)**

```bash
# Create budget alert
az consumption budget create \
  --budget-name "CodingEngineDailyBudget" \
  --category Cost \
  --amount 10 \
  --time-grain Monthly \
  --time-period start-date=2025-11-01 \
  --resource-group ai-ta-2 \
  --notifications \
    threshold=80 \
    operator=GreaterThan \
    contact-emails="rabdin@griddynamics.com" \
    contact-roles="Owner"
```

**Alert Thresholds:**
- 80% of budget ($8/day): Warning email
- 100% of budget ($10/day): Critical email + Slack
- 150% of budget ($15/day): Critical email + Slack + SMS

**Via Azure Portal:**
1. Go to **Cost Management + Billing** → **Budgets**
2. Click **+ Add**
3. **Scope**: Resource group `ai-ta-2`
4. **Budget details:**
   - Name: `CodingEngineDailyBudget`
   - Amount: $10
   - Reset period: Monthly
5. **Alert conditions:**
   - Type: Actual
   - % of budget: 80%, 100%, 150%
   - Action group: `CodingEngineAlerts`
6. Click **Create**

---

### **Alert 2: Service Down (Backend Not Responding)**

```bash
# Create availability alert
az monitor metrics alert create \
  --name "BackendDown" \
  --resource-group ai-ta-2 \
  --scopes /subscriptions/dab771f2-8670-4bf4-8067-ea813decb669/resourceGroups/ai-ta-2/providers/Microsoft.App/containerApps/ai-ta-ra-coding-engine \
  --condition "avg Requests < 1" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 0 \
  --description "Backend is not receiving any requests" \
  --action CodingEngineAlerts
```

**What it does:**
- Checks if backend received < 1 request in last 5 minutes
- If true for 1 minute → Send alert
- Severity: Critical (0)
- Notifications: Email + Slack

---

### **Alert 3: High Error Rate**

```bash
# Create error rate alert
az monitor metrics alert create \
  --name "HighErrorRate" \
  --resource-group ai-ta-2 \
  --scopes /subscriptions/.../containerApps/ai-ta-ra-coding-engine \
  --condition "avg Percentage HTTP Server Error > 5" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 1 \
  --description "More than 5% of requests are failing" \
  --action CodingEngineAlerts
```

**What it does:**
- Checks if 5xx error rate > 5%
- Alert if sustained for 5 minutes
- Notifications: Email + Slack

---

### **Alert 4: Session Pool at Capacity**

```bash
# Create capacity alert
az monitor metrics alert create \
  --name "SessionPoolNearCapacity" \
  --resource-group ai-ta-2 \
  --scopes /subscriptions/.../sessionPools/ai-ta-RA-session-pool \
  --condition "avg ActiveSessions > 45" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 2 \
  --description "Session pool is at 90% capacity (45/50 sessions)" \
  --action CodingEngineAlerts
```

**What it does:**
- Warns when 90% of sessions are in use
- Gives you time to scale up before hitting limit
- Notifications: Email + Slack

---

### **Alert 5: Unusual Traffic Spike**

```bash
# Create traffic spike alert
az monitor metrics alert create \
  --name "UnusualTrafficSpike" \
  --resource-group ai-ta-2 \
  --scopes /subscriptions/.../containerApps/ai-ta-ra-coding-engine \
  --condition "avg Requests > 1000" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 2 \
  --description "Receiving more than 1000 requests/min (possible DDoS or contest started)" \
  --action CodingEngineAlerts
```

**What it does:**
- Alerts if traffic > 1000 req/min
- Could indicate:
  - Contest started (expected)
  - DDoS attack (unexpected)
  - Bot traffic (unexpected)
- Notifications: Email + Slack

---

### **Alert 6: Long Queue (Users Waiting)**

```bash
# Create queue alert
az monitor metrics alert create \
  --name "LongQueue" \
  --resource-group ai-ta-2 \
  --scopes /subscriptions/.../sessionPools/ai-ta-RA-session-pool \
  --condition "avg QueueLength > 10" \
  --window-size 2m \
  --evaluation-frequency 1m \
  --severity 1 \
  --description "More than 10 users waiting for sessions" \
  --action CodingEngineAlerts
```

**What it does:**
- Alerts if > 10 requests are queued
- Indicates need to scale up
- Notifications: Email + Slack

---

### **Alert 7: Slow Response Time**

```bash
# Create latency alert
az monitor metrics alert create \
  --name "SlowResponseTime" \
  --resource-group ai-ta-2 \
  --scopes /subscriptions/.../containerApps/ai-ta-ra-coding-engine \
  --condition "avg Request Duration > 10000" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 2 \
  --description "Average response time > 10 seconds" \
  --action CodingEngineAlerts
```

**What it does:**
- Alerts if avg response time > 10s
- Indicates performance issues
- Notifications: Email + Slack

---

### **Alert 8: Container Restarts**

```bash
# Create restart alert
az monitor metrics alert create \
  --name "ContainerRestarting" \
  --resource-group ai-ta-2 \
  --scopes /subscriptions/.../containerApps/ai-ta-ra-coding-engine \
  --condition "total Restarts > 0" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 1 \
  --description "Backend container is restarting (possible crash)" \
  --action CodingEngineAlerts
```

**What it does:**
- Alerts on any container restart
- Indicates crashes or OOM kills
- Notifications: Email + Slack

---

## 📱 Slack Alert Format

When an alert fires, you'll receive a Slack message like:

```
🚨 ALERT: High Error Rate

Severity: Warning
Resource: ai-ta-ra-coding-engine
Condition: avg Percentage HTTP Server Error > 5%
Current Value: 7.2%
Time: 2025-11-24 18:00:00 UTC

Description: More than 5% of requests are failing

Actions:
• Check backend logs
• Verify session pool status
• Review recent deployments

View in Azure Portal: [Link]
```

---

## 📧 Email Alert Format

```
Subject: [ALERT] High Error Rate - ai-ta-ra-coding-engine

Alert Details:
- Alert Name: High Error Rate
- Severity: Warning
- Resource: ai-ta-ra-coding-engine
- Condition: avg Percentage HTTP Server Error > 5%
- Current Value: 7.2%
- Fired At: 2025-11-24 18:00:00 UTC

Description:
More than 5% of requests are failing

Recommended Actions:
1. Check backend logs in Log Analytics
2. Verify session pool status
3. Review recent deployments

View in Azure Portal:
https://portal.azure.com/#blade/...
```

---

## 🎯 Complete Setup Script

```bash
#!/bin/bash
# setup_monitoring.sh

RESOURCE_GROUP="ai-ta-2"
SUBSCRIPTION_ID="dab771f2-8670-4bf4-8067-ea813decb669"
EMAIL="rabdin@griddynamics.com"
SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# 1. Create Action Group
echo "Creating action group..."
az monitor action-group create \
  --name "CodingEngineAlerts" \
  --resource-group "$RESOURCE_GROUP" \
  --short-name "CodeAlert" \
  --email-receiver \
    name="AdminEmail" \
    email-address="$EMAIL" \
    use-common-alert-schema=true \
  --webhook-receiver \
    name="SlackWebhook" \
    service-uri="$SLACK_WEBHOOK" \
    use-common-alert-schema=true

# 2. Create Budget Alert
echo "Creating budget alert..."
az consumption budget create \
  --budget-name "CodingEngineDailyBudget" \
  --category Cost \
  --amount 10 \
  --time-grain Monthly \
  --time-period start-date=2025-11-01 \
  --resource-group "$RESOURCE_GROUP"

# 3. Create Metric Alerts
echo "Creating metric alerts..."

# High Error Rate
az monitor metrics alert create \
  --name "HighErrorRate" \
  --resource-group "$RESOURCE_GROUP" \
  --scopes "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.App/containerApps/ai-ta-ra-coding-engine" \
  --condition "avg Percentage HTTP Server Error > 5" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 1 \
  --action CodingEngineAlerts

# Session Pool Capacity
az monitor metrics alert create \
  --name "SessionPoolNearCapacity" \
  --resource-group "$RESOURCE_GROUP" \
  --scopes "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.App/sessionPools/ai-ta-RA-session-pool" \
  --condition "avg ActiveSessions > 45" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 2 \
  --action CodingEngineAlerts

# Long Queue
az monitor metrics alert create \
  --name "LongQueue" \
  --resource-group "$RESOURCE_GROUP" \
  --scopes "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.App/sessionPools/ai-ta-RA-session-pool" \
  --condition "avg QueueLength > 10" \
  --window-size 2m \
  --evaluation-frequency 1m \
  --severity 1 \
  --action CodingEngineAlerts

# Unusual Traffic
az monitor metrics alert create \
  --name "UnusualTrafficSpike" \
  --resource-group "$RESOURCE_GROUP" \
  --scopes "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.App/containerApps/ai-ta-ra-coding-engine" \
  --condition "avg Requests > 1000" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 2 \
  --action CodingEngineAlerts

echo "✅ Monitoring setup complete!"
echo "You will receive alerts via:"
echo "  - Email: $EMAIL"
echo "  - Slack: $SLACK_WEBHOOK"
```

---

## ✅ Summary

### **What You Get:**

1. **Email Notifications** ✅ FREE
   - High cost alerts
   - Service down alerts
   - Error rate alerts
   - Capacity alerts

2. **Slack Notifications** ✅ FREE
   - Same alerts as email
   - Real-time notifications
   - Formatted messages

3. **8 Critical Alerts:**
   - Cost budget exceeded
   - Service down
   - High error rate
   - Session pool capacity
   - Unusual traffic
   - Long queue
   - Slow response
   - Container restarts

4. **Cost:** $0/month (within free tier)

### **Setup Time:**
- Email: 5 minutes
- Slack: 10 minutes
- All alerts: 15 minutes
- **Total: 30 minutes**

Would you like me to create the `setup_monitoring.sh` script as a file you can run?
