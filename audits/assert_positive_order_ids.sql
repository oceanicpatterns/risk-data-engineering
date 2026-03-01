AUDIT (
  name assert_positive_transaction_id
);

SELECT *
FROM @this_model
WHERE
  transaction_id < 0;
