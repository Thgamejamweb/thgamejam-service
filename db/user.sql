CREATE TABLE user
(
    id              BIGINT(20) PRIMARY KEY AUTO_INCREMENT   COMMENT 'id',
    name            VARCHAR(64)                NULL         COMMENT '用户名',
    email           VARCHAR(50)                NULL         COMMENT '邮箱',
    password        VARCHAR(50)                NOT NULL     COMMENT '密码',
    description     VARCHAR(100)               NULL         COMMENT '用户描述',
    is_staff        BOOLEAN DEFAULT FALSE      NOT NULL     COMMENT '是否为主办方',
    public_key      VARCHAR(4096)              NULL         COMMENT '公钥',
    private_key     VARCHAR(4096)              NULL         COMMENT '私钥',
    ctime           DATETIME                   NULL         COMMENT '创建时间',
    mtime           DATETIME                   NULL         COMMENT '修改时间',
    deleted         BOOLEAN DEFAULT FALSE      NOT NULL     COMMENT '是否删除'
);
