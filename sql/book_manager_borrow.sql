create table borrow
(
    _id     int auto_increment
        primary key,
    user_id int                                not null,
    book_id int                                not null,
    date    datetime default CURRENT_TIMESTAMP not null,
    status  int      default 0                 not null comment '0 - 已提交借阅申请
1 - 已成功借阅
2 - 拒绝借阅
3 - 已归还',
    constraint borrow__id_uindex
        unique (_id),
    constraint fk_book_id
        foreign key (book_id) references book (_id),
    constraint fk_user_id
        foreign key (user_id) references user (_id)
);

INSERT INTO book_manager.borrow (_id, user_id, book_id, date, status) VALUES (6, 4, 1, '2022-05-14 23:58:05', 3);
INSERT INTO book_manager.borrow (_id, user_id, book_id, date, status) VALUES (7, 4, 2, '2022-05-14 23:58:11', 1);
INSERT INTO book_manager.borrow (_id, user_id, book_id, date, status) VALUES (8, 4, 3, '2022-05-15 21:55:34', 2);
