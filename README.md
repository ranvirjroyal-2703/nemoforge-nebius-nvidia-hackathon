# NemoSwarm – Multi-Agent Coding System

**Nebius x NVIDIA Global AI Hackathon — Coding and Agentic Engineering Track**

Specialized agents collaborate to plan, code, test, execute, and review:

- **Planner** (Nemotron Ultra) — plan + acceptance criteria
- **Coder** (Nemotron Ultra) — writes the implementation
- **Tester** (Nemotron Ultra) — generates tests
- **Reviewer** (Nemotron Nano) — judges based on real execution results
- Real code + test execution between rounds

## Run
```bash
export NEBIUS_API_KEY=your_key
pip install -r requirements.txt
python nemoswarm.py
```

## Built With
Nebius Token Factory + NVIDIA Nemotron Ultra & Nano

This is a multi-agent system with real execution feedback, not a single-loop generator.

MIT License
