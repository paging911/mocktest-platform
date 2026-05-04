# Mock Test Platform Over Frappe / ERPNext LMS

This starter package shows how to transform Frappe LMS into a mock test platform without fighting the existing LMS course model.

Recommended approach:

- Keep Frappe LMS for courses, lessons, batches, enrolment, discussions, and certificates.
- Add this custom app as the assessment engine.
- Link exams to LMS batches or courses later through custom fields.
- Keep mock-test attempts separate from normal LMS quiz attempts, because competitive exams need stricter timing, ranking, negative marking, analytics, and attempt logs.

## Step-by-Step Transformation Plan

### 1. Prepare the Frappe Bench

Install ERPNext and Frappe LMS first.

```bash
bench get-app erpnext
bench get-app lms
bench --site your-site.local install-app erpnext
bench --site your-site.local install-app lms
```

Then add this mock test app.

```bash
bench get-app /path/to/mocktest_platform
bench --site your-site.local install-app mocktest_platform
bench --site your-site.local migrate
bench restart
```

During development, place this folder inside your bench `apps` directory or copy the generated app into an app created with:

```bash
bench new-app mocktest_platform
```

### 2. Data Model

Use these core DocTypes:

- `MT Exam`: main mock test configuration.
- `MT Exam Section`: child table for sections such as Physics, Chemistry, Math, Reasoning, English.
- `MT Question`: reusable question bank item.
- `MT Question Option`: child table for MCQ options.
- `MT Exam Question`: child table mapping selected questions to an exam.
- `MT Exam Attempt`: one student attempt.
- `MT Attempt Answer`: child table storing selected answers and score per question.

### 3. Admin Workflow

1. Create questions in `MT Question`.
2. Add options and mark the correct option.
3. Create an `MT Exam`.
4. Add sections, duration, marks, negative marks, and passing score.
5. Add questions to the exam.
6. Publish the exam.
7. Assign it to students or LMS batches using permissions/custom linking.

### 4. Student Workflow

1. Student opens exam page.
2. Frontend calls `mocktest_platform.api.start_attempt`.
3. Student answers questions.
4. Frontend calls `mocktest_platform.api.save_answer` after each answer.
5. On submit or timer expiry, frontend calls `mocktest_platform.api.submit_attempt`.
6. Result is calculated and saved.

### 5. Recommended Frontend Screens

Build these as Frappe pages or Vue components inside the LMS portal:

- `/mock-tests`: list available exams.
- `/mock-test/<exam>`: exam instructions and start button.
- `/mock-test-attempt/<attempt>`: full-screen test interface.
- `/mock-test-result/<attempt>`: scorecard and analytics.

Essential test UI features:

- Countdown timer.
- Section tabs.
- Question palette.
- Save and next.
- Mark for review.
- Clear response.
- Auto-submit on timer end.
- Warning on page refresh or tab close.

### 6. Scoring Rules

For each question:

- Correct: add question marks.
- Wrong: subtract negative marks.
- Skipped: zero.

After submit:

- Save total score.
- Save max score.
- Save percentage.
- Save correct, wrong, skipped counts.
- Mark status as `Submitted`.

### 7. Analytics Phase

After MVP, add:

- Topic-wise accuracy.
- Section-wise score.
- Time spent per question.
- Rank per exam.
- Percentile.
- Weak topic suggestions.
- PDF report card.

### 8. Monetization Phase

Use ERPNext items, sales invoices, payment gateway, or Frappe LMS memberships to sell:

- Individual exams.
- Test series packages.
- Course + test bundles.
- Batch-based access.

### 9. Anti-Cheating Phase

Add gradually:

- Full-screen mode.
- Tab switch logs.
- Copy/paste blocking.
- Attempt activity log.
- IP/device tracking.
- Optional webcam proctoring.

## Files Included

This workspace contains a starter Frappe app scaffold:

```text
mocktest_platform/
  setup.py
  pyproject.toml
  mocktest_platform/
    hooks.py
    modules.txt
    api.py
    mock_test_platform/doctype/...
```

The code is intentionally small and readable so you can adapt it to your exact Frappe/ERPNext version.

