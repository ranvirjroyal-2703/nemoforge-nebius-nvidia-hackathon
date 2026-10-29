import os
import json
import subprocess
import tempfile
import streamlit as st
from openai import OpenAI

# Nebius Token Factory
client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1",
    api_key=os.getenv("NEBIUS_API_KEY")
)

def call_model(prompt: str, model: str, temperature: float = 0.2) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=3000
    )
    return response.choices[0].message.content.strip()

def safe_execute(code: str, timeout: int = 8) -> dict:
    """Execute code with timeout and capture results. Isolated temp file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        path = f.name
    try:
        result = subprocess.run(
            ["python", path],
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
        return {"success": False, "stdout": "", "stderr": "Execution timed out", "returncode": -1}
    finally:
        os.unlink(path)

def run_tests(code: str, tests: str) -> dict:
    """Combine code + tests and execute."""
    full = code + "\n\n" + tests
    return safe_execute(full)

def agent_loop(task: str, max_iters: int = 3):
    trace = []
    
    # Phase 1: Plan (Ultra)
    plan = call_model(
        f"Create a detailed plan with test cases for: {task}. Number the steps.",
        "nvidia/nemotron-ultra"
    )
    trace.append({"phase": "Plan", "content": plan})
    
    code = ""
    tests = ""
    execution = {"success": False, "stderr": "Initial"}
    
    for i in range(max_iters):
        # Generate code + tests
        gen_prompt = f"""Task: {task}
Plan: {plan}
Previous error: {execution.get('stderr', '')}
Write complete Python code AND separate pytest-style tests.
Format:
CODE:
<python code>
TESTS:
<pytest tests>"""
        generated = call_model(gen_prompt, "nvidia/nemotron-ultra")
        
        # Simple split (in production use better parsing)
        if "TESTS:" in generated:
            code_part, tests_part = generated.split("TESTS:", 1)
            code = code_part.replace("CODE:", "").strip()
            tests = tests_part.strip()
        else:
            code = generated
            tests = "print('No tests generated')"
        
        execution = run_tests(code, tests)
        trace.append({
            "phase": f"Iteration {i+1}",
            "code": code[:800],
            "tests": tests[:400],
            "execution": execution
        })
        
        if execution["success"] and "Error" not in execution.get("stderr", ""):
            break
        
        # Critique with Nano
        critique = call_model(
            f"Improve the code based on this real execution result:\n{execution}\nCode was:\n{code}",
            "nvidia/nemotron-nano"
        )
        code = critique  # simplified for demo
    
    return {"trace": trace, "final_success": execution.get("success", False)}

# Streamlit UI
st.set_page_config(page_title="NemoAgent Studio", layout="wide")
st.title("NemoAgent Studio")
st.caption("Autonomous coding agent with real execution & test feedback | Nebius + NVIDIA Nemotron")

task = st.text_area("Coding Task", value="Write a function that checks if a string is a palindrome (ignore case, spaces, punctuation) and include tests for edge cases.", height=100)

if st.button("Run Agent", type="primary"):
    if not os.getenv("NEBIUS_API_KEY"):
        st.error("Set NEBIUS_API_KEY environment variable")
    else:
        with st.spinner("Agent is planning, coding, executing, and iterating..."):
            result = agent_loop(task)
        
        st.success("Agent finished") if result["final_success"] else st.warning("Agent finished with issues")
        
        for step in result["trace"]:
            with st.expander(step["phase"], expanded=True):
                if "content" in step:
                    st.markdown(step["content"])
                if "code" in step:
                    st.code(step["code"], language="python")
                if "execution" in step:
                    st.json(step["execution"])
