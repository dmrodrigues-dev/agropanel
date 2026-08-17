
create table produtos (
  id bigint generated always as identity primary key,
  nome varchar(80) not null,
  preco_de_venda numeric(10,2) not null,
  estoque int not null default 0
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

create or replace function put_estoque()
returns trigger as $$
begin
  if old.produto_id = new.produto_id then
    update produtos
    set estoque = estoque - (old.qtd * TG_ARGV[0]::integer) + (new.qtd * TG_ARGV[0]::integer)
    where id = old.produto_id;
  else
    update produtos
    set estoque = estoque - (old.qtd * TG_ARGV[0]::integer)
    where id = old.produto_id;
    update produtos
    set estoque = estoque + (new.qtd * TG_ARGV[0]::integer)
    where id = new.produto_id;
  end if;
  return new;
end;
$$ language plpgsql;

create or replace function insert_or_delete_estoque()
returns trigger as $$
begin
  if (TG_OP = 'INSERT') then
    update produtos
    set estoque = estoque + new.qtd * TG_ARGV[0]::integer
    where id = new.produto_id;
    return new;
  elsif TG_OP = 'DELETE' then
    update produtos
    set estoque = estoque - old.qtd * TG_ARGV[0]::integer
    where id = old.produto_id;
    return old;
  end if;
end;
$$ language plpgsql;

create trigger add_del_compra_gatilho
after insert or delete on compras
for each row
execute function insert_or_delete_estoque('1');

create trigger add_del_vendas_gatilho
after insert or delete on vendas
for each row
execute function insert_or_delete_estoque('-1');

create trigger put_compra_gatilho
after update on compras
for each row
when (old.qtd is distinct from new.qtd or old.produto_id is distinct from new.produto_id)
execute function put_estoque('1');

create trigger put_venda_gatilho
after update on vendas
for each row
when (old.qtd is distinct from new.qtd or old.produto_id is distinct from new.produto_id)
execute function put_estoque('-1');