# Evolution of Todo - Global Constitution

> **Supreme Governing Document**
> Version: 1.0
> Scope: Phase I through Phase V
> Status: ACTIVE AND IMMUTABLE

---

## Preamble

This Constitution establishes the fundamental laws, principles, and constraints governing the development of the "Evolution of Todo" project. All agents, specifications, plans, and implementations must comply with this document. No code shall be written, no feature shall be added, and no architectural decision shall be made without explicit alignment to this Constitution and its derivative specifications.

---

## Article I: Spec-Driven Development Mandate

### Section 1.1 - Core Principle
Spec-Driven Development is **MANDATORY** for all project activities. No exceptions are permitted.

### Section 1.2 - Development Hierarchy
All work must follow this strict hierarchy:

```
Constitution (this document)
      ↓
Specifications (phase-specific specs)
      ↓
Plans (implementation strategies)
      ↓
Tasks (atomic work units)
      ↓
Implementation (code)
```

### Section 1.3 - Specification Requirements
- No agent may write code without approved specifications
- All specifications must be documented in the `/specs` directory
- Specifications must be versioned and traceable
- Each specification must reference this Constitution

### Section 1.4 - Approval Gates
- Specifications require review before plan generation
- Plans require approval before task breakdown
- Tasks require validation before implementation
- Implementation requires verification against specifications

---

## Article II: Agent Behavior Rules

### Section 2.1 - Prohibited Actions
The following actions are **STRICTLY FORBIDDEN**:

1. **No Manual Human Coding**: All code must be generated through AI agents following approved specs
2. **No Feature Invention**: Agents must not create features not explicitly defined in specifications
3. **No Specification Deviation**: Implementation must match specifications exactly
4. **No Scope Creep**: Work must remain within the boundaries of the current phase
5. **No Assumption-Based Development**: Ambiguities must be resolved through specification refinement

### Section 2.2 - Required Actions
Agents **MUST**:

1. Consult this Constitution before beginning any work
2. Reference the relevant phase specification
3. Create or follow an approved plan
4. Break work into traceable tasks
5. Implement only what is specified
6. Validate output against specifications

### Section 2.3 - Refinement Protocol
- All refinements must occur at the **specification level**, not the code level
- Code changes require specification updates first
- The flow is always: Spec Change → Plan Update → Task Revision → Code Modification

### Section 2.4 - Agent Communication
- Agents must document decisions and rationale
- Agents must flag specification gaps or ambiguities
- Agents must not proceed with ambiguous requirements

---

## Article III: Phase Governance

### Section 3.1 - Phase Isolation
Each phase is **strictly scoped** by its specification:

| Phase | Scope | Boundaries |
|-------|-------|------------|
| Phase I | In-Memory Console App | Python CLI, no persistence, no API |
| Phase II | Database Integration | Add persistence, maintain CLI |
| Phase III | API Layer | REST API, maintain backward compatibility |
| Phase IV | Frontend & AI | Next.js UI, AI capabilities |
| Phase V | Cloud-Native Distribution | Kubernetes, event-driven, full scale |

### Section 3.2 - Feature Leakage Prevention
- **Future-phase features must NEVER leak into earlier phases**
- Each phase must be complete and functional independently
- Phase boundaries are non-negotiable
- Cross-phase dependencies must be documented in specifications

### Section 3.3 - Architecture Evolution
- Architecture may evolve **ONLY** through updated specifications and plans
- No architectural changes without Constitution compliance verification
- Evolution must be backward-compatible unless explicitly specified
- Each phase builds upon, not replaces, previous phases

### Section 3.4 - Phase Completion Criteria
A phase is complete only when:
1. All specified features are implemented
2. All deliverables are present
3. Documentation is complete
4. The implementation passes specification validation

---

## Article IV: Technology Constraints

### Section 4.1 - Mandatory Technology Stack

#### Phase I (Console App)
- **Runtime**: Python 3.13+
- **Package Manager**: UV
- **Development**: Claude Code, Spec-Kit Plus

#### Phase II (Database)
- **ORM**: SQLModel
- **Database**: Neon DB (PostgreSQL)

#### Phase III (API)
- **Framework**: FastAPI
- **Validation**: Pydantic

#### Phase IV (Frontend & AI)
- **Frontend**: Next.js
- **AI Framework**: OpenAI Agents SDK
- **Protocol**: MCP (Model Context Protocol)

#### Phase V (Cloud-Native)
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Messaging**: Kafka
- **Runtime**: Dapr

### Section 4.2 - Technology Substitution
- Core technologies listed above are **NON-NEGOTIABLE**
- Supporting libraries may be added if they don't conflict with core stack
- All technology additions must be documented in phase specifications

### Section 4.3 - Version Requirements
- All dependencies must use stable, production-ready versions
- Security updates are permitted without specification changes
- Major version upgrades require specification amendment

---

## Article V: Quality Principles

### Section 5.1 - Clean Architecture
All implementations must adhere to:

1. **Single Responsibility**: Each module has one reason to change
2. **Dependency Inversion**: Depend on abstractions, not concretions
3. **Interface Segregation**: No client should depend on unused methods
4. **Open/Closed**: Open for extension, closed for modification
5. **Liskov Substitution**: Subtypes must be substitutable for base types

### Section 5.2 - Separation of Concerns
The codebase must maintain clear boundaries between:

- **Presentation Layer**: User interface and input/output handling
- **Business Logic Layer**: Core domain rules and operations
- **Data Layer**: Storage and retrieval mechanisms

### Section 5.3 - Stateless Services
Where applicable (Phase III+):

- Services must be stateless
- State must be externalized to databases or caches
- No in-process session storage in API services

### Section 5.4 - Cloud-Native Readiness
All code must be written with cloud deployment in mind:

- Configuration through environment variables
- No hardcoded secrets or connection strings
- Graceful shutdown handling
- Health check compatibility
- Horizontal scalability considerations

### Section 5.5 - Code Quality Standards
- Meaningful variable and function names
- Docstrings for public interfaces
- Type hints throughout (Python)
- No magic numbers or strings
- Error handling with meaningful messages

---

## Article VI: Documentation Requirements

### Section 6.1 - Required Documentation
Every phase must include:

1. **README.md**: Setup and usage instructions
2. **CLAUDE.md**: Claude Code specific instructions
3. **Specification Files**: In `/specs` directory
4. **Inline Documentation**: Code comments where necessary

### Section 6.2 - Specification Documentation
Each specification must contain:

- Feature description
- Acceptance criteria
- Technical constraints
- Dependencies
- Deliverables

### Section 6.3 - Change Documentation
All changes must be traceable:

- Specification version history
- Plan revision records
- Implementation change logs

---

## Article VII: Enforcement

### Section 7.1 - Constitution Supremacy
This Constitution is the **supreme governing document**. In case of conflict:

1. Constitution takes precedence over all other documents
2. Phase specifications take precedence over plans
3. Plans take precedence over individual tasks
4. Tasks take precedence over implementation decisions

### Section 7.2 - Violation Handling
Constitution violations require:

1. Immediate halt of violating work
2. Root cause analysis
3. Specification-level correction
4. Re-implementation following proper flow

### Section 7.3 - Amendment Process
This Constitution may only be amended through:

1. Formal amendment proposal
2. Impact analysis across all phases
3. Explicit approval documentation
4. Version increment of this document

---

## Article VIII: Definitions

| Term | Definition |
|------|------------|
| **Agent** | AI system (Claude Code) performing development tasks |
| **Specification** | Formal document defining features and requirements |
| **Plan** | Strategic document outlining implementation approach |
| **Task** | Atomic unit of work derived from a plan |
| **Phase** | Major project milestone with defined scope |
| **Constitution** | This supreme governing document |

---

## Signatures

**Document Status**: RATIFIED
**Effective Date**: 2025-12-29
**Governing Scope**: All phases of Evolution of Todo project
**Authority**: Project Constitution - Immutable unless formally amended

---

*This Constitution ensures consistent, high-quality, specification-driven development across the entire Evolution of Todo project lifecycle.*
