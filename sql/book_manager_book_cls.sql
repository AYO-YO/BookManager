create table book_cls
(
    _id      int auto_increment
        primary key,
    cls_name varchar(30) not null,
    constraint book_cls__id_uindex
        unique (_id)
);

INSERT INTO book_manager.book_cls (_id, cls_name) VALUES (1, '无');
INSERT INTO book_manager.book_cls (_id, cls_name) VALUES (2, '科幻');
INSERT INTO book_manager.book_cls (_id, cls_name) VALUES (3, '诗歌');
INSERT INTO book_manager.book_cls (_id, cls_name) VALUES (4, '小说');
