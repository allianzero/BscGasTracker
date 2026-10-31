"""BSC gas price tracker.

Reads the current gas price from a public BSC JSON-RPC endpoint with
eth_gasPrice, converts it to gwei, suggests slow/standard/fast levels,
and estimates transaction cost in BNB for a given gas limit. Read-only:
it never sends a transaction and never needs a private key.
"""
import argparse
import json
import sys

import requests

DEFAULT_RPC = "https://bsc-dataseed.binance.org/"


def get_gas_price_gwei(rpc_url=DEFAULT_RPC):
    payload = {"jsonrpc": "2.0", "id": 1, "method": "eth_gasPrice", "params": []}
    resp = requests.post(rpc_url, json=payload, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"RPC error: {data['error']}")
    return int(data["result"], 16) / 10**9


def recommend_levels(gas_price_gwei):
    """Return slow/standard/fast suggestions around the current price."""
    return {
        "slow": round(gas_price_gwei * 0.9, 3),
        "standard": round(gas_price_gwei, 3),
        "fast": round(gas_price_gwei * 1.2, 3),
    }


def estimate_cost_bnb(gas_price_gwei, gas_limit):
    """Cost in BNB for a transaction at a gas price and gas limit."""
    return gas_price_gwei * 10**9 * gas_limit / 10**18


def main(argv=None):
    parser = argparse.ArgumentParser(description="BSC gas price tracker")
    parser.add_argument("--rpc", default=DEFAULT_RPC)
    parser.add_argument("--gas-limit", type=int, default=21000, help="Gas limit for cost estimate")
    args = parser.parse_args(argv)
    try:
        price = get_gas_price_gwei(args.rpc)
    except Exception as exc:  # noqa: BLE001 - CLI should report, not crash
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    levels = recommend_levels(price)
    result = {
        "gas_price_gwei": price,
        "levels_gwei": levels,
        "estimated_cost_bnb": {
            "slow": estimate_cost_bnb(levels["slow"], args.gas_limit),
            "standard": estimate_cost_bnb(levels["standard"], args.gas_limit),
            "fast": estimate_cost_bnb(levels["fast"], args.gas_limit),
        },
        "gas_limit": args.gas_limit,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
