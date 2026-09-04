# GameForge — Enterprise Game Development & Publishing Management Platform

**GameForge** is a centralized, production-grade enterprise web platform designed for game development studios, indie teams, publishers, and live-operations crews. Built on **Django 5 (MVT Architecture)** with **SQLite3**, it unifies the entire game production lifecycle: project roadmaps, agile sprints, defect tracking, CI/CD build pipelines, digital asset vaults, semantic versioning, multi-platform publishing gates, store listings, player telemetries, gamer achievements, competitive leaderboards, virtual economy monetization, help desk support, audit logging, and role-based access control (RBAC).

---

## Key Feature Matrix & Apps Architecture

GameForge is structured into **22 focused Django applications** inside the `apps/` directory:

| App | Purpose & Core Capabilities |
|---|---|
| [`accounts`](file:///apps/accounts/) | Custom User model with 10 enterprise roles, user avatars, API keys, preferences, auth workflows, and command center. |
| [`organizations`](file:///apps/organizations/) | Studio multi-tenancy, departments, role invitations, seat tiers, and organizational profiles. |
| [`teams`](file:///apps/teams/) | Development squads, discipline skill mapping, member workload capacities, and squad hubs. |
| [`games`](file:///apps/games/) | Franchise catalog across Unreal Engine 5, Unity 6, Godot 4, Custom C++, budgets, platforms, and milestone tracking. |
| [`projects`](file:///apps/projects/) | Sub-project roadmaps, risk registers, progress percentages, and producer management. |
| [`tasks`](file:///apps/tasks/) | Full Kanban board, sprint backlogs, task types, time logging, subtasks, and real-time status updates. |
| [`bugs`](file:///apps/bugs/) | QA defect tracker with blocker/critical triage, reproduction steps, callstack crash logs, and retest states. |
| [`builds`](file:///apps/builds/) | CI/CD build pipelines for Win64, Linux, macOS, PS5, Xbox Series X, Switch, Android & iOS with QA smoke gates. |
| [`assets`](file:///apps/assets/) | Digital asset vault for 3D high-poly meshes, 4K PBR textures, spatial audio WAVs, shaders, and UI packs. |
| [`versions`](file:///apps/versions/) | Semantic versioning manager (v1.0.0, v2.1.0-beta), changelogs, and binary link associations. |
| [`releases`](file:///apps/releases/) | Deployment gate sign-offs, stage checklists, multi-store launch schedules, and rollback management. |
| [`store`](file:///apps/store/) | Storefront CMS for Steam, Epic Games Store, PlayStation Network, Xbox Marketplace & Nintendo eShop. |
| [`players`](file:///apps/players/) | Player profiles, level progression, XP telemetry, virtual wallet balances, and moderation bans. |
| [`achievements`](file:///apps/achievements/) | Gamer points, Bronze/Silver/Gold/Platinum trophy tiers, and unlock rules. |
| [`leaderboards`](file:///apps/leaderboards/) | Competitive seasonal ranking ladders, high scores, speedrun time-trials, and rank calculations. |
| [`analytics`](file:///apps/analytics/) | LiveOps executive analytics, DAU/MAU charts, CCU monitoring, framerate stability, and event ingestion. |
| [`monetization`](file:///apps/monetization/) | Battle passes, DLC expansion packs, cosmetic skins, virtual currency packs, and purchase ledgers. |
| [`notifications`](file:///apps/notifications/) | In-app notification center, real-time alert badges, task assignment pings, and build status warnings. |
| [`support`](file:///apps/support/) | Customer support desk, ticket priority routing, player communication threads, and resolution workflows. |
| [`reports`](file:///apps/reports/) | Executive studio summaries, QA defect velocity reports, revenue breakdowns, and print/PDF export layouts. |
| [`permissions`](file:///apps/permissions/) | Interactive matrix-based Role-Based Access Control (RBAC) security policy inspector. |
| [`audit`](file:///apps/audit/) | Immutable system activity stream, security authentication audits, and operational change tracking. |

---

## Technology Stack

- **Backend**: Python 3.11, Django 5.0.6 (MVT Architecture), Django ORM, Django Templates, Class-Based Views & Mixins.
- **Database**: SQLite3 (`db.sqlite3`) with indexing and foreign-key integrity. Zero external database required.
- **Frontend**: Responsive Dark SaaS Design System, Bootstrap 5.3, Bootstrap Icons, Chart.js 4.4, custom CSS with neon cyberpunk accents.
- **Security**: Strict CSRF protection, RBAC permission checks, SQL injection prevention, safe file uploads, sanitized inputs.

---

## Quick Start & Installation

### 1. Database Setup & Migrations
```powershell
python manage.py migrate
```

### 2. Populate Enterprise Demo Data
GameForge includes a complete studio demo seeder:
```powershell
python manage.py seed_gameforge_demo
```

### 3. Launch the Server
```powershell
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/`** in your browser.

---

## Default Demo Credentials

| Role | Username | Password |
|---|---|---|
| **Super Admin / CTO** | `admin` | `AdminPass123!` |
| **Studio Head** | `sarah_connor` | `StudioPass123!` |
| **Lead Producer** | `marcus_fenix` | `StudioPass123!` |
| **Lead Graphics Architect** | `elena_fisher` | `StudioPass123!` |
| **Senior Gameplay Dev** | `gordon_freeman` | `StudioPass123!` |
| **Lead 3D Artist** | `claire_redfield` | `StudioPass123!` |
| **QA Strike Lead** | `leon_kennedy` | `StudioPass123!` |
| **Publishing Director** | `sam_porter` | `StudioPass123!` |
| **Player Support Agent** | `ada_wong` | `StudioPass123!` |

---

## Automated Test Suite

Execute the full automated test suite covering all 22 modules:
```powershell
python manage.py test apps.accounts apps.organizations apps.teams apps.games apps.projects apps.tasks apps.bugs apps.builds apps.assets apps.versions apps.releases apps.store apps.players apps.achievements apps.leaderboards apps.analytics apps.monetization apps.notifications apps.support apps.reports apps.permissions apps.audit
```
All tests pass cleanly with **0 failures, 0 errors**.
