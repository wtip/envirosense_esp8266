# EnviroSense ESP8266 - Environmental sensing WiFi IoT board
This current iteration is using a [NodeMCU](https://en.wikipedia.org/wiki/NodeMCU) ESP8266 board with a HC-SR501 PIR motion sensor and Bosch BME280, humidity, barometric pressure and ambient temperature sensor.
I'm using micropython to export the metrics for a [Prometheus](http://prometheus.io/) server to scrape.
Metrics are then graphed using a [Grafana](https://grafana.com/) dashboard
