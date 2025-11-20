SELECT
  O.ID AS "ID do Pedido",
  O.CUSTOMER_ID AS "ID do Cliente",
  O.PAYMENT_ID AS "ID do Pagamento",
  O.STATUS_ID AS "ID do Status",
  OS.NAME AS "Nome do Status",
  O.VALE_ORDER_ID AS "Código VALE",
  O.TOTAL_VALUE AS "Valor Total",
  O.PORTAL AS "Portal de Origem",
  O.CENTER AS "Centro",
  O.BESC_ORDER_ID AS "Código BESC",
  O.CONTRACT_NUMBER AS "Número do Contrato",
  O.INVOICE_NUMBER AS "Número da Nota",
  O.PROPOSAL_ID AS "ID da Proposta",
  O.CREATED_AT AS "Data de Criação",
  O.UPDATED_AT AS "Data de Atualização"
FROM
  ORDERS AS O
INNER JOIN
  ORDERS_STATUS AS OS
    ON O.STATUS_ID = OS.ID;
