
## Overview

The **Demo Router** does the following:

- Runs a `FreeRADIUS` server for enterprise network authentication
- Creates the following access points:
    - `demo-wifi` (WPA2-Personal)
    - `demo-wifi2` (WPA2-Enterprise)

## Preparation

Copy the `client.cert`, `client.key`, `ca.pem` to the `sys` folder on the **Duet Board**'s SD card.

## Demo

Connect your **Duet Board** to your **Host PC** via USB. Open the serial port to the **Duet Board**  and send the Gcode below.

### Configuring

#### WPA2-Personal
```
M587 S"demo-wifi" P"demo-pswd"
```

#### WPA2-Enterprise

EAP-TLS
```
M587 X1 S"demo-wifi2" U"client.crt" P"client.key" A"demo-anon"
```

EAP-PEAP-MSCHAPv2

```
M587 X2 S"demo-wifi2" U"demo-user" P"demo-pswd"
```

EAP-TTLS-MSCHAPv2

```
M587 X3 S"demo-wifi2" U"demo-user" P"demo-pswd"
```

Notes:

- The CA certificate can be specified using the `C` parameter.


### Connecting

#### WPA2-Personal
```
M552 S1 P"demo-wifi"
```

#### WPA2-Enterprise
```
M552 S1 P"demo-wifi2"
```