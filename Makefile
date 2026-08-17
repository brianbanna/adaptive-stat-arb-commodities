.PHONY: help test lint typecheck parity cointegration filters breaks engine corridors backtest notes clean

PKG = statarb

help:
	@echo "Targets, in the order SPEC Part F builds them:"
	@echo "  parity         D3 parity gate, legacy Brent WTI pair. Nothing proceeds until green."
	@echo "  cointegration  D4 D6 Johansen and VECM per basket"
	@echo "  filters        D5 multivariate Kalman"
	@echo "  breaks         D7 D8 D9 D10 the overlay and the traffic light"
	@echo "  engine         D11 D12 D13 pricing engine and the engine gate"
	@echo "  corridors      D15 physical arbitrage corridors"
	@echo "  backtest       D16 D17 backtest and attribution"
	@echo "  notes          D6 D14 D18 regenerate every note from artifacts"
	@echo "  test lint typecheck"

test:
	python -m pytest tests/ -v

lint:
	python -m ruff check .

typecheck:
	python -m mypy $(PKG)

# D3. THE PARITY GATE. No science change rides along with the refactor, and nothing
# downstream proceeds until this is green.
parity:
	python -m pytest tests/ -v -k parity

cointegration:
	python -m $(PKG).cointegration

filters:
	python -m $(PKG).filters

breaks:
	python -m $(PKG).breaks

# The engine harness. Runs as CI here and as an import check in the 2 projects that
# import statarb.pricing. A red harness does not merge, before or after the freeze.
engine:
	python -m pytest tests/ -v -k engine

corridors:
	python -m $(PKG).corridors

backtest:
	python -m $(PKG).backtest

notes:
	python -m $(PKG).reporting

# Processed data only. data/raw is the record and is never touched by a clean target.
clean:
	rm -rf data/processed/*
	rm -rf results/figures/* results/tables/* results/tearsheets/*
