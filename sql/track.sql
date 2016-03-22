CREATE TABLE `orpheus`.`track` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `processing_stage` ENUM('ps_new', 'ps_processing', 'ps_done', 'ps_not_found') NOT NULL DEFAULT 'ps_new' COMMENT '',
  `name` VARCHAR(128) NULL COMMENT '',
  `author` VARCHAR(64) NULL COMMENT '',
  `url_page` VARCHAR(256) NULL COMMENT '',
  `url_track` VARCHAR(256) NULL COMMENT '',
  `url_disk` VARCHAR(512) NULL COMMENT '',
  `data` VARCHAR(4096) NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '',
  UNIQUE INDEX `id_UNIQUE` (`id` ASC)  COMMENT '');
