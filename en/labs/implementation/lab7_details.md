# Lab 7 — Observability & Optimization

> **Main Lab Guide:** [Lab 7: Operations & Observability](../lab7.md)
> **ISO Domains:** OMD (Operations & Management), UD (User Domain)
> **GreenField Context:** Building James's Health Dashboard - knowing which nodes need battery replacement

## Objectives
- Collect metrics (latency, loss, notification throughput).
- Implement caching and rate limiting in dashboard.
- (Optional) Streaming (WebSocket/SSE) for push updates.
- Add simple access token (hardcoded or .env).

## Context
This implementation guide provides step-by-step technical instructions for metrics collection and dashboard optimization. It complements the [main lab guide](../lab7.md) which covers telemetry vs. business data and the cost of observability.

## Project Setup

### 1. Continue with the Lab 3 Project

This lab continues developing the project started in Lab 3. Make sure you have the `lab03` project (or equivalent) open in VS Code.

### 2. Add Base CoAP Code + Sensor + Observability Features

**CoAP + sensor base same as Lab 5**, then add caching, rate limiting, and metrics.

**Add caching and rate limiting structures** in `main/coap_demo.c`:
```c
#include <time.h>

// Sensor data cache (5s TTL)
typedef struct {
    sensor_data_t data;
    time_t timestamp;
} sensor_cache_t;

static sensor_cache_t sensor_cache = {0};

// Simple rate limiting (per IP, 1 req/s)
#define MAX_CLIENTS 10
typedef struct {
    struct in6_addr ip;
    time_t last_request;
    int request_count;
} client_rate_limit_t;

static client_rate_limit_t rate_limits[MAX_CLIENTS] = {0};
```

**Rate limiting function**:
```c
static bool check_rate_limit(const struct in6_addr *client_ip) {
    time_t now = time(NULL);

    for (int i = 0; i < MAX_CLIENTS; i++) {
        if (memcmp(&rate_limits[i].ip, client_ip, sizeof(struct in6_addr)) == 0) {
            if (now - rate_limits[i].last_request < 1) { // 1s limit
                rate_limits[i].request_count++;
                if (rate_limits[i].request_count > 5) { // burst limit
                    return false;
                }
            } else {
                rate_limits[i].request_count = 1;
            }
            rate_limits[i].last_request = now;
            return true;
        }
    }

    // New client
    for (int i = 0; i < MAX_CLIENTS; i++) {
        if (rate_limits[i].last_request == 0) {
            memcpy(&rate_limits[i].ip, client_ip, sizeof(struct in6_addr));
            rate_limits[i].last_request = now;
            rate_limits[i].request_count = 1;
            return true;
        }
    }
    return false; // Too many clients
}
```

**Modify handlers for caching and rate limiting** (example in handle_sensor):
```c
static void handle_sensor(coap_context_t *ctx, coap_resource_t *resource,
                          coap_session_t *session, coap_pdu_t *request,
                          coap_binary_t *token, coap_string_t *query,
                          coap_pdu_t *response)
{
    char payload[128];
    size_t len;
    time_t now = time(NULL);
    coap_address_t *client_addr = coap_session_get_addr_remote(session);

    if (request->code != COAP_REQUEST_GET) {
        response->code = COAP_RESPONSE_CODE_METHOD_NOT_ALLOWED;
        return;
    }

    // Rate limiting
    if (!check_rate_limit(&client_addr->addr.sin6.sin6_addr)) {
        response->code = COAP_RESPONSE_CODE_TOO_MANY_REQUESTS;
        ESP_LOGW(TAG, "Rate limit exceeded for client");
        return;
    }

    // Caching (5s TTL)
    if (now - sensor_cache.timestamp > 5) {
        read_sensor_mock(&sensor_cache.data);
        sensor_cache.timestamp = now;
        ESP_LOGI(TAG, "Sensor cache updated");
    } else {
        ESP_LOGI(TAG, "Sensor cache hit");
    }

    len = snprintf(payload, sizeof(payload),
                   "{\"temp\":%.1f,\"hum\":%.1f,\"ts\":%u,\"seq\":%u}",
                   sensor_cache.data.temperature,
                   sensor_cache.data.humidity,
                   sensor_cache.data.timestamp,
                   sensor_cache.data.sequence);

    response->code = COAP_RESPONSE_CODE_CONTENT;
    coap_add_data_blocked_response(resource, session, request, response,
                                   token, COAP_MEDIATYPE_APPLICATION_JSON, 0,
                                   len, (const uint8_t *)payload);
}
```

**Add `/metrics` endpoint** for basic metrics:
```c
static void handle_metrics(coap_context_t *ctx, coap_resource_t *resource,
                           coap_session_t *session, coap_pdu_t *request,
                           coap_binary_t *token, coap_string_t *query,
                           coap_pdu_t *response)
{
    char payload[256];
    size_t len;

    if (request->code != COAP_REQUEST_GET) {
        response->code = COAP_RESPONSE_CODE_METHOD_NOT_ALLOWED;
        return;
    }

    // Simple metrics (extend as needed)
    len = snprintf(payload, sizeof(payload),
                   "{\"uptime\":%u,\"heap_free\":%u,\"light_state\":%d}",
                   esp_log_timestamp() / 1000, esp_get_free_heap_size(), light_on);

    response->code = COAP_RESPONSE_CODE_CONTENT;
    coap_add_data_blocked_response(resource, session, request, response,
                                   token, COAP_MEDIATYPE_APPLICATION_JSON, 0,
                                   len, (const uint8_t *)payload);
}

// Register in coap_server_task
coap_resource_t *metrics_resource = coap_resource_init(coap_make_str_const("metrics"), 0);
coap_register_handler(metrics_resource, COAP_REQUEST_GET, handle_metrics);
coap_add_resource(ctx, metrics_resource);
```

### 3. Configure Settings

**Use same `sdkconfig` as Lab 5**, no additional changes.

**Build and flash:**
```bash
idf.py set-target esp32c6
idf.py build
idf.py flash
idf.py monitor
```

### 4. Optional Streaming with WebSocket/SSE

**Add WebSocket to dashboard** (optional):

**Modify `dashboard.py`:**
```python
from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
import subprocess
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# ... previous code ...

@socketio.on('connect')
def handle_connect():
    emit('sensor_update', get_sensor_data())

def stream_sensor_data():
    while True:
        data = get_sensor_data()
        socketio.emit('sensor_update', data)
        socketio.sleep(5)

socketio.start_background_task(stream_sensor_data)

@app.route('/')
def dashboard():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>IoT Lab Dashboard</title>
        <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
    </head>
    <body>
        <h1>IoT Sensor Dashboard</h1>
        <div id="sensor-data">Loading...</div>
        <h2>Light Control</h2>
        <button onclick="controlLight(1)">Turn On</button>
        <button onclick="controlLight(0)">Turn Off</button>

        <script>
        const socket = io();
        socket.on('sensor_update', function(data) {
            document.getElementById('sensor-data').innerHTML = data;
        });

        function controlLight(state) {
            fetch('/control_light', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({state: state})
            });
        }
        </script>
    </body>
    </html>
    ''')

# ... rest of code ...
```

**Add authentication with simple token:**

**Modify dashboard to include token:**
```python
@app.route('/')
def dashboard():
    # Include token in requests
    return render_template_string('''
    ...
    <script>
    const TOKEN = 'iotlab2024'; // In production use environment variable

    function getSensorData() {
        return fetch('/api/sensor', {
            headers: {'Authorization': 'Bearer ' + TOKEN}
        }).then(r => r.json());
    }
    ...
    </script>
    ''')
```

### 5. Measure Performance Metrics

**Script for automatic measurements:**
```python
import time
import subprocess
import statistics

def measure_latency(host, endpoint, num_requests=10):
    latencies = []
    for i in range(num_requests):
        start = time.time()
        result = subprocess.run([
            "python", "tools/coap_client.py",
            "--host", host, "get", endpoint
        ], capture_output=True)
        end = time.time()
        if result.returncode == 0:
            latencies.append((end - start) * 1000)  # ms

    return {
        'avg_latency': statistics.mean(latencies),
        'min_latency': min(latencies),
        'max_latency': max(latencies),
        'success_rate': len(latencies) / num_requests
    }

# Measure sensor latency with/without cache
print("Without cache:", measure_latency(NODE_IP, "/sensor"))
# Force without cache by changing parameter or restarting
print("With cache:", measure_latency(NODE_IP, "/sensor"))
```

## Deliverables
- Collected metrics (latency, loss, notification throughput)
- Functional `/metrics` endpoint with uptime, heap, light state
- Caching implementation (5s TTL) and rate limiting (1 req/s per IP)
- Optimization logs (cache hits/misses, rate limit violations)
- Simple token authentication (hardcoded for demo)
- (Optional) Streaming with WebSocket/SSE showing push updates
