<div align="center">
  <img src="assets/jaswanth-hero.svg" alt="Jaswanth Rathore — Software Engineer, Full-Stack Developer, DevOps and Cloud Engineer, AI/ML Engineer" width="100%">
</div>

<br>

## About

I'm a software engineer with a B.E. in Computer Science and Engineering from Sathyabama Institute of Science and Technology, Chennai (2022–2026). I work across the stack: React and TypeScript front ends, Node.js and Python back ends, containerised services, and automated pipelines.

The projects below share a theme: make decisions inspectable. TalentLens AI keeps every screening decision reviewable and deterministic, with an optional, bounded LLM layer. The learning-activity tracker records only what it can actually observe.

<!--
EDUCATION — CGPA intentionally omitted: no evidence in the repo. If you want it shown, add:
B.E. Computer Science and Engineering · CGPA 7.63/10
-->

## Experience

**Tiger Analytics** — DevOps Intern (Full-Stack Development)

<!--
VERIFY AND UNCOMMENT — dates and responsibilities were not in the supplied files. Add only what your resume supports:

*Month YYYY – Month YYYY*
- <responsibility 1, e.g. what you built or automated, with the real tools you used>
- <responsibility 2>
- <outcome, only if it is real and you can stand behind it>
-->

## Achievements

- **Google Skills** — 44 badges on my [public profile](https://www.skills.google/public_profiles/def4bf30-fead-4bf0-81b4-d1c68bcbb7bc) (count observed 21 Oct 2026).
- **LeetCode** — 111 accepted problems (37 easy · 56 medium · 18 hard), observed 21 Oct 2026. [Profile](https://leetcode.com/u/JaswanthRathore/)

<!--
CERTIFICATIONS / COMPETITIONS — none could be verified from the supplied files, so none are listed.
Add each as: - **Exact certification name** — Issuer, Month YYYY ([credential](real-url))

Previously listed in the old README without supporting evidence (add back only with proof such as merged PR links):
- Elite Coders — Winter of Code 2025
- Open Source Connect Global — 2025
-->

## Selected projects

### TalentLens AI
A command-line resume screener that reads a folder of PDF resumes, applies hard eligibility rules, scores the eligible candidates out of 100 with visible evidence, and writes a ranked JSON report plus a terminal summary.

- **Deterministic core:** eligibility, scoring and ranking contain no model calls, so results are reproducible. A candidate qualifies only with Python and AI/agentic work shown inside a project or job entry, not just listed under skills.
- **Evidence model:** each signal is graded from keyword-only to deep implementation, and the JSON carries the supporting text. An optional LLM pass is schema-validated, capped at ±6 points, and falls back to deterministic scoring on failure.
- **Robustness:** SHA-256 duplicate detection, per-file failure isolation, and cached GitHub enrichment. The suite has 60 pytest tests.

`Python` `pypdf` `requests` `pytest` · [Repository](https://github.com/Jass-pvt/talentlens-ai)

### GATE 2027 Tracker
A full-stack study tracker with a working core: JWT authentication, a dashboard (exam countdown, streaks, weekly and monthly hours, progress ring, study-hours chart), a daily study log, and a subjects module. The repository's own README marks the remaining modules as scaffolded, not built.

- **API design:** Express and TypeScript with Sequelize on PostgreSQL, bcrypt password hashing, Helmet, rate-limited auth routes, and model-level validation (ranges, email format).
- **Delivery:** backend Dockerfile (multi-stage) and a Docker Compose setup for the API and database, with Jest and Supertest tests.

`React` `TypeScript` `Vite` `Tailwind CSS` `Node.js` `Express` `PostgreSQL` `Docker` · [Repository](https://github.com/Jass-pvt/gate2027-tracker)

### Learning Activity Analytics
A Python tracker that snapshots my public Google Skills, LeetCode and GeeksforGeeks profiles on a schedule and logs only activity it can actually observe.

- **Honest data handling:** the first run is a baseline with no backfill, unavailable values stay `null` instead of being guessed, and the last good state is kept when a source fails.
- **Automation:** a daily GitHub Actions workflow commits dated JSON snapshots, and a CI workflow runs 7 pytest tests.
- **Limitation:** the collectors are best-effort and depend on third-party page structure and rate limits.

`Python` `requests` `BeautifulSoup` `GitHub Actions` `pytest` · [Repository](https://github.com/Jass-pvt/learning-activity-analytics)

## Skills

Listed from what the repositories above actually use.

| Area | Technologies |
| :-- | :--  |
| Languages | Python · TypeScript · JavaScript |
| Front end | React · Vite · Tailwind CSS · Recharts · Framer Motion |
| Back end | Node.js · Express · Sequelize · REST APIs · JWT authentication |
| Databases | PostgreSQL |
| Cloud and DevOps | Docker · Docker Compose · GitHub Actions (CI and scheduled jobs) |
| AI and data | LLM integration with schema validation and fallbacks · PDF text extraction · rule-based NLP and scoring |
| Testing and tools | pytest · Jest · Supertest · Git · ESLint |

## Links

[Portfolio](https://jass-pvt.github.io/jr-portfolio/) · [LinkedIn](https://www.linkedin.com/in/jaswanthrathore/) · [LeetCode](https://leetcode.com/u/JaswanthRathore/) · [GeeksforGeeks](https://www.geeksforgeeks.org/profile/jaswanthrathore) · [HackerRank](https://www.hackerrank.com/profile/rathoresjaswanth) · [Google Skills](https://www.skills.google/public_profiles/def4bf30-fead-4bf0-81b4-d1c68bcbb7bc)

<br>

<div align="center">
  <img src="assets/jaswanth-footer.svg" alt="Jaswanth Rathore, Jass-pvt" width="100%">
</div>
     