--SELECT title FROM movies
--WHERE title BEGIN "%Harry Potter%"; ... MY GUESS on how to List titles and release years of all HP movies in Chronological order

SELECT year, title
FROM movies
WHERE title LIKE '%Harry Potter%'
ORDER BY year ASC;