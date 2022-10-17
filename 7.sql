 SELECT AVG(energy) ame FROM songs WHERE artist_id = (SELECT id FROM artists WHERE name = 'Drake');
 -- SAMe as 6.sql except here i am looking for average (AVG)