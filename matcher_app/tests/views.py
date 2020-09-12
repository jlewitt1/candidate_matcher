from django.test import TestCase
from matcher_app.models import Note, Job, Skill, Candidate


class TestNote(TestCase):
    def test_can_send_note(self):
        """Check that notes can only be added if job is open and candidate has received a like"""
        job = Job.objects.create(title="Software Developer", status="opened", skill="Python")
        job.status = 'opened'  # job status must be set to open in order to add "like" and note
        skill_one = Skill.objects.create(skill_name="Python")
        skill_two = Skill.objects.create(skill_name="Javascript")
        skill_three = Skill.objects.create(skill_name="Postgres")
        candidate = Candidate.objects.create(title="Software Developer")
        candidate.skills.set([skill_one.pk, skill_two.pk, skill_three.pk])
        # need to first like the candidate in order to provide a note
        opinion_data = {"job_id": job.job_id, "candidate_id": candidate.candidate_id, "is_liked": True}
        self.client.post("/candidate/opinion/", data=opinion_data, content_type='application/json')
        note_data = {"job_id": job.job_id, "candidate_id": candidate.candidate_id,
                     "note": "This is a great candidate!"}
        self.client.post("/candidate/note/", data=note_data, content_type="application/json")
        self.assertEqual(Note.objects.count(), 1)

    def test_get_all_matching_candidates(self):
        # Create an instance of a GET request.
        pass
