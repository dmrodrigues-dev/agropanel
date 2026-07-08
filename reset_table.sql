set foreign_key_checks = 0;
truncate vendas;
truncate compras;
truncate produtos;
set foreign_key_checks = 1;

-- Produtos
INSERT INTO produtos (id, nome) VALUES
(1, 'Ração para bovinos'),
(2, 'Ração para equinos'),
(3, 'Ração para aves'),
(4, 'Suplemento mineral'),
(5, 'Vacina febre aftosa'),
(6, 'Sal mineral'),
(7, 'Antiparasitário'),
(8, 'Cama de frango'),
(9, 'Concentrado proteico');

-- Compras (junho/2026)
INSERT INTO compras (id, dia, produto_id, preco, qtd, fornecedor) VALUES
(NULL, curdate() - interval 23 day , 1, 120.00, 50, 'AgroForte'),
(NULL, curdate() - interval 22 day, 2, 95.50, 30, 'NutriPlus'),
(NULL, curdate() - interval 20 day, 3, 60.00, 80, 'AviSupply'),
(NULL, curdate() - interval 18 day, 4, 45.00, 100, 'MineraisBR'),
(NULL, curdate() - interval 15 day, 5, 15.00, 200, 'VetFarma'),
(NULL, curdate() - interval 13 day, 6, 30.00, 60, 'MineraisBR'),
(NULL, curdate() - interval 10 day, 7, 22.00, 90, 'VetFarma'),
(NULL, curdate() - interval 7 day, 8, 18.00, 150, 'AviSupply'),
(NULL, curdate() - interval 5 day, 9, 75.00, 40, 'AgroForte');

-- Vendas (junho/2026)
INSERT INTO vendas (id, dia, produto_id, preco, qtd, comprador) VALUES
(NULL, curdate() - interval 21 day, 1, 150.00, 40, 'Fazenda Boa Vista'),
(NULL, curdate() - interval 19 day, 2, 120.00, 25, 'Haras São José'),
(NULL, curdate() - interval 17 day, 3, 80.00, 70, 'Granja Caipira'),
(NULL, curdate() - interval 16 day, 4, 55.00, 90, 'Sítio Esperança'),
(NULL, curdate() - interval 14 day, 5, 20.00, 180, 'Fazenda Boa Vista'),
(NULL, curdate() - interval 11 day, 6, 40.00, 50, 'Sítio Esperança'),
(NULL, curdate() - interval 8 day, 3, 80.00, 60, 'Granja Caipira'),
(NULL, curdate() - interval 6 day, 7, 30.00, 80, 'Haras São José'),
(NULL, curdate() - interval 3 day, 9, 95.00, 35, 'Fazenda Boa Vista'),
(NULL, curdate(), 1, 150.00, 20, 'Granja Caipira');
