CREATE TABLE `perceptual_hashes` (
  `hash` bigint(9) unsigned NOT NULL,
  `track` int(9) unsigned NOT NULL,
  `band` tinyint(5) unsigned NOT NULL,
  KEY `index_band` (`band`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


