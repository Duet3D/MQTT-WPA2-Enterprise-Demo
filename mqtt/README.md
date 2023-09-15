
# Requirements

- [Python](https://www.python.org/downloads/) - runs the demo script, `echo.py`, which runs broker and `echo` client
    - [Paho](https://www.eclipse.org/paho/index.php?page=clients/python/index.php) - used to implement the `echo` MQTT client

# Overview


The demo has three components: the MQTT broker, the `echo` MQTT client and the RRF MQTT client.
The MQTT broker runs on the **Demo Router**, the `echo` MQTT client on the **Host PC**, and the RRF MQTT client on the **Duet Board**.

The RRF MQTT client publishes message using `M118` under the topic `topic-duet`.
The `echo` MQTT client is subscribed to this topic, which retransmits the message under the topic `topic-echo`. The RRF MQTT client is, in turn, subscribed to `topic-echo`. The RRF MQTT client receives and displays the message under `topic-echo`.

MQTT broker configuration can be found in [mosquitto.conf](mosquitto.conf). This configuration:
- disallows anonymous clients, allowing only clients with authentication credentials to connect
- specifies the password file, [passwords.txt](passwords.txt), whose contents are the allowed client usernames and the corresponding password hashes
- specifies the MQTT broker port, 1883


The clear text contents of the password file [passwords.txt](./passwords.txt) are as follows:

```
mqtt-echo:mqtt-echo-pswd
mqtt-duet:mqtt-duet-pswd
```

Running the command `mosquitto_passwd -U passwords.txt` on the clear text contents will replace the password part (the text after the colon on each row) with its hash.

The first row are the credentials for the `echo` MQTT client; the second are the credentials for the RRF MQTT client.


# Running the Demo

## Demo Router

The MQTT broker is a service on the **Demo Router**; if the **Demo Router** is up, the MQTT broker is also be up.

## Host PC

Open a command line/terminal and `cd` into this directory, then run the command below.

```
python echo.py
```

The following log should be seen:

```
echo: connecting to 'demo-router' on port '1883' as 'echo'...
echo: connect succeeded, subscribing to topic 'topic-duet'...
echo: subscribe to 'topic-duet' succeeded.
echo: subscribing to extra topic 'topic-extra'...
echo: subscribe to 'topic-extra' succeeded.
echo: subscribing to will topic 'topic-will'...
echo: subscribe to 'topic-will' succeeded.
```

## Duet Board

Connect your **Duet Board** to your **Host PC** via USB. Open the serial port to the **Duet Board**  and send the Gcode below.

### Enable debugging messages (optional)

```
M111 P2 S1
```

### Configure the MQTT client

#### Client ID
```
; Set client id as 'duet'
M586.4 C"duet"
```
#### Credentials
```
; Set username and password for authenticating with MQTT broker
M586.4 U"mqtt-duet" K"mqtt-duet-pswd"
```
#### Subscriptions
```
; Subscribe to topic 'topic-echo'
M586.4 S"topic-echo"
```

#### Last Will and Testament
```
; Set last will and testament message and topic
M586.4 W"message-will" T"topic-will"
```

Notes:

- Max QOS=0 for 'topic-echo' subscription since it's not specified. It can be specified using parameter `O`.
- QOS=0, retain=False for last will and testament, since they're not specified. These can be specified using parameters `Q` and `R`, respectively.

### Enable the MQTT protocol

```
; Sets 192.168.111.1 as MQTT broker IP address on default port 1883 since not specified
M586 P4 H192.168.111.1 S1
```

Notes:

- If port is not specified, the standard MQTT broker port 1883 is used. This can be specified using parameter `R`.

### Publish message via M118

```
; Publish message under 'topic-duet', board should recieve the same message under 'topic-echo'.
M118 P6 S"message-echo" T"topic-duet"
```

This message will be recieved and published back by the `echo` client, under topic `topic-echo`.

```
echo: received message with topic 'topic-duet': 'b'message-echo', echoing...
echo: echo succeeded
```

Since the MQTT client on the board is subscribed to this topic, it should receive that message.

```
Received message from topic 'topic-echo': 'message-echo'
```

It's possible to publish on multiple topics. For this demo, the `echo` client also subscribes to `topic-extra`.

```
; Publish message under 'topic-extra', not echoed.
M118 P6 S"message-extra" T"topic-extra"
```

Messages published under 'topic-extra' is recieved by the `echo` client, but not re-published
under 'topic-echo'.

```
echo: recieved message with topic 'topic-extra': b'message-extra'
```

Notes:


- Both messages above are published with QOS=0, retain=False and duplicate=False since they're not specified. These can be specified with parameters `Q`, `R`, and `D`, respectively.

### Disable the MQTT Protocol

This gracefully ends the MQTT session established by `M586 P4 H192.168.111.1 S1`.

```
M586 P4 S0
```

If the MQTT session is not gracefully closed by using `M586 P4 S0`, the will message is sent by the broker to subscribers of the will topic.

For this demo, one way to do this is to disable the network interface **without** issuing a `M586 P4 S0` first. For example, if using WiFi, that would be `M552 S0`.
The following message will be printed by the `echo` client.

```
echo: recieved will message with topic 'topic-will': b'message-will'
```