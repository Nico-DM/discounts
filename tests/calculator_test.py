import pytest
from decimal import Decimal
from src.calculator import (
    DiscountCalculator,
    InvalidDiscountError,
    InvalidPriceError,
    calculate_discount
)


class TestDiscountCalculator:
    """Tests unitarios para la calculadora de descuentos basados en SPEC.md"""

    def test_escenario_1_descuento_porcentual_valido(self):
        """
        Escenario 1: Descuento porcentual válido
        Dado que tengo 10% de descuento en mi compra de 200 pesos.
        Cuando calcule el descuento.
        Entonces el precio final será 180 pesos y la cantidad ahorrada serán 20 pesos.
        """
        calc = DiscountCalculator(200)
        calc.apply_discount("10%")

        assert calc.get_final_price() == Decimal('180.00')
        assert calc.get_total_saved() == Decimal('20.00')

    def test_escenario_2_descuento_porcentual_negativo(self):
        """
        Escenario 2: Descuento porcentual negativo
        Dado que tengo -50% de descuento en mi compra de 100 pesos.
        Cuando calcule el descuento.
        Entonces me indicará que los descuentos no pueden ser negativos.
        """
        calc = DiscountCalculator(100)

        with pytest.raises(InvalidDiscountError) as exc_info:
            calc.apply_discount("-50%")

        assert "no pueden ser negativos" in str(exc_info.value).lower()

    def test_escenario_3_descuento_fijo_mayor_que_precio(self):
        """
        Escenario 3: Descuento fijo mayor que el precio
        Dado que tengo un descuento de 300 pesos en mi compra de 50 pesos.
        Cuando calcule el descuento.
        Entonces me indicará que el precio final es 0 pesos y la cantidad ahorrada serán 50 pesos.
        """
        calc = DiscountCalculator(50)
        calc.apply_discount("$300")

        assert calc.get_final_price() == Decimal('0.00')
        assert calc.get_total_saved() == Decimal('50.00')

    def test_escenario_4_multiples_descuentos_secuenciales(self):
        """
        Escenario 4: Múltiples descuentos secuenciales
        Dado que tengo un 10% de descuento y luego un descuento fijo de 20 pesos sobre una compra de 200 pesos.
        Cuando calcule el descuento.
        Entonces el primer descuento reducirá el precio a 180 pesos, y el segundo lo reducirá a 160 pesos.
        Y la cantidad total ahorrada será 40 pesos.
        """
        calc = DiscountCalculator(200)
        calc.apply_discount("10%")
        calc.apply_discount("$20")

        assert calc.get_final_price() == Decimal('160.00')
        assert calc.get_total_saved() == Decimal('40.00')

    def test_escenario_5_descuento_del_100_porciento(self):
        """
        Escenario 5: Descuento del 100%
        Dado que tengo un 100% de descuento en mi compra de 500 pesos.
        Cuando calcule el descuento.
        Entonces el precio final será 0 pesos y la cantidad ahorrada serán 500 pesos.
        """
        calc = DiscountCalculator(500)
        calc.apply_discount("100%")

        assert calc.get_final_price() == Decimal('0.00')
        assert calc.get_total_saved() == Decimal('500.00')

    def test_escenario_6_precio_inicial_negativo(self):
        """
        Escenario 6: Precio inicial negativo
        Dado que tengo un precio inicial de -100 pesos.
        Cuando calcule el descuento.
        Entonces me indicará que el precio inicial no puede ser negativo.
        """
        with pytest.raises(InvalidPriceError) as exc_info:
            DiscountCalculator(-100)

        assert "no puede ser negativo" in str(exc_info.value).lower()

    def test_escenario_7_sin_descuentos_aplicados(self):
        """
        Escenario 7: Sin descuentos aplicados
        Dado que tengo una compra de 250 pesos sin descuentos.
        Cuando calcule el descuento.
        Entonces el precio final será 250 pesos y la cantidad ahorrada será 0 pesos.
        """
        calc = DiscountCalculator(250)

        assert calc.get_final_price() == Decimal('250.00')
        assert calc.get_total_saved() == Decimal('0.00')

    def test_escenario_8_descuento_no_reconocido(self):
        """
        Escenario 8: Descuento no reconocido
        Dado que ingreso un descuento de tipo "cupón".
        Cuando calcule el descuento.
        Entonces me indicará que el tipo de descuento no es válido.
        """
        calc = DiscountCalculator(100)

        with pytest.raises(InvalidDiscountError) as exc_info:
            calc.apply_discount("cupón")

        assert "no es válido" in str(exc_info.value).lower()

    def test_escenario_9_redondeo_de_decimales(self):
        """
        Escenario 9: Redondeo de decimales
        Dado que tengo un 12.345% de descuento sobre una compra de 199.99 pesos.
        Cuando calcule el descuento.
        Entonces el resultado deberá redondearse a dos decimales, mostrando el precio final con precisión monetaria.
        """
        calc = DiscountCalculator(199.99)
        calc.apply_discount("12.345%")

        final_price = calc.get_final_price()
        total_saved = calc.get_total_saved()

        # Verificar que tiene exactamente 2 decimales
        assert str(final_price).split('.')[-1] == '30'  # Dos decimales
        assert str(total_saved).split('.')[-1] == '69'  # Dos decimales
        assert final_price == Decimal('175.30')
        assert total_saved == Decimal('24.69')


class TestCasosEspeciales:
    """Tests para casos especiales mencionados en SPEC.md"""

    def test_precio_inicial_cero(self):
        """
        Caso especial: Precio inicial de 0
        El precio final siempre será 0, independientemente de los descuentos.
        """
        calc = DiscountCalculator(0)
        calc.apply_discount("50%")

        assert calc.get_final_price() == Decimal('0.00')
        assert calc.get_total_saved() == Decimal('0.00')

    def test_descuento_de_cero_no_afecta_resultado(self):
        """
        Caso especial: Descuento de 0
        No afecta el resultado.
        """
        calc = DiscountCalculator(100)
        calc.apply_discount("0%")

        assert calc.get_final_price() == Decimal('100.00')
        assert calc.get_total_saved() == Decimal('0.00')

    def test_descuento_mayor_al_100_porciento(self):
        """
        Caso especial: Descuento del 100% o más
        El precio final será 0.
        """
        calc = DiscountCalculator(200)
        calc.apply_discount("150%")

        assert calc.get_final_price() == Decimal('0.00')
        assert calc.get_total_saved() == Decimal('200.00')

    def test_formato_entrada_invalido_porcentaje(self):
        """
        Caso especial: Formatos de entrada inválidos (texto no numérico)
        Se informará error.
        """
        calc = DiscountCalculator(100)

        with pytest.raises(InvalidDiscountError):
            calc.apply_discount("abc%")

    def test_formato_entrada_invalido_fijo(self):
        """
        Caso especial: Formatos de entrada inválidos (texto no numérico en descuento fijo)
        Se informará error.
        """
        calc = DiscountCalculator(100)

        with pytest.raises(InvalidDiscountError):
            calc.apply_discount("$xyz")

    def test_mezcla_tipos_descuentos_valida(self):
        """
        Caso especial: Mezcla de tipos (fijo + proporcional)
        Es válida si se respeta el orden.
        """
        calc = DiscountCalculator(1000)
        calc.apply_discount("$200")  # 1000 - 200 = 800
        calc.apply_discount("25%")   # 800 * 0.25 = 200, entonces 800 - 200 = 600

        assert calc.get_final_price() == Decimal('600.00')
        assert calc.get_total_saved() == Decimal('400.00')


class TestCasosLimite:
    """Tests para casos límite - TODOs para implementación futura"""

    # TODO: Test para descuentos con espacios en blanco antes/después
    def test_descuento_con_espacios_en_blanco(self):
        """Los descuentos con espacios deben manejarse correctamente"""
        calc = DiscountCalculator(100)
        calc.apply_discount("  10%  ")

        assert calc.get_final_price() == Decimal('90.00')

    # TODO: Test para múltiples descuentos que llevan el precio a 0
    def test_multiples_descuentos_exceden_precio(self):
        """Múltiples descuentos que en conjunto exceden el precio inicial"""
        calc = DiscountCalculator(100)
        calc.apply_discount("$60")
        calc.apply_discount("$50")

        assert calc.get_final_price() == Decimal('0.00')
        assert calc.get_total_saved() == Decimal('100.00')

    # TODO: Test para descuento fijo de $0
    def test_descuento_fijo_cero(self):
        """Descuento fijo de $0 no debe afectar el precio"""
        calc = DiscountCalculator(100)
        calc.apply_discount("$0")

        assert calc.get_final_price() == Decimal('100.00')
        assert calc.get_total_saved() == Decimal('0.00')

    # TODO: Test para descuentos negativos en formato fijo
    def test_descuento_fijo_negativo(self):
        """Descuento fijo negativo ($-50) debe lanzar error"""
        calc = DiscountCalculator(100)

        with pytest.raises(InvalidDiscountError):
            calc.apply_discount("$-50")

    # TODO: Test para precisión con muchos decimales
    # Verificar que el redondeo se realiza correctamente con números con muchos decimales

    # TODO: Test para precios muy grandes
    # Verificar límites numéricos con precios extremadamente altos

    # TODO: Test para descuentos muy pequeños (menores a 0.01)
    # Verificar comportamiento con descuentos menores al centavo

    # TODO: Test para aplicar el mismo descuento múltiples veces
    # Verificar que se puede aplicar el mismo descuento más de una vez

    # TODO: Test para entrada con Decimal vs float
    # Verificar compatibilidad entre tipos de datos numéricos

    # TODO: Test para lista vacía de descuentos
    # Verificar comportamiento cuando se pasa una lista vacía

    # TODO: Test para descuento sin símbolo de moneda o porcentaje
    # Verificar que se rechaza "100" sin "$" o "%"

    # TODO: Test para descuentos con formato de moneda alternativo
    # Por ejemplo: "USD 100" o "100 pesos"

    # TODO: Test para aplicación de descuentos usando apply_discounts()
    # Verificar el método que acepta una lista de descuentos

    # TODO: Test para la función calculate_discount() de alto nivel
    # Verificar la función helper que devuelve un diccionario
