# calendar_gen
Generates .ics files from syllabi

# build
install dependancies:
- install docker

build and run:
```shell
cd calendar_gen
docker build -t calendar-gen .
docker run -p 5000:5000 --name calendar-gen -t calendar-gen
```