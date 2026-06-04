create database commerce
default char set utf8
default collate utf8_general_ci;

use commerce;

create table if not exists produtos (
id smallint not null auto_increment,
nome varchar(80) not null,
primary key (id)) default char set utf8;

create table if not exists compras (
id int not null auto_increment,
dia date not null,
produto_id smallint not null,
preco float not null,
qtd smallint not null,
fornecedor varchar(80) not null,
primary key (id),
foreign key (produto_id) references produtos(id)) default char set utf8;

create table if not exists vendas (
id int not null auto_increment,
dia date not null,
produto_id smallint not null,
preco float not null,
qtd smallint not null,
comprador varchar(80),
primary key (id),
foreign key (produto_id) references produtos(id)) default char set utf8;
