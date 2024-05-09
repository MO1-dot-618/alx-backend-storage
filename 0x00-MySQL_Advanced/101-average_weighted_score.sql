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


-- Procedure to compute weighted average score of all users
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE user_id_cursor CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN user_id_cursor;
    user_loop: LOOP
        FETCH user_id_cursor INTO user_id;
        IF done THEN
            LEAVE user_loop;
        END IF;
        
        -- Call the ComputeAverageWeightedScoreForUser procedure for each user
        CALL ComputeAverageWeightedScoreForUser(user_id);
    END LOOP;

    CLOSE user_id_cursor;
END$$

DELIMITER ;
