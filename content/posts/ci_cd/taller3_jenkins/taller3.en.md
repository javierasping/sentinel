---
title: "Workshop 3: Continuous Integration of Django Application (Test)"
date: 2024-03-14T10:00:00+00:00
description: "Workshop 3: Continuous Integration of Django Application (Test)"
tags: [Jenkins, CI/CD]
hero: images/ci_cd/jenkins/taller3.png
---

We will work with the application repository [django_tutorial](https://github.com/josedom24/django_tutorial). This application has a series of tests defined, which can be studied in the `tests.py` file in the `polls` directory.

Each test is defined by a function. In the file, you can read the comments to understand what each test is checking, or you can refer to the document [Tests in the Django tutorial application](https://fp.josedomingo.org/iaw/5_ic/test_tutorial_django.html).

To run the tests, execute:

```bash
python3 manage.py test
```

At this moment, a temporary database is created where the defined tests are executed:

```bash
python3 manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..........
----------------------------------------------------------------------
Ran 10 tests in 0.024s

OK
Destroying test database for alias 'default'...
```

For example, two tests are defined in the `test_no_questions` function and in the `test_future_question` function. These check that if there are no questions in the database, the message **"No polls are available"** should appear. If a programmer modifies the application and changes the message in `polls/templates/polls/index.html`:

```html
...
    <p>No hay encuestas disponibles.</p>
...
```

Since the tests check for a different message, they will fail:

```bash
python3 manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..F.F.....
======================================================================
FAIL: test_future_question (polls.tests.QuestionIndexViewTests)
Questions with a pub_date in the future aren't displayed on
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/jose/github/django_tutorial/polls/tests.py", line 143, in test_future_question
    self.assertContains(response, "No polls are available.")
  File "/home/jose/virtualenv/django_tutorial/lib/python3.9/site-packages/django/test/testcases.py", line 471, in assertContains
    self.assertTrue(real_count != 0, msg_prefix + "Couldn't find %s in response" % text_repr)
AssertionError: False is not true : Couldn't find 'No polls are available.' in response

======================================================================
FAIL: test_no_questions (polls.tests.QuestionIndexViewTests)
If no questions exist, an appropriate message is displayed.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/jose/github/django_tutorial/polls/tests.py", line 115, in test_no_questions
    self.assertContains(response, "No polls are available.")
  File "/home/jose/virtualenv/django_tutorial/lib/python3.9/site-packages/django/test/testcases.py", line 471, in assertContains
    self.assertTrue(real_count != 0, msg_prefix + "Couldn't find %s in response" % text_repr)
AssertionError: False is not true : Couldn't find 'No polls are available.' in response

----------------------------------------------------------------------
Ran 10 tests in 0.022s

FAILED (failures=2)
```

**Remember:** To make a test fail, you should not modify the `test.py` file. The tests fail because modifying the application code causes the conditions defined in the tests to no longer be met.

## Pipeline to Perform an Automatic Test [Permalink](https://fp.josedomingo.org/iaw/5_ic/taller3.html#pipeline-para-perform-a-test-autom%C3%A1tico)

Knowing how the tests are executed, we can create a pipeline to automate this process:

```groovy
pipeline {
    agent {
        docker { 
            image 'python:3'
            args '-u root:root'
        }
    }
    stages {
        stage('Clone') {
            steps {
                git branch: 'master', url: 'https://github.com/josedom24/django_tutorial.git'
            }
        }
        stage('Install') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'python3 manage.py test'
            }
        }
    }
}
```

1. To install the packages with `pip`, we need to execute the commands as root (`args '-u root:root'`).
2. We clone the repository.
3. We install the required dependencies.
4. We run the tests.

Try modifying the application code to cause a test to fail and verify how the pipeline detects the failure.

### 1. Screenshot of a successful build:

![Successful Build](/ci_cd/taller3_jenkins/img/Pasted_image_20240305231003.png)

### 2. Modify the application code to trigger a failure.

**Remember:** To make a test fail, you should not modify the `test.py` file. The tests fail because modifying the application code causes the conditions defined in the tests to no longer be met. Avoid modifying the "No polls are available." message, as we already covered that case in this workshop.

Modify the function as follows:

```python
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) >= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
```

### 3. Screenshot of a failed build:

![Failed Build](/ci_cd/taller3_jenkins/img/Pasted_image_20240306091906.png)
