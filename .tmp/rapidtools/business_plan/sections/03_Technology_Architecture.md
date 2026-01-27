# Technology Architecture

> **The Core Insight:** RapidTools encodes 10+ years of manufacturing tooling expertise into software—using the right mix of **computational geometry algorithms & CAD kernels**, **generative AI**, **LLMs**, and **intuitive UX** depending on what's being designed.

---

## The Simple Idea

**Traditional tooling design:** Hire a $150K/year CAD engineer → wait 2-4 weeks → hope it works.

**RapidTools:** Upload your part → answer 5 questions → get a manufacturing-ready tool in hours.

**How?** We've encoded the decision-making process of expert tooling engineers into software. The system knows:

- What questions to ask for each tool type
- What constraints matter (tolerances, materials, manufacturing method)
- How to validate that the design will actually work

---

## The Technology Mix

RapidTools isn't a single technology—it's a **platform that combines four technologies** in different proportions depending on the design task:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     THE RAPIDTOOLS TECHNOLOGY STACK                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────┐ │
│   │  INTUITIVE   │  │    LLMs      │  │  GENERATIVE  │  │  CAD    │ │
│   │     UX       │  │  (GPT-4)     │  │     AI       │  │ KERNELS │ │
│   └──────────────┘  └──────────────┘  └──────────────┘  └─────────┘ │
│         ↓                  ↓                 ↓               ↓      │
│   Captures user      Understands       Generates 3D     Validates   │
│   intent quickly     natural language  geometry fast    precision   │
│                                                         B-spline +  │
│                                                         mesh ops    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
                    ┌───────────────────────────────┐
                    │   MANUFACTURING-READY OUTPUT   │
                    │   (STEP/STL files, ready to    │
                    │    3D print or CNC machine)    │
                    └───────────────────────────────┘
```

**The key insight:** Different tool types need different mixes of these technologies.

---

## 10 Design Automation Tools

Each tool type uses a **tailored combination** of UX, LLMs, Generative AI, and CAD Kernels (B-spline + mesh algorithms):

| **#**  | **Tool Type**                 | **Primary Tech Mix**                                    | **Why This Mix Works**                                                  |
| ------ | ----------------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------- |
| **1**  | **Jigs & Fixtures**           | UX (40%) + CAD Kernels (40%) + LLM (20%)                | Precision-critical; B-spline GD&T validation, mesh Booleans for pockets |
| **2**  | **Assembly Guides**           | UX (50%) + Gen AI (30%) + CAD Kernels (20%)             | Visual complexity; AI generates forms, mesh validation ensures fit      |
| **3**  | **Drilling Guides**           | CAD Kernels (60%) + UX (30%) + LLM (10%)                | Tolerance-critical; NURBS cylinders for exact hole positions (±0.1mm)   |
| **4**  | **Alignment Tools**           | CAD Kernels (50%) + UX (40%) + LLM (10%)                | Datum surfaces require B-spline mathematical precision                  |
| **5**  | **Shadow Boxes**              | Gen AI (50%) + UX (30%) + CAD Kernels (20%)             | Complex 3D pockets; AI generates shapes, mesh Booleans carve cavities   |
| **6**  | **Custom Palletizing**        | LLM (40%) + UX (40%) + CAD Kernels (20%)                | Optimization problem; mesh collision detection validates clearances     |
| **7**  | **Sand Casting Tools**        | Gen AI (40%) + CAD Kernels (40%) + UX (20%)             | Complex patterns; B-spline accuracy for shrinkage compensation          |
| **8**  | **Vacuum Casting Tools**      | CAD Kernels (50%) + Gen AI (30%) + UX (20%)             | Material flow critical; B-spline surface continuity for casting quality |
| **9**  | **Soft Jaws**                 | UX (50%) + CAD Kernels (40%) + LLM (10%)                | B-spline surface matching for exact jaw profile; STEP export for CNC    |
| **10** | **EOAT (End of Arm Tooling)** | LLM (30%) + Gen AI (30%) + CAD Kernels (30%) + UX (10%) | Mesh interference detection + B-spline mounting interface precision     |

---

## How Each Technology Contributes

### 1. Intuitive UX — "Capture Intent Fast"

**What it does:** Guides users through operation-specific questions instead of CAD menus.

**Example (Drilling Guide):**

```
Step 1: Upload your part (STEP file or photo)
Step 2: Select operation → "Drilling"
Step 3: Mark hole locations (click on part)
Step 4: Specify: Hole diameter? → 8mm
                 Tolerance? → ±0.1mm
                 Material? → ABS (3D printed)
Step 5: [Generate] → Done in 2 minutes
```

**Why it matters:** No CAD expertise required. A shop floor technician can design a drilling guide.

### 2. LLMs (GPT-5/Claude) — "Understand Complex Requirements"

**What it does:** Parses natural language into structured design parameters.

**Example (Custom Palletizing):**

```
User types: "I need to pack 48 bottles (75mm diameter, 200mm tall)
            into a 600×400mm Euro pallet, leaving 10mm gaps for
            automated picking."

LLM extracts:
  - Item: Cylinder, Ø75mm × 200mm
  - Quantity: 48
  - Container: 600×400mm
  - Gap requirement: 10mm
  - Constraint: Automated picking access

→ Generates optimal packing layout (6×8 grid)
→ Creates pallet fixture with labeled positions
```

**Why it matters:** Users describe what they need, not how to build it.

### 3. Generative AI — "Create Complex Geometry Fast"

**What it does:** Generates 3D shapes that would take hours to model manually.

**Example (Shadow Box):**

```
Input: Complex automotive part (brake caliper)

Gen AI process:
1. Analyze part geometry (find all surfaces, edges, features)
2. Generate "negative space" (the pocket the part sits in)
3. Add clearances (0.5mm all around)
4. Create registration features (alignment pins)

Output: Shadow box with perfect part-shaped pocket
Time: 30 seconds (vs. 4+ hours manual CAD)
```

**Why it matters:** Complex organic shapes are generated, not hand-modeled.

### 4. Computational Geometry & CAD Kernels — "Guarantee It Works"

**What it does:** Validates every design against manufacturing constraints using industrial-grade geometric algorithms operating in both **B-spline (NURBS)** and **mesh** representations.

**The Dual-Representation Architecture:**

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CAD KERNEL ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌─────────────────────────┐    ┌─────────────────────────┐        │
│   │   B-SPLINE / NURBS      │    │   MESH SPACE            │        │
│   │   (Parametric CAD)      │    │   (Triangulated)        │        │
│   ├─────────────────────────┤    ├─────────────────────────┤        │
│   │ • Exact surface math    │    │ • Fast Boolean ops      │        │
│   │ • GD&T calculations     │    │ • Collision detection   │        │
│   │ • Tolerance analysis    │    │ • Interference checks   │        │
│   │ • STEP/IGES export      │    │ • STL generation        │        │
│   │ • Fillet/chamfer ops    │    │ • Printability analysis │        │
│   └───────────┬─────────────┘    └───────────┬─────────────┘        │
│               │                              │                       │
│               └──────────┬───────────────────┘                       │
│                          ↓                                           │
│              ┌───────────────────────┐                               │
│              │  HYBRID VALIDATION    │                               │
│              │  Best of both worlds  │                               │
│              └───────────────────────┘                               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Why both representations matter:**

| **Operation**              | **B-spline (NURBS)**             | **Mesh Space**                   |
| -------------------------- | -------------------------------- | -------------------------------- |
| **Tolerance calculation**  | ✅ Exact (mathematical surfaces) | ❌ Approximation only            |
| **Boolean operations**     | 🐢 Slow, edge cases              | ✅ Fast, robust                  |
| **GD&T validation**        | ✅ True geometric analysis       | ⚠️ Limited accuracy              |
| **3D print slicing**       | ❌ Must convert first            | ✅ Direct STL output             |
| **Interference detection** | ⚠️ Complex computation           | ✅ Fast triangle-triangle checks |
| **CAD exchange (STEP)**    | ✅ Native format                 | ❌ Lossy conversion              |

**RapidTools' approach:** We use B-spline representations for precision-critical operations (GD&T, tolerances, CAD export) and switch to mesh space for speed-critical operations (Booleans, collision detection, printability). The kernel seamlessly converts between representations as needed.

**The Validation Pipeline:**

| **Check**                  | **What It Validates**                  | **Why It Matters**            |
| -------------------------- | -------------------------------------- | ----------------------------- |
| **Tolerance Stack-Up**     | All dimensions within spec             | Parts actually fit together   |
| **Interference Detection** | No collisions between part and fixture | Design is physically possible |
| **Material Compensation**  | Accounts for shrinkage (ABS: 0.7%)     | Final part is correct size    |
| **Printability**           | Overhangs <45°, min wall thickness     | Design can be manufactured    |
| **Stress Analysis**        | Clamping forces won't break fixture    | Design is durable             |

**Why it matters:** This is what TRELLIS, Meta 3D Gen, and Tripo3D **cannot do**. They generate mesh-only outputs optimized for visual appearance. RapidTools operates in both B-spline (parametric CAD) and mesh space—guaranteeing a hole is exactly 8.0mm ± 0.1mm while also validating printability and generating production-ready STL files.

---

## Tool-by-Tool Technology Breakdown

### 1. Jigs & Fixtures

**Use case:** Hold parts in precise positions during machining, welding, or assembly.

**Technology mix:** UX (40%) + CAD Kernels (40%) + LLM (20%)

**Why this mix:**

- **UX:** User specifies operation type, clamping requirements, access points
- **CAD Kernels:** B-spline analysis for GD&T (parallelism, perpendicularity); mesh Booleans for clearance pockets
- **LLM:** Parses complex requirements ("hold at 45° with flip capability")

**Output:** Production-ready fixture with GD&T compliance (ASME Y14.5) — STEP + STL exports

---

### 2. Assembly Guides

**Use case:** Step-by-step guides showing workers how to assemble products.

**Technology mix:** UX (50%) + Generative AI (30%) + Computational Geometry (20%)

**Why this mix:**

- **UX:** User sequences assembly steps, adds annotations
- **Gen AI:** Generates ergonomic handle positions, visual cues
- **Comp Geom:** Validates part clearances at each step

**Output:** 3D-printable assembly guide with visual instructions

---

### 3. Drilling Guides

**Use case:** Ensure drilled holes are in exactly the right positions.

**Technology mix:** CAD Kernels (60%) + UX (30%) + LLM (10%)

**Why this mix:**

- **CAD Kernels:** B-spline math for exact hole positions (±0.1mm); NURBS cylinders for precision bushings
- **UX:** User clicks hole positions on uploaded part
- **LLM:** Understands "2 M8 holes, 50mm spacing"

**Output:** Drilling guide with precision bushings — B-spline accuracy, mesh-validated for printability

---

### 4. Alignment Tools

**Use case:** Ensure parts are positioned correctly before operations.

**Technology mix:** CAD Kernels (50%) + UX (40%) + LLM (10%)

**Why this mix:**

- **CAD Kernels:** B-spline surface fitting for datum accuracy; NURBS-based parallelism/perpendicularity validation
- **UX:** User selects reference surfaces, alignment requirements
- **LLM:** Parses alignment specs ("parallel within 0.05mm")

**Output:** Alignment fixture with guaranteed datum accuracy — mathematically exact surfaces

---

### 5. Shadow Boxes

**Use case:** Organize tools/parts with custom-shaped pockets (5S/lean manufacturing).

**Technology mix:** Generative AI (50%) + UX (30%) + CAD Kernels (20%)

**Why this mix:**

- **Gen AI:** Generates complex "negative space" from 3D scan of objects
- **UX:** User arranges objects, adds labels
- **CAD Kernels:** Mesh Boolean operations for pocket generation; draft angle validation in both spaces

**Output:** Custom foam/3D-printed organizer — mesh-optimized for fast Booleans, validated geometry

---

### 6. Custom Palletizing

**Use case:** Optimal packing layouts for parts in trays/containers.

**Technology mix:** LLM (40%) + UX (40%) + Computational Geometry (20%)

**Why this mix:**

- **LLM:** Solves bin-packing optimization from natural language
- **UX:** User specifies container size, part dimensions, constraints
- **CAD Kernels:** Mesh-space collision detection for clearance validation; B-spline export for CNC machining

**Output:** Pallet tray with optimized part positions

---

### 7. Sand Casting Tools

**Use case:** Patterns and core boxes for sand casting foundries.

**Technology mix:** Generative AI (40%) + CAD Kernels (40%) + UX (20%)

**Why this mix:**

- **Gen AI:** Generates parting lines, draft angles, gating systems
- **CAD Kernels:** B-spline surfaces for pattern accuracy; shrinkage compensation in parametric space
- **UX:** User uploads part, specifies material (aluminum, iron, bronze)

**Output:** Pattern + core box — NURBS accuracy for pattern-making, mesh validation for moldability

---

### 8. Vacuum Casting Tools

**Use case:** Silicone molds for low-volume plastic production.

**Technology mix:** CAD Kernels (50%) + Generative AI (30%) + UX (20%)

**Why this mix:**

- **CAD Kernels:** B-spline analysis for surface continuity; mesh-space flow simulation for air vents
- **Gen AI:** Generates optimal mold split lines
- **UX:** User specifies material, quantity, surface finish

**Output:** Master pattern + mold design — smooth B-spline surfaces for casting quality

---

### 9. Soft Jaws

**Use case:** Custom chuck jaws that grip specific part shapes.

**Technology mix:** UX (50%) + CAD Kernels (40%) + LLM (10%)

**Why this mix:**

- **UX:** User uploads part, specifies grip surface
- **CAD Kernels:** B-spline surface matching for exact jaw profile; STEP export for CNC machining
- **LLM:** Understands "grip on OD with 3mm wall clearance"

**Output:** Soft jaw design — parametric CAD output ready for CNC programming

---

### 10. EOAT (End of Arm Tooling)

**Use case:** Custom robot gripper/tool attachments.

**Technology mix:** LLM (30%) + Generative AI (30%) + CAD Kernels (30%) + UX (10%)

**Why this mix:**

- **LLM:** Understands robot specs, payload constraints, cycle time requirements
- **Gen AI:** Generates gripper fingers, suction cup layouts
- **CAD Kernels:** Mesh-space interference detection for robot arm clearance; B-spline accuracy for mounting interfaces
- **UX:** User specifies robot model, part to handle

**Output:** Robot-ready EOAT — precision mounting surfaces (B-spline), validated clearances (mesh)

---

## Why This Approach Is Defensible

### vs. Pure AI (TRELLIS, Meta SAM3D Object Gen, Tripo3D)

| **Capability**           | **Pure AI**            | **RapidTools**             |
| ------------------------ | ---------------------- | -------------------------- |
| Generate 3D geometry     | ✅ Fast                | ✅ Fast                    |
| Dimensional accuracy     | ❌ "Approximately 8mm" | ✅ "Exactly 8.0mm ± 0.1mm" |
| Manufacturing validation | ❌ None                | ✅ 7-step pipeline         |
| Repeatable output        | ❌ Different each time | ✅ Identical every time    |
| Output format            | ❌ Mesh only (visual)  | ✅ B-spline + Mesh         |
| CAD exchange             | ❌ No STEP/IGES        | ✅ Native CAD formats      |

**The gap:** AI models generate mesh-only outputs optimized for visual similarity. RapidTools' CAD kernels operate in both B-spline (for precision) and mesh (for speed) spaces—enabling true manufacturing accuracy AND efficient computation.

### vs. Traditional CAD (Autodesk, Siemens)

| **Capability**     | **Traditional CAD**   | **RapidTools**       |
| ------------------ | --------------------- | -------------------- |
| Design time        | 🐢 2-4 weeks          | ⚡ 2-4 hours         |
| Expertise required | ❌ 80+ hours training | ✅ 30 minutes        |
| Who can use it     | CAD engineers only    | Anyone on shop floor |

**The gap:** CAD tools are geometry-centric; we're operation-centric.

---

## The Moat: Encoded Expertise

**What makes RapidTools hard to replicate:**

1. **Domain expertise encoded:** 10+ years of tooling engineering knowledge in validation rules
2. **Tool-specific workflows:** Each of the 10 tools has a tailored UX + validation pipeline
3. **Dual-space CAD kernels:** B-spline algorithms for precision, mesh algorithms for speed—seamlessly integrated
4. **Manufacturing constraints database:** Material properties, tolerance standards, DfAM rules
5. **Data flywheel:** Every design improves our models (10K designs Year 1 → 100K by Year 5)

**Competitors can copy individual technologies** (LLMs, Gen AI). **They can't easily replicate:**

- The **dual-space CAD kernel** architecture (B-spline + mesh operations working together)
- The **domain expertise** encoded in tool-specific validation rules
- The **integration** of 4 technology layers tuned per tool type

---

## Summary for Investors

**The pitch in 30 seconds:**

> RapidTools is Canva for manufacturing tooling. We encode expert knowledge into software, using the right mix of AI + computational geometry + UX for each tool type. A shop floor technician can now design a drilling fixture in 2 hours instead of waiting 2 weeks for a CAD engineer. We're starting with 10 tool types and $650M SAM in India/SE Asia.

**The technology advantage:**

- **Not just AI:** We add CAD kernel validation (what TRELLIS/Meta can't do with mesh-only outputs)
- **Not just CAD:** We add speed + accessibility (what Autodesk can't do without simplifying their kernels)
- **The blend is the moat:** Dual-space CAD kernels + domain expertise + tool-specific technology mix

---

_Last Updated: January 26, 2026_  
_Purpose: Technology Overview for Sequoia Investment Evaluation_  
_Author: RapidTools Technical Team_
