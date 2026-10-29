# CodeEvolve – Autonomous Coding Agent with Real Execution Feedback

**Nebius x NVIDIA Global AI Hackathon – Coding and Agentic Engineering Track**

CodeEvolve is an autonomous coding agent that plans, writes, **actually executes**, and iteratively improves code using real runtime feedback.

Unlike simple code generators, it runs the generated code, captures stdout/stderr/exceptions, and feeds those real results back into the next reasoning step.

## Key Features
- Real code execution via Python subprocess (not simulated)
- Multi-step agent loop: Plan → Generate → Execute → Critique with results → Iterate
- Model routing: Nemotron Ultra for planning & generation, Nemotron Nano for fast critique
- Powered by Nebius Token Factory + NVIDIA open-source models

## Setup
1. Claim free Nebius credits on the hackathon resources page (code: `NEBIUS-DEVPOST-GLOBAL26`)
2. `export NEBIUS_API_KEY=your_key`
3. `pip install -r requirements.txt`
4. `python codeevolve.py`

## How it works
1. Plans the solution with Nemotron Ultra
2. Generates complete runnable code
3. Executes it in a real Python process and captures output/errors
4. Feeds the actual execution results to Nemotron Nano for critique and improvement
5. Repeats until the code passes or max iterations reached

## Built With
- Nebius Token Factory
- NVIDIA Nemotron Ultra & Nano
- Python subprocess for real execution

## Why this is different
It closes the loop with **actual runtime evidence**, not just LLM self-critique. This is the core of agentic engineering.

MIT License
