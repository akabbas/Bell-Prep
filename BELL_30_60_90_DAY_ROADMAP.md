# 📋 Bell Textron SAP Ariba Administrator Onboarding Guide
## 30/60/90 Day Roadmap

**Official supervisor onboarding checklist**  
**Source:** SAP Ariba Administrator Onboarding Guide from supervisor  
**Start Date:** January 12, 2026  
**Current Phase:** Days 1-30 (Foundation & Exposure)

---

## 🎯 DAYS 1-30: FOUNDATION & EXPOSURE

**Overall Goal:** Build foundational understanding of SAP Ariba, Strategic Sourcing, Internal Processes & Automation

---

### Phase 1.1: Ariba Fundamentals

**Objectives:**
- [ ] Complete Ariba Intro training modules
- [ ] Learn core terminology: projects, events, templates, supplier profiles, workflows
- [ ] Explore test realm safely
- [ ] Navigate sourcing events, templates, and supplier records

**Key Concepts to Master:**
- Projects (what are they, how are they created)
- Events (sourcing events, types, lifecycle)
- Templates (what they are, how they're used)
- Supplier profiles (structure, data fields)
- Workflows (process flows, approvals)

---

### Phase 1.2: Application Access

**Get Access To:**
- [ ] SAP
- [ ] Ariba Sourcing (test realm)
- [ ] Ariba Sourcing (production realm)
- [ ] Ariba Supply Chain Collaboration (test realm)
- [ ] Ariba Supply Chain Collaboration (production realm)
- [ ] SAP ECC (SR5X roll)
- [ ] Production Linux server
- [ ] DDM.io (soon to be Databricks)
- [ ] SAP Training Academy Courses
- [ ] Azure DevOps

**Status Tracker:**
| Application | Access Level | Date Received | Notes |
|---|---|---|---|
| SAP | | | |
| Ariba Sourcing Test | | | |
| Ariba Sourcing Prod | | | |
| SAP CC Test | | | |
| SAP CC Prod | | | |
| SAP ECC | | | |
| Linux Server | | | |
| Databricks | | | |
| Azure DevOps | | | |

---

### Phase 1.3: Technical Landscape Overview

**Understanding Server Environments:**
- [ ] Understand T01 (test environment) vs P02 (production environment)
- [ ] Learn the differences and why they exist
- [ ] Understand data flow between environments
- [ ] Know when to use test vs production

**API & Access Concepts:**
- [ ] Review API keys (structure, storage, rotation)
- [ ] Understand realm separation (Bell-T vs Bell-P)
- [ ] Learn how realms are isolated
- [ ] Understand why realm separation matters

**Directory & Infrastructure:**
- [ ] Learn directory structures (where code lives, how it's organized)
- [ ] Understand CRON jobs (what they are, how to schedule them)
- [ ] Learn logging concepts (where logs go, how to read them)
- [ ] Understand virtual environments (why they're needed, how to use)

**Key Infrastructure Concepts:**
| Concept | What It Is | Why It Matters |
|---|---|---|
| T01 | Test environment | Safe place to test changes |
| P02 | Production environment | Where real data lives |
| Bell-T | Test realm | Test your Ariba configs |
| Bell-P | Production realm | Real supplier data |
| CRON jobs | Scheduled tasks | Automate recurring work |
| Logging | Record of what happened | Debug issues, audit trail |

---

### Phase 1.4: ADO (Azure DevOps) & Python Codebase Orientation

**Understand Git/ADO Concepts:**
- [ ] Understand ADO branching strategy
- [ ] Learn pull request (PR) workflow
- [ ] Understand deployment process
- [ ] Know code review expectations

**Learn Python Patterns:**
- [ ] Review AUTH modules (authentication handling)
- [ ] Understand pagination logic (why it matters, how it works)
- [ ] Learn rate limit handling (what it is, why we do it)
- [ ] Master logging patterns (how to log properly)

**Database Integration:**
- [ ] Understand Databricks/MS SQL interaction
- [ ] Learn how data flows between systems
- [ ] Understand upstart pipelines

**API Practice:**
- [ ] Run basic API calls in test realm
- [ ] Understand request/response flow
- [ ] Learn error handling
- [ ] Practice with real data (test realm)

**Checklist:**
- [ ] Can create a branch in ADO
- [ ] Can make a pull request
- [ ] Understand code review process
- [ ] Can read Python logging
- [ ] Can write a basic API call
- [ ] Understand pagination
- [ ] Know what rate limiting means

---

### Phase 1.5: Initial Contributions

**Your First Tasks:**
- [ ] Take small L1 tickets related to user guidance
- [ ] Run scripts manually and review logs
- [ ] Apply small fixes under supervision
- [ ] Document what you learned

**Success Criteria:**
- [ ] Completed at least 3 L1 tickets
- [ ] Ran scripts successfully
- [ ] Read and understood logs
- [ ] Made at least 1 supervised fix
- [ ] Asked good questions

---

## 📊 DAYS 31-60: BUILDING COMPETENCE & CAPABILITY

**Overall Goal:** Begin contributing independently, modify code, resolve majority of L1 and some L2 tasks

**Level:** INTERMEDIATE

---

### Phase 2.1: Admin Skill Development

**User & Group Management:**
- [ ] Manage users (create, modify, deactivate accounts)
- [ ] Manage groups and group assignments
- [ ] Configure approvals and approval workflows
- [ ] Manage commodity assignments
- [ ] Handle access requests

**Template & Event Understanding:**
- [ ] Understand template behavior (how templates work, when they're used)
- [ ] Learn events (sourcing events, types, lifecycle, statuses)
- [ ] Understand sourcing concepts (RFQ, RFP, auctions, etc.)
- [ ] Master supplier profiles (structure, fields, updates)
- [ ] Connect templates to real business processes

**Migration Skills:**
- [ ] Learn migration steps from test to production
- [ ] Understand what can/cannot be migrated
- [ ] Know approval process for migrations
- [ ] Understand rollback procedures
- [ ] Practice migrations (with oversight first)

**Checklist:**
- [ ] Can create a new user
- [ ] Can assign user to group
- [ ] Can explain a template
- [ ] Can describe an event
- [ ] Can perform a test-to-prod migration (with supervision)

---

### Phase 2.2: Academy Progression

**SAP Training Academy:**
- [ ] Start at least one lesson
- [ ] Complete at least one lesson
- [ ] Document what you learned
- [ ] Plan remaining courses

**Databricks Training Academy:**
- [ ] Start at least one lesson
- [ ] Complete at least one lesson
- [ ] Document what you learned
- [ ] Plan remaining courses

**Self-Development:**
- [ ] Plan out complete training path
- [ ] Identify courses relevant to your role
- [ ] Schedule time for training
- [ ] Track completion

**Completed Courses:**
| Academy | Course Name | Completed | Date |
|---|---|---|---|
| SAP | | | |
| Databricks | | | |

---

### Phase 2.3: Python & Automation Contributions

**API Work:**
- [ ] Write or extend endpoint wrappers
- [ ] Understand Ariba API structure
- [ ] Learn how to make API calls
- [ ] Handle API responses properly

**ETL Script Development:**
- [ ] Build new extraction scripts
- [ ] Write transform logic
- [ ] Create load procedures
- [ ] Extract supplier data
- [ ] Extract sourcing data
- [ ] Get data pipeline working end-to-end

**Code Quality:**
- [ ] Add error handling (try/except)
- [ ] Add comprehensive logging
- [ ] Add job completion tracking
- [ ] Test thoroughly in test realm
- [ ] Handle edge cases

**Deployment:**
- [ ] Deploy changes via ADO pipeline
- [ ] Validate results after deployment
- [ ] Monitor for issues
- [ ] Be ready to rollback if needed

**Deliverables by Day 60:**
- [ ] 2-3 working automation scripts
- [ ] Proper error handling on all scripts
- [ ] Comprehensive logging
- [ ] Job completion tracking
- [ ] Successfully deployed to test realm
- [ ] Documentation for each script

**Scripts Completed:**
| Script Name | Type | Status | Deployed? | Notes |
|---|---|---|---|---|
| | ETL/Wrapper/Other | | | |
| | ETL/Wrapper/Other | | | |
| | ETL/Wrapper/Other | | | |

---

### Phase 2.4: Ticket Handling & Support

**L1 Ticket Resolution (Common Issues):**
- [ ] Resolve common user issues independently
- [ ] Troubleshoot missing data (where did it go? why?)
- [ ] Handle access issues (user can't access what they need)
- [ ] Troubleshoot workflow routing problems (task went to wrong person)
- [ ] Provide clear solutions

**L2 Ticket Identification:**
- [ ] Identify configuration issues requiring L2 support
- [ ] Know when to escalate vs solve
- [ ] Document escalations properly
- [ ] Learn from L2 solutions

**Support Skills:**
- [ ] Handle tickets professionally
- [ ] Communicate clearly with users
- [ ] Document solutions
- [ ] Know what you don't know and ask

**Ticket Stats by Day 60:**
| Metric | Target | Actual |
|---|---|---|
| L1 tickets resolved independently | 80% | |
| Common issue types handled | 5+ | |
| L2 escalations made (proper) | 2-3 | |

---

### Phase 2.5: Production Readiness

**Learn Production Practices:**
- [ ] Understand change control process
- [ ] Learn deployment procedures
- [ ] Understand rollback procedures
- [ ] Master performance monitoring
- [ ] Learn incident response

**Practice:**
- [ ] Observe a production deployment
- [ ] Understand testing requirements
- [ ] Know approval workflows
- [ ] Learn what "production ready" means

---

## 🚀 DAYS 61-90: OWNERSHIP & INDEPENDENCE

**Overall Goal:** Become a fully capable Ariba Admin + Automation Developer able to own processes end-to-end

---

### Phase 3.1: Functional Ownership

**Take Ownership Of:**
- [ ] Specific templates or workflows (assigned by supervisor)
- [ ] User support for your ownership areas
- [ ] Performance optimization
- [ ] Documentation and knowledge base

**Responsibilities:**
- [ ] Take responsibility for assigned templates/workflows
- [ ] Maintain documentation for ownership areas
- [ ] Perform test-to-prod template migrations (with oversight)
- [ ] Monitor performance
- [ ] Handle escalations

**Documentation Requirements:**
- [ ] Process documentation
- [ ] Troubleshooting guides
- [ ] Configuration guides
- [ ] Known issues and workarounds

---

### Phase 3.2: Automation & Engineering Maturity

**Build Production-Ready Automation:**
- [ ] Write production-quality Python scripts
- [ ] Implement caching for performance
- [ ] Add reliability features (retries, backoff)
- [ ] Optimize performance
- [ ] Handle edge cases

**Create Monitoring & Visibility:**
- [ ] Build dashboards showing system health
- [ ] Create logs summarizing API performance
- [ ] Monitor job success/failure rates
- [ ] Alert on failures
- [ ] Track metrics

**Performance Improvements:**
- [ ] Enhance API performance
- [ ] Add caching where appropriate
- [ ] Improve reliability
- [ ] Document improvements

---

### Phase 3.3: Advanced Support

**Handle Complex Issues:**
- [ ] Resolve complex workflow logic issues
- [ ] Debug routing problems
- [ ] Troubleshoot template behavior
- [ ] Handle API failures
- [ ] Assist in integration issues

**Become the Expert:**
- [ ] Know the system deeply
- [ ] Understand edge cases
- [ ] Can explain "why"
- [ ] Mentor others when possible

---

### Phase 3.4: Deliverables by Day 90

**You Must Deliver:**

1. **Ability to resolve 80% of user issues independently**
   - Can handle most support tickets alone
   - Know when to escalate
   - Consistently fix issues

2. **Ownership of one or more automation workflows**
   - You own it end-to-end
   - You maintain it
   - You can explain it
   - You can modify it

3. **Demonstrated ability to deploy to production safely**
   - Can follow deployment procedures
   - Can verify deployments
   - Understand rollback
   - Know what "safe" means

4. **Two meaningful process improvements delivered**
   - Improvement 1: _________________ (efficiency/reliability/performance)
   - Improvement 2: _________________ (efficiency/reliability/performance)
   - Both have measurable impact
   - Both are documented

---

## 📈 Progress Tracking

### Days 1-30 Status
| Category | Status | Notes |
|---|---|---|
| Ariba Fundamentals | | |
| Application Access | | |
| Technical Landscape | | |
| ADO & Python Orientation | | |
| Initial Contributions | | |

### Days 31-60 Status
| Category | Status | Notes |
|---|---|---|
| Ariba Advanced Topics | | |
| Automation Development | | |
| System Administration | | |
| Production Readiness | | |

### Days 61-90 Status
| Category | Status | Notes |
|---|---|---|
| Functional Ownership | | |
| Automation & Engineering | | |
| Advanced Support | | |
| Day 90 Deliverables | | |

---

## 💡 Key Success Factors

**Throughout All 90 Days:**
- ✅ Ask questions when stuck
- ✅ Document as you learn
- ✅ Test in test realm first
- ✅ Never deploy without testing
- ✅ Follow the process even when it feels slow
- ✅ Celebrate small wins
- ✅ Build relationships with your team
- ✅ Be a learner, not an expert (yet)

**By Day 30:**
- You should understand the concepts
- You should have basic access
- You should be making small contributions
- You should feel less lost than day 1

**By Day 60:**
- You should be handling most tasks independently
- You should have written automation
- You should understand the systems
- You should be confidently contributing

**By Day 90:**
- You should own specific areas
- You should be solving hard problems
- You should be helping others
- You should be ready for independent work

---

## 📝 Daily Learning Log

**Use this section to document what you learn each day for future reference:**

### Week 1 (Days 1-7)
**Day 1 (Jan 12):**
- 

**Day 2 (Jan 13):**
- 

**Day 3 (Jan 14):**
- 

**Day 4 (Jan 15):**
- 

**Day 5 (Jan 16):**
- 

**Day 6 (Jan 17):**
- 

**Day 7 (Jan 18):**
- 

---

## 🎯 Quick Reference

**When you need to remember something:**
- Phase 1 focus: Understand concepts, get access, make small contributions
- Phase 2 focus: Develop competency, build automation, become independent
- Phase 3 focus: Own processes, solve hard problems, mentor others

**Feeling lost?**
- Check what phase you're in
- Review the checklist for that phase
- Ask your supervisor what's next
- Document what you learn

---

*This document is your roadmap. Update it as you progress. You've got this! 💪*
