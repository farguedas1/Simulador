#!/usr/bin/env bash

fetch_cash_flow() {
  echo "Fetching Cash Flow Statement for ${1}"
  curl -qs https://financialmodellingprep.com/api/v3/financials/cash-flow-statement/${1}?datatype=csv > ${1}-orig.csv
  ../transpose.py ${1}-orig.csv ${1}.csv
  rm ${1}-orig.csv
}

fetch_cash_flow PG
fetch_cash_flow UL
