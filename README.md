
# LogFusion-AI 🚀

An intelligent, autonomous incident management agent that eliminates the manual effort of digging through infrastructure logs and piecing together operational context during production outages. 

LogFusion-AI bridges the gap between infrastructure state and deployment history. By running a single local command, it correlates real-time OpenSearch container logs with Git deployment histories in milliseconds, providing an instant root-cause analysis and an actionable, step-by-step remediation runbook.

---

## 🏗️ Architecture & How It Works

LogFusion-AI is built specifically to solve cross-system debugging without the weight of an external data warehouse or a brittle ETL pipeline.

```text
[OpenSearch Container] ──┐
                         ├──> [ Coral Unified Query Layer ] ──> [ LLM (via OpenRouter) ] ──> Actionable Runbook
[Git Deployment File] ───┘         (In-Memory SQL Join)

```

1. **The Log Layer (OpenSearch):** Tracks system-level backend infrastructure logs (e.g., database pool exhaustion timeouts).
2. **The Deployment Layer (Git History):** A localized record of repository deployments, commit IDs, authors, and configuration changes.
3. **The Core Engine (Coral v3):** Coral federates these entirely distinct data sources into virtual SQL tables using standard, declarative YAML manifests. It uses an in-memory execution engine to perform immediate timestamp correlation across both systems.
4. **The Intelligence Layer (OpenRouter):** The structured data payload is passed to a lightweight, highly available LLM to diagnose the failure and write target rollback scripts.

---

## 🛠️ How LogFusion-AI Uses Coral

Coral serves as the complete data abstraction engine for this project. Instead of writing custom API integration scripts or fetching, parsing, and cleaning raw data streams, LogFusion-AI delegates everything to Coral:

* **Custom Declarative Manifests:** Maps the OpenSearch `/_search` REST API directly into a queryable relational table schema.
* **Local File Abstraction:** Wraps flat JSONL deployment history logs into a local file-backed SQL source.
* **Cross-Source In-Memory Joins:** Executes a high-performance relational `JOIN` connecting OpenSearch logs directly to Git history based on strict temporal constraints (`l.timestamp >= g.committed_at`), executing the entire operations layer in a single pass.

---

## 🚀 Getting Started

### Prerequisites

* Docker & Docker Compose
* Python 3.10+
* An OpenRouter API Key (Free tier)

### 1. Clone the Repository

```bash
git clone [https://github.com/OpswhizMir/LogFusion-AI.git](https://github.com/OpswhizMir/LogFusion-AI.git)
cd LogFusion-AI

```

### 2. Start the Local Infrastructure

Spin up the pre-configured OpenSearch and workspace containers:

```bash
docker-compose up -d

```

### 3. Install Python Dependencies

```bash
pip3 install openai

```

### 4. Configure Your Environment

Export your free OpenRouter API key so the agent can safely communicate with the model:

```bash
export OPENROUTER_API_KEY="your-free-openrouter-api-key-here"

```

### 5. Run the Analyzer Agent

Execute the main engine to analyze the current active infrastructure incident:

```bash
python3 agent.py

```

---

## 📊 Sample Output: AI SRE Remediation Report

When executed during a production database timeout incident, LogFusion-AI instantly outputs the following report:

```text
==============================================
         AI SRE REMEDIATION REPORT
==============================================

1. ROOT CAUSE ANALYSIS
- What happened?
  At 2026-05-30T21:00:00Z the payment-service emitted a log entry: "Database connection timeout: pool exhausted."
- Why it happened?
  The service was recently deployed with commit a1b2c3d titled "Optimized DB connection pooling configuration." The change aggressively lowered the idle limits, causing pool saturation under production load.

2. SUSPECT COMMIT
+-----------+----------+-----------------------------------------------+
| Commit ID | Author   | Commit Message                                |
+-----------+----------+-----------------------------------------------+
| a1b2c3d   | john.doe | Optimized DB connection pooling configuration |
+-----------+----------+-----------------------------------------------+

3. REMEDIATION ACTION (Immediate Fix)
# Roll back to the previous stable revision
kubectl set image deployment/payment-service payment-service=myrepo/payment-service:<PREVIOUS_TAG> -n production

# Revert the specific commit via GitOps
git revert a1b2c3d --no-edit -m 1
git push origin main

```

---

## 🏆 Hackathon Track

Submitted to the **Enterprise Agent Track** for the *Pirates of the Coral-bean* Hackathon. Built to showcase the power of localized data federation using Coral v3.

```

```
