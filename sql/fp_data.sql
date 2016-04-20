# current
CREATE TABLE `fp_data` (
  `id` int(9) unsigned NOT NULL,
  `fingerprints` MEDIUMTEXT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
