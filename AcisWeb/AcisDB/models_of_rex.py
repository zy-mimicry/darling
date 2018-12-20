from django.db import models

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Erds(models.Model):
    """
    From ERD Excel Table items:
    - erd_id
    - category
    - title
    - description
    - product_priority
    - author
    - version

    From JIRA Ticket items:
    - l1_jira
    - l2_jira
    - bug_jiras
    - platform
    - workload
    """

    erd_id = models.CharField(max_length=20)
    category = models.CharField(max_length=40)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    product_priority = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    version = models.CharField(max_length=10)
    HLD = models.TextField()
    l1_jira = models.CharField(max_length=20)
    l2_jira = models.CharField(max_length=20)
    bug_jiras = models.TextField()
    status = models.CharField(max_length=10)
    platform = models.CharField(max_length=20)
    workload = models.CharField(max_length=30)

    def __str__(self):
        return self.erd_id

class TestCases(models.Model):
    """
    Get items from JIRA new-feature(L2-JIRA-Ticket) Ticket 'test/evidences field'.
    """

    case_name = models.CharField(max_length=50)
    age = models.DateTimeField()
    erd = models.ForeignKey("Erds", on_delete=models.CASCADE)

    def __str__(self):
        return self.case_name


class TestReports(models.Model):
    """
    Get [report_path,date] from JIRA new-feature(L2-JIRA-Ticket) Ticket 'test/evidences field'.
    Get [test_result,fw_version,test_log] items from jenkins build result.
    """

    test_result = models.CharField(max_length=10)
    test_log = models.TextField()
    report_path = models.TextField()
    fw_version = models.CharField(max_length=50)
    date = models.DateTimeField()
    test_case = models.ForeignKey("TestCases", on_delete=models.CASCADE)

    def __str__(self):
        return self.report_path
