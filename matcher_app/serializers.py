from rest_framework import serializers
from matcher_app.models import Job, Like, Note, Dislike, Match


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('job_id', 'title', 'status', 'skill')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('candidate_id', 'time_liked', 'job_id')


class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ('candidate_id', 'time_disliked', 'job_id')


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('candidate_id', 'job_id', 'note')


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('candidate_id', 'time_matched', 'job_id')
