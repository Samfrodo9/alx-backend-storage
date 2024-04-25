-- a SQL script that generates the view need_meeting,
-- which contains a list of all students with a strict score 
-- less 80 and no recent meetings or more than a month have passed.
CREATE VIEW need_meeting AS SELECT name from students WHERE score < 80
AND (last_meeting IS NULL OR last_meeting < DATE(CURDATE() - INTERVAL 1 MONTH));

