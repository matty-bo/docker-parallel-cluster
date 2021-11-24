# build an image
docker build -t parallel-example .

# run script in docker shell
docker run parallel-example sh ./mean.sh 1 2 3 4 5