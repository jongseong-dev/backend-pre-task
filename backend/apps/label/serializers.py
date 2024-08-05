from rest_framework import serializers

from apps.label.models import Label


class LabelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50, required=True, help_text="라벨 이름"
    )

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)

    class Meta:
        model = Label
        fields = ["id", "name"]


class LabelListSerializer(serializers.ModelSerializer):
    """
    연락처 정보에서 중첩된 구문으로 라벨 정보를 보여주기 위한 Serializer
    """

    id = serializers.IntegerField(source="label.id", help_text="라벨 ID")
    name = serializers.CharField(
        source="label.name",
        max_length=50,
        read_only=True,
        help_text="라벨 이름",
    )

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().update(instance, validated_data)

    class Meta:
        model = Label
        fields = ["id", "name"]
