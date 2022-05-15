create table user
(
    _id       int auto_increment
        primary key,
    user_name varchar(20)          not null,
    user_pwd  varchar(128)         not null,
    role      tinyint(1) default 1 not null comment '0 - 管理员
1 - 用户',
    constraint user__id_uindex
        unique (_id),
    constraint user_user_name_uindex
        unique (user_name)
);

INSERT INTO book_manager.user (_id, user_name, user_pwd, role) VALUES (4, '赵春旭', '123', 1);
INSERT INTO book_manager.user (_id, user_name, user_pwd, role) VALUES (5, '帆帆', '123', 0);
