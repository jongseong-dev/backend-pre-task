from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from apps.label.models import Label
from apps.label.serializers import LabelSerializer


@extend_schema(
    summary="라벨 API",
    description="연락처 분류를 위한 라벨을 조회, 생성, 삭제하는 API",
    tags=["Label"],
)
class LabelViewSet(ModelViewSet):
    serializer_class = LabelSerializer
    queryset = Label.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
