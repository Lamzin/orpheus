CREATE TABLE `fingerprints` (
  `frequency` bigint(9) unsigned NOT NULL,
  `track_id` int(9) NOT NULL,
  `track_part` tinyint(3) unsigned DEFAULT NULL,
  KEY `idx_fingerprints_frequency` (`frequency`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
