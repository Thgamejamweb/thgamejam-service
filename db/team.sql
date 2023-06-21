CREATE TABLE team
(
    id              BIGINT(20) PRIMARY KEY AUTO_INCREMENT   COMMENT 'id',
    name            VARCHAR(20)                NOT NULL     COMMENT '团队名称',
    ctime           DATETIME                   NULL         COMMENT '创建时间',
    mtime           DATETIME                   NULL         COMMENT '修改时间',
    deleted         BOOLEAN DEFAULT FALSE      NOT NULL     COMMENT '是否删除'
);
