import os
import json
from openai import OpenAI  # Nebius Token Factory is OpenAI-compatible

# Set your Nebius Token Factory key
client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1",  # Confirm exact base URL in your Nebius dashboard
    api_key=os.getenv("NEBIUS_API_KEY")
)

def call_nemotron(prompt: str, model: str = "nvidia/nemotron-ultra", temperature: float = 0.3) -> str:
    """Call NVIDIA Nemotron via Nebius Token Factory"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=2000
    )
    return response.choices[0].message.content

def plan_task(task: str) -> str:
    prompt = f"""You are an expert software engineer. Create a clear step-by-step plan to solve this coding task.
Task: {task}
Return only the numbered plan."""
    return call_nemotron(prompt, model="nvidia/nemotron-ultra")

def generate_code(task: str, plan: str) -> str:
    prompt = f"""Write clean, working Python code for this task.
Task: {task}
Plan: {plan}
Include basic tests or validation logic. Return only the code."""
    return call_nemotron(prompt, model="nvidia/nemotron-ultra")

def critique_and_improve(code: str, task: str) -> str:
    prompt = f"""Review this code for the task. Find bugs, edge cases, or improvements.
Task: {task}
Code:
{code}
Provide improved version of the full code."""
    return call_nemotron(prompt, model="nvidia/nemotron-nano")  # Faster model for iteration

def run_agent(task: str, max_iterations: int = 2) -> dict:
    print("Planning...")
    plan = plan_task(task)
    
    print("Generating initial code...")
    code = generate_code(task, plan)
    
    for i in range(max_iterations):
        print(f"Iteration {i+1}: Critiquing...")
        improved = critique_and_improve(code, task)
        if improved.strip():
            code = improved
    
    return {
        "task": task,
        "plan": plan,
        "final_code": code
    }

if __name__ == "__main__":
    sample_task = "Write a Python function that validates if a string is a valid palindrome, ignoring spaces and punctuation."
    result = run_agent(sample_task)
    print("\n=== FINAL RESULT ===")
    print(json.dumps(result, indent=2))
