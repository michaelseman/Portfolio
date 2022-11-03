-- Frank Rodriguez &
-- Michael Seman
-- Final Project
-- CTS 2433
-- Professor Marcel Socorro Borges

/* For our database we pulled a csv file for all the end of season individual player stats for the NBA 2021-2022 season.
We then created web scraping code in python using Beautiful Soup, to scrape the player information and team information from the web.
The division table was created by hand. */

CREATE DATABASE NBA;
USE NBA;


-- CREATING THE DIVISONS TABLE
-- This table is for all the divisions in the NBA, the PK here will be used as a foreign key in the TEAM database
CREATE TABLE dbo.Divisions(DivisionID TINYINT IDENTITY CONSTRAINT Pk_Divisions PRIMARY KEY CLUSTERED,
DivisionName CHAR(10) NOT NULL,
Conference CHAR(4) NOT NULL)


GO
BULK INSERT dbo.Divisions
FROM 'C:\Users\Michael\Desktop\School\SQLImplementation\FinalProject\divisions.csv'
WITH
(
        FORMAT='CSV',
        FIRSTROW=1
)
GO

--test query
SELECT * FROM Divisions


--  CREATING THE TEAMS TABLE
-- This is the table for the TEAMS, including some stats like Win, Loss record, Points Per Game, and Opponent'S PPG
-- The TeamID PK will be used as a foreign key in the Player Stats table
CREATE TABLE dbo.Teams (
TeamID CHAR(3) PRIMARY KEY,
TeamName VARCHAR(30) NOT NULL,
DivisionID TINYINT NOT NULL
CONSTRAINT FK_Division REFERENCES Divisions (DivisionID),
Wins INT NOT NULL,
Loses INT NOT NULL,
WinPCT FLOAT NOT NULL,
GamesBehind INT NOT NULL,
HomeWins TINYINT NOT NULL,
HomeLosses TINYINT NOT NULL,
AwayWins TINYINT NOT NULL,
AwayLosses TINYINT NOT NULL,
DivisionWins TINYINT NOT NULL,
DivisionLosses TINYINT NOT NULL,
ConferenceWins TINYINT NOT NULL,
ConferenceLosses TINYINT NOT NULL,
PPG FLOAT NOT NULL,
OPP_PPG FLOAT NOT NULL)

GO
BULK INSERT dbo.Teams
FROM 'C:\Users\Michael\Desktop\School\SQLImplementation\FinalProject\teams.csv'
WITH
(
        FORMAT='CSV',
        FIRSTROW=2
)
GO

-- test query
SELECT * FROM Teams;
SELECT T.TeamName, D.DivisionName FROM Teams T JOIN Divisions D on T.DivisionID = d.DivisionID ORDER BY D.DivisionName;


-- CREATING THE PLAYERS TABLE
-- The players table will hold name, weight, height, school, jerseynumber, and country.  We separated this from PlayerStats, to achieve first normal form.  Some players have multiple
-- statlines from different teams. PlayerID is the PK and will be used as a FK in the playerstats table
CREATE TABLE Players(PlayerID INT IDENTITY CONSTRAINT Pk_Players PRIMARY KEY CLUSTERED,
FirstName VARCHAR(30) NOT NULL,
LastName VARCHAR(30) NOT NULL,
JerseyNumber TINYINT,
Height VARCHAR(5),
Weight INT,
School VARCHAR(50),
Country VARCHAR(50))

GO
BULK INSERT dbo.Players
FROM 'C:\Users\Michael\Desktop\School\SQLImplementation\FinalProject\playerdata.csv'
WITH
(
        FORMAT='CSV',
        FIRSTROW=1
)
GO

-- test query
select * from players where school IS NOT NULL;


-- CREATING THE PLAYERSTATS TABLE
-- this table contains the stats proper.  Bear in mind many stats are PER GAME AVERAGES.
-- FK's PlayerID and TeamID can be combined for a composite key.
-- GamesPlayed, GamesStarted are the only NON per game stats.
CREATE TABLE PlayerStats(PlayerID INT NOT NULL
CONSTRAINT FK_Players REFERENCES Players (PlayerID),
TeamID CHAR(3) NOT NULL
CONSTRAINT FK_Teams REFERENCES Teams (TeamID),
Position CHAR(2) NOT NULL,
Age INT NOT NULL,
GamesPlayed INT NOT NULL,
GamesStarted INT NOT NULL,
MinutesPlayed Float NOT NULL,
FieldGoalMade FLOAT NOT NULL,
FieldGoalAttempted FLOAT NOT NULL,
FieldGoalPercentage FLOAT NOT NULL,
ThreePointMade FLOAT NOT NULL,
ThreePointAttempts FLOAT NOT NULL,
ThreePointPercentage FLOAT NOT NULL,
TwoPointMade FLOAT NOT NULL,
TwoPointAttempts FLOAT NOT NULL,
TwoPointPercentage FLOAT NOT NULL,
EffectiveFieldGoalPercentage FLOAT NOT NULL,
FreeThrowMade FLOAT NOT NULL,
FreeThrowAttempts FLOAT NOT NULL,
FreeThrowPercentage FLOAT NOT NULL,
OffensiveRebounds FLOAT NOT NULL,
DefensiveRebounds FLOAT NOT NULL,
TotalRebounds FLOAT NOT NULL,
Assists FLOAT NOT NULL,
Steals FLOAT NOT NULL,
Blocks FLOAT NOT NULL,
Turnovers FLOAT NOT NULL,
Fouls FLOAT NOT NULL,
PointsPerGame FLOAT NOT NULL)

-- ADDING THE Primary Key constraint to PLAYERSTATS
ALTER TABLE PlayerStats
ADD CONSTRAINT PK_PlayerStats PRIMARY KEY (PlayerID, TeamID)

GO
BULK INSERT dbo.PlayerStats
FROM 'C:\Users\Michael\Desktop\School\SQLImplementation\FinalProject\playerstats.csv'
WITH
(
        FORMAT='CSV',
        FIRSTROW=2
)
GO

--test queries
SELECT * FROM PlayerStats;
SELECT * FROM PlayerStats JOIN Players ON PlayerStats.PlayerID = Players.PlayerID;

----------------------------------------------------------------------------------------------
/* This project consists of completing a different group of tasks using a database created by you. The minimum requirements for the database design are:
Insert at least three tables into your database.
Create at least three columns per table, be creative when it comes to the data types of your variables.
In addition, insert 7 records per table.
Define a primary key for each table and  make use of the foreign key concept in a query. 
Once you have finished with the database design, please follow the instructions listed below:
*/

/*1- Add a constraint to a column in any of the tables. (Example: add constraint minimum_date check(Transaction_date >='01.01.2019')...) */
-- we decided to create a contraint for the length of the TeamID - it has to be length exactly 3
ALTER TABLE dbo.teams
ADD CONSTRAINT CK_TeamID_Length_3 
CHECK (LEN(TeamID) = 3);

/* 1.1- Test the constraint by inserting a new record that violates it.*/
INSERT INTO dbo.Teams  
VALUES ('JM','NBA Jam Team',1,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

/*2- Run at least three queries: 
2.1- One query should involve at least three different tables. */

-- We joined the player, playerstats, and team tables to show all the players who played on the Miami Heat this season
-- Those without jersey numbers ended this season without a team.
SELECT
CONCAT(p.FirstName, ' ', p.LastName) AS PlayerFullName,
p.JerseyNumber,
t.TeamName
FROM
dbo.Players p
JOIN dbo.PlayerStats ps
ON p.PlayerID = ps.PlayerID
JOIN dbo.Teams t
ON t.TeamID = ps.TeamID
WHERE t.TeamID = 'MIA';

/*2.2- In at least one of them, Join operators must be used. */

--The query below shows the players that have played in the league this year that have been on more than 1 team.
-- Either because of a trade or because of earlier issues in the season with players having COVID and could not play so 
-- many teams picked up players on 10 day contracts.
SELECT
CONCAT(p.FirstName, ' ', p.LastName) AS PlayerFullName,
COUNT(TeamID) AS NumberOfTeams
FROM
dbo.Players p
JOIN dbo.PlayerStats ps
ON p.PlayerID = ps.PlayerID
GROUP BY CONCAT(p.FirstName, ' ', p.LastName)
HAVING COUNT(TeamID) > 1
ORDER BY COUNT(TeamID) DESC; 

/* 2.3- In at least one of the queries you should use the HAVING clause.*/

-- We wanted to create a query to later be used for a view.
-- We wanted this query to take all 605 players and get their total stats for the year.
-- This presented some problems because all the stats are PER GAME stats (aside from Games played obviously).
-- Some players switched teams throughout the year, and thus had multiple statlines we needed to total
-- We couldn't just use the SUM and AVG functions as a result of most stats being Per Game stats.
-- Another problem was encountered with a divide by 0 error when computing stats such as Field Goal percentage and Three Point percentage.
-- If a player had no three point attempts, this would result in an error for the query.
-- This query fixes all those problems.
select CONCAT(P.LastName, ', ', P.FirstName) AS FullName, 
SUM(S.GamesPlayed) as GP,
ROUND(SUM(s.MinutesPlayed*s.GamesPlayed)/SUM(s.GamesPlayed),1) as MP, 
CASE
	WHEN SUM(S.FieldGoalAttempted)= 0
	THEN NULL
	ELSE ROUND(SUM(S.FieldGoalMade)/SUM(s.FieldGoalAttempted)*100,2)
END as 'FG%',
ROUND(SUM(S.FieldGoalAttempted*S.GamesPlayed)/SUM(S.GamesPlayed),1) as FGA,
CASE
	WHEN SUM(S.ThreePointAttempts)= 0
	THEN NULL
	ELSE ROUND(SUM(S.ThreePointMade)/SUM(s.ThreePointAttempts)*100,2)
END as '3P%',
ROUND(SUM(s.ThreePointAttempts*S.GamesPlayed)/SUM(S.GamesPlayed),2) AS '3PA',
CASE
	WHEN SUM(S.TwoPointAttempts)= 0
	THEN NULL
	ELSE ROUND(SUM(S.TwoPointMade)/SUM(s.TwoPointAttempts)*100,2) 
END AS '2P%',
CASE
	WHEN SUM(S.FieldGoalAttempted)= 0
	THEN NULL
	ELSE ROUND(SUM(S.FieldGoalMade+.5*s.ThreePointMade)/SUM(s.FieldGoalAttempted)*100,2) 
END AS 'EFG%', 
CASE
	WHEN SUM(s.FreeThrowAttempts)= 0
	THEN NULL
	ELSE ROUND(SUM(S.FreeThrowMade)/SUM(s.FreeThrowAttempts)*100,2)
END AS 'FT%', 
ROUND(SUM(s.FreeThrowAttempts*S.GamesPlayed)/SUM(S.GamesPlayed),2) AS 'FTA',
ROUND(SUM(s.OffensiveRebounds*s.GamesPlayed)/SUM(S.GamesPlayed),1) as 'OReb',
ROUND(SUM(S.DefensiveRebounds*s.GamesPlayed)/SUM(S.GamesPlayed),1) as 'DReb',
ROUND(SUM(S.TotalRebounds*s.GamesPlayed)/SUM(S.GamesPlayed),1) as 'TotReb',
ROUND(SUM(S.Assists*s.GamesPlayed)/SUM(S.GamesPlayed),1) as 'Asst',
ROUND(SUM(S.Steals*s.GamesPlayed)/SUM(S.GamesPlayed),1) as 'Stl',
ROUND(SUM(S.Blocks*s.GamesPlayed)/SUM(S.GamesPlayed),1) as 'Blk',
ROUND(SUM(S.Turnovers*s.GamesPlayed)/SUM(S.GamesPlayed),1) as 'TO',
ROUND(SUM(S.PointsPerGame*s.GamesPlayed)/SUM(S.GamesPlayed),1) as 'PPG'
FROM PlayerStats s JOIN Players P ON s.PlayerID = p.PlayerID
GROUP BY CONCAT(p.LastName, ', ', P.FirstName)
HAVING SUM(s.GamesPlayed) >= 10
ORDER BY PPG DESC;

/* 3- Update a column based on a condition that needs to be met using the where clause.*/

-- Some of the players from foreign countries had NULL values for the school due to lack of information.
-- In order to change this we used the where clause to find them and update by replacing the NULL values with N/A for not available
UPDATE Players
SET School = 'N/A'
WHERE School IS NULL;

SELECT PlayerID, FirstName, LastName, School, Country FROM Players WHERE School = 'N/A';

/* 4- Retrieve data with a query directly into a variable. The variables must be initially declared. The final query must return
the minimum and maximum valuesthrough the variables previously declared. 
Find out more information in Chapter 6 of the book and assignments related to it. */

-- Effective Field Goal percentage is a newer metric in the NBA.  I wanted to find the league's best and worst in this stat,
-- but only for players who played MORE than the NBA average amount of games played. 
DECLARE @MaxEFG FLOAT, @MinEFG FLOAT, @AvgGP FLOAT;
SELECT @AvgGP = AVG(GamesPlayed) FROM PlayerStats;
SELECT @MaxEFG = MAX(EffectiveFieldGoalPercentage) *100,
@MinEFG = MIN(EffectiveFieldGoalPercentage) * 100 FROM PlayerStats
WHERE GamesPlayed > @AvgGP;
SELECT @MaxEFG AS 'League Best Effective FG %', @MinEFG AS 'League Worst Effective FG %';

-- SEE BOTTOM 'EXTRA QUERIES' section for use a DECLARE to create a variable in a WHILE loop

/* 5- You must create a procedure that returns full details of one of the tables of your choosing based on a given condition using the WHERE clause.
Check chapter 17 and Video uploaded in Blackboard.
Example:
Create procedure procedure_name
AS
SELECT Columns FROM table name WHERE condition 
EXEC procedure_name
*/

--The procedure I am creating below is to show the NBA Playoff eligible teams in the Eastern Conference this year
CREATE PROCEDURE Playoff_Eligible_East_Teams
AS
SELECT TOP 10
t.TeamID,
t.TeamName,
t.Wins,
t.Loses,
t.WinPCT,
d.DivisionName,
t.DivisionWins,
t.ConferenceWins
FROM dbo.Teams t
JOIN dbo.Divisions d
ON t.DivisionID = d.DivisionID
WHERE d.Conference = 'EAST'
ORDER BY t.WinPCT DESC;

--The query below will execute the stored procedure above
EXEC Playoff_Eligible_East_Teams;

--The query below will display the definition of the stored procedure above
EXEC sp_helptext Playoff_Eligible_East_Teams;

/* The Final Project grade is divided in the following way:
1-Sql file along with comments in order to complete the previous taks. (70% of the grade)
2-Presentation. Each team's presentation should not last more/less than 10 minutes. (20% of the grade)
3-Q&A section (10% of the grade). Each student should elaborate at least one question to other team's presentation. */

-- This was the view we created just for fun.
IF object_id('V_dbo_Full_Player_Stats','v') is not null
DROP view V_dbo_Full_Player_Stats;
GO
CREATE VIEW V_dbo_Full_Player_Stats
AS
select CONCAT(p.LastName, ', ', P.FirstName) AS FullName, 
CONCAT(P.FirstName, ' ', P.LastName) AS NormalName,
S.Age,
SUM(s.GamesPlayed) as GP,
ROUND(SUM(s.MinutesPlayed*s.GamesPlayed)/SUM(s.GamesPlayed),1) as MP, 
CASE
	WHEN SUM(S.FieldGoalAttempted)= 0
	THEN NULL
	ELSE ROUND(SUM(S.FieldGoalMade)/SUM(s.FieldGoalAttempted)*100,2)
END as 'FG%',
ROUND(SUM(S.FieldGoalAttempted*S.GamesPlayed)/SUM(S.GamesPlayed),1) as FGA,
CASE
	WHEN SUM(S.ThreePointAttempts)= 0
	THEN NULL
	ELSE ROUND(SUM(S.ThreePointMade)/SUM(s.ThreePointAttempts)*100,2)
END as '3P%',
ROUND(SUM(s.ThreePointAttempts*S.GamesPlayed)/SUM(S.GamesPlayed),2) AS '3PA',
CASE
	WHEN SUM(S.TwoPointAttempts)= 0
	THEN NULL
	ELSE ROUND(SUM(S.TwoPointMade)/SUM(s.TwoPointAttempts)*100,2) 
END AS '2P%',
CASE
	WHEN SUM(S.FieldGoalAttempted)= 0
	THEN NULL
	ELSE ROUND(SUM(S.FieldGoalMade+.5*s.ThreePointMade)/SUM(s.FieldGoalAttempted)*100,2) 
END AS 'EFG%', 
CASE
	WHEN SUM(s.FreeThrowAttempts)= 0
	THEN NULL
	ELSE ROUND(SUM(S.FreeThrowMade)/SUM(s.FreeThrowAttempts)*100,2)
END AS 'FT%', 
ROUND(SUM(s.FreeThrowAttempts*S.GamesPlayed)/SUM(S.GamesPlayed),2) AS 'FTA',
ROUND(SUM(s.OffensiveRebounds*s.GamesPlayed)/SUM(S.GamesPlayed),1) as 'OReb',
ROUND(SUM(S.DefensiveRebounds*s.GamesPlayed)/SUM(S.GamesPlayed),1) as 'DReb',
ROUND(SUM(S.TotalRebounds*s.GamesPlayed)/SUM(S.GamesPlayed),1) as 'TotReb',
ROUND(SUM(S.Assists*s.GamesPlayed)/SUM(S.GamesPlayed),1) as 'Asst',
ROUND(SUM(S.Steals*s.GamesPlayed)/SUM(S.GamesPlayed),1) as 'Stl',
ROUND(SUM(S.Blocks*s.GamesPlayed)/SUM(S.GamesPlayed),1) as 'Blk',
ROUND(SUM(S.Turnovers*s.GamesPlayed)/SUM(S.GamesPlayed),1) as 'TO',
ROUND(SUM(S.PointsPerGame*s.GamesPlayed)/SUM(S.GamesPlayed),1) as 'PPG'
FROM PlayerStats s JOIN Players P ON s.PlayerID = p.PlayerID
GROUP BY CONCAT(p.LastName, ', ', P.FirstName), Age, CONCAT(P.FirstName, ' ', P.LastName);


-- EXTRA QUERIES SECTION
-- this queries were done by Michael Seman to take advantage of the view he created.

-- simple player comparison
SELECT FullName, Age, GP, MP, [FG%], [3P%], [2P%], [EFG%], [FT%],  PPG  FROM V_dbo_Full_Player_Stats WHERE NormalName = ('Jimmy Butler') or NormalName = 'Demar DeRozan'

-- I want to start examining the best Three point shooters...

-- so let's pull the best 3pt shooters in order, averaging over 2 shots per game
SELECT * FROM V_dbo_Full_Player_Stats WHERE [3PA] > 2 ORDER BY [3P%] DESC 

-- From the result, we need to add in a games played minimum of 10, lets just sort my EFG for fun
SELECT * FROM V_dbo_Full_Player_Stats WHERE [3PA] > 2 AND GP > 10 ORDER BY [EFG%] DESC 

--Now lets rank 3 pt shooters and partition it by age, and make the game minimum half the season (41 games out of 82)
SELECT  *, RANK() OVER(PARTITION BY AGE ORDER BY [3P%] DESC) AS '3ptRanking' FROM V_dbo_Full_Player_Stats WHERE [3PA] >2 AND GP > 41

-- I want to get the top 5 three point shooters per age group with the above restrictions
-- In order to do this, I'm using a while loop
DECLARE @Counter INT, @CounterEnd INT
Select @Counter = min(age), @CounterEnd = MAX(Age) FROM V_dbo_Full_Player_Stats WHERE [3PA] >2 AND GP > 41;
WHILE @Counter <= @CounterEnd
	BEGIN
		SELECT  *, RANK() OVER(ORDER BY [3P%] DESC) AS '3ptRanking' FROM V_dbo_Full_Player_Stats WHERE [3PA] >2 AND GP > 41 AND AGE=@Counter ORDER BY AGE OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY
		SET @Counter += 1
	END

-- this is the same loop but if I wanted to store that info in a new table
DECLARE @Counter INT, @CounterEnd INT, @MinAge INT
Select @Counter = min(age), @CounterEnd = MAX(Age), @MinAge = min(age) FROM V_dbo_Full_Player_Stats WHERE [3PA] >2 AND GP > 41;
WHILE @Counter <= @CounterEnd
	BEGIN
		IF @counter =  @MinAge
			SELECT  *, RANK() OVER(ORDER BY [3P%] DESC) AS '3ptRankingByAge' INTO ThreePointAgeRank FROM V_dbo_Full_Player_Stats WHERE [3PA] >2 AND GP > 41 AND AGE=@Counter ORDER BY AGE OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY
		ELSE
			INSERT INTO ThreePointAgeRank ([FullName],[NormalName],[Age],[GP],[MP],[FG%],[FGA],[3P%],[3PA],[2P%],[EFG%],[FT%],[FTA],[OReb],[DReb],[TotReb],[Asst],[Stl],[Blk],[TO],[PPG],[3ptRankingByAge])
			SELECT  *, RANK() OVER(ORDER BY [3P%] DESC) AS '3ptRankingByAge' FROM V_dbo_Full_Player_Stats 
			WHERE [3PA] >2 AND GP > 41 AND AGE=@Counter ORDER BY AGE OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY
		SET @Counter += 1
	END

SELECT * FROM ThreePointAgeRank
DROP TABLE ThreePointAgeRank


-- Data sources
--https://www.kaggle.com/datasets/vivovinco/nba-player-stats
--https://www.nba.com/players
--https://www.espn.com/nba/standings