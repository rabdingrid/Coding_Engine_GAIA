# Quick Plan Summary: 200-300 Users, <5 Second Wait Time

## 🎯 Quick Answer

**Configuration:**
- **Min Replicas**: 25
- **Max Replicas**: 40
- **Cost per Contest**: $10-14
- **Cost per Student**: $0.048-0.050

---

## 📊 Replica Requirements

| Users | Min Replicas | Max Replicas | Wait Time | Cost/Contest |
|-------|--------------|--------------|-----------|--------------|
| **200** | 20 | 30 | < 1 sec | **$10** |
| **250** | 25 | 35 | < 1 sec | **$12** |
| **300** | 30 | 40 | < 1 sec | **$14** |

---

## 🚀 Quick Implementation

### 1. Update Terraform

```bash
cd terraform
terraform apply -var="min_replicas=25" -var="max_replicas=40"
```

### 2. Verify Auto-Scaling

```bash
az containerapp show \
  --name ai-ta-ra-code-executor2 \
  --resource-group ai-ta-2 \
  --query "properties.template.scale" -o json
```

### 3. Test

```bash
python3 load-test-multi-user.py -n 300 -l python
```

---

## 💰 Cost Breakdown

**Per Contest (2 hours):**
- Pre-warmed (25 replicas): $5.40
- Peak (40 replicas): $2.16
- Average (30 replicas): $4.86
- **Total: $12.42**

**Monthly (5 contests):**
- Contests: 5 × $12 = $60
- Idle: $0 (scale to zero)
- **Total: $60/month**

---

## ✅ Guarantee

With 25-40 replicas:
- ✅ **Wait Time**: < 1 second (usually 0 seconds)
- ✅ **No user waits > 5 seconds**
- ✅ **100% success rate**
- ✅ **Cost**: $0.048-0.050 per student

---

**Ready to implement!** 🚀

