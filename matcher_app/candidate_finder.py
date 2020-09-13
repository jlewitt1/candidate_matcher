"""
The naive approach taken below checks for a match based on title matching (or some substring
of the title matching) as well as a skills match.

A more advanced approach for this use case would be to use fuzzy matching. Since the goal is to link some text
(candidate job title / skills) with the target job title / skill, we can try to identify non-exact matches
between the two.

We can do this by calculating the Levenshtein Distance representing the number of transformations required to get
from the source string to the target string, with a lower distance representing a higher match probability.

The downside to this approach is that it does not account for relevance, and misspellings / typos could completely
transform the meaning of the word. This would be problematic when comparing "Developer" to "Engineer".
Even though the two words are very similar job wise, the Levenshtein distance would be large between the two.

Another way to solve this is to extract features from the text using something like word2vec, where
the text data is converted into numeric format.
"""
from matcher_app import utils, models
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


def rank_final_candidates(final_candidates, job_obj):
    """This function shows at a high level how to approach ranking all candidates that have been matched"""
    # candidate1_skills = ["ruby", "javascript"]  # 0 points
    # candidate2_skills = ["cobalt", "azure"]  # 99 points

    # job_skills = ["cobalt"] --> working under assumption for this exercise that job contains only 1 skill
    # job_probabilities = [1] # represented as %
    """
    We can assign probabilities to each job skill - for example, we assume 70% of 
    candidates know python, while only 1% know cobalt. 
    
    We can convert each skill into points based on this percentage (ex: 70% --> 30 points, 1% --> 99 points) and 
    sum the total points for each candidate to create a ranking. This rewards candidates who 
    have a skill that is less common and presumably also more difficult to learn. 

    There are a few problems with this approach:
    1. It is linear - the maximum points that can be given for a given skill with this method
    is 99 points. It would be better for the point system to be exponential, where a skill 
    that a smaller percentage of candidates have is represented by a greater number of points
    
    2. It does not take into account conditional probabilities: for example, a candidate 
    who has skills of django and python, where django is conditional on knowing python
    """
    return final_candidates


def get_matches_from_job_title(job_obj):
    """check for identical or partial match with certain substring (ex: Software Engineer / Software Developer)"""
    job_title = models.Job.objects.get(job_id=job_obj.job_id).title
    title_list = job_title.split()
    if len(title_list) == 2:  # naive approach - assuming all titles are max 2 words
        query_set_titles = models.Candidate.objects.filter(
            (Q(title__icontains=title_list[0]) | Q(title__icontains=title_list[1])))
    else:
        query_set_titles = models.Candidate.objects.filter(title=job_title)

    return query_set_titles


def get_matches_from_skill(job_obj):
    """checks for candidates who have the skill required for the job"""
    skill_to_check = job_obj.skill.capitalize()
    skill_id = models.Skill.objects.get(skill_name=skill_to_check).id
    query_set_skills = models.Candidate.objects.filter(skills=skill_id)

    return query_set_skills


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
    ranked_candidates = []
    try:
        # for a more accurate approach -> implement levenshtein distance algorithm as described at the top of the file
        matching_title_candidates = get_matches_from_job_title(job_obj)
        matching_skills_candidates = get_matches_from_skill(job_obj)

        # ideal candidates will match with both title and skill
        potential_candidates = list(set(matching_title_candidates) & set(matching_skills_candidates))
        if not potential_candidates:  # if there are no matches for both skills - try taking candidates with only one
            potential_candidates = list(set(matching_title_candidates) | set(matching_skills_candidates))

        # If an opinion was expressed for the candidate for this job, remove candidate from final list of candidates
        final_candidates = check_if_opinions_exist_for_candidates(potential_candidates)

        # rank the final candidates based on how strong the match is to the job
        ranked_candidates = rank_final_candidates(final_candidates, job_obj)

        # save final list of matched candidates to Match table
        if ranked_candidates:
            utils.add_ranked_candidates_to_table(ranked_candidates, job_obj.job_id)

    except Exception as e:
        logger.error(f'Error getting all matching candidates: {e}')

    return ranked_candidates
