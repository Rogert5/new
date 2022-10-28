--SELECT name FROM people WHERE title FROM movie WHERE year is 2004 AND ORDER BY birth

-- SELECT name , birth FROM people
-- JOIN stars ON stars.movie_id = movies.id
-- JOIN movies ON movies.year = stars.movie_id
-- ORDER BY birth ASC; ...............MY INITIAL GUESS

SELECT DISTINCT name FROM people
JOIN stars ON stars.person_id = people.id
JOIN movies ON movies.id = stars.movie_id
WHERE movies.year = 2004
ORDER BY people.birth ASC;



