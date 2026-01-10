# Lab 8 — Consolidation & Hardening (Final Integration)

> **Main Lab Guide:** [Lab 8: Capstone Integration](../lab8.md)
> **ISO Domains:** All Six Domains (System View)
> **GreenField Context:** Creating the "Golden Master" v1.0 firmware for pilot deployment
> **Ethics:** Complete your [DDR Section 11](../../3_deliverables_template.md) ethics assessment

## Objectives
- Automated end-to-end tests (script).
- Mini pentest: unauthorized join attempt / invalid CoAP.
- Light stress test (20 request burst).
- Final documentation + demo video.

## Context
This implementation guide provides step-by-step technical instructions for final system integration and testing. It complements the [main lab guide](../lab8.md) which covers Samuel's "Chaos Script" stress test criteria and the final ethics assessment.

## Project Setup

### 1. Continue with the Lab 3 Project

This lab continues developing the project started in Lab 3. Make sure you have the `lab03` project (or equivalent) open in VS Code.

### 2. Add Complete Base Code + Hardening (Token Auth)

**Complete base same as Lab 7**, then add simple authentication with token.

**Add token auth** in `main/coap_demo.c` (after defines):
```c
#define AUTH_TOKEN "iotlab2024"  // Hardcoded token for demo (in production use NVS or similar)

static bool check_auth_token(coap_pdu_t *request) {
    coap_opt_iterator_t opt_iter;
    coap_opt_t *token_option = coap_check_option(request, COAP_OPTION_URI_QUERY, &opt_iter);

    if (!token_option) {
        return false;
    }

    char token_str[32];
    size_t token_len = coap_opt_length(token_option);
    if (token_len >= sizeof(token_str)) {
        return false;
    }

    coap_opt_value(token_option, (uint8_t *)token_str);
    token_str[token_len] = '\0';

    // Check if token=AUTH_TOKEN
    if (strncmp(token_str, "token=", 6) == 0 && strcmp(token_str + 6, AUTH_TOKEN) == 0) {
        return true;
    }

    return false;
}
```

**Modify handlers to require token** (example in handle_light):
```c
static void handle_light(coap_context_t *ctx, coap_resource_t *resource,
                         coap_session_t *session, coap_pdu_t *request,
                         coap_binary_t *token, coap_string_t *query,
                         coap_pdu_t *response)
{
    // Auth check
    if (!check_auth_token(request)) {
        response->code = COAP_RESPONSE_CODE_UNAUTHORIZED;
        ESP_LOGW(TAG, "Unauthorized access to /light");
        return;
    }

    // Rate limiting
    coap_address_t *client_addr = coap_session_get_addr_remote(session);
    if (!check_rate_limit(&client_addr->addr.sin6.sin6_addr)) {
        response->code = COAP_RESPONSE_CODE_TOO_MANY_REQUESTS;
        return;
    }

    // Original logic...
    const char *response_data;
    size_t response_data_len;

    switch (request->code) {
    case COAP_REQUEST_GET:
        response->code = COAP_RESPONSE_CODE_CONTENT;
        response_data = light_on ? "1" : "0";
        response_data_len = strlen(response_data);
        coap_add_data_blocked_response(resource, session, request, response,
                                       token, COAP_MEDIATYPE_TEXT_PLAIN, 0,
                                       response_data_len,
                                       (const uint8_t *)response_data);
        break;
    case COAP_REQUEST_PUT:
        if (request->data && request->data->length == 1 &&
            (request->data->s[0] == '0' || request->data->s[0] == '1')) {
            light_on = (request->data->s[0] == '1');
            response->code = COAP_RESPONSE_CODE_CHANGED;
        } else {
            response->code = COAP_RESPONSE_CODE_BAD_REQUEST;
        }
        break;
    default:
        response->code = COAP_RESPONSE_CODE_METHOD_NOT_ALLOWED;
        break;
    }
}
```

**Apply same check to handle_sensor and handle_metrics**.

### 3. Configure Final Settings

**Use same `sdkconfig` as Lab 7**, add hardening:
```bash
# Security hardening
CONFIG_COMPILER_OPTIMIZATION_LEVEL_DEBUG=n
CONFIG_COMPILER_OPTIMIZATION_LEVEL_RELEASE=y
CONFIG_STACK_CHECK_NONE=n
CONFIG_STACK_CHECK_NORM=y
```

**Build and flash:**
```bash
idf.py set-target esp32c6
idf.py build
idf.py flash
idf.py monitor
```

### 4. Automated End-to-End Test Script

**Use the test suite from `tools/test_e2e.py`** (already included in the repository).

**Run tests:**
```bash
# Basic tests
python tools/test_e2e.py fd11:22:33:0:0:0:0:1

# With Border Router
python tools/test_e2e.py fd11:22:33:0:0:0:0:1 fd11:22:33:0:0:0:0:100
```

### 5. Mini Pentest and Residual Hardening

**Security tests:**
```bash
# Attempt unauthorized join (from device without credentials)
# In Thread CLI of unauthorized device:
dataset set active <incorrect_hex_dataset>
ifconfig up
thread start
# Should fail

# Invalid CoAP requests
python tools/coap_client.py --host [IPv6] get /invalid_endpoint
python tools/coap_client.py --host [IPv6] put /light invalid_payload

# Resource stress test
# Run multiple instances of stress test
for i in {1..5}; do
    python tools/test_e2e.py fd11:22:33:0:0:0:0:1 &
done
```

### 6. Final Documentation and Demo Video

**Documentation structure:**
- General system architecture
- Documented CoAP APIs
- Deployment guide
- Common troubleshooting
- Performance metrics

**Demo video checklist:**
- Thread network formation
- Basic CoAP functionality
- Dashboard in operation
- Border Router and network access
- OTA update
- End-to-end tests
- Security demo (rate limiting, auth)

## Deliverables
- Automated test suite (`tools/test_e2e.py`) with latency and success metrics
- End-to-end test report (success ratio, average latency)
- Stress test logs (20 request burst) and resource usage
- Mini pentest results (unauthorized join attempts, invalid CoAP)
- Complete final documentation of the IoT system
- Demo video showing full functionality and tests
