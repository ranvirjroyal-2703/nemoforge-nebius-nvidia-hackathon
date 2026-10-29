import os
import json
import subprocess
import tempfile
from openai import OpenAI

# Nebius Token Factory (OpenAI-compatible)
client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1",
    api_key=os.getenv("NEBIUS_API_KEY")
)

def call_model(prompt: str, model: str = "nvidia/nemotron-ultra", temperature: float = 0.2) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=2500
    )
    return response.choices[0].message.content.strip()

def execute_code(code: str, timeout: int = 10) -> dict:
    """Actually run the generated code and capture real results."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_path = f.name
    try:
        result = subprocess.run(
            ["python", temp_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "stdout": "", "stderr": "Timeout", "returncode": -1}
    finally:
        os.unlink(temp_path)

def plan_task(task: str) -> str:
    prompt = f"""You are an expert software engineer. Create a precise step-by-step plan to solve this coding task completely, including tests.
Task: {task}
Return only the numbered plan."""
    return call_model(prompt, "nvidia/nemotron-ultra")

def generate_code(task: str, plan: str, previous_error: str = "") -> str:
    error_context = f"\nPrevious execution error to fix:\n{previous_error}" if previous_error else ""
    prompt = f"""Write complete, runnable Python code for this task. Include a main block or clear test calls so it can be executed and verified.
Task: {task}
Plan: {plan}{error_context}
Return ONLY the Python code, no explanations."""
    return call_model(prompt, "nvidia/nemotron-ultra")

def critique_with_results(code: str, execution: dict, task: str) -> str:
    prompt = f"""The following code was executed. Improve it based on the real results.
Task: {task}
Code:
{code}

Execution result:
Success: {execution['success']}
Stdout: {execution['stdout']}
Stderr: {execution['stderr']}

Return the full improved Python code only."""
    return call_model(prompt, "nvidia/nemotron-nano")

def run_codeevolve(task: str, max_iterations: int = 3) -> dict:
    print("=== CodeEvolve Agent Started ===")
    print("Planning with Nemotron Ultra...")
    plan = plan_task(task)
    print(plan)
    
    code = ""
    execution = {"success": False, "stderr": "No code yet"}
    
    for i in range(max_iterations):
        print(f"\n--- Iteration {i+1} ---")
        print("Generating code with Nemotron Ultra...")
        code = generate_code(task, plan, execution.get("stderr", ""))
        
        print("Executing code (real runtime)...")
        execution = execute_code(code)
        print(f"Success: {execution['success']}")
        if execution["stdout"]:
            print(f"Output: {execution['stdout'][:500]}")
        if execution["stderr"]:
            print(f"Error: {execution['stderr'][:500]}")
        
        if execution["success"] and not execution["stderr"]:
            print("Code passed execution. Stopping.")
            break
        
        if i < max_iterations - 1:
            print("Critiquing with real results using Nemotron Nano...")
            code = critique_with_results(code, execution, task)
    
    return {
        "task": task,
        "plan": plan,
        "final_code": code,
        "final_execution": execution,
        "iterations": i + 1
    }

if __name__ == "__main__":
    task = "Write a Python function is_palindrome that ignores case, spaces and punctuation, and test it with at least 5 examples including edge cases."
    result = run_codeevolve(task)
    print("\n=== FINAL RESULT ===")
    print(json.dumps({
        "success": result["final_execution"]["success"],
        "iterations": result["iterations"],
        "stdout": result["final_execution"]["stdout"][:300]
    }, indent=2))
