# current
CREATE TABLE `fp_queue` (
  `id` int(9) unsigned NOT NULL,
  `processing_stage` enum('ps_done_fp','ps_processing','ps_error') NOT NULL DEFAULT 'ps_done_fp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
