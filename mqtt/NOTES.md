
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
