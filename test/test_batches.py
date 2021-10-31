from django.test import TestCase
from allocation.models import Batch, OrderLine, Money, Name, Line, Person
from datetime import date

def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch("batch-001", sku, batch_qty, eta=date.today()),
        OrderLine("order-123", sku, line_qty)
    )

class BatchesModelTestCase(TestCase):
    def setUp(self):
        self.batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
        self.line = OrderLine('order-ref', "SMALL-TABLE", 2)

    def test_allocating_to_a_batch_reduces_the_available_quantity(self):
        self.batch.allocate(self.line)
        self.assertEqual(self.batch.available_quantity, 18)

    def test_can_allocate_if_available_greater_than_required(self):
        large_batch, small_line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
        self.assertTrue(large_batch.can_allocate(small_line))
    
    def test_cannot_allocate_if_available_smaller_than_required(self):
        small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
        self.assertFalse(small_batch.can_allocate(large_line))

    def test_can_allocate_if_available_equal_to_required(self):
        batch, line = make_batch_and_line("ELEGANT-LAMP", 2, 2)
        self.assertTrue(batch.can_allocate(line))

    def test_cannot_allocate_if_skus_do_not_match(self):
        batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, eta=None)
        different_sku_line = OrderLine("order-123", "EXPENSIVE-TOASTER", 10)
        self.assertFalse(batch.can_allocate(different_sku_line))

    def test_can_only_deallocate_allocated_lines(self):
        batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
        batch.deallocate(unallocated_line)
        self.assertEqual(batch.available_quantity, 20)

    def test_allocation_is_idempotent(self):
        batch, line = make_batch_and_line("ANGULAR-DESK", 20, 2)
        batch.allocate(line)
        batch.allocate(line)
        self.assertEqual(batch.available_quantity, 18)

    def test_equality(self):
        self.assertEqual(Money('gbp', 10), Money('gbp', 10))
        self.assertNotEqual(Name('Harry', 'Percival'), Name('Bob', 'Gregory'))
        self.assertEqual(Line('RED-CHAIR', 5), Line('RED-CHAIR', 5))

    def test_name_equality(self):
        self.assertNotEqual(Name("Harry", "Percival"), Name("Barry", "Percival"))

    def test_barry_is_harry(self):
        harry = Person(Name("Harry", "Percival"))
        barry = harry 

        barry.name = Name("Barry", "Percival")

        self.assertEqual(harry, barry)
        self.assertEqual(barry, harry)