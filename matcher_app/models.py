from django.db import models
from django.utils import timezone

CLOSED = 'closed'
OPENED = 'opened'
PENDING = 'pending'
jobStatusChoices = [
    (CLOSED, 'closed'),
    (OPENED, 'opened'),
    (PENDING, 'pending'),
]


class Skill(models.Model):
    skill_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.skill_name


class Candidate(models.Model):
    candidate_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.title


class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=200, choices=jobStatusChoices)
    skill = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Note(models.Model):
    candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    note = models.TextField()

    def __str__(self):
        return self.note


class Like(models.Model):
    candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    time_liked = models.DateTimeField(max_length=60, default=timezone.now)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-time_liked']


class Dislike(models.Model):
    candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    time_disliked = models.DateTimeField(max_length=60, default=timezone.now)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-time_disliked']


class Match(models.Model):
    candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    time_matched = models.DateTimeField(max_length=60, default=timezone.now)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-time_matched']
