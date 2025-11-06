1. Criamos clientes 
    - retorna um ID para o cliente

2. Criamos pedidos 
    - Gera um ID para o pedido
    [13]
    - [Associamos o Pedido para um cliente]

3. Criamos o tributario
    - Gera um ID do tributario

3. Criamos o produto
    - Gera um ID para o produto
    - [associa 1 produto para 1 Pedido]
    - [associa 1 produto para 1 tributario]



(api-manager-orders) ➜  api-manager-orders git:(main) ✗ alembic revision --autogenerate -m "add numero_pedido column to pedidos"
(api-manager-orders) ➜  alembic upgrade head



[]
Podemos criar algumas metricas 

- Quantidade de notas emitidas
- Preco total faturado pelo robo
    - mes
    - dia
    - semana
