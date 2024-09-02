import unittest
from unittest.mock import MagicMock
from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient, ExecutionException

class LimitOrderAgentTest(unittest.TestCase):

    def test_something(self):
        self.fail("not implemented")
     
    def setUp(self):
        """
        Create a new LimitOrderAgent instance and a mock ExecutionClient before each test.
        """
        self.mock_execution_client = MagicMock(spec=ExecutionClient)
        self.agent = LimitOrderAgent(self.mock_execution_client)

    def test_buy_order_execution(self):
        """
        Test that a buy order is executed when the market price is at or below the limit.
        """
        # Add a buy order with a limit price of 100
        self.agent.add_order('buy', 'IBM', 1000, 100.0)

        # Simulate a price tick where the price is 99
        self.agent.on_price_tick('IBM', 99.0)

        # Check if the buy method was called on the mock execution client
        self.mock_execution_client.buy.assert_called_once_with('IBM', 1000)

    def test_sell_order_execution(self):
        """
        Test that a sell order is executed when the market price is at or above the limit.
        """
        # Add a sell order with a limit price of 100
        self.agent.add_order('sell', 'IBM', 1000, 100.0)

        # Simulate a price tick where the price is 101
        self.agent.on_price_tick('IBM', 101.0)

        # Check if the sell method was called on the mock execution client
        self.mock_execution_client.sell.assert_called_once_with('IBM', 1000)

    def test_order_not_executed_if_price_not_favorable(self):
        """
        Test that an order is not executed if the market price is not favorable.
        """
        # Add a buy order with a limit price of 100
        self.agent.add_order('buy', 'IBM', 1000, 100.0)

        # Simulate a price tick where the price is 101 (not favorable)
        self.agent.on_price_tick('IBM', 101.0)

        # Check if the buy method was not called
        self.mock_execution_client.buy.assert_not_called()

    def test_order_not_executed_if_not_matching_product(self):
        """
        Test that an order is not executed if the price tick is for a different product.
        """
        # Add a buy order for IBM
        self.agent.add_order('buy', 'IBM', 1000, 100.0)

        # Simulate a price tick for a different product
        self.agent.on_price_tick('AAPL', 99.0)

        # Check if the buy method was not called
        self.mock_execution_client.buy.assert_not_called()

    def test_order_execution_fails(self):
        """
        Test that an ExecutionException is handled properly when executing an order.
        """
        # Add a buy order with a limit price of 100
        self.agent.add_order('buy', 'IBM', 1000, 100.0)

        # Make the mock buy method raise an ExecutionException
        self.mock_execution_client.buy.side_effect = ExecutionException("Execution error")

        # Simulate a price tick where the price is 99
        with self.assertRaises(ExecutionException):
            self.agent.on_price_tick('IBM', 99.0)

if __name__ == '__main__':
    unittest.main()
    

