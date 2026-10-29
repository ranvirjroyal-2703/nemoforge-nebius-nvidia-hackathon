# NemoForge – Autonomous Coding Agent

Autonomous multi-step coding agent powered by NVIDIA Nemotron models on Nebius Token Factory.

Built for the Nebius x NVIDIA Global AI Hackathon (Coding and Agentic Engineering Track).

## Setup
1. Get Nebius Token Factory API key (use code NEBIUS-DEVPOST-GLOBAL26 for free credits on the hackathon resources page).
2. Create a `.env` file or export: `export NEBIUS_API_KEY=your_key_here`
3. `pip install -r requirements.txt`
4. `python nemoforge.py`

## How it works
- Plans the solution with Nemotron Ultra (deep reasoning)
- Generates code with Nemotron Ultra
- Critiques and iterates with Nemotron Nano (faster model)
- Self-improvement loop for higher quality code

## Built With
- Nebius Token Factory
- NVIDIA Nemotron (Ultra + Nano)
- Python + OpenAI-compatible client

## License
MIT
