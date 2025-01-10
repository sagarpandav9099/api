============================================
User Flow
============================================
1. Register a new user (or multiple) via http://127.0.0.1:9000/client/register/.
    If you register an admin user, you can create exams from the API side or add an Admin from createsuperuser.
2. Login at http://127.0.0.1:9000/client/login/.
3. Exam creation (only for admin):
    Either use the Django Admin at http://127.0.0.1:8000/admin/ (if you want to create the data directly in DB) or call the POST /api/exams/create/ with a JSON body like:

    {
    "title": "Sample Exam",
    "questions": [
        {
        "question_text": "What is 2+2?",
        "options": [
            {"option_text": "3", "is_correct": false},
            {"option_text": "4", "is_correct": true}
        ]
        }
    ]
    }

    Use Bearer <ACCESS_TOKEN> from an admin user.

4. View exam list: http://127.0.0.1:9000/client/exam-list/.
5. Take an exam: pick from the list, answer, then submit.
6. View results: http://127.0.0.1:9000/client/exam-results/.
