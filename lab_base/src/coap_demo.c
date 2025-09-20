/*
 * Esqueleto de servidor CoAP para Lab 1.
 * Se compila solo si CONFIG_IOT_LAB_COAP_SERVER=y
 */

#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>
#include <zephyr/net/coap.h>
#include <zephyr/net/socket.h>
#include <zephyr/net/openthread.h>

#if !IS_ENABLED(CONFIG_IOT_LAB_COAP_SERVER)
LOG_MODULE_REGISTER(coap_demo_stub, LOG_LEVEL_INF);
/* Si la opción está deshabilitada no iniciamos el servidor */
int main(void) { return 0; }
#else


LOG_MODULE_REGISTER(coap_demo, LOG_LEVEL_INF);

/* Puerto estándar CoAP */
#define COAP_PORT 5683

/* Bufferes básicos */
static uint8_t request_buf[256];
static uint8_t response_buf[256];

/* Estado simulado del LED */
static bool light_on;
/* Contador para /sensor (mock) */
static uint32_t sensor_counter;

/* TODO: Reemplazar con acceso real a GPIO en Lab 5 (sensores) */

static int build_simple_response(struct coap_packet *response,
                                uint8_t *data, size_t max_len,
                                const struct coap_packet *request,
                                uint8_t code, const uint8_t *payload, size_t payload_len)
{
    int r = coap_packet_init(response, data, max_len, 1, COAP_TYPE_ACK,
                             coap_header_get_token(request),
                             coap_header_get_token_len(request), code,
                             coap_header_get_id(request));
    if (r < 0) {
        return r;
    }
    if (payload && payload_len) {
        r = coap_packet_append_payload_marker(response);
        if (r < 0) {
            return r;
        }
        r = coap_packet_append_payload(response, payload, payload_len);
    }
    return r;
}

static int handle_light(const struct coap_packet *request, struct coap_packet *response,
                        uint8_t *resp_buf, size_t resp_len)
{
    uint8_t code = COAP_RESPONSE_CODE_NOT_FOUND;
    const uint8_t method = coap_header_get_code(request);

    /* Método GET */
    if (method == COAP_METHOD_GET) {
        /* TODO: devolver '1' o '0' según light_on */
        const char *val = light_on ? "1" : "0";
        code = COAP_RESPONSE_CODE_CONTENT;
        return build_simple_response(response, resp_buf, resp_len, request, code,
                                     (const uint8_t *)val, strlen(val));
    }

    /* Método PUT */
    if (method == COAP_METHOD_PUT) {
        /* TODO: leer payload y actualizar light_on; validar tamaño */
        const uint8_t *pl;
        uint16_t pl_len;
        pl = coap_packet_get_payload(request, &pl_len);
        if (pl && pl_len == 1 && (pl[0] == '0' || pl[0] == '1')) {
            light_on = (pl[0] == '1');
            code = COAP_RESPONSE_CODE_CHANGED;
            return build_simple_response(response, resp_buf, resp_len, request, code, NULL, 0);
        }
        code = COAP_RESPONSE_CODE_BAD_REQUEST;
        return build_simple_response(response, resp_buf, resp_len, request, code, NULL, 0);
    }

    code = COAP_RESPONSE_CODE_METHOD_NOT_ALLOWED;
    return build_simple_response(response, resp_buf, resp_len, request, code, NULL, 0);
}

static int handle_sensor(const struct coap_packet *request, struct coap_packet *response,
                         uint8_t *resp_buf, size_t resp_len)
{
    /* Solo GET */
    if (coap_header_get_code(request) != COAP_METHOD_GET) {
        return build_simple_response(response, resp_buf, resp_len, request,
                                     COAP_RESPONSE_CODE_METHOD_NOT_ALLOWED, NULL, 0);
    }
    /* TODO: incrementar contador y devolver JSON simulado */
    sensor_counter++;
    char payload[32];
    int len = snprintk(payload, sizeof(payload), "{\"val\":%u}", sensor_counter);
    return build_simple_response(response, resp_buf, resp_len, request,
                                 COAP_RESPONSE_CODE_CONTENT, (const uint8_t *)payload, len);
}

static void process_coap(int sock)
{
    struct sockaddr_in6 from;
    socklen_t from_len = sizeof(from);
    int r = recvfrom(sock, request_buf, sizeof(request_buf), 0,
                     (struct sockaddr *)&from, &from_len);
    if (r <= 0) {
        return;
    }

    struct coap_packet request;
    if (coap_packet_parse(&request, request_buf, r, NULL, 0) < 0) {
        LOG_WRN("CoAP parse falló");
        return;
    }

    /* Extraer path */
    struct coap_option options[8];
    int opt_count = 0;
    uint8_t token[8];
    uint8_t tkl = coap_header_get_token(&request);
    memcpy(token, coap_header_get_token_ptr(&request), tkl);

    opt_count = coap_find_options(&request, COAP_OPTION_URI_PATH, options, 8);
    char path[32] = {0};
    size_t offset = 0;
    for (int i = 0; i < opt_count; i++) {
        if (offset + options[i].len + 1 >= sizeof(path)) {
            break;
        }
        memcpy(&path[offset], options[i].value, options[i].len);
        offset += options[i].len;
        path[offset++] = '/';
    }
    if (offset > 0) {
        path[offset - 1] = '\0';
    }

    struct coap_packet response;
    int ret;
    if (strcmp(path, "light") == 0) {
        ret = handle_light(&request, &response, response_buf, sizeof(response_buf));
    } else if (strcmp(path, "sensor") == 0) {
        ret = handle_sensor(&request, &response, response_buf, sizeof(response_buf));
    } else {
        ret = build_simple_response(&response, response_buf, sizeof(response_buf), &request,
                                    COAP_RESPONSE_CODE_NOT_FOUND, NULL, 0);
    }
    if (ret < 0) {
        LOG_WRN("Error construyendo respuesta (%d)", ret);
        return;
    }
    sendto(sock, coap_packet_get_data(&response), coap_packet_get_data_len(&response), 0,
           (struct sockaddr *)&from, from_len);
}

static int create_coap_socket(void)
{
    int sock;
    struct sockaddr_in6 addr6 = {0};
    sock = socket(AF_INET6, SOCK_DGRAM, IPPROTO_UDP);
    if (sock < 0) {
        return -errno;
    }
    addr6.sin6_family = AF_INET6;
    addr6.sin6_port = htons(COAP_PORT);
    addr6.sin6_addr = in6addr_any;
    if (bind(sock, (struct sockaddr *)&addr6, sizeof(addr6)) < 0) {
        int e = -errno;
        LOG_ERR("bind falló: %d", e);
        return e;
    }
    return sock;
}

static void coap_server_thread(void)
{
    int sock = create_coap_socket();
    if (sock < 0) {
        LOG_ERR("No se pudo crear socket CoAP");
        return;
    }
    LOG_INF("Servidor CoAP base listo (puerto %d)", COAP_PORT);
    while (1) {
        process_coap(sock);
        k_sleep(K_MSEC(10));
    }
}

K_THREAD_DEFINE(coap_srv, 4096, coap_server_thread, NULL, NULL, NULL, 7, 0, 0);

/* TODO (Lab 1):
 * - Documentar en DDR decisión de formato JSON /sensor.
 * - Añadir confirmable vs non-confirmable (actualmente implicit ACK simple).
 * - Mejorar parsing path (usar API option walk). 
 */
#endif /* CONFIG_IOT_LAB_COAP_SERVER */