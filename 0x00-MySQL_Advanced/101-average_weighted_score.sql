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
