from django.test import TestCase
from allocation.models import Batch, OrderLine, allocate
from datetime import date, timedelta

today = date.today()
yesterday = today - timedelta(days = 1)
tomorrow = today + timedelta(days = 1) 
later = today + timedelta(days = 2)

class AllocationLogicTestCase(TestCase):
    def setUp(self):
        pass

    def test_prefers_current_stock_batches_to_shipments(self):
        in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
        shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
        line = OrderLine("oref", "RETRO-CLOCK", 10)

        allocate(line, [in_stock_batch, shipment_batch])

        self.assertEqual(in_stock_batch.available_quantity, 90)
        self.assertEqual(shipment_batch.available_quantity, 100)

    def test_prefers_earlier_batches(self):
        earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=today)
        medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
        latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=later)
        line = OrderLine("order1", "MINIMALIST-SPOON", 10)

        allocate(line, [medium, earliest, latest])

        self.assertEqual(earliest.available_quantity, 90)
        self.assertEqual(medium.available_quantity, 100)
        self.assertEqual(latest.available_quantity, 100)

    def test_returns_allocated_batch_ref(self):
        in_stock_batch = Batch("in-stock-batch-ref", "HIGHBROW-POSTER", 100, eta=None)
        shipment_batch = Batch("shipment-batch-ref", "HIGHBROW-POSTER", 100, eta=tomorrow)
        line = OrderLine("oref", "HIGHBROW-POSTER", 10)

        allocation = allocate(line, [in_stock_batch, shipment_batch])

        self.assertEqual(allocation, in_stock_batch.reference)
