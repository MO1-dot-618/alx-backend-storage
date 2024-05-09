-- procedure to compute weighted average score of students
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
	DECLARE total_weight FLOAT;
	DECLARE total_weighted_score FLOAT;

	SELECT SUM(projects.weight) AS total_weight,
	SUM(corrections.score * projects.weight) AS total_weighted_score
	INTO
        total_weight,
        total_weighted_score
	FROM corrections
	JOIN projects ON corrections.project_id = projects.id
	WHERE
        corrections.user_id = user_id;

	UPDATE users
	SET
	average_score = total_weighted_score / NULLIF(total_weight, 0)
	WHERE id = user_id;
END$$

DELIMITER ;
