# CHIMERA — AI-Powered Adaptive Deception Network

## 📖 Overview
CHIMERA is a graduation project that combines cybersecurity honeypot techniques with 
Large Language Models (LLMs) to create an intelligent, conversational deception system. 
Instead of static, pre-programmed responses, CHIMERA uses an LLM to generate realistic, 
context-aware replies to an attacker's commands in real time — engaging them longer, 
gathering more threat intelligence, and producing automated attacker profiling reports.

## 🎯 Objectives
- Build a custom SSH honeypot server from scratch (Python + Paramiko)
- Integrate an LLM to generate dynamic, realistic terminal responses
- Classify attacker commands by risk level (Safe / Suspicious / Malicious)
- Automatically generate a Threat Intelligence report after each session
- Visualize all captured sessions in a live dashboard

## 🏗️ Architecture
- `core/` — Virtual SSH server & filesystem simulation
- `ai_engine/` — LLM integration & persona management
- `intelligence/` — Command classification & threat report generation
- `dashboard/` — Web dashboard to visualize sessions
- `tests/` — Unit tests
- `docs/` — Documentation & diagrams

## 🚧 Status
Project in active development — see commit history for progress.

## 👤 Author
Graduation Project — Level 4, Computer Science & AI (Cybersecurity Major)
