import json
from rest_framework import serializers, status

from verifier.models import Company, TaskObject, VerificationTaskResult


class TaskSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False)

    class Meta:
        model = TaskObject
        fields = '__all__'

    ## add company based on the user on create
    def validate(self, attrs):
        if 'company' not in attrs and self.context['request'].user.company:
            attrs['company'] = self.context['request'].user.company
        else:
            attrs['company'] = Company.objects.get(id=1)
        return attrs

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance = super().create(validated_data)
        instance.tags = tags_data
        instance.save()
        return instance


class VerificationTaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationTaskResult
        fields = '__all__'