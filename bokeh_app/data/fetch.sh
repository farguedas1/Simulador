#!/usr/bin/env bash

fetch_income_statement() {
  echo "Fetching Income Statement for ${1}"
  curl -qs https://financialmodellingprep.com/api/v3/financials/income-statement/${1}?datatype=csv > ${1}/income-statement-orig.csv
  ./transpose.py ${1}/income-statement-orig.csv ${1}/income-statement.csv
  rm ${1}/income-statement-orig.csv
}

fetch_cash_flow() {
  echo "Fetching Cash Flow Statement for ${1}"
  curl -qs https://financialmodellingprep.com/api/v3/financials/cash-flow-statement/${1}?datatype=csv > ${1}/cash-flow-orig.csv
  ./transpose.py ${1}/cash-flow-orig.csv ${1}/cash-flow.csv
  rm ${1}/cash-flow-orig.csv
}

fetch_balance_sheet() {
  echo "Fetching Balance Sheet Statement for ${1}"
  curl -qs https://financialmodellingprep.com/api/v3/financials/balance-sheet-statement/${1}?datatype=csv > ${1}/balance-sheet-orig.csv
  ../transpose.py ${1}/balance-sheet-orig.csv ${1}/balance-sheet.csv
  rm ${1}/balance-sheet-orig.csv
}

fetch_balance_sheet ${1}
fetch_income_statement ${1}
fetch_cash_flow ${1}
