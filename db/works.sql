CREATE TABLE works
(
    id              BIGINT(20) PRIMARY KEY AUTO_INCREMENT   COMMENT 'id',
    name            VARCHAR(64)                NOT NULL     COMMENT '作品名',
    team_id         BIGINT(20)                 NOT NULL     COMMENT '团队id',
    header_imageURL VARCHAR(255)               NULL         COMMENT '头图',
    ctime           DATETIME                   NULL         COMMENT '创建时间',
    mtime           DATETIME                   NULL         COMMENT '修改时间',
    deleted         BOOLEAN DEFAULT FALSE      NOT NULL     COMMENT '是否删除'
);
