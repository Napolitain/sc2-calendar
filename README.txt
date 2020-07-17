To run locally

1)
docker run --name sc2calendar-redis -p 6379:6379 -d redis
OU
docker run -d redis

2)
functions-framework --target main

To run on google cloud functions

1)
Commit
Push

2)
Deploy