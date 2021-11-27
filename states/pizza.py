from transitions import Machine


class PizzaFsm:
    size = None
    payment = None
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
    ]

    transitions = [
        {'trigger': 'big', 'source': 'Ждем заказ', 'dest': 'Большую', 'after': 'size'},
        {'trigger': 'small', 'source': 'Ждем заказ', 'dest': 'Маленькую', 'after': 'size'},
        {'trigger': 'cash', 'source': ['Большую', 'Маленькую'], 'dest': 'Наличкой', 'after': 'payment'},
        {'trigger': 'with_card', 'source': ['Большую', 'Маленькую'], 'dest': 'Банковской картой', 'after': 'payment'},
        {'trigger': 'yes', 'source': ['Банковской картой', 'Наличкой'], 'dest': 'Ждем заказ'},
        {'trigger': 'no', 'source': ['Банковской картой', 'Наличкой'], 'dest': 'Ждем заказ'},
        # {'trigger': 'remove', 'source': ['Банковской картой', 'Наличкой', 'Большую', 'Маленькую'], 'dest': 'Ждем заказ',
        #  'after': 'clear'}
    ]

    def __init__(self):
        self.machine = Machine(model=self, states=PizzaFsm.states, transitions=PizzaFsm.transitions,
                               initial='Ждем заказ')

    def size(self):
        self.size = self.state

    def payment(self):
        self.payment = self.state
