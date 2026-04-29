\# LLM SRE Multi-Agent MVP



一个基于大语言模型的智能 SRE 故障自动诊断与复盘多智能体（Multi-Agent）MVP。



\## 功能



\- 告警 webhook 接入

\- 告警降噪、聚合、初步分类

\- Diagnosis Agent 结构化 ReAct 风格诊断

\- Remediation Agent 生成修复建议与自动化脚本草案

\- Post-mortem Agent 自动生成 RCA Markdown 报告

\- 支持 mock 数据源，本地可直接运行

\- 支持切换 OpenAI-compatible LLM



\## 技术栈



\- FastAPI

\- SQLAlchemy + SQLite

\- Pydantic v2

\- Mock / OpenAI-compatible LLM

\- Prometheus / Elasticsearch 工具抽象



\## 快速开始



\### 1. 安装依赖



```bash

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

\### 2. 启动服务
```bash
uvicorn app.main:app --reload
\### 3. 健康检查
```bash
curl http://127.0.0.1:8000/health
\### 4. 发送测试告警
```bash
curl -X POST http://127.0.0.1:8000/webhooks/alerts \
  -H "Content-Type: application/json" \
  -d '{
    "source": "prometheus",
    "alerts": [
      {
        "fingerprint": "abc123",
        "status": "firing",
        "labels": {
          "alertname": "HighErrorRate",
          "service": "checkout-service",
          "severity": "critical",
          "namespace": "prod"
        },
        "annotations": {
          "summary": "High 5xx error rate detected",
          "description": "5xx error rate > 10% for 5m"
        },
        "startsAt": "2026-04-29T10:00:00Z"
      }
    ]
  }'
```
返回示例：
```bash
{
  "incident_id": "inc_xxxxxxxx",
  "status": "processing",
  "message": "Incident created and workflow started"
}
```
\### 5. 查看 Incident
```bash
curl http://127.0.0.1:8000/incidents/{incident_id}
\### 6. 查看 RCA 报告
```bash
curl http://127.0.0.1:8000/reports/{incident_id}
```
\##API
\-GET /health
\-POST /webhooks/alerts
\-GET /incidents/{incident_id}
\-GET /reports/{incident_id}
\##LLM 模式
\###Mock 模式
默认 LLM_MODE=mock，适合本地演示和测试。

\###OpenAI-compatible 模式
设置：

\-LLM_MODE=openai
\-OPENAI_BASE_URL
\-OPENAI_API_KEY
\-OPENAI_MODEL
\##诊断流程
\-Perception Agent：告警标准化、去重、聚合
\-Diagnosis Agent：调用指标、日志、拓扑、runbook 工具进行结构化推理
\-Remediation Agent：推荐处置动作、生成脚本草案
\-Postmortem Agent：生成结构化 RCA 报告
