# pulse_api


DJango REST API and Mysql based REST API boilerplate

API is consistant with http://jsonapi.org/

Its on Docker

To get started 

1: Clone Repo

2: Run "docker-compose build" from root dir

3: Run "docker-compose up" from root dir 
   When you run first time it creates db and teakes time, if you see any errors termitate it with CTRL-C 
   and restart it with docker-compose up
   
4: Djano server will start on port 3200


To test API:

``` javascript 

curl -i -X POST -H "Content-Type: application/json" -d '
{
    "data": {
        "type": "pulse",
        "attributes": {
            "name": "anish pulse", 
            "maximum_rabi_rate": 100.32,
            "polar_angle": 0.1,
            "pulse_type": "cinbb"
        }
    }
}  
' http://127.0.0.1:3200/pulses/

```

  
