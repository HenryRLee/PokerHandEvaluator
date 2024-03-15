package evaluator;

class Evaluate7{

  static int evaluate7Cards(int a, int b, int c, int d, int e, int f, int g){
    int suitHash = 0;

    suitHash += Evaluator.SUITBIT_BY_ID[a];
    suitHash += Evaluator.SUITBIT_BY_ID[b];
    suitHash += Evaluator.SUITBIT_BY_ID[c];
    suitHash += Evaluator.SUITBIT_BY_ID[d];
    suitHash += Evaluator.SUITBIT_BY_ID[e];
    suitHash += Evaluator.SUITBIT_BY_ID[f];
    suitHash += Evaluator.SUITBIT_BY_ID[g];

    if(DPTables.SUITS[suitHash] != 0){

      int[] suitBinary = new int[4];

      suitBinary[a & 0x3] |= Evaluator.BINARIES_BY_ID[a];
      suitBinary[b & 0x3] |= Evaluator.BINARIES_BY_ID[b];
      suitBinary[c & 0x3] |= Evaluator.BINARIES_BY_ID[c];
      suitBinary[d & 0x3] |= Evaluator.BINARIES_BY_ID[d];
      suitBinary[e & 0x3] |= Evaluator.BINARIES_BY_ID[e];
      suitBinary[f & 0x3] |= Evaluator.BINARIES_BY_ID[f];
      suitBinary[g & 0x3] |= Evaluator.BINARIES_BY_ID[g];

      int z = DPTables.SUITS[suitHash] - 1;

      return HashTable.FLUSH()[suitBinary[z]];
    }

    byte[] quinary = new byte[13];

    quinary[a >> 2]++;
    quinary[b >> 2]++;
    quinary[c >> 2]++;
    quinary[d >> 2]++;
    quinary[e >> 2]++;
    quinary[f >> 2]++;
    quinary[g >> 2]++;

    final int hash = Hash.hashQuinary(quinary, 7);

    return HashTable.NO_FLUSH_7()[hash];
  }

}
