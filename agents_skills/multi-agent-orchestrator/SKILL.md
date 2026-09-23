---
name: multi-agent-orchestrator
description: >-
  Complete 5-Part Elevating Antigravity master engineering suite: interactive UI interviewing (ask_question + user_prefs.json), parameterized visual asset generation (generate_image), parallel subagent dispatch (define_subagent + invoke_subagent across isolated branches), mid-flight telemetry dashboards (send_message), and active process governance & hard circuit breakers (manage_subagents).
---

# Complete 5-Part Elevating Antigravity Architecture & Governance

This master skill provides end-to-end patterns, schemas, state hydration protocols, visual prompt synthesis engines, and process governance for autonomous agent engineering in Google Antigravity.

---

## 🏗️ 1. The Unified 5-Tool Architecture

```mermaid
flowchart TD
    User["Developer / User Input"] --> Parent["1. Parent Orchestrator (juanjo-copilot)
(Main Context: Clean, Sharp & Unpolluted)"]
    
    subgraph Part1_2["Human-in-the-Loop & Visual Studio (Parts 1 & 2)"]
        Parent -->|1. Hydrate State| Hydrate["user_prefs.json State Hydration"]
        Hydrate -->|2. ask_question| Modal["Interactive UI Modals (Radios / Checkboxes)"]
        Modal -->|3. Persist State| Persist["Namespaced Config Persistence"]
        Parent -->|4. generate_image| VisualStudio["Parameterized Visual Studio
(SCENE + CAMERA + LIGHTING + ImagePaths)"]
        VisualStudio -->|5. ask_question Review Loop| AssetReview{"Keep or Regenerate?"}
        AssetReview -->|Keep| PermAsset["Persist to public/images/<name>.png"]
    end
    
    subgraph Part3_5["Orchestration & Governance (Parts 3 & 5)"]
        Parent -->|define_subagent| Reg["Persona Registry (Least Privilege)"]
        Parent -->|invoke_subagent| Swarm["Parallel Workers (Workspace: 'branch')"]
        Parent -->|manage_subagents: list| Audit["Fleet State & Telemetry Auditing"]
        Parent -->|manage_subagents: kill_all| Circuit["Hard Circuit Breaker (SIGKILL)"]
    end
    
    subgraph Part4["Parallel Execution & Mid-Flight Telemetry (Part 4)"]
        Swarm --> W1["Worker 1 (Data Processing)"]
        Swarm --> W2["Worker 2 (Model Training)"]
        W1 -.->|send_message (JSON Telemetry)| Parent
        W2 -.->|send_message (FATAL_ERROR Alarm)| Parent
    end
    
    Parent -->|Reactive Dashboard Update| LiveDash["Live Progress Dashboard"]
    Parent -->|Forensic Report| FinalRep["Consolidated Matrix / Deliverables"]
```

---

## 🎨 2. Part 1: Interactive UI & Round-Trip State Hydration (`ask_question`)

- **State Hydration:** Read `user_prefs.json` at workspace root. Prefix saved values with `"(Current Setting) "` and list them first.
- **Native Write-In:** Omit manual `"Other"` options; `ask_question` automatically provides a native write-in text field.
- **State Persistence:** Write updated selections back to `user_prefs.json` under domain namespaces (`"FORMS"`, `"DEPLOYMENT"`, `"TESTING"`, `"BIOCHEM"`).

---

## 📸 3. Part 2: Parameterized Visual Asset Studio (`generate_image`)

Passing raw prompts causes visual inconsistency and tech debt. Parameterize prompts using structured design tokens:

### A. Structured Prompt Synthesis Template:
```text
Professional studio product photograph of [SUBJECT].
[SCENE: smooth matte light gray surface, seamless background curve with soft infinite horizon].
[CAMERA: macro lens photography, sharp focus from front to back, f/11 aperture, crisp details, zero digital noise].
[LIGHTING: three-point soft-diffuse lighting, 48-inch octagonal softbox key light at 45 degrees, gentle fill light, backlit soft ambient glow, no harsh glare, premium catalog style].
```

### B. Visual Asset Lifecycle & Review Loop:
1. **Check Existing Asset:** Verify whether `public/images/<image_name>.png` already exists to prevent redundant compute.
2. **Issue Parameterized Tool Call:**
   ```json
   {
     "Prompt": "Professional studio product photograph of [SUBJECT]...",
     "ImageName": "mock_product_hero",
     "AspectRatio": "16:9",
     "ImagePaths": ["file:///path/to/reference_logo.png"],
     "toolAction": "Generating hero asset",
     "toolSummary": "Generate product image"
   }
   ```
3. **Interactive Review (`ask_question`):** Prompt developer with `["Keep", "Regenerate", "Exit"]`.
4. **Asset Persistence:** If approved, copy from brain artifact storage to `<workspace>/public/images/<image_name>.png` and render clickable markdown links.

---

## ⚡ 4. Part 3: Parallel Subagents across Isolated Branches (`define_subagent` + `invoke_subagent`)

- **Least Privilege Persona Definition (`define_subagent`):** Set `enable_write_tools: false` for read-only agents; keep `enable_subagent_tools: false`.
- **Branch Isolation (`Workspace: "branch"`):** Concurrently execute workers in isolated branches to eliminate build cache, staging, and lockfile collisions.
- **Zero-Polling Reactive Wakeup:** Parent sleeps; Antigravity reactively wakes the parent when background tasks finish.

---

## 📡 5. Part 4: Mid-Flight Telemetry & Live Dashboards (`send_message`)

- **Structured JSON Telemetry:** Workers transmit milestone payloads (`{"worker": "<Role>", "step": 2, "status": "COMPLETE"}`).
- **Grounded Parent Addressing:** Parent injects its `Conversation ID` into launch prompts.
- **Live Markdown Dashboards:** Parent renders visual progress bars (`[██████████░░░░░░░░░░] Step 2/4`) as events arrive.

---

## 🛑 6. Part 5: Process Governance & Hard Circuit Breakers (`manage_subagents`)

- **Active Fleet Auditing (`manage_subagents: list`):** Inspect active worker states without polling loops.
- **Targeted Kill (`manage_subagents: kill`):** Terminate stuck or looping subagents by ID.
- **Hard Emergency Circuit Breaker (`manage_subagents: kill_all`):** Instantly halt the entire swarm on fatal exceptions, reclaim temporary workspace branches, and preserve logs for forensic post-mortem analysis.

---

## 🛡️ 7. The Complete 14 Anti-Patterns Guardrails

### Interactive UI Anti-Patterns (`ask_question`):
1. ❌ **Option-Fatigue:** Options > 7 items. *Keep under 5–7; pre-filter large datasets.*
2. ❌ **Write-In Redundancy:** Adding explicit `"Other"`. *Antigravity provides native write-ins automatically.*
3. ❌ **Flat Root Keys:** Flat keys in config files. *Always namespace under domain blocks.*
4. ❌ **Third-Person Phrasing:** Command phrasing (*"Set layout"*). *Format as direct user answers (*"Floating labels"*).*

### Visual Asset Anti-Patterns (`generate_image`):
5. ❌ **Raw Prompt Injection:** Passing un-parameterized raw prompts. *Synthesize prompts with SCENE, CAMERA, LIGHTING, and STYLE tokens.*
6. ❌ **Broken / Volatile Links:** Storing assets in `/tmp`. *Copy approved images to permanent `<workspace>/public/images/` paths.*
7. ❌ **Redundant Generation Calls:** Regenerating without checking disk. *Verify if asset exists before triggering `generate_image`.*

### Orchestration Anti-Patterns (`define_subagent` / `invoke_subagent`):
8. ❌ **Over-Permissioning Workers:** Granting full write/MCP tools to read-only agents. *Enforce Least Privilege.*
9. ❌ **Tight-Loop Status Polling:** Polling `manage_task` or sleeping in loops. *Rely on zero-polling reactive wakeup.*
10. ❌ **Un-Scoped Worker Prompts:** Assuming shared context. *Provide 100% self-contained prompts with explicit paths and parent IDs.*
11. ❌ **Un-Isolated Workspaces:** Running parallel builds in shared directories. *Always use `Workspace: "branch"`.*

### Telemetry & Governance Anti-Patterns (`send_message` / `manage_subagents`):
12. ❌ **Unbounded Ping-Pong Loops:** Unconditioned message exchanges. *Enforce mandatory `STATUS: COMPLETE` / `TERMINATE` exit flags.*
13. ❌ **Un-Grounded Recipient IDs:** Forgetting to pass parent ID. *Inject target conversation ID in launch prompts.*
14. ❌ **Free-Form Text Dumps & Spam:** Conversational dumps or high-frequency messages. *Use structured JSON strictly on milestone boundaries.*
