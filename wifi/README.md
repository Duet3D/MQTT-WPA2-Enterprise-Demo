
## Overview

`FreeRADIUS` server in demo router



- `demo-wifi` - WPA2-PSK
- `demo-wifi2` - WPA2-EAP
- `demo-wifi3` - WPA3-EAP

## Setup

Copy the `client.pem`, `client.cert`, and `client.key` to the `sys` folder on your board's SD card.

## Demo

### Configuring

EAP-TLS
```
M587 X1 S"demo-wifi2" U"client.crt" P"client.key"
M587 X1 S"demo-wifi3" U"client.crt" P"client.key"
```

EAP-PEAP-MSCHAPv2

```
M587 X2 S"demo-wifi2" U"eap" P"eap-pswd"
M587 X2 S"demo-wifi3" U"eap" P"eap-pswd"
```

EAP-TTLS-MSCHAPv2

```
M587 X3 S"demo-wifi2" U"eap" P"eap-pswd"
M587 X3 S"demo-wifi3" U"eap" P"eap-pswd"
```

### Connecting

```
M552 S1 P"demo-wifi2"
```
or 

```
M552 S1 P"demo-wifi3"
```