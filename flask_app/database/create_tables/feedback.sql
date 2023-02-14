CREATE TABLE IF NOT EXISTS `feedback` (
`comment_id`     int(11)       NOT NULL AUTO_INCREMENT 	COMMENT 'Unique identifier for each comment',
`name`           varchar(100)  NOT NULL                	COMMENT 'The name of the commentator',
`email`          varchar(100)  NOT NULL                	COMMENT 'Commentators email',
`Comment`        varchar(100)  DEFAULT NULL            	COMMENT 'comment text',
PRIMARY KEY  (`comment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Feedback";