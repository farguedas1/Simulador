#!/usr/bin/env bash

fetch_balance_sheet() {
  echo "Fetching Balance Sheet Statement for ${1}"
  curl -qs https://financialmodellingprep.com/api/v3/financials/balance-sheet-statement/${1}?datatype=csv > ${1}-orig.csv
  ../transpose.py ${1}-orig.csv ${1}.csv
  rm ${1}-orig.csv
}

fetch_balance_sheet PG
fetch_balance_sheet UL
