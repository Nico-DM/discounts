from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


class InvalidDiscountError(Exception):
    pass


class InvalidPriceError(Exception):
    pass


class DiscountCalculator:
    def __init__(self, initial_price):
        if initial_price < 0:
            raise InvalidPriceError("El precio inicial no puede ser negativo")

        self.initial_price = Decimal(str(initial_price))
        self.current_price = self.initial_price
        self.total_saved = Decimal('0')

    def _apply_percentage_discount(self, percentage: Decimal):
        if percentage < 0:
            raise InvalidDiscountError("Los descuentos no pueden ser negativos")
        # Si porcentaje es 100% o más, el descuento es todo el precio actual
        if percentage >= 100:
            discount_amount = self.current_price
        else:
            discount_amount = self.current_price * (percentage / Decimal('100'))
        self._register_discount(discount_amount)

    def _apply_fixed_discount(self, amount: Decimal):
        if amount < 0:
            raise InvalidDiscountError("Los descuentos no pueden ser negativos")
        discount_amount = min(amount, self.current_price)
        self._register_discount(discount_amount)

    def _register_discount(self, discount_amount: Decimal):
        # Asegurar que nunca guardamos descuentos negativos
        if discount_amount < 0:
            raise InvalidDiscountError("El descuento calculado no puede ser negativo")
        self.current_price -= discount_amount
        # Evitar precio negativo por seguridad (shouldn't happen por min/limit)
        if self.current_price < 0:
            self.current_price = Decimal('0')
        self.total_saved += discount_amount

    def apply_discount(self, discount):
        discount = discount.strip()

        if discount.endswith('%'):
            raw = discount[:-1].strip()
            try:
                percentage = Decimal(raw)
            except (InvalidOperation, ValueError):
                raise InvalidDiscountError("Formato de porcentaje inválido")
            self._apply_percentage_discount(percentage)
        elif discount.startswith('$'):
            raw = discount[1:].strip()
            try:
                fixed_amount = Decimal(raw)
            except (InvalidOperation, ValueError):
                raise InvalidDiscountError("Formato de descuento fijo inválido")
            self._apply_fixed_discount(fixed_amount)
        else:
            raise InvalidDiscountError("El tipo de descuento no es válido")

    def get_final_price(self):
        return self.current_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def get_total_saved(self):
        return self.total_saved.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def calculate_discount(initial_price, discounts=None):
    calculator = DiscountCalculator(initial_price)

    if discounts:
        for discount in discounts:
            calculator.apply_discount(discount)

    return {
        'final_price': calculator.get_final_price(),
        'total_saved': calculator.get_total_saved()
    }
