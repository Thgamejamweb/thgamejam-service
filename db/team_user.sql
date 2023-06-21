CREATE TABLE team
(
    id              BIGINT(20) PRIMARY KEY AUTO_INCREMENT   COMMENT 'id',
    team_id         BIGINT(20)                 NOT NULL     COMMENT '团队id'
    user_id         BIGINT(20)                 NOT NULL     COMMENT '用户id'
    is_admin        BOOLEAN DEFAULT FALSE      NOT NULL     COMMENT '是否为管理员',
    is_join         BOOLEAN DEFAULT FALSE      NOT NULL     COMMENT '是否加入',
    ctime           DATETIME                   NULL         COMMENT '创建时间',
    mtime           DATETIME                   NULL         COMMENT '修改时间',
    deleted         BOOLEAN DEFAULT FALSE      NOT NULL     COMMENT '是否删除'
);
