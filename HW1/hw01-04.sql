.open chicago-red-light-cameras.db

SELECT SUM(Num_Violations)
FROM Violations
WHERE Violation_Date like "%2020" AND
      Camera_ID IN (SELECT Camera_ID FROM Cameras Where Intersection = "ROOSEVELT AND HALSTED");

SELECT SUM(Num_Violations)
FROM Violations
WHERE Violation_Date like "%2023" AND
      Camera_ID IN (SELECT Camera_ID FROM Cameras Where Intersection = "ROOSEVELT AND HALSTED");