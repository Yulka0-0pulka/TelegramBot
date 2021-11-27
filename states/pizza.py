from transitions import Machine


class PizzaFsm(object):
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
        'Конец заказа',
    ]

    transitions = [
        {'trigger': 'big', 'source': 'Ждем заказ', 'dest': 'Большую'},
        {'trigger': 'small', 'source': 'Ждем заказ', 'dest': 'Маленькую'},
        {'trigger': 'cash', 'source': ['Большую', 'Маленькую'], 'dest': 'Наличкой'},
        {'trigger': 'with_card', 'source': ['Большую', 'Маленькую'], 'dest': 'Банковской картой'},
        {'trigger': 'yes', 'source': ['Банковской картой', 'Наличкой'], 'dest': 'Конец заказа',
         'after': 'set_state_end_order'},
        {'trigger': 'no', 'source': ['Банковской картой', 'Наличкой'], 'dest': 'Конец заказа',
         'after': 'set_state_end_order'},
    ]

    def __init__(self):
        self.machine = Machine(model=self, states=PizzaFsm.states, transitions=PizzaFsm.transitions,
                               initial='Ждем заказ')

    def set_state_end_order(self):
        self.machine.set_state('Ждем заказ')
