from decimal import Decimal, ROUND_HALF_UP


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

    def apply_discount(self, discount):
        discount = discount.strip()

        if discount.endswith('%'):
            percentage = Decimal(discount[:-1])

            if percentage < 0:
                raise InvalidDiscountError("Los descuentos no pueden ser negativos")

            discount_amount = self.current_price * (percentage / Decimal('100'))
            self.current_price -= discount_amount
            self.total_saved += discount_amount
        elif discount.startswith('$'):
            fixed_amount = Decimal(discount[1:])

            # El descuento no puede ser mayor que el precio actual
            actual_discount = min(fixed_amount, self.current_price)
            self.current_price -= actual_discount
            self.total_saved += actual_discount
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
