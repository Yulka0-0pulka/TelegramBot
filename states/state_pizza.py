from transitions import Machine


class PizzaFsm(object):
    size = ''
    payment = ''
    message = 'Какую вы хотите пиццу? Большую или маленькую?'
    command = [
        'Большую',
        'Маленькую',
        'Наличкой',
        'Банковской картой',
        'Картой',
        'Да',
        'Нет',
    ]
    states = [
        'Ждем заказ',
        'Большую',
        'Маленькую',
        'Наличкой',
        'Банковской картой',
        'Конец заказа',
    ]

    transitions = [
        {'trigger': 'Большую', 'source': 'Ждем заказ', 'dest': 'Большую', 'after': 'select_pizza_size'},
        {'trigger': 'Маленькую', 'source': 'Ждем заказ', 'dest': 'Маленькую', 'after': 'select_pizza_size'},
        {'trigger': 'Наличкой', 'source': ['Большую', 'Маленькую'], 'dest': 'Наличкой', 'after': 'select_payment'},
        {'trigger': 'Банковской картой', 'source': ['Большую', 'Маленькую'], 'dest': 'Банковской картой',
         'after': 'select_payment'},
        {'trigger': 'Картой', 'source': ['Большую', 'Маленькую'], 'dest': 'Банковской картой',
         'after': 'select_payment'},
        {'trigger': 'Да', 'source': ['Банковской картой', 'Наличкой'], 'dest': 'Конец заказа',
         'after': 'yes_end_order'},
        {'trigger': 'Нет', 'source': ['Банковской картой', 'Наличкой'], 'dest': 'Конец заказа',
         'after': 'no_end_order'},
    ]

    def __init__(self):
        self.machine = Machine(model=self, states=PizzaFsm.states, transitions=PizzaFsm.transitions,
                               initial='Ждем заказ')

    def yes_end_order(self):
        self.message = 'Спасибо за заказ! Чтобы заказать снова, нажмите /pizza'

    def no_end_order(self):
        self.message = 'Заказ отменен! Чтобы заказать снова, нажмите /pizza'

    def select_payment(self):
        self.payment = self.state
        self.message = f'Вы хотите {self.size} пиццу, оплата - {self.payment}?'

    def select_pizza_size(self):
        self.size = self.state
        self.message = 'Как вы будете платить, наличкой или банковской картой?'
