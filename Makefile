# Makefile for QuantEcon.news

news:
	@echo "[QuantEcon.news] Building HTML and RST News Pages from news.yaml"
	python generate_news.py