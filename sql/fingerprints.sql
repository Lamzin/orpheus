# current
CREATE TABLE `fingerprints` (
  `hash` bigint(9) unsigned NOT NULL,
  `track` int(9) unsigned NOT NULL,
  KEY `idx_fingerprints_frequency` (`hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
