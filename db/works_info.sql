CREATE TABLE works_info
(
    id              BIGINT(20) PRIMARY KEY AUTO_INCREMENT   COMMENT 'id',
    name            VARCHAR(64)                NOT NULL     COMMENT '作品名',
    team_id         BIGINT(20)                 NOT NULL     COMMENT '团队id',
    image_url_list  TEXT                       NOT NULL     COMMENT '轮播图url',
    content         TEXT                       NOT NULL     COMMENT '比赛介绍富文本',
    works_url       TEXT                       NOT NULL     COMMENT '作品下载url',
    ctime           DATETIME                   NULL         COMMENT '创建时间',
    mtime           DATETIME                   NULL         COMMENT '修改时间',
    deleted         BOOLEAN DEFAULT FALSE      NOT NULL     COMMENT '是否删除'
);
