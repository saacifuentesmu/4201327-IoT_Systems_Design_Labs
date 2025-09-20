iot_lab_base: Proyecto base de laboratorios IoT (Thread + Shell + CoAP habilitado)

Este proyecto sirve como punto de partida para todos los labs fusionados (8 semanas).

Extensiones se añadirán progresivamente (CoAP endpoints, sensores, OTA, métricas, etc.).

Estructura principal:

- ``prj.conf``: Config base Thread + shell + CoAP.
- ``overlay-ot-rcp-host.conf``: Overlay avanzado para Border Router/RCP (Lab 4 en adelante).
- ``src/main.c``: Punto de entrada mínimo.
- ``src/coap_demo.c``: Servidor CoAP esqueleto con recursos ``/light`` y ``/sensor`` (mock) a completar.
- ``Kconfig``: Opción ``CONFIG_IOT_LAB_COAP_SERVER`` para habilitar/deshabilitar servidor.

Build rápido:

.. code-block:: bash

	west build -p auto -b esp32c6_devkitc/esp32c6/hpcore -d build-lab-base
	west flash
	west espressif monitor

En la consola (Thread shell) inicializa red:

.. code-block:: none

	ot dataset init new
	ot dataset commit active
	ot ifconfig up
	ot thread start
	state
	ipaddr

Segundo nodo: repetir el build con otro directorio de build (``build-lab-base-node2``) y formar la red.

Prueba CoAP básica (desde segundo nodo cuando el servidor ya está activo):

.. code-block:: none

	coap get coap://[<ipv6-del-primer-nodo>]/light
	coap put coap://[<ipv6-del-primer-nodo>]/light 1
	coap get coap://[<ipv6-del-primer-nodo>]/sensor

TODOs para estudiantes (Lab 1):

* Ajustar payload de ``/sensor`` (e.g., JSON con timestamp).
* Añadir validaciones extra en PUT ``/light``.
* Experimentar con confirmable vs non-confirmable.
* Documentar decisiones en DDR (formato datos, códigos usados).

Scripts de apoyo (directorio ``tools/``):

.. code-block:: bash

	# Cliente simple GET/PUT
	pip install aiocoap
	python tools/coap_client.py --host <ipv6> get /sensor
	python tools/coap_client.py --host <ipv6> put /light 1

	# Stub medición latencias
	python tools/test_e2e_stub.py --host <ipv6> --count 5

Para desactivar temporalmente el servidor CoAP (solo probar Thread):

.. code-block:: bash

	west build -b esp32c6_devkitc/esp32c6/hpcore -DCONFIG_IOT_LAB_COAP_SERVER=n

Notas:

* El servidor actual construye respuestas tipo ACK simples (code apropiado) y no implementa observe todavía (se hace en Lab 4).
* Para el Border Router, aplicar overlay y reconstruir (ver guías de labs).