import os
import json
import subprocess
import tempfile
from openai import OpenAI

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1",
    api_key=os.getenv("NEBIUS_API_KEY")
)

def call_agent(role_prompt: str, user_content: str, model: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": role_prompt},
            {"role": "user", "content": user_content}
        ],
        temperature=0.2,
        max_tokens=2500
    )
    return response.choices[0].message.content.strip()

def execute(code: str, timeout: int = 10) -> dict:
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        path = f.name
    try:
        r = subprocess.run(["python", path], capture_output=True, text=True, timeout=timeout)
        return {"success": r.returncode == 0, "stdout": r.stdout, "stderr": r.stderr}
    except subprocess.TimeoutExpired:
        return {"success": False, "stdout": "", "stderr": "Timeout"}
    finally:
        os.unlink(path)

# Specialized Agents
PLANNER = "You are the Planner Agent. Create a precise plan and clear acceptance criteria for the coding task."
CODER = "You are the Coder Agent. Write clean, complete, runnable Python code that satisfies the plan and acceptance criteria."
TESTER = "You are the Tester Agent. Write pytest-style tests that verify the acceptance criteria. Then the system will execute them."
REVIEWER = "You are the Reviewer Agent. Analyze the code and real test/execution results. Decide if it passes or what must be fixed."

def nemoswarm(task: str, max_rounds: int = 3):
    print("=== NemoSwarm Multi-Agent System ===\n")
    
    # Planner
    plan = call_agent(PLANNER, f"Task: {task}", "nvidia/nemotron-ultra")
    print("PLANNER:\n", plan, "\n")
    
    code = ""
    tests = ""
    execution = {"success": False, "stderr": "None"}
    
    for round_num in range(1, max_rounds + 1):
        print(f"--- Round {round_num} ---")
        
        # Coder
        code = call_agent(
            CODER,
            f"Plan and criteria:\n{plan}\nPrevious issues:\n{execution.get('stderr', '')}\nWrite the full Python code.",
            "nvidia/nemotron-ultra"
        )
        print("CODER produced code.")
        
        # Tester
        tests = call_agent(
            TESTER,
            f"Acceptance criteria from plan:\n{plan}\nCode to test:\n{code}\nWrite only the test code.",
            "nvidia/nemotron-ultra"
        )
        print("TESTER produced tests.")
        
        # Execute code + tests
        full = code + "\n\n" + tests
        execution = execute(full)
        print(f"EXECUTION → success={execution['success']}")
        if execution["stderr"]:
            print("Errors:", execution["stderr"][:300])
        
        # Reviewer
        review = call_agent(
            REVIEWER,
            f"Code:\n{code}\nTests:\n{tests}\nExecution result:\n{json.dumps(execution)}\nDoes this pass the acceptance criteria? What must change?",
            "nvidia/nemotron-nano"
        )
        print("REVIEWER:\n", review[:400], "\n")
        
        if execution["success"] and "pass" in review.lower():
            print("Swarm consensus: PASSED")
            break
    
    return {"plan": plan, "final_code": code, "final_tests": tests, "execution": execution}

if __name__ == "__main__":
    task = "Implement a function that validates email addresses with reasonable rules and provide thorough tests."
    result = nemoswarm(task)
    print("\n=== SWARM COMPLETE ===")
    print("Final success:", result["execution"]["success"])
