CREATE TABLE competition_info
(
    id              BIGINT(20) PRIMARY KEY AUTO_INCREMENT   COMMENT 'id',
    competition_id  BIGINT(20)                 NOT NULL     COMMENT '比赛ID',
    content         TEXT                       NOT NULL     COMMENT '介绍页面富文本',
    ctime           DATETIME                   NULL         COMMENT '创建时间',
    mtime           DATETIME                   NULL         COMMENT '修改时间',
    deleted         BOOLEAN DEFAULT FALSE      NOT NULL     COMMENT '是否删除'
);
