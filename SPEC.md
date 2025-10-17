# CALCULADORA DE DESCUENTOS

## Propósito
Dado un precio inicial y una serie de descuentos, calcular la cantidad total ahorrada y el precio final luego de aplicar los descuentos según reglas definidas.

## Glosario
* **Descuento:** Reducción del precio original aplicable a una compra.
* **Descuento fijo:** Reducción expresada como una cantidad monetaria (por ejemplo, $100).
* **Descuento proporcional:** Reducción expresada como un porcentaje del precio actual (por ejemplo, 10%).
* **Precio Inicial:** Valor base del producto o servicio antes de aplicar cualquier descuento.
* **Precio Final:** Valor resultante luego de aplicar todos los descuentos válidos.
* **Cantidad Ahorrada:** Diferencia entre el precio inicial y el precio final. Nunca puede ser negativa.

## Escenarios de prueba

**Escenario 1:** Descuento porcentual válido  
*Dado* que tengo 10% de descuento en mi compra de 200 pesos.  
*Cuando* calcule el descuento.  
*Entonces* el precio final será 180 pesos y la cantidad ahorrada serán 20 pesos.

**Escenario 2:** Descuento porcentual negativo  
*Dado* que tengo -50% de descuento en mi compra de 100 pesos.  
*Cuando* calcule el descuento.  
*Entonces* me indicará que los descuentos no pueden ser negativos.

**Escenario 3:** Descuento fijo mayor que el precio  
*Dado* que tengo un descuento de 300 pesos en mi compra de 50 pesos.  
*Cuando* calcule el descuento.  
*Entonces* me indicará que el precio final es 0 pesos y la cantidad ahorrada serán 50 pesos.

**Escenario 4:** Múltiples descuentos secuenciales  
*Dado* que tengo un 10% de descuento y luego un descuento fijo de 20 pesos sobre una compra de 200 pesos.  
*Cuando* calcule el descuento.  
*Entonces* el primer descuento reducirá el precio a 180 pesos, y el segundo lo reducirá a 160 pesos.  
*Y* la cantidad total ahorrada será 40 pesos.

**Escenario 5:** Descuento del 100%  
*Dado* que tengo un 100% de descuento en mi compra de 500 pesos.  
*Cuando* calcule el descuento.  
*Entonces* el precio final será 0 pesos y la cantidad ahorrada serán 500 pesos.

**Escenario 6:** Precio inicial negativo  
*Dado* que tengo un precio inicial de -100 pesos.  
*Cuando* calcule el descuento.  
*Entonces* me indicará que el precio inicial no puede ser negativo.

**Escenario 7:** Sin descuentos aplicados  
*Dado* que tengo una compra de 250 pesos sin descuentos.  
*Cuando* calcule el descuento.  
*Entonces* el precio final será 250 pesos y la cantidad ahorrada será 0 pesos.

**Escenario 8:** Descuento no reconocido  
*Dado* que ingreso un descuento de tipo “cupón”.  
*Cuando* calcule el descuento.  
*Entonces* me indicará que el tipo de descuento no es válido.

**Escenario 9:** Redondeo de decimales  
*Dado* que tengo un 12.345% de descuento sobre una compra de 199.99 pesos.  
*Cuando* calcule el descuento.  
*Entonces* el resultado deberá redondearse a dos decimales, mostrando el precio final con precisión monetaria.

## Reglas de negocio

* El **precio inicial** debe ser un número positivo o cero, admitiendo decimales.
* Los **descuentos** pueden ser proporcionales (porcentaje) o fijos (monto monetario).
* Los descuentos deben indicarse de forma explícita (por ejemplo: “10%” o “$100”).
* Se permite ingresar uno o más descuentos.
* Los descuentos se aplican **secuencialmente** en el orden en que se reciben.
* Ningún descuento puede ser negativo.
* Si un descuento excede el precio actual, el precio final se ajustará a **0**.
* Si no hay descuentos, el precio final será igual al inicial.
* Se utilizará una precisión de **dos decimales** y se redondeará al centavo más cercano.
* En caso de error (por ejemplo, datos inválidos), se deberá generar un mensaje descriptivo y el cálculo no continuará.
* Se podrá definir en el futuro un modo de acumulación alternativo (no requerido en esta versión).
* Los cálculos deben ser realizados de la manera más eficiente posible en cuanto a uso de memoria y tiempo.

## Casos especiales
* Precio inicial de 0: el precio final siempre será 0, independientemente de los descuentos.
* Descuento de 0: no afecta el resultado.
* Descuento del 100% o más: el precio final será 0.
* Formatos de entrada inválidos (por ejemplo, texto no numérico): se informará error.
* Mezcla de tipos (fijo + proporcional) es válida si se respeta el orden.

## Cosas que no se incluirán

* Interfaz de usuario (gráfica o web).
* Persistencia de precios o descuentos.
* Implementación de modos de acumulación alternativos (aunque se prevé su futura inclusión).
* Tope configurable distinto de 0 (el precio mínimo permitido sigue siendo 0).
