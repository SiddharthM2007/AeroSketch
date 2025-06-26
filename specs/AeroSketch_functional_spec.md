
# Functional Specification: AI-Accelerated Aerodynamic Simulation Platform for Students

---

## 1. Purpose

To provide a web-based aerodynamic simulation platform that allows students and student organizations to import any 3D design and interactively simulate airflow, lift, drag, and pressure characteristics in real time. The platform leverages AI to reduce computational costs and integrates with large language models (LLMs) via a Model Control Plane (MCP) to function as a copilot, enabling users to ideate and simulate designs conversationally.

---

## 2. Goals

- Democratize access to aerodynamic analysis for students without requiring expensive HPC or CFD expertise.
- Enable rapid iteration of designs through AI-enhanced surrogate simulations.
- Allow LLMs to function as copilots for design ideation, simulation setup, and results interpretation.
- Create an interactive, intuitive, browser-based platform with minimal installation and learning curve.

---

## 3. User Interaction Flow

### A. Manual UI Flow
1. **Login / Register** (OAuth via Google or student email)
2. **Dashboard**: View saved projects, templates, or start a new simulation
3. **Upload 3D Model**: Upload STL/OBJ/glTF file
4. **Parameter Setup**:
   - Select fluid: Air / Water / Custom
   - Set initial conditions: velocity, gravity, fluid density, thrust, angle of attack
   - Choose material: preset options or input density/viscosity
5. **Simulate**:
   - AI engine predicts lift/drag/flow fields based on surrogate model
   - Display vector fields, streamlines, pressure overlays using Bernoulli principle
6. **Analyze Results**:
   - Numeric output: CL, CD, force graphs, pressure maps
   - Visualization: toggle views (lift, drag, velocity, streamlines)
7. **Iterate**:
   - Adjust parameters or geometry
   - Re-simulate or run sensitivity analysis
8. **Export**:
   - Export visualization images, graphs, or download simulation report

### B. LLM Copilot Flow via MCP
1. LLM sends instruction (e.g., "Simulate this shape in water at 15 m/s")
2. MCP API translates into parameterized simulation job
3. Platform returns:
   - Visualization results URL
   - CL/CD values, force diagrams
   - Short explanation for user (via LLM)
4. LLM responds to student: "Your shape has a drag coefficient of 0.7; consider smoothing the rear edge to reduce wake turbulence. Want to try that?"
5. User replies to LLM to rerun with new geometry or parameter tweak
6. Simulation loop continues

---

## 4. Core Features

### A. Simulation Core
- AI surrogate model trained on CFD datasets (OpenFOAM, SU2, etc.)
- Predicts lift, drag, flow visualization fields (pressure, velocity)
- Supports common use-cases: flat plate, airfoil, wing, drone fins, car spoilers

### B. Physics Configuration
- Fluids: Air, Water, Custom (density, viscosity)
- Forces: Gravity toggle, Thrust input, Initial velocity
- Object parameters: Mass, Material properties
- Angle of attack and orientation controls

### C. 3D Visualization
- WebGL/Three.js based visualizer
- Vector overlays: Lift, Drag, Airflow
- Color maps for pressure, velocity
- Adjustable camera, lighting, rotation tools

### D. File Handling
- Upload support: STL, OBJ, glTF
- Model cleanup: auto-check for watertight meshes
- Save/load simulation state

### E. Copilot (LLM Integration)
- MCP-compatible API endpoints:
  - `/simulate`
  - `/set_parameters`
  - `/get_results`
  - `/suggest_optimization`
- Natural language-to-simulation translation
- Result summarization for LLM interface
- Prompt completion APIs for conversational loop

### F. Account & Access Management
- OAuth with Google/Edu
- Role-based access (student, educator)
- Simulation quota limits per tier (free/paid)

### G. Export & Reporting
- Graph exports (CSV, PNG)
- Simulation reports (PDF)
- Export to GitHub repo (optional for student orgs)

---

## 5. Future Enhancements
- Federated training from student-generated designs (with consent)
- LLM-driven design generation (“Create a low-drag fin for water at 5 m/s”)
- VR mode for immersive simulation lab
- Integration with LMS (Canvas, Moodle)

---

This specification defines the baseline for technical design and architecture. Next steps include defining the surrogate model architecture, API schema, frontend wireframes, and training pipeline for physics emulation.
