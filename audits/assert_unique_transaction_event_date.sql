AUDIT (
  name assert_unique_transaction_event_date
);

SELECT transaction_id, event_date, COUNT(*) as cnt
FROM @this_model
GROUP BY transaction_id, event_date
HAVING cnt > 1;
