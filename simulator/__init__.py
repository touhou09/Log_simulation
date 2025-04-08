from .member import MemberSimulator
from .order import OrderSimulator
from .payment import PaymentSimulator

def get_all_simulators():
    return {
        "member": MemberSimulator(),
        "order": OrderSimulator(),
        "payment": PaymentSimulator()
    }