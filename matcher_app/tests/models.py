from django.test import TestCase
from matcher_app.models import Candidate, Skill, Job, Note


class TestModels(TestCase):
    def test_candidate_has_a_skill(self):
        """make sure the Many to Many relationship is working correctly"""
        candidate = Candidate.objects.create(title="Lawyer")
        skill_one = Skill.objects.create(skill_name="Law")
        skill_two = Skill.objects.create(skill_name="Writing")
        candidate.skills.set([skill_one.pk, skill_two.pk])
        self.assertEqual(candidate.skills.count(), 2)

    def test_model_str(self):
        """Check str representation of relevant models"""
        candidate = Candidate.objects.create(title="Doctor")
        skill_one = Skill.objects.create(skill_name="Physics")
        skill_two = Skill.objects.create(skill_name="Math")
        skill_three = Skill.objects.create(skill_name="Medicine")
        candidate.skills.set([skill_one.pk, skill_two.pk, skill_three.pk])

        job = Job.objects.create(title="Doctor", status="opened", skill="Medicine")
        note = Note.objects.create(candidate_id_id=candidate.candidate_id, job_id_id=job.job_id,
                                   note="This doctor is the best!")

        self.assertEqual(str(candidate), "Doctor")
        self.assertEqual(str(job), "Doctor")
        self.assertEqual(str(note), "This doctor is the best!")
