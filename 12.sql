SELECT title FROM movies
JOIN stars ON stars.movie_id = movies.id
JOIN people ON people.id = stars.person_id
WHERE people.name = "Johnny Depp"
AND title IN
(SELECT title FROM movies
JOIN stars ON stars.movie_id = movies.id
JOIN people ON people.id = stars.person_id
WHERE people.name = "Helena Bonham Carter");

-- list all movies in wich both Johnny Depp and Helena Bonham Carter starred

--Line 6 intersects both names that match title for both persons