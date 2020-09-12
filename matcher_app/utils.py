from matcher_app import models, serializers
import logging

logger = logging.getLogger(__name__)


def add_matched_candidates_to_table(matching_candidates, job_id):
    res_list = [{"candidate_id": candidate_id, "job_id": job_id} for candidate_id in matching_candidates]
    match_serializer = serializers.MatchSerializer(data=res_list, many=True)
    if match_serializer.is_valid(raise_exception=True):
        logger.info(f"USER \\ Adding new matched candidates to table...")
        match_serializer.save()


def get_notes_for_liked_candidates(liked_candidates):
    """get all notes for each liked candidate for a particular job"""
    candidate_idx = 1
    notes_dict = {}  # used for tracking notes for all candidates
    for idx, candidate in enumerate(liked_candidates):
        try:
            # account for candidate who has received multiple likes but has not received the same number of notes
            candidate_notes = models.Note.objects.filter(candidate_id_id=candidate['candidate_id'],
                                                         job_id_id=candidate['job_id'])
            for candidate_note in candidate_notes:
                notes_dict[candidate_note.id] = candidate_note.note
            if candidate_idx in notes_dict:  # if given candidate has received a note
                liked_candidates[idx]['note'] = notes_dict[candidate_idx]
        except Exception as e:
            logger.error(f"Error querying note for candidate: {e}")
        candidate_idx += 1
    return liked_candidates
