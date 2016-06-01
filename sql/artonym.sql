

CREATE TABLE `artonym`.`art_image_hash` (
  `hash` BIGINT(15) UNSIGNED NOT NULL,
  `post_id` BIGINT(15) UNSIGNED NOT NULL,
  PRIMARY KEY (`hash`),
  UNIQUE KEY `hash_UNIQUE` (`hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;