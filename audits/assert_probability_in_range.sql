AUDIT (
  name assert_probability_in_range
);

SELECT *
FROM @this_model
WHERE probability_default < 0 OR probability_default > 1;
