# pywasn : A Wireless Acoustic Sensor Network client for Python

## Introduction

Wireless Acoustic Sensor Networks (WASNs) consist of multiple devices which contain one or more microphones and are connected using a wireless medium such as WiFi.
Such devices may be notebooks, cell phones, voice assistants, hearing aids, etc. 

The goal of transmitting acoustic information over a network is to create network-connected microphone arrays, which allows for tasks such as source localization and beamforming to be performed. 

The goal of this project is to provide a simple way for devices to share their microphone recordings over wireless networks. This is achieved using the Message Queue Telemetry Transport (MQTT) protocol, an established protocol for Internet-of-Things (IoT) applications. An important agent in MQTT is the message broker, a server which is responsible for transferring messages between devices. In WASN terminology, the message broker may be viewed as a fusion centre, although a distributed architecture is possible by instantiating one message broker in each connected device.

A second key concept in the MQTT protocol is the publisher-subscriber paradigm. In MQTT, a message is not sent to a receiver directly. Instead, the *publisher* sends the message to the broker along with a "topic name". In turn, interested devices must *subscribe* to the aforementioned topic. Finally, the broker will take care of automatically relaying the messages to the interested parties.


## Installation
1. Install the [Mosquitto](https://mosquitto.org/) MQTT message broker.
2. Install the [paho](https://www.eclipse.org/paho/clients/python/) MQTT client for Python using `pip install paho-mqtt`
3. Clone this repository 

## Usage
1. Start a mosquitto server on one or more devices: On Windows, open Powershell as admin and execute `net start mosquitto` 
2. Start the pywasn client
