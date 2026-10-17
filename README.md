# AI Agent Evaluation - Agent Evaluation Harness Ohovo Evaloo Go

**Simple Tool to Test AI Agents**

This tool helps you test how good an AI agent is.
It checks if the agent solves problems correctly and how consistent it is.

---

## What is this tool?

This is a free Python tool that evaluates AI agents.
It works with Claude, ChatGPT, Grok, Gemini, Cursor, and any tool that can run Python.

## Who can use it?

Anyone who builds AI agents and wants to test them.

## Compatible with

- Claude
- ChatGPT
- Grok
- Gemini
- Cursor
- Google Colab
- Any tool that can run Python code

---

How to use this tool (Very Easy Steps)

You do not need to create any file.
Just copy and paste the code directly into the chat.

---

Step 1: Install the tool

What this does?
This installs the evaluation tool.

Where to paste?
Copy the code below and paste it into your AI chat, then press Enter.

```bash
pip install -e .

**What you will see?**

The tool will start installing. Wait until it finishes.

---

### Step 2: Load the tool

**What this does?**

This loads the evaluation tool.

**Where to paste?**

Copy the code below and paste it into the same chat.
```

from live_agent_evalimport EvalHarness

```

**What you will see?**

Nothing special. It just loads the tool.

---

### Step 3: Create the evaluator

**What this does?**

This creates the evaluation tool.

**Where to paste?**

Copy the code below and paste it into the same chat.
```

harness= EvalHarness()

```

**What you will see?**

Nothing appears. It is ready.

---

### Step 4: Load sample issues

**What this does?**

This loads example problems to test the agent.

**Where to paste?**

Copy the code below and paste it into the same chat.
```

issues= harness.load_sample_issues()
print(f"Loaded{len(issues)} sample issues")

```

**What you will see?**

You will see how many sample issues were loaded.

---

### Step 5: Test one issue

**What this does?**

This tests the agent on one problem.

**Where to paste?**

Copy the code below and paste it into the same chat.
```

issue= issues[0]
agent_answer= "Fixed by adding a bounds check"
result= harness.evaluate_one(issue, agent_answer)
print(result)

```

**What you will see?**

You will see the score and result of the test.

---

## Full Example (Copy everything together & paste in the chat)
```

from live_agent_evalimport EvalHarness

harness= EvalHarness()

issues= harness.load_sample_issues()
print(f"Loaded{len(issues)} sample issues")

issue= issues[0]
agent_answer= "Fixed by adding a bounds check"
result= harness.evaluate_one(issue, agent_answer)
print(result)

```

---

## License

Apache-2.0

Free for personal and commercial use.
```
