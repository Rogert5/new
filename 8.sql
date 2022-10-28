-- SELECT name FROM people WHERE title = (SELECT id FROM movies WHERE name = 'Toy Story'); .........MY INITIAL GUESS

SELECT name FROM people
JOIN stars ON stars.person_id = people.id
JOIN movies ON movies.id = stars.movie_id
WHERE movies.title = 'Toy Story';