CREATE TABLE works_info
(
    id             BIGINT(20) PRIMARY KEY AUTO_INCREMENT COMMENT 'id',
    team_id        BIGINT(20)            NOT NULL COMMENT '团队id',
    image_url_list TEXT                  NOT NULL COMMENT '轮播图url',
    works_id       bigint(20)            Not Null COMMENT 'works_id',
    content        TEXT                  NOT NULL COMMENT '比赛介绍富文本',
    file_id        BIGINT(20)            NOT NULL COMMENT '作品文件id',
    ctime          DATETIME              NULL COMMENT '创建时间',
    mtime          DATETIME              NULL COMMENT '修改时间',
    deleted        BOOLEAN DEFAULT FALSE NOT NULL COMMENT '是否删除'
);
