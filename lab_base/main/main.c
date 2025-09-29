/* Proyecto base IoT Labs: shell Thread + preparación CoAP.
 * CoAP server minimal se añadirá en Lab 1 por estudiantes.
 */
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "openthread/instance.h"
#include "openthread/tasklet.h"
#include "openthread/cli.h"
#include "esp_openthread.h"
#include "esp_openthread_cli.h"

static const char *TAG = "iot_lab_base";

// Forward declaration
void start_coap_server(void);

void app_main(void) {
    // Initialize NVS
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // Initialize OpenThread
    esp_openthread_platform_config_t config = {
        .radio_config = {
            .radio_mode = RADIO_MODE_NATIVE,
        },
        .host_config = {
            .host_connection_mode = HOST_CONNECTION_MODE_NONE,
        },
        .port_config = {
            .storage_partition_name = "nvs",
            .netif_queue_size = 10,
            .task_queue_size = 10,
        },
    };

    ESP_ERROR_CHECK(esp_openthread_init(&config));

    // Start OpenThread
    ESP_ERROR_CHECK(esp_openthread_launch_mainloop());

    // Initialize CLI
    esp_openthread_cli_init();

    ESP_LOGI(TAG, "OpenThread initialized with CLI");

    // Start CoAP server
    start_coap_server();

    // La lógica principal se añadirá progresivamente en los labs.
}