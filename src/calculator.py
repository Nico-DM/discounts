from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import Optional, Iterable
from enum import Enum  # Nuevo Enum


class InvalidDiscountError(Exception):
    pass


class InvalidPriceError(Exception):
    pass


class DiscountType(Enum):  # Nuevo Enum para tipos de descuento internos
    PERCENT = 'percent'
    FIXED = 'fixed'


class DiscountCalculator:
    def __init__(self, initial_price: int | float | Decimal | str):
        try:
            price_decimal = Decimal(str(initial_price))
        except (InvalidOperation, ValueError):
            raise InvalidPriceError("El precio inicial debe ser numérico")
        if price_decimal < 0:
            raise InvalidPriceError("El precio inicial no puede ser negativo")
        self.initial_price = price_decimal
        self.current_price = self.initial_price
        self.total_saved = Decimal('0')

    def __repr__(self):  # Nuevo para depuración
        return (
            f"DiscountCalculator(initial={self.initial_price}, current={self.current_price}, "
            f"saved={self.total_saved})"
        )

    def _q(self, value: Decimal) -> Decimal:
        """Redondea a dos decimales usando ROUND_HALF_UP (helper centralizado)."""
        return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def _apply_percentage_discount(self, percentage: Decimal):
        """Aplica descuento porcentual, validando rango y evitando precio negativo."""
        if percentage < 0:
            raise InvalidDiscountError("Los descuentos no pueden ser negativos")
        # Simplificado: limita el porcentaje a 100 para evitar precio negativo sin branch separado
        capped = min(percentage, Decimal('100'))
        discount_amount = self.current_price * (capped / Decimal('100'))
        self._register_discount(discount_amount)

    def _apply_fixed_discount(self, amount: Decimal):
        """Aplica descuento fijo, limitándolo para no exceder el precio actual."""
        if amount < 0:
            raise InvalidDiscountError("Los descuentos no pueden ser negativos")
        discount_amount = min(amount, self.current_price)
        self._register_discount(discount_amount)

    def _register_discount(self, discount_amount: Decimal):
        """Actualiza estado interno con el monto de descuento validado."""
        if discount_amount < 0:
            raise InvalidDiscountError("El descuento calculado no puede ser negativo")
        self.current_price -= discount_amount
        # Evitar precio negativo por seguridad (shouldn't happen por min/limit)
        if self.current_price < 0:
            self.current_price = Decimal('0')
        self.total_saved += discount_amount

    def _parse_discount(self, discount: str) -> tuple[DiscountType, Decimal]:
        """Parsea el string de descuento y devuelve (DiscountType, valor)."""
        discount = discount.strip()
        if discount.endswith('%'):
            raw = discount[:-1].strip()
            try:
                percentage = Decimal(raw)
            except (InvalidOperation, ValueError):
                raise InvalidDiscountError("Formato de porcentaje inválido")
            return (DiscountType.PERCENT, percentage)
        if discount.startswith('$'):
            raw = discount[1:].strip()
            try:
                fixed_amount = Decimal(raw)
            except (InvalidOperation, ValueError):
                raise InvalidDiscountError("Formato de descuento fijo inválido")
            return (DiscountType.FIXED, fixed_amount)
        raise InvalidDiscountError("El tipo de descuento no es válido")

    def apply_discount(self, discount: str):
        tipo, valor = self._parse_discount(discount)
        if tipo is DiscountType.PERCENT:
            self._apply_percentage_discount(valor)
        else:  # DiscountType.FIXED
            self._apply_fixed_discount(valor)

    def apply_discounts(self, discounts: Iterable[str]):
        """Aplica secuencialmente una lista/iterable de descuentos."""
        for d in discounts:
            self.apply_discount(d)

    def get_final_price(self) -> Decimal:
        return self._q(self.current_price)

    def get_total_saved(self) -> Decimal:
        return self._q(self.total_saved)


def calculate_discount(initial_price: int | float | Decimal | str, discounts: Optional[Iterable[str]] = None):
    calculator = DiscountCalculator(initial_price)
    if discounts:
        calculator.apply_discounts(discounts)
    return {
        'final_price': calculator.get_final_price(),
        'total_saved': calculator.get_total_saved()
    }


def simulate_discounts(initial_price: int | float | Decimal | str, discounts: Optional[Iterable[str]] = None):
    """Función pura para simular descuentos sin exponer la clase (envoltorio)."""
    return calculate_discount(initial_price, discounts)
