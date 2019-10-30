# Python Library

## Tests

Run `run.sh` to perform tests in the `python` folder.

### Unit tests
To perform correctness tests, run
```bash
sh run.sh 
```
or
```bash
sh run.sh unittest
```



### Tests for tables
These tests are for understanding the way of constructing hash tables.
The tables are based on the algorithm of Cactus Kev.
To see the results of table building and tables from CPP version are same, run
```bash
sh run.sh (the name of table)
```
where `the name of table` can be `dptables` or `hashtable` or `hashtable5`.

So, for example, to see the result of building `hashtable5` and that of from CPP version, run
```bash
sh run.sh hashtable5
```
