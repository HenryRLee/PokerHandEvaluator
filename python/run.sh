#!/bin/bash


if [[ $# -eq 0 ]]; then
  python -m test.test
elif [[ "$1" == "unittest" ]]; then
  python -m test.test
elif [[ "$1" == "dptables" ]]; then
  python -m test_tables.test_dptables
elif [[ "$1" == "hashtable" ]]; then
  python -m test_tables.test_hashtable
elif [[ "$1" == "hashtable5" ]]; then
  python -m test_tables.test_hashtable5
else
  echo "Unknown argument"
fi
