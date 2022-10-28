-- SELECT total FROM movies WHERE rating = 10; ...... THIS was my first guess to how to determine number of movies with rating of 10

SELECT COUNT(rating) FROM ratings
WHERE rating = 10;