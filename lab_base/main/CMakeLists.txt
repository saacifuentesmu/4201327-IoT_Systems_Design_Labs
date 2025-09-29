idf_component_register(SRCS "main.c" "coap_demo.c"
                       INCLUDE_DIRS "."
                       REQUIRES openthread libcoap esp_openthread_cli)