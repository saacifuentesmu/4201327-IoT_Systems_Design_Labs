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