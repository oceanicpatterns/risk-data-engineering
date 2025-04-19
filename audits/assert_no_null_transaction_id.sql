AUDIT (
  name assert_no_null_transaction_id
);

SELECT *
FROM @this_model
WHERE transaction_id IS NULL;
