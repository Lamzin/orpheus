DELETE FROM `orpheus`.`hashes0`;
DELETE FROM `orpheus`.`hashes1`;
DELETE FROM `orpheus`.`hashes2`;
DELETE FROM `orpheus`.`hashes3`;
DELETE FROM `orpheus`.`hashes4`;
DELETE FROM `orpheus`.`hashes5`;



CREATE TABLE `orpheus`.`hashes0` (
  `hash` SMALLINT(9) UNSIGNED NOT NULL,
  `full_hash` BIGINT(15) UNSIGNED NOT NULL,
  `track_id` INT UNSIGNED NOT NULL,
  KEY `idx_fingerprints_frequency` (`hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `orpheus`.`hashes1` (
  `hash` SMALLINT(9) UNSIGNED NOT NULL,
  `full_hash` BIGINT(15) UNSIGNED NOT NULL,
  `track_id` INT UNSIGNED NOT NULL,
  KEY `idx_fingerprints_frequency` (`hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `orpheus`.`hashes2` (
  `hash` SMALLINT(9) UNSIGNED NOT NULL,
  `full_hash` BIGINT(15) UNSIGNED NOT NULL,
  `track_id` INT UNSIGNED NOT NULL,
  KEY `idx_fingerprints_frequency` (`hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `orpheus`.`hashes3` (
  `hash` SMALLINT(9) UNSIGNED NOT NULL,
  `full_hash` BIGINT(15) UNSIGNED NOT NULL,
  `track_id` INT UNSIGNED NOT NULL,
  KEY `idx_fingerprints_frequency` (`hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `orpheus`.`hashes4` (
  `hash` SMALLINT(9) UNSIGNED NOT NULL,
  `full_hash` BIGINT(15) UNSIGNED NOT NULL,
  `track_id` INT UNSIGNED NOT NULL,
  KEY `idx_fingerprints_frequency` (`hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `orpheus`.`hashes5` (
  `hash` SMALLINT(9) UNSIGNED NOT NULL,
  `full_hash` BIGINT(15) UNSIGNED NOT NULL,
  `track_id` INT UNSIGNED NOT NULL,
  KEY `idx_fingerprints_frequency` (`hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
