CREATE TABLE UserSettings (
    UserName NVARCHAR(50) NOT NULL UNIQUE,
    R INT NOT NULL,
    G INT NOT NULL,
    B INT NOT NULL,
    CONSTRAINT CHK_RGB CHECK (R >= 0 AND R <= 255 AND G >= 0 AND G <= 255 AND B >= 0 AND B <= 255)
);

ALTER TABLE UserSettings
DROP column Id;

ALTER TABLE UserSettings
Add brightness int default 0;

ALTER TABLE UserSettings
ADD CONSTRAINT constraint_name CHECK (UserName <> '');

ALTER TABLE UserSettings
ADD Id INT;

ALTER TABLE UserSettings
ADD Id INT IDENTITY(1,1) PRIMARY KEY;


UPDATE UserSettings
SET Id = (SELECT COUNT(*) FROM UserSettings AS T WHERE T.Id <= UserSettings.Id);

ALTER TABLE UserSettings
ADD Id INT;

WITH CTE AS (
    SELECT *, ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS rn
    FROM UserSettings
)
UPDATE CTE SET Id = rn

ALTER TABLE UserSettings
ALTER COLUMN Id INT NOT NULL;

ALTER TABLE UserSettings
ADD CONSTRAINT PK_your_table_Id PRIMARY KEY (Id);


CREATE TRIGGER sustain_Id
ON UserSettings
AFTER DELETE, UPDATE
AS
BEGIN
    WITH CTE AS (
        SELECT *, ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS rn
        FROM UserSettings
    )
    UPDATE CTE SET Id = rn;
END

CREATE TRIGGER sustain_Id_2
ON UserSettings
AFTER DELETE, INSERT
AS
BEGIN
    WITH CTE AS (
        SELECT *, ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS rn
        FROM UserSettings
    )
    UPDATE CTE SET Id = rn;
END

INSERT INTO UserSettings (UserName, R, G, B, brightness, Id) VALUES ('³ÂìÌ¿¬2', 255, 255, 255, 1, 0);

ALTER TABLE UserSettings
ADD CONSTRAINT CHK_Brightness
CHECK (brightness BETWEEN 1 AND 5);









