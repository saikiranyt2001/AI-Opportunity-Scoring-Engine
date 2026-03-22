# AI Opportunity Scoring Engine

AI-powered backend system built with FastAPI for scoring and evaluating product or business opportunities using asynchronous pipelines and modular architecture.

## 🚀 Overview

This system processes multiple input signals, applies scoring logic, and delivers structured results via REST APIs. Designed for scalability, reliability, and real-time evaluation workflows.
Built with a focus on non-blocking async execution and resilient pipeline design.

## ⚙️ Tech Stack

- Python 3.11+
- FastAPI (async)
- SQLAlchemy (async ORM)
- PostgreSQL / SQLite
- APScheduler (task orchestration)
- Pytest (testing)
- Docker

## 🧠 Key Features

- Async FastAPI backend with high-performance request handling  
- Modular scoring pipeline for extensibility  
- Background task execution using APScheduler  
- Clean separation of routes, services, and tasks  
- Fully tested backend with pytest (all tests passing)  
- REST API endpoints for scoring and data retrieval
- Concurrent data aggregation using async calls (simulating multi-source signal ingestion)
- Fault-tolerant pipeline ensuring partial failures do not break overall scoring

## 🧪 Testing

All core modules are covered with pytest.


Example test run:
```
16 passed in 2.03s

'''
Built with a focus on non-blocking async execution and resilient pipeline design.
```
