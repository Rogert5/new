SELECT DISTINCT name FROM people
JOIN directors ON person_id = people.id
JOIN movies ON movies.id = directors.movies.id
JOIN ratings ON ratings.movie_id = movies.id
WHERE rating >= 9.0;