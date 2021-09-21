# sc2-calendar has been discontinued. To find new version, look at [sc2-calendar-2](https://github.com/Napolitain/sc2-calendar-2)

### What is it ?

sc2-calendar is a web scrapper / iCalendar server which uses https://liquipedia.net/starcraft2/Liquipedia:Upcoming_and_ongoing_matches as a source and Flask as a iCalendar server.

The end result is a customizable link which permits to subscribe to arbitrary number of players and teams, pro or not as long as it figures on Liquipedia webpage.

![image](https://user-images.githubusercontent.com/18146363/134248454-f5817f99-e780-431f-b56d-20a8c4d3dbfd.png)

Once the link added in a Calendar App, events are auto generated and look like this.

<img width="766" src="https://user-images.githubusercontent.com/18146363/134247169-57a25f93-66bd-47fd-906e-38641afe084d.png">


### To run locally

```
1)
docker run --name sc2calendar-redis -p 6379:6379 -d redis
OR
docker start -d redis

2)
...
```


### To run on production
```
1)
Commit
Push

2)
Hook / pull

3)
Run
```

### Ressources
https://www.e-tinkers.com/2018/08/how-to-properly-host-flask-application-with-nginx-and-guincorn/
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
