
create table produtos (
  id bigint generated always as identity primary key,
  nome varchar(80) not null
);

CREATE TABLE compras (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    dia date NOT NULL,
    produto_id bigint NOT NULL,
    preco numeric(10,2) NOT NULL,
    qtd integer NOT NULL,
    fornecedor varchar(80) NOT NULL,

    FOREIGN KEY (produto_id)
    REFERENCES produtos(id)
);

CREATE TABLE vendas (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    dia date NOT NULL,
    produto_id bigint NOT NULL,
    preco numeric(10,2) NOT NULL,
    qtd integer NOT NULL,
    comprador varchar(80),

    FOREIGN KEY (produto_id)
    REFERENCES produtos(id)
);