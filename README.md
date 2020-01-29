# envirosense_esp8266 - Enviromental sensing IoT board
This current iteration is using a NodeMCU ESP8266 board with a HC-SR501 PIR motion sensor and Bosch BME280, humidity, barometric pressure and ambient temperature sensor.
I'm using micropython to export the metrics for a [Prometheus](http://prometheus.io/) server to scrape.
Metrics are then graphed using a [Grafana](https://grafana.com/) dashboard
