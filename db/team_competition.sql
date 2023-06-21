CREATE TABLE team_competition
(
    id              BIGINT(20) PRIMARY KEY AUTO_INCREMENT   COMMENT 'id',
    team_id         BIGINT(20)                 NOT NULL     COMMENT '团队id',
    competition_id  BIGINT(20)                 NOT NULL     COMMENT '比赛id',
    works_id        BIGINT(20)                 NULL         COMMENT '作品id',
    team_name       VARCHAR(64)                NOT NULL     COMMENT '团队名称',
    ctime           DATETIME                   NULL         COMMENT '创建时间',
    mtime           DATETIME                   NULL         COMMENT '修改时间',
    deleted         BOOLEAN DEFAULT FALSE      NOT NULL     COMMENT '是否删除'
);
