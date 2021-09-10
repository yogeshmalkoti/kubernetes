#test the run
docker run --mount type=bind,source="$(pwd)"/assets,target=/app/assets day2-api:v1.0 -d assets -e prod

#build and tag
docker build -t ymalkoti/day2-api:v1.0 .
#push to repo
docker push ymalkoti/day2-api:v1.0