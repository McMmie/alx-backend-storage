-- a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
	ALTER TABLE users ADD weighted_score INT NOT NULL;
	ALTER TABLE users ADD weight INT NOT NULL;

	UPDATE users
	SET total_weighted_score = (
	SELECT SUM(corrections.score * projects.weight)
	FROM corrections
	INNER JOIN projects
	ON corrections.project_id = projects.id
	WHERE corrections.user_id = users.id
	);

	UPDATE users
	SET weight = (
	SELECT SUM(projects.weight)
	FROM corrections
	INNER JOIN projects
	ON corrections.project_id = projects.id
	WHERE corrections.user_id = users.id
	);

	UPDATE users
	SET users.average_score = IF(users.weight = 0, 0, users.weighted_score / users.weight);
	
	ALTER TABLE users
	DROP COLUMN weighted_score;
	
	ALTER TABLE users
	DROP COLUMN weight;
END $$
DELIMITER ;
