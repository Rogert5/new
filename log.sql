-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT id,street,description FROM crime_scene_reports WHERE id = 295;
-- ... this narrowed it down to 5 id selections from reports

SELECT id , name, transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE "%bakery%";
-- info to try to get only Locations and types of transactions

SELECT people.name, atm_transactions.transaction_type FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.year = 2021
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_location = "Leggett Street"
AND atm_transactions.transaction_type = "withdraw";
--Used to find account numbers now i can search TABLE bank_accounts to find account_number(s) , person_id(s) to help pin point suspects

SELECT bakery_security_logs.activity , bakery_security_logs.license_plate , people.name  FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.year = 2021
AND bakery_security_logs.month = 7
AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute >= 15
AND bakery_security_logs.minute <= 25;
--Able to find out suspect who left within the next ten minutes of the robbery at 10:15 am

UPDATE phone_calls
SET caller_name = people.name
FROM people
WHERE phone_calls.caller = people.phone_number;

UPDATE phone_calls
SET receiver_name = people.name
FROM people
WHERE phone_calls.receiver = people.phone_number;

SELECT caller,caller_name, receiver_name, receiver, duration FROM phone_calls
WHERE year = 2021
AND month = 7
AND day = 28
AND duration < 60;
--USed to find a call under 60 sec and UPDATED AND SET receiver_name and Caller_name to table (deleted now for no confusion in program)

--.......deleted.......
--UPDATE flights
--SET origin_airport_id = airports.city
--FROM airports
--WHERE flights.origin_airport_id = airports.id

--UPDATE flights
--SET destination_airport_id = airports.city
--FROM aiports
--WHERE flights.destination_airport_id = airports.id;


UPDATE flights
SET origin_airport_id = airports.city
FROM airports
WHERE flights.origin_airport_id = airports.id;

UPDATE flights
SET destination_airport_id = airports.city
FROM airports
WHERE flights.destination_airport_id = airports.id;

SELECT id, hour, minute, origin_airport_id, destination_airport_id
FROM flights
WHERE year = 2021
AND month = 7
AND day = 29
ORDER BY hour ASC
LIMIT 1;
--USed to find the earliest flight the next day with origib city and its destination city

SELECT flights.destination_airport_id, name, phone_number,license_plate FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON flights.id = passengers.flight_id
WHERE flights.id = 36
ORDER BY flights.hour ASC;
--Used to identify passengers and familiar names that took flights out of city


SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON flights.id = passengers.flight_id
WHERE (flights.year = 2021 AND flights.month = 7 AND flights.day = 29 AND flights.id = 36)
AND NAME IN
(SELECT phone_calls.caller_name FROM phone_calls
WHERE year = 2021
AND month = 7
AND day = 28
AND duration < 60)
AND NAME IN
(SELECT people.name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.year = 2021
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_location = "Leggett Street"
AND atm_transactions.transaction_type = "withdraw")
AND NAME IN
(SELECT people.name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.year = 2021
AND bakery_security_logs.month = 7
AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute >= 15
AND bakery_security_logs.minute <= 25);
--COMBINING ALL LOGS I WROTE IN TO FIND BRUCE THE THIEF