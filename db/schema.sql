create table auth_user
(
    id           int auto_increment
        primary key,
    password     varchar(128) not null,
    last_login   datetime(6)  null,
    is_superuser tinyint(1)   not null,
    username     varchar(150) not null,
    first_name   varchar(150) not null,
    last_name    varchar(150) not null,
    email        varchar(254) not null,
    is_staff     tinyint(1)   not null,
    is_active    tinyint(1)   not null,
    date_joined  datetime(6)  not null,
    constraint username
        unique (username)
);

create table contactbook
(
    id                bigint auto_increment
        primary key,
    created_datetime  datetime(6)  not null comment '생성일시',
    updated_datetime  datetime(6)  not null comment '수정일시',
    name              varchar(50)  not null comment '저장한 이름',
    email             varchar(254) not null comment '저장한 이메일',
    phone             varchar(20)  not null comment '저장한 전화번호',
    company           varchar(50)  not null comment '저장한 회사',
    position          varchar(50)  not null comment '저장한 직책',
    memo              longtext     not null comment '메모',
    profile_image_url varchar(200) not null comment '프로필 이미지 URL',
    address           varchar(100) not null comment '주소',
    birthday          datetime(6)  null comment '생일',
    website_url       varchar(200) not null comment '웹사이트 URL',
    owner_id          int          not null comment '주소록 소유자',
    constraint contactbook_owner_id_7acde38a_fk_auth_user_id
        foreign key (owner_id) references auth_user (id)
)
    comment '주소록';

create index contactbook_name_5f92a9_idx
    on contactbook (name);

create table label
(
    id               bigint auto_increment
        primary key,
    created_datetime datetime(6) not null comment '생성일시',
    updated_datetime datetime(6) not null comment '수정일시',
    name             varchar(50) not null comment '라벨 이름',
    owner_id         int         not null comment '주소록 소유자',
    constraint label_owner_id_35ce755f_fk_auth_user_id
        foreign key (owner_id) references auth_user (id)
)
    comment '라벨';

create table contactbook_label
(
    id               bigint auto_increment
        primary key,
    created_datetime datetime(6) not null comment '생성일시',
    updated_datetime datetime(6) not null comment '수정일시',
    contact_id       bigint      not null comment '주소록',
    label_id         bigint      not null comment '라벨',
    constraint contactbook_label_contact_id_330bb23a_fk_contactbook_id
        foreign key (contact_id) references contactbook (id),
    constraint contactbook_label_label_id_d037c5ac_fk_label_id
        foreign key (label_id) references label (id)
)
    comment '주소록에 있는 연락처의 라벨링을 관리하는 테이블';

