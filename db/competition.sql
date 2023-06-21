CREATE TABLE competition
(
    id              BIGINT(20) PRIMARY KEY AUTO_INCREMENT   COMMENT 'id',
    name            VARCHAR(64)                NOT NULL     COMMENT '比赛名称',
    staff_id        BIGINT(20)                 NOT NULL     COMMENT '主办方id',
    description     VARCHAR(100)               NULL         COMMENT '比赛简介描述',
    header_imageURL VARCHAR(255)               NULL         COMMENT '头图',
    signup_start_date   DATETIME               NULL         COMMENT '报名开始日期',
    signup_end_date     DATETIME               NULL         COMMENT '报名结束日期',
    start_date          DATETIME               NULL         COMMENT '比赛开始日期',
    end_date            DATETIME               NULL         COMMENT '比赛结束日期',
    score_start_date    DATETIME               NULL         COMMENT '评分开始日期',
    score_end_date      DATETIME               NULL         COMMENT '评分结束日期',
    ctime           DATETIME                   NULL         COMMENT '创建时间',
    mtime           DATETIME                   NULL         COMMENT '修改时间',
    deleted         BOOLEAN DEFAULT FALSE      NOT NULL     COMMENT '是否删除'
);
