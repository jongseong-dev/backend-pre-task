from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiExample,
    extend_schema,
)

from apps.contactbook.serializers import (
    ContactBookRetrieveSerializer,
    ContactBookListSerializer,
)

contact_book_parameters = [
    OpenApiParameter(
        name="ordering",
        description="필드 이름을 넣으면 해당 필드를 기준으로 정렬"
        "필드 종류는 이름, 이메일, 전화번호다. 내림차순으로 정렬하고 싶으면 앞에 `-`를 붙이면 된다.",
        examples=[
            OpenApiExample(
                "이름 내림차순 정렬",
                summary="이름 기준으로 내림차순 정렬",
                description="이름을 기준으로 내림차순으로 정렬합니다.",
                value="-name",
                parameter_only=True,
            ),
            OpenApiExample(
                "이메일 기준으로 내림차순 정렬",
                summary="이메일 기준으로 내림차순 정렬",
                description="이메일을 기준으로 내림차순으로 정렬합니다.",
                value="-email",
                parameter_only=True,
            ),
            OpenApiExample(
                "전화번호 내림차순 정렬",
                summary="전화번호 기준으로 내림차순 정렬",
                description="전화번호를 기준으로 내림차순으로 정렬합니다.",
                value="-phone",
                parameter_only=True,
            ),
        ],
    ),
]


contact_book_create_docs = extend_schema(
    summary="연락처 생성 API",
    tags=["ContactBook"],
    description="주소록의 연락처를 생성하는 API",
    request=ContactBookRetrieveSerializer,
)


contact_book_list_docs = extend_schema(
    summary="연락처 목록을 조회하는 API",
    tags=["ContactBook"],
    description="본인의 연락처 목록을 조회하는 API",
    parameters=contact_book_parameters,
    request=ContactBookListSerializer,
)

contact_book_retrieve_docs = extend_schema(
    summary="연락처 상세를 조회하는 API",
    tags=["ContactBook"],
    description="본인의 연락처를 상세 조회한다.",
    request=ContactBookRetrieveSerializer,
)
