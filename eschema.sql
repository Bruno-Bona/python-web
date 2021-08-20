drop table if exists entradas;

create table entradas (
    id integer PRIMARY key AUTOINCREMENT,
    titulo string not null,
    texto string not null
);