CREATE TABLE file (
    id                  BIGINT  PRIMARY KEY         AUTO_INCREMENT,
    file_name           VARCHAR(64) NOT NULL                    COMMENT '文件名',
    e_tag               VARCHAR(50) NOT NULL                    COMMENT '文件哈希',
    is_upload BOOLEAN   DEFAULT FALSE NOT NULL                  COMMENT '是否上传成功',
    ctime               DATETIME                   NULL         COMMENT '创建时间',
    mtime               DATETIME                   NULL         COMMENT '修改时间',
    deleted             BOOLEAN DEFAULT FALSE      NOT NULL     COMMENT '是否删除'
);