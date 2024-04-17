from rest_framework import serializers
# from rest_framework.exceptions import ValidationError

from .models import Summary
from .utils import summarize_content
from core.exceptions import ValidationError
from text_extraction.models import ExtractedText


class SummaryCreationSerializer(serializers.ModelSerializer):

    text_id = serializers.CharField(required=False)
    content = serializers.CharField(required=False)

    class Meta:
        model = Summary
        fields = ['text_id', 'content']

    def create(self, validated_data):
        extracted_text_obj = getattr(self, 'extracted_text', None)
        # If 'text_id' was passed, get the text to be
        # summarized from the corresponding 'ExtractedText' model.
        if extracted_text_obj: 
            text = extracted_text_obj.extracted_text
        else:
            text = validated_data.get('content')
        print("Text:    ============= ", text)
        summary_content = summarize_content(text)
        data = {
            'extracted_text': extracted_text_obj,
            'summary_content': summary_content
        }
        return super().create(data)

    def validate(self, data):
        text_id = data.get('text_id')
        content = data.get('content')
        # If 'text_id' and 'content' were passed at once, delete one
        if text_id and content:
            data.pop('text_id')

        return super().validate(data)

    def validate_text_id(self, text_id):
        extracted_obj = get_object_or_none(ExtractedText, text_id=text_id)
        if not obj:
            _msg = "Invalid text id"
            raise ValidationError(detail=_msg)

        # If a text_id was passed, save the fetched 'extracted_obj'
        # to avoid another db read query.
        self.extracted_text = extracted_obj

        return text_id

    def validate_content(self, content):
        return content


class SummarizedTextSerializer(serializers.ModelSerializer):

    class Meta:
        model = Summary
        fields = ['summary_content']
