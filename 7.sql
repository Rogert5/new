--SELECT title AND rating = (SELECT rating ORDER BY DESC) FROM movies
--WHERE year = 2010 AND movies ....................MY gguess not completed due to not understanding how to seperate
                    --  same ratings into alphabetical order

SELECT title, rating FROM movies
JOIN ratings ON movies.id = ratings.movie_id
WHERE year = 2010
ORDER BY rating DESC,title ASC;