truncate table produtos, compras, vendas restart identity cascade;

INSERT INTO produtos(nome, preco_de_venda, estoque) VALUES
('Ração para bovinos', 110, 0),
('Ração para equinos', 120, 0),
('Ração para aves', 100, 0),
('Suplemento mineral', 35, 0),
('Vacina febre aftosa', 50, 0),
('Sal mineral', 25, 0),
('Antiparasitário', 107, 0),
('Cama de frango', 20, 0),
('Suplemento proteico', 160, 0);

INSERT INTO compras(dia, produto_id, preco, qtd, fornecedor) VALUES
(current_date - interval '23 days' , 1, 90.00, 10, 'AgroForte'),
(current_date - interval '22 days', 2, 110.50, 10, 'NutriPlus'),
(current_date - interval '20 days', 3, 80.00, 20, 'AviSupply'),
(current_date - interval '18 days', 4, 25.00, 5, 'MineraisBR'),
(current_date - interval '15 days', 5, 35.00, 20, 'VetFarma'),
(current_date - interval '13 days', 6, 20.00, 10, 'MineraisBR'),
(current_date - interval '10 days', 7, 95.00, 5, 'VetFarma'),
(current_date - interval '7 days', 8, 18.00, 20, 'AviSupply'),
(current_date - interval '5 days', 9, 150.00, 5, 'AgroForte');

INSERT INTO vendas(dia, produto_id, preco, qtd, comprador) VALUES
(current_date - interval '21 days', 1, 110.00, 4, 'Fazenda Boa Vista'),
(current_date - interval '19 days', 2, 120.00, 7, 'Haras São José'),
(current_date - interval '17 days', 3, 95.00, 7, 'Granja Caipira'),
(current_date - interval '16 days', 4, 35.00, 3, 'Sítio Esperança'),
(current_date - interval '14 days', 5, 50.00, 10, 'Fazenda Boa Vista'),
(current_date - interval '11 days', 6, 25.00, 5, 'Sítio Esperança'),
(current_date - interval '8 days', 3, 100.00, 8, 'Granja Caipira'),
(current_date - interval '6 days', 7, 105.00, 4, 'Haras São José'),
(current_date - interval '3 days', 9, 150.00, 5, 'Fazenda Boa Vista'),
(current_date, 1, 110.00, 2, 'Fazenda Boa Vista');