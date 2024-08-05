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

    @extend_schema(
        summary="라벨 생성",
        description="라벨을 생성하는 API",
        tags=["Label"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="라벨 조회",
        description="본인이 생성한 라벨을 조회하는 API",
        tags=["Label"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
