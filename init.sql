CREATE
DATABASE IF NOT EXISTS study;

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `task_log`;
CREATE TABLE `task_log`  (
  `id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `task_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '任务名',
  `operator` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '任务执行人 （系统，用户手动）',
  `execute_time` datetime NULL DEFAULT NULL COMMENT '执行时间',
  `result` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '执行结果',
  `during_time` int NULL DEFAULT NULL COMMENT '执行时间(ms)',
  `task_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '任务id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

DROP TABLE IF EXISTS `task`;
CREATE TABLE `task`  (
  `id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `task_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '任务名',
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '任务类型 cron ,date',
  `cron` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '表达式',
  `execute_time` datetime NULL DEFAULT NULL COMMENT '执行时间',
  `seconds` int NULL DEFAULT NULL COMMENT '间隔秒数',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '任务脚本',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '任务描述',
  `run_count` int NULL DEFAULT NULL COMMENT '运行次数',
  `last_run_times` datetime NULL DEFAULT NULL COMMENT '最后执行时间',
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '任务状态 -1 结束 0 暂停 1 运行中',
  `uid` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '任务归属人（创建人）',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of task
-- ----------------------------
INSERT INTO `task` VALUES ('1654348297', 'cron任务', 'cron', '* * * * * ?', NULL, NULL, 'def hello():  print(\'hello\')', '每秒执行一次', NULL, NULL, '-1', NULL);
INSERT INTO `task` VALUES ('1654348298', '日期任务', 'date', '', '2024-07-02 23:30:09', NULL, 'def hello():  print(\'hello2\')', '日期时间到了，执行一次', NULL, NULL, '-1', NULL);
INSERT INTO `task` VALUES ('1654348299', '间隔任务', 'interval', '', NULL, 5, 'def hello():  print(\'hello3\')', '间隔5秒执行', NULL, NULL, '', NULL);




