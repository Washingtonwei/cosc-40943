# Syllabus: Software Engineering

!!! note "The syllabus is your first course reading"
    It provides an orientation to, overview of the flow, and expectations of the course. Turn to the syllabus for details on assignments and course policies.

## Course and Instructor Information

### Course

| | |
|---|---|
| **Course title, prefix, number, section** | Software Engineering, COSC 40943, 020 |
| **Semester and year** | Fall 2026 |
| **Number of credits** | 3 |
| **Course component type** | Lecture |
| **Class location** | SWR LH3 |
| **Class meeting days and times** | MWF 10:00 - 10:50 AM |

### Instructor

| | |
|---|---|
| **Instructor** | Bingyang Wei |
| **Office** | Tucker Technology Center 341D |
| **Office hours** | MW 11:00 AM - 12:00 PM, or by appointment |
| **Preferred contact** | Email |
| **Email** | b.wei@tcu.edu |

### Teaching assistants

| Teaching assistant | Email |
|---|---|
| Hiep Nguyen (lead) | HIEP.N.NGUYEN@tcu.edu |
| Ali Gasimli | A.GASIMLI@tcu.edu |
| Yuv Raj Pant | YUV.RAJ.PANT@tcu.edu |

Each TA is assigned four project teams and works with those same teams all semester: in Friday studio, at checkpoint presentations, and as the team's first line of help. See [Friday Studio](studio.md).

### Course communication

**Slack** is the course channel: announcements, questions whose answers help everyone, and your team's own channel. Join in week 1.

<!-- TODO(instructor): add the Slack workspace invite link. -->

Email b.wei@tcu.edu for anything private. For anything about your project, ask your TA first.

## Final Evaluative Exercise and Important Dates

| | |
|---|---|
| **First day of class** | Monday, August 24, 2026 |
| **Labor Day holiday**, no class | Monday, September 7, 2026 |
| **Fall break**, no class | Thursday, October 8 and Friday, October 9, 2026. Classes recess Wednesday Oct 7 at 10:00 PM and resume Monday Oct 12 at 8:00 AM. |
| **Midterm exam** | Monday, October 19, 2026, in class |
| **Thanksgiving break**, no class | Monday, November 23 through Friday, November 27, 2026. Classes recess Friday Nov 20 at 10:00 PM and resume Monday Nov 30 at 8:00 AM. |
| **MVP demos to clients** | December 4, 7, and 9, 2026, in class |
| **Last day of class** | Wednesday, December 9, 2026 |
| **Reading days** | Thursday, December 10 and Friday, December 11, 2026 |
| **Final exam** | Monday, December 14, 2026, 8:00 - 10:30 AM, SWR LH3 |

Dates are from the TCU Registrar's [Fall 2026 academic dates](https://registrar.tcu.edu/fall-academic-dates.php).

## Student Resources and Policy Information

**[TCU Student Resources and Policy Information](https://cte.tcu.edu/tcu-syllabus-policies/)** holds the approved syllabus policy statements and the resources that support you as a TCU student.

Read the sections on **Student Access and Accommodation**, **Academic Conduct and Course Materials Policies**, and **Emergency Response and TCU Alert**.

## Course Description

### Catalog description

Stages of the software development life cycle (requirements analysis, specification, design, implementation, testing), evolution, and quality assurance are covered. Classical and alternative process models are described. Project management issues, professional responsibilities, and ethics of the profession are discussed. This course includes team projects.

### Prerequisites and concurrent enrollment

COSC 30603 or concurrent, senior standing in COSC or CITE or DASC (24 hours in the major). All prerequisites need to be C- or better.

## Course Materials

### Required materials

None. Course notes, references, and readings are published on this website.

Every student needs access to an AI coding agent. Details are in [Working with AI](ai.md).

## Teaching Philosophy and Methodology

This course teaches you how to guide the development of a software product from inception to delivery: how to identify stakeholders, elicit and refine a client's requirements, communicate those requirements to a team, and monitor a project so it stays aligned with client needs and reaches a defensible level of quality. This course is approved for TCU Core: Writing Emphasis.

What is different about this offering is the premise. AI can now read requirements, generate design and code, write tests, review pull requests, and analyze logs. The question this course answers is not whether software engineering still matters, but **what software engineering becomes when AI is a permanent member of every development team**. Engineering judgment and technical taste become more valuable, not less, as AI automates the transformations between artifacts.

You will learn a specific method for working this way, **spec-driven, agent-assisted development**:

> Author a specification and a breadth-complete architecture, prove them with one vertical slice, then fan out one use case at a time, looping what you learn back into the specification.

An AI coding agent does the per-use-case design and implementation. It works against a contract you wrote, reviewed, and own. That specification is version-controlled Markdown in your repository, not a throwaway prompt, because there has to be something to review the code against. Classic software engineering topics (requirements, architecture, testing, static analysis, CI/CD, observability, code review) are taught at the moment the method demands them, not as a disconnected survey.

**This course is where your Senior Design project starts.** You will work in a team of six students on a real software project for a real external client. The project continues into COSC 40993 in spring 2027 and is officially due in April 2027, but your team must get started this fall and have a working first version of the software running by the end of the fall semester.

### How the week works

The course meets MWF, and the three days do different jobs.

- **Monday and Wednesday are lecture.** A software engineering topic, demonstrated on [Project Pulse](https://github.com/Washingtonwei/project-pulse), a real Vue.js and Spring Boot application. You watch the move performed on real code.
- **Friday is studio.** Same room, whole class, TA-led. Your team applies that week's move to your own client project while the TAs circulate. On four Fridays, studio is your team's checkpoint presentation. See [Friday Studio](studio.md).
- **Outside class**, your team meets, meets its client, and builds. Full team working meetings and client meetings happen outside the class period.

### What this course expects of your time

Plan your semester around this course rather than fitting it into the gaps. Senior design is a capstone and a graduation requirement, it runs for a full year, and a real external client is depending on what your team delivers in December. Treat it as the course that comes first.

Concretely, **expect 6 to 9 hours per week outside of class**, and expect that time to be scheduled by your team rather than chosen by you. Your team will set recurring meeting times, and:

- **Attendance at team meetings is graded.** Each absence from a lecture, studio, team meeting, presentation practice, or client meeting costs 1% of your final grade.
- **Your teammates evaluate your contribution every week**, and those peer evaluations are 20% of your grade.
- **Your client evaluates you twice**, worth another 10%.

None of that works if you are unavailable. If a job, a commute, athletics, or another course makes 6 to 9 hours genuinely impossible this term, tell me in **week 1**, not in October. There are real options in August (rearranging a schedule, dropping a competing commitment, taking this course next year) and almost none in week 10, when your team has been carrying you and your peer evaluations show it.

## Learning Outcomes

Students completing this course are expected to be able to:

1. Turn a real client's problem into a specification that serves as the development contract (glossary, vision and scope, use cases, business rules, quality attributes), with the use case as the unit of work, citation, and test. `SLO-spec-as-contract`
2. Make and defend design and architecture decisions, documenting the alternatives considered and the reasoning behind the choice. `SLO-design-decisions`
3. Work in a team using GitHub as the single source of truth: issues, pull requests, reviews, traceability. `SLO-github-workflow`
4. Build, test, and ship a working MVP through a CI/CD pipeline with at least one quality gate. `SLO-ship-mvp`
5. Apply static and dynamic analysis and read software metrics to reason about quality, maintainability, and technical debt. `SLO-analysis-and-metrics`
6. Collaborate with AI across the lifecycle: delegating appropriately, supplying the context it cannot infer, and verifying its output without lowering the engineering bar. `SLO-ai-collaboration`
7. Conduct effective code and design reviews, and give and receive engineering feedback. `SLO-reviews`
8. Maintain living traceability from specification to design to code to test, and keep it honest with tooling as the system evolves at AI speed. `SLO-traceability`
9. Act as a professional teammate: team contract, conflict resolution, accountability, ethics. `SLO-professionalism`
10. Size up an unfamiliar problem quickly, naming the hard part, the bottleneck, the risks that could kill it, a plausible stack, and whether it is feasible for this team in this time, then defend that judgment against the agent's version of it. `SLO-solution-shaping`

## Assignments

### Exams

A **midterm** on Monday, October 19, covering weeks 1 through 8, and a **final exam** on Monday, December 14. Exams assess the software engineering concepts individually: the delegation boundary, specification quality, architecture and design reasoning, traceability, testing, and analysis.

### Individual Project Pulse assignments

Five individual assignments on **Project Pulse**, the instructor's own application and the codebase demonstrated in lecture. Each follows the shape of real work on an unfamiliar codebase: open an issue, make a change, submit a pull request. You work in your own private copy of the repository, issued to you for each assignment. Each is framed around the AI workflow and **graded on judgment, not on whether it ran**. These are individual work; see [Working with AI](ai.md) for what that means when you have an agent.

The full set, with timing, is on the [Assignments](assignments.md) page.

### Senior Design project

Teams of six students, assigned by the instructor from a short interest and skills survey completed in the first week of class, work with a real external client. Twelve teams this term.

**Deliverables.** Your team's specification and design set, version-controlled in your team's GitHub repository:

- Project glossary
- Vision and scope document
- Use cases
- Business rules
- Software requirements specification (SRS)
- Architecture-of-record
- At least one design-of-record, one use-case area taken through the design gate
- Traceability matrix, kept current
- Source code on GitHub
- MVP demo and presentation

**Where each thing lives.** The specification and design set are **Markdown in your team's GitHub repository**, not documents in a folder. That is not a formatting preference: your coding agent builds against those files, the consistency checks resolve the IDs in them, and traceability only works on text you can diff and review. A specification your agent cannot read is not a contract.

Each team also creates a **Google Drive** for the work that does not belong in a repository: weekly activity reports, team and client meeting minutes, client-facing slides, and shared working drafts. Share it with the instructor and your TA at kickoff.

**Checkpoints.** Four times in the term (Sep 4, Oct 2, Oct 23, Nov 13) your team presents progress to its TA during the Friday studio hour. What each checkpoint requires is on the [Senior Design Project](project.md) page.

**Presentation and software demo.** Your team demos the MVP software in the December presentations. **Working software with limited features MUST be available for the client to test at the end of the fall semester. Failing to do so will result in a letter grade reduction for the entire team.**

### Weekly evaluations

Your project grade is **not** determined solely by the deliverables produced by the team. It is also determined by your individual contribution and your collaboration with team members. Tardiness and absenteeism are considered unprofessional and cannot be tolerated. Your team needs you to be in class, in project meetings, on time, responsive, and productive.

There will be **nine weekly evaluations**, each worth 2.2% of your overall grade. Once the project starts:

- A **weekly activity report (WAR)** is due at the beginning of every Monday class. Inflating time and activities reported in a WAR is considered academic dishonesty. Failure to submit the WAR by that time results in a zero for that week's evaluation. Late WARs will not be accepted.
- The team must **meet regularly outside the classroom** to work on the project together. Feedback from the software industry indicates that the most effective software development happens when the team works together at the same location.
- The team must **meet with your client regularly** to report progress and clarify questions. Advise the instructor well in advance of client meetings so he can attend as many as his schedule allows. The client evaluation is part of your overall grade.
- **Meeting minutes** for both team meetings and client meetings must be submitted every Monday before class time. Team members take turns preparing the minutes using the provided template. Failure to submit meeting minutes results in a 2.2% grade reduction for the team member preparing the minutes that week.
- **Prompt attendance is required.** Absence from lectures, studio, weekly team meetings, presentation practice, and client meetings is a serious problem without official documentation. Each absence causes a 1% grade reduction.

Team checkpoint presentations are assessed within the weekly evaluation for the week in which they fall.

### Peer evaluations

There will be **nine peer evaluations**, each worth 2.2% of your overall grade. Once the project starts, peer evaluations for your teammates (including yourself) on their performance during the past week are due every Tuesday at 10:00 AM. Your evaluation should be based on your observation of your teammates and their submitted WARs. Failure to submit peer evaluations by that time results in a zero for that week. Late peer evaluations will not be accepted.

### Client evaluations

Your senior design client provides **two evaluations** of your performance during the semester. Be active and get involved during team and client meetings.

### Project contribution

- **Every team member must contribute to the document writing.** Track your contribution in your WAR. Each section in a document should have one main author; many people can review and comment on it, and only the main author chooses to accept or reject suggestions.
- **Every team member must contribute to the coding part of the project.** Commit history (GitHub contributor activity) is monitored by the instructor periodically.

## Working with AI

This course requires you to use an AI coding agent, and it holds you responsible for everything the agent produces under your name. The full policy, including what is expected, what is prohibited, and how AI use interacts with academic integrity, is on the [Working with AI](ai.md) page. Read it before the first assignment.

## Academic Integrity

This course operates under TCU's [Academic Conduct Policy](http://tcu.smartcatalogiq.com/current/Undergraduate-Catalog/Student-Policies/Academic-Conduct-Policy-Details) and Section 3.4 of the Student Code of Conduct. Where they conflict with anything here, the university policy governs.

Because an agent writes code in this course, the usual line between help and dishonesty needs stating in operational terms:

- **The test is explanation.** You are responsible for everything submitted under your name, whoever or whatever typed it. Submitting work you cannot explain is the violation, and it is the one that gets applied.
- **Exams are closed.** No agent, no notes, no outside resources.
- **Reports and evaluations record what happened.** Inflating time or activities in a weekly activity report, fabricating peer evaluations, or generating meeting minutes and passing them off as a record of what someone said is academic dishonesty, agent-assisted or not.
- **Do your own share.** Every team member contributes to the writing and to the code. Commit history is monitored.

[Working with AI](ai.md) has the full policy, including what AI use is required, permitted, and prohibited per activity.

## Grading Philosophy and Policy

### Late work

Assignments must be submitted no later than the beginning of class on the due day. Late work incurs a **15% penalty for each late day**, including weekends and holidays. Work more than **two days** late will not be accepted, except for Official University Absences or medical reasons.

Students are responsible for making sure work is uploaded properly. Failing to do so results in a zero for that assignment.

### Questions on grading

Requests for re-evaluation of points on exams, assignments, weekly evaluations, and projects must be made to the instructor **within one week** of receiving your grade, accompanied by a brief written description of the grading error you believe was made. After this time, grades are final. Resubmission for re-evaluation subjects the entire assignment to review: if an error was made in your favor, you may lose points.

## Participation, Engagement, and Attendance

Each absence from lectures, studio, weekly team meetings, presentation practice, and client meetings causes a **1% grade reduction**.

## Course Assignments and Final Grade

| Assignment | Percentage |
|---|---|
| Midterm | 15 |
| Final | 15 |
| Individual Project Pulse assignments (5) | 20 |
| Senior Design project: weekly evaluations (9) | 20 |
| Senior Design project: peer evaluations (9) | 20 |
| Senior Design project: client evaluations (2) | 10 |
| **Total** | **100** |

### Grading scale

| Grade | Score |
|---|---|
| A | 90 - 100 |
| B | 80 - 89 |
| C | 70 - 79 |
| D | 60 - 69 |
| F | 0 - 59 |

## Course Schedule

The week-by-week schedule is on its own page: [Schedule](schedule.md).

This calendar represents current plans and objectives. As we go through the semester, those plans may need to change to enhance the class learning opportunities. Such changes will be clearly communicated.
