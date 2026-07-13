truncate table produtos, compras, vendas, restart identity cascade;

INSERT INTO produtos(nome) VALUES
('Ração para bovinos'),
('Ração para equinos'),
('Ração para aves'),
('Suplemento mineral'),
('Vacina febre aftosa'),
('Sal mineral'),
('Antiparasitário'),
('Cama de frango'),
('Concentrado proteico');

INSERT INTO compras(dia, produto_id, preco, qtd, fornecedor) VALUES
(current_date - interval '23 days' , 1, 120.00, 50, 'AgroForte'),
(current_date - interval '22 days', 2, 95.50, 30, 'NutriPlus'),
(current_date - interval '20 days', 3, 60.00, 80, 'AviSupply'),
(current_date - interval '18 days', 4, 45.00, 100, 'MineraisBR'),
(current_date - interval '15 days', 5, 15.00, 200, 'VetFarma'),
(current_date - interval '13 days', 6, 30.00, 60, 'MineraisBR'),
(current_date - interval '10 days', 7, 22.00, 90, 'VetFarma'),
(current_date - interval '7 days', 8, 18.00, 150, 'AviSupply'),
(current_date - interval '5 days', 9, 75.00, 40, 'AgroForte');

INSERT INTO vendas(dia, produto_id, preco, qtd, comprador) VALUES
(current_date - interval '21 days', 1, 150.00, 40, 'Fazenda Boa Vista'),
(current_date - interval '19 days', 2, 120.00, 25, 'Haras São José'),
(current_date - interval '17 days', 3, 80.00, 70, 'Granja Caipira'),
(current_date - interval '16 days', 4, 55.00, 90, 'Sítio Esperança'),
(current_date - interval '14 days', 5, 20.00, 180, 'Fazenda Boa Vista'),
(current_date - interval '11 days', 6, 40.00, 50, 'Sítio Esperança'),
(current_date - interval '8 days', 3, 80.00, 60, 'Granja Caipira'),
(current_date - interval '6 days', 7, 30.00, 80, 'Haras São José'),
(current_date - interval '3 days', 9, 95.00, 35, 'Fazenda Boa Vista'),
(current_date, 1, 150.00, 20, 'Granja Caipira');