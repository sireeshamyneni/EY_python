from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        
        self.execution_client = ExecutionClient
        self.orders = []

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        """
        :param product_id: product name
        :param price:  
        """
        
        for order in self.orders:
            if order['product_id'] == product_id and not order['executed']:
                if self._is_price_favourable(order, price):
                    self._execute_order(order)
    
    def _is_price_favorable(self, order, price: float) -> bool:
        """
        Determines if the current price is favorable to execute the order.
        :param order: The order details.
        :param price: The current market price.
        :return: True if the price is favorable, False otherwise.
        """
        if order['buy_sell_flag'] == 'buy' and price <= order['limit_price']:
            return True
        elif order['buy_sell_flag'] == 'sell' and price >= order['limit_price']:
            return True
        return False
        
    def _execute_order(self, order):
        """
        Executes an order if the price is favorable.
        :param order: The order details.
        """
        try:
            if order['buy_sell_flag'] == 'buy':
                self.execution_client.buy(order['product_id'], order['amount'])
            elif order['buy_sell_flag'] == 'sell':
                self.execution_client.sell(order['product_id'], order['amount'])
            order['executed'] = True
            print(f"Executed {order['buy_sell_flag']} order for {order['amount']} units of {order['product_id']} at or better than {order['limit_price']}.")
        except ExecutionException as e:
            print(f"Failed to execute order: {e}")
        
    def add_order(self, buy_sell_flag: str, product_id: str, amount: int, limit_price: float):
        """
        Adds an order to the agent.
        :param buy_sell_flag: 'buy' for buying, 'sell' for selling.
        :param product_id: The product identifier (e.g., 'IBM').
        :param amount: The amount to buy or sell.
        :param limit_price: The limit price at which to buy or sell.
        """
        order = {
            "buy_sell_flag": buy_sell_flag,
            "product_id": product_id,
            "amount": amount,
            "limit_price": limit_price,
            "executed": False,
        }
        self.orders.append(order)
