from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from matcher_app import models, serializers, utils, candidate_finder
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(['GET'])
def get_all_candidates_for_job(request, job_id):
    """returns list of all matching candidate ids for given job"""
    if request.method == 'GET':
        job_obj = models.Job.objects.get(job_id=job_id)
        is_closed = job_obj.status == 'closed'
        if is_closed:  # do not return any candidates if given job is closed
            return Response([], status=status.HTTP_204_NO_CONTENT)

        # calls candidate_finder function - checks for valid matches, and adds the matches to the Match table
        all_candidates = candidate_finder.candidate_finder(job_obj)
        logger.info(f'All candidates for job {job_id}: {all_candidates}')
        return Response(all_candidates, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def add_opinion_for_candidate(request):
    """provide an opinion (like or dislike) for a given candidate based on given job"""
    if request.method == 'POST':
        opinion_data = request.data
        job_obj = models.Job.objects.get(job_id=int(opinion_data['job_id']))
        if opinion_data['is_liked']:  # add to like table
            is_open = job_obj.status == 'opened'
            if not is_open:  # check if job is open before adding like
                return Response('Job is not open - cannot add like', status=status.HTTP_400_BAD_REQUEST)

            like_serializer = serializers.LikeSerializer(data=opinion_data)
            if like_serializer.is_valid(raise_exception=True):
                logger.info(f"USER \\ Creating new like...")
                like_serializer.save()
                return Response('Like added', status=status.HTTP_200_OK)

        else:  # add to dislike table
            dislike_serializer = serializers.DislikeSerializer(data=opinion_data)
            if dislike_serializer.is_valid(raise_exception=True):
                logger.info(f"USER \\ Creating new dislike...")
                dislike_serializer.save()
                return Response('Dislike added', status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_data_for_liked_candidates(request, job_id):
    """retrieve all data associated with liked candidates for a given job (order desc by time)"""
    if request.method == 'GET':
        job_obj = models.Job.objects.get(job_id=job_id)
        is_closed = job_obj.status == 'closed'
        if is_closed:  # do not return any candidates if given job is closed
            return Response([], status=status.HTTP_204_NO_CONTENT)

        liked_candidates = models.Like.objects.filter(job_id_id=job_id)
        serializer = serializers.LikeSerializer(liked_candidates, many=True)
        data_list = list(serializer.data)
        # add any notes that exist for liked candidates
        all_results = utils.get_notes_for_liked_candidates(data_list)
        # could return duplicate candidates if a given candidate has received multiple notes for same job
        return Response(all_results, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def add_note_for_liked_candidate(request):
    """add note for liked candidate for specific job - new note saved to the Note table"""
    if request.method == 'POST':  # add note for liked candidate
        note_data = request.data
        job_id = int(note_data['job_id'])
        job_obj = models.Job.objects.get(job_id=job_id)
        # check if given note meets conditions to be added to table (job not closed and candidate is liked)
        is_closed = job_obj.status == 'closed'
        # using filter since a given candidate could be liked multiple times for the same job
        is_liked = models.Like.objects.filter(candidate_id_id=note_data['candidate_id'], job_id_id=job_id)
        if is_closed or not is_liked:  # check if conditions are met to add like
            logger.info(f"USER \\ Job must be open and candidate must be liked")
            return Response("Invalid entry - job must be open and candidate must be liked",
                            status=status.HTTP_400_BAD_REQUEST)
        else:  # add the note for the given candidate
            serializer = serializers.NoteSerializer(data=note_data)
            if serializer.is_valid(raise_exception=True):
                logger.info(f"USER \\ Creating new note for job_id {note_data['job_id']}")
                serializer.save()
        return Response('Added note successfully', status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['PUT', 'GET'])
def handle_given_job(request, job_id=None):
    """handles actions related to a specific job - updating its status or getting various stats"""
    if request.method == 'PUT':  # update status of given job - data provided in request body
        job_id = request.data['job_id']
        job_status = request.data['status']
        job_status_options = [choice[0] for choice in models.jobStatusChoices]
        if job_status not in job_status_options:
            return Response(f'Unable to update job with status {job_status}: ', status=status.HTTP_400_BAD_REQUEST)

        models.Job.objects.filter(job_id=job_id).update(status=job_status)
        return Response(f'Status updated to {job_status}', status=status.HTTP_200_OK)

    if request.method == 'GET':  # get all stats on given job
        num_likes = models.Like.objects.filter(job_id_id=job_id).count()
        num_dislikes = models.Dislike.objects.filter(job_id_id=job_id).count()
        num_notes = models.Note.objects.filter(job_id_id=job_id).count()
        # get all unique candidate matches for given job (candidate could be matched multiple times for same job)
        matching_candidates = models.Match.objects.filter(job_id_id=job_id).order_by().values('candidate_id').distinct()
        res_dict = {"num_likes": num_likes, "num_dislikes": num_dislikes, "num_notes": num_notes,
                    "num_matches": len(matching_candidates)}
        return Response(res_dict, status=status.HTTP_200_OK)
