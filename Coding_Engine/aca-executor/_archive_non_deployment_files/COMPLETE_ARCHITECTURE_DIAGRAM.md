# 🏗️ Complete Architecture Diagram - Coding Engine

## 📊 Single Comprehensive Mermaid Diagram

```mermaid
graph TB
    %% =========================
    %% Users & Frontend Layer
    %% =========================
    subgraph Users["👥 Users"]
        U1[Candidate 1]
        U2[Candidate 2]
        U3[Candidate N]
    end
    
    subgraph Frontend["🖥️ Frontend Layer"]
        UI[Test UI<br/>Node.js Express<br/>Port 3001]
    end
    
    %% =========================
    %% Security Layer
    %% =========================
    subgraph Security["🔐 Security Layer"]
        SEC_NET[Network Isolation]
        SEC_FW[Firewall Rules<br/>IP Whitelist]
        SEC_SSL[SSL/TLS<br/>Encryption]
    end
    
    %% =========================
    %% Azure Container Apps
    %% =========================
    subgraph ContainerApps["☁️ Azure Container Apps Environment"]
        LB[Load Balancer<br/>Auto-distributes<br/>Round-robin]
        
        subgraph Replicas["🔄 Code Executor Replicas"]
            R1[Replica 1<br/>2 vCPU, 4GB RAM<br/>8 concurrent]
            R2[Replica 2<br/>2 vCPU, 4GB RAM<br/>8 concurrent]
            R3[Replica 3<br/>2 vCPU, 4GB RAM<br/>8 concurrent]
        end
    end
    
    %% =========================
    %% Execution Sandbox
    %% =========================
    subgraph Sandbox["🛡️ Execution Sandbox"]
        SEC_SBOX[Isolated Environment]
        SEC_RES[Resource Limits<br/>CPU/Memory/Time]
        SEC_FS[Read-only Filesystem]
        SEC_NONROOT[Non-root User]
    end
    
    %% =========================
    %% Container Registry
    %% =========================
    subgraph Registry["📦 Container Registry"]
        ACR[Azure Container Registry<br/>aitaraacr1763805702<br/>executor-secure:v17-csharp]
    end
    
    %% =========================
    %% Database Layer
    %% =========================
    subgraph Database["🗄️ Database Layer"]
        PG[(Azure PostgreSQL<br/>Flexible Server<br/>ai-ta-ra-postgre<br/>Standard_B1ms<br/>32GB Storage)]
    end
    
    %% =========================
    %% Monitoring & Observability
    %% =========================
    subgraph Monitoring["📊 Monitoring Stack"]
        LOGS[Application Logs]
        METRICS[Performance Metrics]
        ALERTS[Alert Rules]
    end
    
    subgraph AzureMonitoring["☁️ Azure Monitoring Services"]
        LOG_ANALYTICS[Log Analytics]
        APP_INSIGHTS[Application Insights]
        MONITOR[Azure Monitor]
    end
    
    %% =========================
    %% Request Flow
    %% =========================
    subgraph RequestFlow["🔄 Request Processing Flow"]
        START([User Submits Code])
        VALIDATE{Validate Input}
        FETCH_Q[Fetch Question<br/>& Test Cases]
        QUEUE_NODE[Queue Request]
        EXEC_NODE[Execute Code]
        COMPILE{Compile?}
        RUN[Run Code]
        MON_NODE[Monitor Resources]
        RES_OK{Within Limits?}
        RESULT_NODE[Collect Results]
        STORE_DB[Store Result]
        RESP([Return Response])
    end
    
    %% =========================
    %% Deployment Pipeline
    %% =========================
    subgraph Deployment["🚀 Deployment Pipeline"]
        COMMIT[Code Commit]
        CI[CI/CD Pipeline]
        D_BUILD[Docker Build]
        D_PUSH[Push to ACR]
        TF_APPLY[Terraform Apply]
        CA_UPDATE[Container Apps<br/>Update]
        H_CHECK[Health Check]
        PROD[Production Live]
    end
    
    %% =========================
    %% User to Frontend Connections
    %% =========================
    U1 --> UI
    U2 --> UI
    U3 --> UI
    
    %% =========================
    %% Frontend to Security
    %% =========================
    UI --> SEC_NET
    SEC_NET --> SEC_FW
    SEC_FW --> SEC_SSL
    
    %% =========================
    %% Security to Load Balancer
    %% =========================
    SEC_SSL --> LB
    
    %% =========================
    %% Frontend to Database
    %% =========================
    UI --> PG
    
    %% =========================
    %% Load Balancer to Replicas
    %% =========================
    LB --> R1
    LB --> R2
    LB --> R3
    
    %% =========================
    %% Replicas to Sandbox
    %% =========================
    R1 --> SEC_SBOX
    R2 --> SEC_SBOX
    R3 --> SEC_SBOX
    
    SEC_SBOX --> SEC_RES
    SEC_RES --> SEC_FS
    SEC_FS --> SEC_NONROOT
    
    %% =========================
    %% Replicas to Database
    %% =========================
    R1 --> PG
    R2 --> PG
    R3 --> PG
    
    %% =========================
    %% Registry to Replicas
    %% =========================
    ACR --> R1
    ACR --> R2
    ACR --> R3
    
    %% =========================
    %% Request Flow Connections
    %% =========================
    START --> VALIDATE
    VALIDATE -->|Valid| FETCH_Q
    VALIDATE -->|Invalid| RESP
    FETCH_Q --> PG
    FETCH_Q --> QUEUE_NODE
    QUEUE_NODE --> LB
    LB --> EXEC_NODE
    EXEC_NODE --> COMPILE
    COMPILE -->|Yes| RUN
    COMPILE -->|No| RUN
    RUN --> MON_NODE
    MON_NODE --> RES_OK
    RES_OK -->|No| RESP
    RES_OK -->|Yes| RESULT_NODE
    RESULT_NODE --> STORE_DB
    STORE_DB --> PG
    STORE_DB --> RESP
    RESP --> UI
    
    %% =========================
    %% Monitoring Connections
    %% =========================
    R1 --> LOGS
    R2 --> LOGS
    R3 --> LOGS
    R1 --> METRICS
    R2 --> METRICS
    R3 --> METRICS
    LOGS --> LOG_ANALYTICS
    METRICS --> APP_INSIGHTS
    APP_INSIGHTS --> MONITOR
    MONITOR --> ALERTS
    
    %% =========================
    %% Deployment Pipeline
    %% =========================
    COMMIT --> CI
    CI --> D_BUILD
    D_BUILD --> D_PUSH
    D_PUSH --> ACR
    D_PUSH --> TF_APPLY
    TF_APPLY --> CA_UPDATE
    CA_UPDATE --> H_CHECK
    H_CHECK --> PROD
    PROD --> R1
    PROD --> R2
    PROD --> R3
    
    %% =========================
    %% Styling
    %% =========================
    classDef user fill:#e1f5ff,stroke:#333,stroke-width:2px
    classDef frontend fill:#fff4e1,stroke:#333,stroke-width:2px
    classDef security fill:#ffeeba,stroke:#333,stroke-width:2px
    classDef replica fill:#d4edda,stroke:#333,stroke-width:2px
    classDef sandbox fill:#f0d9ff,stroke:#333,stroke-width:2px
    classDef db fill:#f8d7da,stroke:#333,stroke-width:2px
    classDef registry fill:#d1ecf1,stroke:#333,stroke-width:2px
    classDef monitor fill:#e2e3ff,stroke:#333,stroke-width:2px
    classDef flow fill:#f0f0f0,stroke:#333,stroke-width:2px
    classDef pipeline fill:#d4f4dd,stroke:#333,stroke-width:2px
    
    class U1,U2,U3 user
    class UI frontend
    class SEC_NET,SEC_FW,SEC_SSL security
    class R1,R2,R3 replica
    class SEC_SBOX,SEC_RES,SEC_FS,SEC_NONROOT sandbox
    class PG db
    class ACR registry
    class LOGS,METRICS,ALERTS,LOG_ANALYTICS,APP_INSIGHTS,MONITOR monitor
    class START,VALIDATE,FETCH_Q,QUEUE_NODE,EXEC_NODE,COMPILE,RUN,MON_NODE,RES_OK,RESULT_NODE,STORE_DB,RESP flow
    class COMMIT,CI,D_BUILD,D_PUSH,TF_APPLY,CA_UPDATE,H_CHECK,PROD pipeline
```

---

## 📋 Component Details

### 1. Users Layer
- **Candidates**: Multiple users submitting code
- **Access**: Via web browser or API

### 2. Frontend Layer
- **Test UI**: Node.js Express server
- **Port**: 3001
- **Functions**: Question display, code submission, results

### 3. Security Layer
- **Network Isolation**: Private VNet (optional)
- **Firewall**: IP whitelist rules
- **SSL/TLS**: Encrypted connections

### 4. Container Apps
- **Load Balancer**: Built-in Azure load balancer
- **Replicas**: 1-3 auto-scaling replicas
- **Resources**: 2 vCPU, 4GB RAM each
- **Capacity**: 8 concurrent requests per replica

### 5. Execution Sandbox
- **Isolation**: Separate environment per execution
- **Resource Limits**: CPU, memory, time constraints
- **Filesystem**: Read-only access
- **User**: Non-root execution

### 6. Container Registry
- **ACR**: Azure Container Registry
- **Image**: `executor-secure:v17-csharp`
- **Versioning**: Tagged images

### 7. Database
- **PostgreSQL**: Azure Flexible Server
- **Storage**: 32GB
- **Backup**: 7 days retention

### 8. Monitoring
- **Logs**: Application logging
- **Metrics**: Performance data
- **Alerts**: Automated notifications

---

## 🔄 Data Flow Summary

1. **User** submits code via **Test UI**
2. **Test UI** validates and fetches question from **Database**
3. Request goes through **Security Layer** (Network → Firewall → SSL)
4. **Load Balancer** distributes to available **Replica**
5. **Replica** creates **Sandbox** environment
6. Code is compiled (if needed) and executed
7. Resources are **Monitored** during execution
8. Results are collected and stored in **Database**
9. Response returned to **User** via **Test UI**
10. **Monitoring** tracks all metrics and logs

---

## 📊 Resource Summary

| Component | Count | Resources | Location |
|-----------|-------|-----------|----------|
| **Users** | N | - | External |
| **Test UI** | 1 | Node.js | Local/Azure |
| **Replicas** | 1-3 | 2 vCPU, 4GB each | Azure Container Apps |
| **Database** | 1 | 1 vCore, 2GB, 32GB | Azure PostgreSQL |
| **Registry** | 1 | 10GB storage | Azure Container Registry |
| **Monitoring** | Multiple | - | Azure Monitor |

---

## 🎯 Key Features

✅ **Auto-scaling**: 1-3 replicas based on load  
✅ **Load Balancing**: Built-in Azure load balancer  
✅ **Security**: Multi-layer security (Network, Firewall, SSL, Sandbox)  
✅ **Monitoring**: Complete observability stack  
✅ **Database**: Persistent storage for questions and results  
✅ **Deployment**: Automated CI/CD pipeline  

---

**This diagram shows the complete architecture in one view!** 🎉

