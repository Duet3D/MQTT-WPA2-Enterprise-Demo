
# Requirements

- [Python](https://www.python.org/downloads/) - runs the demo script, `echo.py`, which runs broker and `echo` client; additional pip dependencies:
    - [Paho](https://www.eclipse.org/paho/index.php?page=clients/python/index.php) - used to implement the `echo` MQTT client
    - [Colorama](https://pypi.org/project/colorama/) - used to colorize log output of `echo.py`

- [Mosquitto](https://mosquitto.org/download/) - MQTT broker used in the demo

# Overview

## Setup

The demo has three components: the MQTT broker, the `echo` MQTT client and the RRF MQTT client.

The RRF MQTT client publishes message sent via `M118` under a topic `topic-duet`.
The `echo` MQTT client is subscribed to this topic, which retransmits the message under the topic `topic-echo`. Since the RRF MQTT client in turn is subscribed to this topic, it receives and displays the retransmitted message.

### Broker

Broker configuration can be found in [mosquitto.conf](./mosquitto.conf). This configuration:
- disallows anonymous clients, allowing only clients with authentication credentials to connect
- specifies the password file, [passwords.txt](./passwords.txt), whose contents are the allowed client usernames and the corresponding password hashes
- runs the MQTT broker on a different port, 1884 instead of the typical 1883

#### Password File

The clear text contents of the password file [passwords.txt](./passwords.txt) are as follows:

```
mqtt-echo:mqtt-echo-pswd
mqtt-duet:mqtt-duet-pswd
```

Running the command `mosquitto_passwd -U passwords.txt` on the clear text contents will replace the password part (the text after the colon on each row) with its hash.

The first row are the credentials for the `echo` client; the second are the credentials for the RRF MQTT client.


# Running the Demo

## Host

Open a command line/terminal and `cd` into this directory, then run the command below.

```
python echo.py
```

Running the [GCode commands on RepRapFirmware](#reprapfirmware), a log similar to the following one should be seen.

```
echo: connecting to 'demo-router' on port '1883' as 'echo'...
echo: connect succeeded, subscribing to topic 'topic-duet'...
echo: subscribe to 'topic-duet' succeeded, waiting for messages...
echo: subscribing to will topic 'topic-will'...
echo: subscribe to 'topic-will' succeeded, waiting for messages...
echo: received message with topic 'topic-duet': 'b'duet-message'', echoing...
echo: echo succeeded
```

## Board


### Enable debugging messages (optional)

```
M111 P2 S1
```

### Configure the MQTT client

```
; Set client id as "duet"
M586.4 C"duet"
; Set credentials for authenticating with MQTT broker
M586.4 U"mqtt-duet" K"mqtt-duet-pswd"
; Messages will be published under topic: "topic-duet";
; QOS=0, do not retain and not duplicate
M586.4 P"topic-duet" Q0 D0 R0
; Subscribe to topic: "topic-echo"
M586.4 S"topic-echo" Q0
; Set last will and testament message and topic
M586.4 W"duet has disconnected" T"topic-will"
```

### Enable the MQTT protocol

```
; Sets 192.168.111.1 as MQTT broker IP, default port 1883 is used
; since it's not specified
M586 P4 H192.168.111.1 S1
```

### Publish a message via M118

```
M118 P6 S"duet-message"
```

This message will be echoed back by the `echo` client, under topic `topic-echo`.
Since the RRF MQTT client is subscribed to this topic, it should receive that message:

```
Received message from topic 'topic-echo': 'duet-message'
```

### Disable the MQTT Protocol

This gracefully ends the MQTT session established by `M586 P4 H192.168.111.1 S1`.

```
M586 P4 S0
```

#### Last Will and Testament

If the MQTT session is not gracefully closed by using `M586 P4 S0`, the will message is sent by
the broker to subscribers of the will topic.

One way to do this is to disable the network interface without issuing a `M586 P4 S0` first. For example, if using WiFi, that would be `M552 S0`.
This message will be printed by `echo.py`:

```
echo: recieved will message with topic 'topic-will': b'duet has disconnected'
```

# Scenarios


1. MQTT protocol is enabled before `echo.py` can be started. This means the broker is not yet started when the RRF MQTT client attempts to connect.

    - This should be ok, as the MQTT client will attempt reconnection automatically.

2. The running `echo.py` is terminated while RRF MQTT client is connected.

    - This should be ok, as the MQTT client will attempt reconnection automatically.

3. MQTT protocol is configured and enabled before starting the network interface via `M552 S1`.

    - This should be ok, the MQTT client will only attempt connection once the network interface is active.

4. MQTT client is configured while connecting/connected.

    - This is not ok, and should results in an error GCode result. Configuration is
        only possible while the protocol is disabled.

5. Network interface is disabled while MQTT client is active```