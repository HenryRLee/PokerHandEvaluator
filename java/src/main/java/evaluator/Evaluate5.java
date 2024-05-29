package evaluator;

class Evaluate5{

  static int evaluate5Cards(int a, int b, int c, int d, int e){
    int suitHash = 0;

    suitHash += Evaluator.SUITBIT_BY_ID[a];
    suitHash += Evaluator.SUITBIT_BY_ID[b];
    suitHash += Evaluator.SUITBIT_BY_ID[c];
    suitHash += Evaluator.SUITBIT_BY_ID[d];
    suitHash += Evaluator.SUITBIT_BY_ID[e];

    if(DPTables.SUITS[suitHash] != 0){

      int[] suitBinary = new int[4];

      suitBinary[a & 0x3] |= Evaluator.BINARIES_BY_ID[a];
      suitBinary[b & 0x3] |= Evaluator.BINARIES_BY_ID[b];
      suitBinary[c & 0x3] |= Evaluator.BINARIES_BY_ID[c];
      suitBinary[d & 0x3] |= Evaluator.BINARIES_BY_ID[d];
      suitBinary[e & 0x3] |= Evaluator.BINARIES_BY_ID[e];

      int z = DPTables.SUITS[suitHash] - 1;

      return HashTable.FLUSH()[suitBinary[z]];

    }

    byte[] quinary = new byte[13];

    quinary[a >> 2]++;
    quinary[b >> 2]++;
    quinary[c >> 2]++;
    quinary[d >> 2]++;
    quinary[e >> 2]++;

    final int hash = Hash.hashQuinary(quinary, 5);

    return HashTable.NO_FLUSH_5()[hash];
  }
}
