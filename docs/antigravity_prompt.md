# Antigravity Prompt: Greenfield NLS (Natural Language Source) MVP

**Role:** You are a Founding Engineer and Language Designer.
**Context:** We are starting a new project called **Natural Language Source (NLS)**.
**Reference Material:** Read `PRD.md` in the current directory carefully, specifically focusing on **Phase 1: Foundation** and the **Strategic Considerations** (MVP Focus).

---

## The Mission

Your goal is to build the **Phase 1 MVP** of NLS.
We are **not** building the VS Code extension, the compliance standard, or the legacy atomization tools yet.
We are building the **Compiler (`nlsc`)** and defining the **Language Schema**.

**The Thesis:** "The conversation is the programming. The `.nl` file is the receipt. The code is the artifact."

## Success Criteria for this Session

By the end of this session, we must have a working CLI tool (`nlsc`) that can:

1.  Initialize a new project (`nlsc init`).
2.  Read a valid `.nl` file (like the math example in Appendix B of the PRD).
3.  Compile it into executable Python code using a deterministic process (mock the LLM part if needed, or use an available API).
4.  Verify that the generated code runs.

## Technical Stack & Constraints

- **Language:** Python (for both the compiler implementation and the target language).
- **Architecture:** Modular (Parser -> Resolver -> Emitter).
- **No "Big Bang":** detailed parsing logic (like Tree-sitter) is good if possible, but a robust regex/structured parser is acceptable for V0 to get the "Math" example working immediately.
- **Determinism:** The compiler _must_ be capable of using a lockfile concept, even if rudimentary.

## Step-by-Step Execution Plan

### Step 1: Schema Definition

Define the strict structure of an ANLU (Atomic Natural Language Unit).

- Create `nl-schema.yaml` or a formal EBNF/Grammar definition.
- Must include: Identifier, Purpose, Inputs, Logic, Returns.

### Step 2: The CLI Scaffold

Create the `nlsc` entry point.

- `nlsc init`: Generates `nl.config.yaml` and folder structure.
- `nlsc compile <file.nl>`: The core command.

### Step 3: The Compiler Core

Implement the compilation pipeline:

- **Parser:** Read `.nl` files into an AST (list of ANLUs).
- **Resolver:** Check simple dependencies (if ANLU A depends on B).
- **Emitter (LLM Integration):**
  - Since we are in a dev environment, use a prompt-template approach.
  - Input: ANLU structure.
  - System Prompt: "You are the NLS Compiler. Translate this ANLU to Python."
  - Output: Python code block.
  - _Constraint:_ If LLM tools are unavailable, implement a "Mock LLM" that handles the Math example deterministically via regex for demonstration.

### Step 4: Verification (The "Math" Example)

Create the exact `src/math.nl` file from Appendix B.
Run `nlsc compile src/math.nl`.
Verify `src/math.py` is generated.
Run the python code to prove `add(2,3) == 5`.

## Your First Action

Analyze `PRD.md` and propose the exact file structure you are about to build. Then, ask for approval to proceed with scaffolding.
