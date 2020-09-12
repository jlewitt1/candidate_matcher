from django.test import TestCase
from matcher_app.models import Candidate, Skill, Job, Note


class TestModels(TestCase):
    def test_candidate_has_a_skill(self):
        """make sure the Many to Many relationship is working correctly"""
        candidate = Candidate.objects.create(title="Software Developer")
        skill_one = Skill.objects.create(skill_name="Python")
        skill_two = Skill.objects.create(skill_name="Javascript")
        skill_three = Skill.objects.create(skill_name="Postgres")
        candidate.skills.set([skill_one.pk, skill_two.pk, skill_three.pk])
        self.assertEqual(candidate.skills.count(), 3)

    def test_model_str(self):
        """Check str representation of relevant models"""
        candidate = Candidate.objects.create(title="Software Developer")
        skill_one = Skill.objects.create(skill_name="Python")
        skill_two = Skill.objects.create(skill_name="Javascript")
        skill_three = Skill.objects.create(skill_name="Postgres")
        candidate.skills.set([skill_one.pk, skill_two.pk, skill_three.pk])
        job = Job.objects.create(title="Software Developer", status="opened", skill="Python")
        note = Note.objects.create(candidate_id_id=candidate.candidate_id, job_id_id=job.job_id,
                                   note="This developer is the best!")
        self.assertEqual(str(candidate), "Software Developer")
        self.assertEqual(str(job), "Software Developer")
        self.assertEqual(str(note), "This developer is the best!")
