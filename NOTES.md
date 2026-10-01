# What I checked, and what the agent got wrong

Write this yourself, in your own words. It is the part of the repo that proves the work is yours.

## What the agent got wrong
The agent deleted three helper functions (is_due, parse_service_date, chunk_list) that I never asked it to remove. It also treats a car with no service reading as 0% worn, which lowers the average. I noticed this when I read its summary of changes.

## What I checked before I accepted its work
I ran the tests, and all of them passed. I ran verify.py, which showed the wear is now about 99.3% for a car at 14,900 km. I also checked that the 15000 km interval and the 80% threshold are the same as before, in both the code and settings.cfg.

## What the data actually said
Cars broke down more when they had gone far since their last service, drove many km per day, and carried heavy loads. Age and total mileage made no difference, even though they look like obvious causes.
