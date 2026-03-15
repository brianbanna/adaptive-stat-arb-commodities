.PHONY: data spreads models signals backtest evaluate report website clean all test

PKG = adaptive_stat_arb

data:
	python -m $(PKG).data.futures_loader

spreads:
	python -m $(PKG).data.spread_builder

models:
	python -m $(PKG).models.kalman_filter

signals:
	python -m $(PKG).signals.entry_exit

backtest:
	python -m $(PKG).backtest.engine

evaluate:
	python -m $(PKG).evaluation.report

report:
	python -m $(PKG).visualization.tearsheet

website:
	@echo "Copy key figures to website/assets/figures/ and open website/index.html"

clean:
	rm -rf data/processed/*
	rm -rf results/figures/*
	rm -rf results/tables/*
	rm -rf results/tearsheets/*

all: data spreads models signals backtest evaluate report

test:
	python -m pytest tests/ -v
