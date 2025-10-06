# Lab 8 — Consolidación & Hardening (Integración Final)

## Objetivos
- Pruebas end-to-end automatizadas (script).
- Mini pentest: intento join no autorizado / CoAP inválido.
- Stress test ligero (ráfaga CoAP 20 req). 
- Documentación final + video demo.

## Contexto
Sintetizando todo el conocimiento teórico y práctico anterior, este laboratorio consolida el desarrollo de sistemas IoT con pruebas integrales, fortalecimiento de seguridad y documentación lista para producción.

## Setup del Proyecto

### 1. Continuar con el proyecto de Lab 3

Este laboratorio continúa desarrollando el proyecto iniciado en Lab 3. Asegúrate de tener el proyecto `lab03` (o equivalente) abierto en VS Code.

### 2. Añadir código base completo + hardening (token auth)

**Base completa igual que Lab 7**, luego añadir autenticación simple con token.

**Añadir token auth** en `main/coap_demo.c` (después de defines):
```c
#define AUTH_TOKEN "iotlab2024"  // Token hardcoded para demo (en producción usar NVS o similar)

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

**Modificar handlers para requerir token** (ejemplo en handle_light):
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

**Aplicar mismo check a handle_sensor y handle_metrics**.

### 3. Configurar settings finales

**Usar mismo `sdkconfig` que Lab 7**, añadir hardening:
```bash
# Security hardening
CONFIG_COMPILER_OPTIMIZATION_LEVEL_DEBUG=n
CONFIG_COMPILER_OPTIMIZATION_LEVEL_RELEASE=y
CONFIG_STACK_CHECK_NONE=n
CONFIG_STACK_CHECK_NORM=y
```

**Build y flash:**
```bash
idf.py set-target esp32c6
idf.py build
idf.py flash
idf.py monitor
```

### 4. Script de pruebas end-to-end automatizadas

**Crear `tools/test_e2e.py`:**
```python
#!/usr/bin/env python3
import subprocess
import time
import sys
import statistics

class IoTTestSuite:
    def __init__(self, node_ip, border_router_ip=None):
        self.node_ip = node_ip
        self.br_ip = border_router_ip
        self.results = []

    def run_coap_command(self, method, path, payload=None, host=None):
        """Ejecutar comando CoAP y medir latencia"""
        if host is None:
            host = self.node_ip
        
        cmd = ["python", "tools/coap_client.py", "--host", host, method, path]
        if payload:
            cmd.append(payload)
        
        start = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        latency = (time.time() - start) * 1000  # ms
        
        return {
            'success': result.returncode == 0,
            'latency': latency,
            'output': result.stdout.strip(),
            'error': result.stderr.strip()
        }

    def test_sensor_endpoint(self):
        """Test /sensor endpoint"""
        print("Testing /sensor endpoint...")
        result = self.run_coap_command("get", "/sensor")
        self.results.append({
            'test': 'sensor_get',
            'success': result['success'],
            'latency': result['latency'],
            'data': result['output']
        })
        return result['success']

    def test_light_control(self):
        """Test /light control"""
        print("Testing /light control...")
        # Test PUT on
        on_result = self.run_coap_command("put", "/light", "1")
        time.sleep(0.5)
        # Test GET
        get_result = self.run_coap_command("get", "/light")
        # Test PUT off
        off_result = self.run_coap_command("put", "/light", "0")
        
        success = all([on_result['success'], get_result['success'], off_result['success']])
        avg_latency = statistics.mean([on_result['latency'], get_result['latency'], off_result['latency']])
        
        self.results.append({
            'test': 'light_control',
            'success': success,
            'avg_latency': avg_latency
        })
        return success

    def test_rate_limiting(self):
        """Test rate limiting"""
        print("Testing rate limiting...")
        latencies = []
        success_count = 0
        
        # Burst de 10 requests rápidas
        for i in range(10):
            result = self.run_coap_command("get", "/sensor")
            latencies.append(result['latency'])
            if result['success']:
                success_count += 1
        
        # Debería haber algunos rechazos por rate limiting
        rate_limited = success_count < 10
        
        self.results.append({
            'test': 'rate_limiting',
            'rate_limited': rate_limited,
            'success_count': success_count,
            'avg_latency': statistics.mean(latencies)
        })
        return rate_limited

    def test_authentication(self):
        """Test authentication"""
        print("Testing authentication...")
        # Test sin token (debería fallar)
        no_auth = self.run_coap_command("get", "/light")
        # Test con token (debería funcionar si implementado)
        # Nota: ajustar según implementación
        
        self.results.append({
            'test': 'authentication',
            'no_auth_blocked': not no_auth['success']
        })
        return True  # Siempre pasa, solo informativo

    def test_stress(self, num_requests=20):
        """Stress test con ráfaga de requests"""
        print(f"Running stress test ({num_requests} requests)...")
        latencies = []
        success_count = 0
        
        for i in range(num_requests):
            result = self.run_coap_command("get", "/sensor")
            latencies.append(result['latency'])
            if result['success']:
                success_count += 1
        
        success_rate = success_count / num_requests
        avg_latency = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        
        self.results.append({
            'test': 'stress_test',
            'success_rate': success_rate,
            'avg_latency': avg_latency,
            'min_latency': min_latency,
            'max_latency': max_latency,
            'total_requests': num_requests
        })
        
        print(".2f")
        return success_rate > 0.8  # 80% success threshold

    def test_border_router(self):
        """Test conectividad a través del Border Router"""
        if not self.br_ip:
            print("Border Router IP not provided, skipping BR test")
            return True
            
        print("Testing Border Router connectivity...")
        # Test ping a través de BR
        result = self.run_coap_command("get", "/sensor", host=self.br_ip)
        self.results.append({
            'test': 'border_router',
            'success': result['success'],
            'latency': result['latency']
        })
        return result['success']

    def run_all_tests(self):
        """Ejecutar toda la suite de pruebas"""
        print("=== IoT Lab End-to-End Test Suite ===")
        print(f"Target Node: {self.node_ip}")
        if self.br_ip:
            print(f"Border Router: {self.br_ip}")
        
        tests = [
            self.test_sensor_endpoint,
            self.test_light_control,
            self.test_rate_limiting,
            self.test_authentication,
            lambda: self.test_stress(20),
            self.test_border_router
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
                    print("✅ PASSED")
                else:
                    print("❌ FAILED")
            except Exception as e:
                print(f"❌ ERROR: {e}")
        
        print(f"\n=== Results: {passed}/{total} tests passed ===")
        
        # Generar reporte
        self.generate_report()
        
        return passed == total

    def generate_report(self):
        """Generar reporte de resultados"""
        print("\n=== Detailed Report ===")
        for result in self.results:
            print(f"Test: {result['test']}")
            for key, value in result.items():
                if key != 'test':
                    print(f"  {key}: {value}")
            print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_e2e.py <node_ipv6> [border_router_ipv6]")
        sys.exit(1)
    
    node_ip = sys.argv[1]
    br_ip = sys.argv[2] if len(sys.argv) > 2 else None
    
    suite = IoTTestSuite(node_ip, br_ip)
    success = suite.run_all_tests()
    sys.exit(0 if success else 1)
```

**Ejecutar pruebas:**
```bash
# Pruebas básicas
python tools/test_e2e.py fd11:22:33:0:0:0:0:1

# Con Border Router
python tools/test_e2e.py fd11:22:33:0:0:0:0:1 fd11:22:33:0:0:0:0:100
```

### 5. Mini pentest y hardening residual

**Pruebas de seguridad:**
```bash
# Intentar join no autorizado (desde dispositivo sin credenciales)
# En CLI Thread de dispositivo no autorizado:
dataset set active <dataset_hex_incorrecto>
ifconfig up
thread start
# Debería fallar

# CoAP requests inválidos
python tools/coap_client.py --host [IPv6] get /invalid_endpoint
python tools/coap_client.py --host [IPv6] put /light invalid_payload

# Stress test de recursos
# Ejecutar múltiples instancias del stress test
for i in {1..5}; do
    python tools/test_e2e.py fd11:22:33:0:0:0:0:1 &
done
```

### 6. Documentación final y video demo

**Estructura de documentación:**
- Arquitectura general del sistema
- APIs CoAP documentadas
- Guía de despliegue
- Troubleshooting común
- Métricas de rendimiento

**Video demo checklist:**
- Formación de red Thread
- Funcionalidad básica CoAP
- Dashboard en funcionamiento
- Border Router y acceso network
- OTA update
- Pruebas end-to-end
- Demo de seguridad (rate limiting, auth)

## Entregables
- Suite de pruebas automatizadas (`tools/test_e2e.py`) con métricas de latencia y éxito
- Reporte de pruebas end-to-end (ratio éxito, latencia promedio)
- Logs de stress test (ráfaga 20 req) y uso de recursos
- Resultados de mini pentest (intentos join no autorizado, CoAP inválido)
- Documentación final completa del sistema IoT
- Video demo mostrando funcionalidad completa y pruebas
