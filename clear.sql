SET FOREIGN_KEY_CHECKS = 0; -- 禁用外键检查

TRUNCATE TABLE CompetitiveKeyword;
TRUNCATE TABLE UserSearchHistory;
TRUNCATE TABLE SeedKeyword;
TRUNCATE TABLE User;
TRUNCATE TABLE DataSourceInfo;

SET FOREIGN_KEY_CHECKS = 1; -- 重新启用外键检查