SELECT name FROM songs WHERE artist_id = (SELECT id FROM artists WHERE name = 'Post Malone');
-- (SELECT id..etc) created to look for specific artist within artist ID .. kind of to identify the number to a name