#!/usr/bin/env bash

fetch_income_statement() {
  echo "Fetching Income Statement for ${1}"
  curl -qs https://financialmodellingprep.com/api/v3/financials/income-statement/${1}?datatype=csv > ${1}-orig.csv
  ../transpose.py ${1}-orig.csv ${1}.csv
  rm ${1}-orig.csv
}

fetch_income_statement PG
fetch_income_statement UL
