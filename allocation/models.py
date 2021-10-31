from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Set, NamedTuple
from datetime import date
from collections import namedtuple

@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int 

class Batch:
    def __init__(
        self, ref: str, sku: str, qty: int, eta: Optional[date]
    ):
        self.reference = ref
        self.sku = sku
        self.eta = eta 
        self._purchased_quantity = qty
        self._allocations = set()

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity
    
    def can_allocate(self, line: OrderLine) -> bool:
        return self.available_quantity >= line.qty and self.sku == line.sku

@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str 

class Money(NamedTuple):
    currency: str
    value: int 

class Person:
    def __init__(self, name: Name):
        self.name = name

Line = namedtuple('Line', ['sku', 'qty'])

