"""
The naive approach taken below checks for a match based on title matching (or some substring
of the title matching) as well as a skills match.

A more advanced approach for this use case would be to use fuzzy matching. Since the goal is to link some text
(candidate job title / skills) with the target job title / skill, we can try to identify non-exact matches
between the two.

We can do this by calculating the Levenshtein Distance representing the number of transformations required to get
from the source string to the target string, with a lower distance representing a higher match probability.

The downside to this approach is that it does not account for relevance, as misspellings / typos could completely
transform the meaning of the word - leading to a higher false positive rate.
"""
from matcher_app import utils, models
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


def get_matches_from_job_title(job_obj):
    """check for identical or partial match with certain substring (ex: Software Engineer / Software Developer)"""
    job_title = models.Job.objects.get(job_id=job_obj.job_id).title
    title_list = job_title.split()
    if len(title_list) == 2:  # naive approach - assuming all titles are max 2 words
        query_set_titles = models.Candidate.objects.filter(
            (Q(title__icontains=title_list[0]) | Q(title__icontains=title_list[1])))
    else:
        query_set_titles = models.Candidate.objects.filter(title=job_title)

    matching_title_candidates = [obj.candidate_id for obj in query_set_titles]
    return matching_title_candidates


def get_matches_from_skill(job_obj):
    skill_to_check = job_obj.skill.capitalize()
    skill_id = models.Skill.objects.get(skill_name=skill_to_check).id
    query_set_skills = models.Candidate.objects.filter(skills=skill_id)
    matching_skills_candidates = [obj.candidate_id for obj in query_set_skills]

    return matching_skills_candidates


def check_if_opinions_exist_for_candidates(potential_candidates):
    """ensures the final list of matched candidates does not include candidates who received an opinion"""
    final_candidates = []
    for candidate in potential_candidates:
        like_opinion = next(iter(models.Like.objects.filter(candidate_id=candidate)), None)
        dislike_opinion = next(iter(models.Dislike.objects.filter(candidate_id=candidate)), None)

        if not dislike_opinion and not like_opinion:  # if no opinions (good or bad) exist for potential candidate
            final_candidates.append(candidate)

    return final_candidates


def candidate_finder(job_obj):
    """utility function to evaluate matches for given job_id"""
    final_candidates = []
    try:
        # for a more accurate approach -> implement levenshtein distance algorithm as described above
        matching_title_candidates = get_matches_from_job_title(job_obj)
        matching_skills_candidates = get_matches_from_skill(job_obj)

        # ideal candidates will match with both title and skill
        potential_candidates = list(set(matching_title_candidates) & set(matching_skills_candidates))
        if not potential_candidates:  # if there are no matches for both skills - try taking candidates with only one
            potential_candidates = list(set(matching_title_candidates) | set(matching_skills_candidates))

        # If an opinion was expressed for the candidate for this job, remove candidate from final list of candidates
        final_candidates = check_if_opinions_exist_for_candidates(potential_candidates)

        # save final list of matched candidates to Match table
        if final_candidates:
            utils.add_matched_candidates_to_table(final_candidates, job_obj.job_id)

    except Exception as e:
        logger.error(f'Error getting all matching candidates: {e}')

    return final_candidates
