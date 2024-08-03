from rest_framework import serializers

from label.models import Label


class LabelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50, required=True, help_text="라벨 이름"
    )

    def create(self, validated_data):
        validated_data["owner"] = self.context[
            "request"
        ].user
        return super().create(validated_data)

    class Meta:
        model = Label
        fields = ["name"]
