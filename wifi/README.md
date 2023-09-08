
## Overview

## Setup

The demo router does the following:

- Runs a `FreeRADIUS` server for enterprise network authentication
- Creates the following access points:
    - `demo-wifi` (WPA2-Personal)
    - `demo-wifi2` (WPA2-Enterprise)
    - `demo-wifi3` (WPA3-Enterprise)

## Preparation

Copy the `client.pem`, `client.cert`, and `client.key` to the `sys` folder on your board's SD card.

## Demo

### Configuring

#### Personal
```
M587 S"demo-wifi" P"demo-pswd"
```

#### Enterprise

EAP-TLS
```
M587 X1 S"demo-wifi2" U"client.crt" P"client.key"
M587 X1 S"demo-wifi3" U"client.crt" P"client.key"
```

EAP-PEAP-MSCHAPv2

```
M587 X2 S"demo-wifi2" U"demo-user" P"demo-pswd"
M587 X2 S"demo-wifi3" U"demo-user" P"demo-pswd"
```

EAP-TTLS-MSCHAPv2

```
M587 X3 S"demo-wifi2" U"demo-user" P"demo-pswd"
M587 X3 S"demo-wifi3" U"demo-user" P"demo-pswd"
```

### Connecting

#### WPA2-Personal
```
M552 S1 P"demo-wifi"
```

#### WPA2-Enterprise
```
M552 S1 P"demo-wifi2"
```
#### WPA3-Enterprise

```
M552 S1 P"demo-wifi3"
```