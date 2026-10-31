# BscGasTracker

A Python tool to check the current BSC gas price from a public JSON-RPC endpoint, suggest slow/standard/fast levels, and estimate transaction cost in BNB.

## Installation

```bash
pip install -r requirements.txt
```

Requires Python 3.9 or later.

## Usage

```bash
python bsc_gas_tracker.py
python bsc_gas_tracker.py --gas-limit 100000
```

Example output:

```json
{
  "gas_price_gwei": 5.0,
  "levels_gwei": {"slow": 4.5, "standard": 5.0, "fast": 6.0},
  "estimated_cost_bnb": {"slow": 0.0000945, "standard": 0.000105, "fast": 0.000126},
  "gas_limit": 21000
}
```

## How it works

- `eth_gasPrice` returns the current gas price in wei; dividing by `10**9` gives gwei.
- Slow is 90% of the current price, standard is the current price, fast is 120%.
- Cost in BNB = `gas_price_gwei * 10**9 * gas_limit / 10**18`.

## Tests

```bash
python -m unittest discover -s tests -v
```

Tests mock the RPC response, so they run offline.

## Limitations

- Gas prices change block by block; a suggestion is a snapshot, not a guarantee.
- Slow transactions may stay pending longer during congestion.
- This tool is read-only. It never sends a transaction or needs a private key.

## License

MIT. See `LICENSE`.
