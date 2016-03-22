CREATE TABLE `track` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `processing_stage` enum('ps_new','ps_processing','ps_done','ps_not_found') NOT NULL DEFAULT 'ps_new',
  `name` varchar(128) DEFAULT NULL,
  `author` varchar(64) DEFAULT NULL,
  `url_page` varchar(256) DEFAULT NULL,
  `url_track` varchar(256) DEFAULT NULL,
  `url_disk` varchar(512) DEFAULT NULL,
  `site_id` int(11) DEFAULT '1',
  `data` varchar(4096) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=236273 DEFAULT CHARSET=utf8;
