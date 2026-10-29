# NemoAgent Studio

**Interactive Autonomous Coding Agent with Real Execution & Test Feedback**

Nebius x NVIDIA Global AI Hackathon — Coding and Agentic Engineering Track

## What it is
A Streamlit-based workspace where an agent plans a coding task, generates code + tests, executes them in a real Python process, captures results, and iterates using the actual runtime feedback.

## Why it is stronger
- Visible product interface (not just a script)
- Real execution + test running
- Structured multi-phase agent loop with full trace
- Model routing: Nemotron Ultra (planning/generation) + Nemotron Nano (critique)
- Clear demonstration of Nebius Token Factory + NVIDIA open models

## Run it
```bash
export NEBIUS_API_KEY=your_key
pip install -r requirements.txt
streamlit run nemoagent_studio.py
```

## Built With
- Nebius Token Factory
- NVIDIA Nemotron Ultra & Nano
- Streamlit
- Python subprocess for controlled execution

MIT License
