CREATE TABLE user
(
    id              BIGINT(20) PRIMARY KEY AUTO_INCREMENT   COMMENT 'id',
    name            VARCHAR(64)                NULL         COMMENT '用户名',
    email           VARCHAR(50)                NULL         COMMENT '邮箱',
    password        VARCHAR(50)                NOT NULL     COMMENT '密码'
    ctime           DATETIME                   NULL         COMMENT '创建时间',
    mtime           DATETIME                   NULL         COMMENT '修改时间',
    deleted         BIT(1) DEFAULT b'0'        NOT NULL     COMMENT '是否删除，0表示未删除，1表示已删除'
);
