/*
 * Esqueleto de servidor CoAP para Lab 1.
 * Usando libcoap en ESP-IDF
 */

#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <sys/select.h>
#include <errno.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "coap3/coap.h"

static const char *TAG = "coap_demo";

/* Puerto estándar CoAP */
#define COAP_PORT 5683

/* Estado simulado del LED */
static bool light_on = false;
/* Contador para /sensor (mock) */
static uint32_t sensor_counter = 0;

/* TODO: Reemplazar con acceso real a GPIO en Lab 5 (sensores) */

static void handle_light(coap_context_t *ctx, coap_resource_t *resource,
                        coap_session_t *session, coap_pdu_t *request,
                        coap_binary_t *token, coap_string_t *query,
                        coap_pdu_t *response)
{
    unsigned char buf[3];
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

static void handle_sensor(coap_context_t *ctx, coap_resource_t *resource,
                         coap_session_t *session, coap_pdu_t *request,
                         coap_binary_t *token, coap_string_t *query,
                         coap_pdu_t *response)
{
    char payload[32];
    size_t len;

    if (request->code != COAP_REQUEST_GET) {
        response->code = COAP_RESPONSE_CODE_METHOD_NOT_ALLOWED;
        return;
    }

    sensor_counter++;
    len = snprintf(payload, sizeof(payload), "{\"val\":%u}", sensor_counter);
    response->code = COAP_RESPONSE_CODE_CONTENT;
    coap_add_data_blocked_response(resource, session, request, response,
                                   token, COAP_MEDIATYPE_APPLICATION_JSON, 0,
                                   len, (const uint8_t *)payload);
}

static void coap_server_task(void *pvParameters)
{
    coap_context_t *ctx = NULL;
    coap_address_t dst;
    coap_resource_t *light_resource = NULL;
    coap_resource_t *sensor_resource = NULL;
    fd_set readfds;
    struct timeval tv;
    int result;
    coap_log_t log_level = COAP_LOG_WARN;

    coap_set_log_level(log_level);
    coap_set_log_handler(NULL);

    /* Prepare the CoAP server socket */
    coap_address_init(&dst);
    dst.addr.sin6.sin6_family = AF_INET6;
    dst.addr.sin6.sin6_port = htons(COAP_PORT);
    dst.addr.sin6.sin6_addr = in6addr_any;

    ctx = coap_new_context(NULL);
    if (!ctx) {
        ESP_LOGE(TAG, "Failed to create CoAP context");
        return;
    }

    coap_new_endpoint(ctx, &dst, COAP_PROTO_UDP);

    /* Initialize resources */
    light_resource = coap_resource_init(coap_make_str_const("light"), 0);
    if (!light_resource) {
        ESP_LOGE(TAG, "Failed to create light resource");
        goto finish;
    }
    coap_register_handler(light_resource, COAP_REQUEST_GET, handle_light);
    coap_register_handler(light_resource, COAP_REQUEST_PUT, handle_light);
    coap_add_resource(ctx, light_resource);

    sensor_resource = coap_resource_init(coap_make_str_const("sensor"), 0);
    if (!sensor_resource) {
        ESP_LOGE(TAG, "Failed to create sensor resource");
        goto finish;
    }
    coap_register_handler(sensor_resource, COAP_REQUEST_GET, handle_sensor);
    coap_add_resource(ctx, sensor_resource);

    ESP_LOGI(TAG, "CoAP server started on port %d", COAP_PORT);

    while (1) {
        FD_ZERO(&readfds);
        FD_SET(coap_context_get_coap_fd(ctx), &readfds);

        tv.tv_sec = 1;
        tv.tv_usec = 0;

        result = select(FD_SETSIZE, &readfds, 0, 0, &tv);
        if (result > 0) {
            if (FD_ISSET(coap_context_get_coap_fd(ctx), &readfds)) {
                coap_io_process(ctx, COAP_IO_WAIT);
            }
        } else if (result < 0) {
            break;
        }
    }

finish:
    coap_free_context(ctx);
    coap_cleanup();

    vTaskDelete(NULL);
}

void start_coap_server(void)
{
    xTaskCreate(coap_server_task, "coap_server", 4096, NULL, 5, NULL);
}

/* TODO (Lab 1):
 * - Documentar en DDR decisión de formato JSON /sensor.
 * - Añadir confirmable vs non-confirmable.
 * - Mejorar manejo de recursos.
 */