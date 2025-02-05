SELECT SUM(Num_Violations)
FROM Violations
WHERE Camera_ID IN (SELECT Camera_ID
                        FROM Cameras
                        WHERE Intersection = 'ROOSEVELT AND HALSTED' AND Violation_Date LIKE '%2020');