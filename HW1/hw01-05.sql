SELECT Camera_ID, SUM(Num_Violations) AS Total_Violations
FROM Violations
GROUP BY Camera_ID
ORDER BY Total_Violations DESC
LIMIT 1;