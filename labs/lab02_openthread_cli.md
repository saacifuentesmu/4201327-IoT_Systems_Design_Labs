# Lab 02 — Conectividad inalámbrica y redes mesh para IoT

## Objetivos de Aprendizaje IoT
- Entender topologías de red para sistemas IoT distribuidos
- Comparar arquitecturas mesh vs star vs tree para IoT
- Explorar auto-configuración y self-healing en redes IoT
- Usar OpenThread como ejemplo de protocolo mesh moderno

## Conceptos IoT Cubiertos
- **Topologías IoT**: Star, Tree, Mesh - cuándo usar cada una
- **Auto-configuración**: Network formation sin intervención manual
- **Self-healing**: Recuperación automática ante fallas de nodos
- **Roles dinámicos**: Leader election, parent selection, load balancing
- **Escalabilidad**: Límites prácticos de redes mesh

## Herramienta: OpenThread como Caso de Estudio
**¿Por qué OpenThread?**
- Protocolo mesh moderno (usado en Google Nest, Matter)
- Auto-configuración completa
- Self-healing demostrable
- Implementación open-source para estudio

**Ejemplo Base**: `samples/net/openthread/shell`

## Experimento Práctico: Red Mesh Auto-Configurable

### Parte A: Preparación (30 min)
1) **Construir ejemplo shell con soporte Thread**:
   ```bash
   west build -b esp32c6_devkitc zephyr/samples/net/openthread/shell -p
   west flash
   west espressif monitor
   ```

2) **Entender los roles en Thread**:
   - **Leader**: Nodo central, gestiona network data
   - **Router**: Forwarding + child support
   - **End Device**: Solo comunicación con parent
   - **REED**: Router Eligible End Device

### Parte B: Formación de Red (45 min)
3) **Crear red desde cero** (placa A):
   ```
   ot dataset init new
   ot dataset channel 20
   ot dataset panid 0x1234  
   ot dataset networkname IoTLab-Red
   ot dataset commit active
   ot ifconfig up
   ot thread start
   ot state               # Debe mostrar "leader"
   ```

4) **Unirse desde otros nodos** (placas B, C, D...):
   ```
   ot dataset channel 20
   ot dataset panid 0x1234
   ot dataset networkname IoTLab-Red 
   ot dataset commit active
   ot ifconfig up
   ot thread start
   ot state               # Observar transición: disabled→detached→child→router
   ```

### Parte C: Análisis de Topología (45 min)
5) **Estudiar la topología formada**:
   ```
   ot router table        # Ver routers activos
   ot neighbor table      # Ver vecinos directos  
   ot parent             # Ver parent selection
   ot leaderdata         # Ver información del leader
   ```

6) **Experimentar con conectividad**:
   ```
   ot ipaddr             # Listar direcciones IPv6
   ot ping <dirección-de-otro-nodo>
   ot discover           # Scan de redes vecinas
   ```

## Verificación
- Two nodes joined and can ping each other.
- Show `ot neighbor` and `ot route` output.

## Notes
- For serial shell, set the correct UART and 115200 baud.
