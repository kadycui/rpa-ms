CREATE TABLE `rpa_job_records` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
    `app_uuid` VARCHAR(36) NOT NULL COMMENT '应用唯一标识 (UUID)',
    `app_name` VARCHAR(255) NOT NULL COMMENT '应用名称',
    `start_time` DATETIME NULL COMMENT '开始时间',
    `end_time` DATETIME NULL COMMENT '结束时间',
    `result_status` ENUM('成功', '运行中', '超时', '失败') NOT NULL DEFAULT '成功' COMMENT '执行状态',
    `result_detail` TEXT NULL COMMENT '执行结果详情',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',

    INDEX `idx_app_uuid` (`app_uuid`),
    INDEX `idx_start_time` (`start_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='RPA任务记录表';
