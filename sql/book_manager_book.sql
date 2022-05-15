create table book
(
    _id    int auto_increment
        primary key,
    name   varchar(50)          not null,
    author varchar(20)          not null,
    press  varchar(20)          null,
    cls    int        default 1 not null,
    active tinyint(1) default 1 null,
    constraint book__id_uindex
        unique (_id),
    constraint fk_book_cls
        foreign key (cls) references book_cls (_id)
);

INSERT INTO book_manager.book (_id, name, author, press, cls, active) VALUES (1, '三国演义', '罗贯中', '文学出版社', 4, 1);
INSERT INTO book_manager.book (_id, name, author, press, cls, active) VALUES (2, '宋词三百首', '苏轼', '文学出版社', 3, 1);
INSERT INTO book_manager.book (_id, name, author, press, cls, active) VALUES (3, '红楼梦', '曹雪芹', '文学出版社', 4, 1);
INSERT INTO book_manager.book (_id, name, author, press, cls, active) VALUES (24, '西游记', '吴承恩', '文学出版社', 4, 1);
