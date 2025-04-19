AUDIT (
  name assert_positive_exposure
);

SELECT *
FROM @this_model
WHERE exposure_at_default < 0;
