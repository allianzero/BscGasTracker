import unittest
from unittest.mock import patch

import bsc_gas_tracker as m


class FakeResp:
    def __init__(self, result):
        self._result = result

    def raise_for_status(self):
        pass

    def json(self):
        return {"jsonrpc": "2.0", "id": 1, "result": self._result}


class TestGas(unittest.TestCase):
    @patch("bsc_gas_tracker.requests.post")
    def test_gas_price(self, mock_post):
        # 5 gwei = 5 * 10^9 wei
        mock_post.return_value = FakeResp(hex(5 * 10**9))
        self.assertEqual(m.get_gas_price_gwei(), 5.0)

    def test_levels(self):
        levels = m.recommend_levels(10)
        self.assertEqual(levels, {"slow": 9.0, "standard": 10.0, "fast": 12.0})

    def test_cost(self):
        # 5 gwei * 21000 gas = 105000 gwei = 0.000105 BNB
        self.assertAlmostEqual(m.estimate_cost_bnb(5, 21000), 0.000105)


if __name__ == "__main__":
    unittest.main()
