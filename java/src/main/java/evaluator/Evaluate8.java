package evaluator;

class Evaluate8{

  static int evaluate8Cards(int a, int b, int c, int d, int e, int f, int g, int h){

    int valueFlush = 10000;
    int valueNoFlush;
    int[] suitCounter = new int[4];

    suitCounter[a & 0x3]++;
    suitCounter[b & 0x3]++;
    suitCounter[c & 0x3]++;
    suitCounter[d & 0x3]++;
    suitCounter[e & 0x3]++;
    suitCounter[f & 0x3]++;
    suitCounter[g & 0x3]++;
    suitCounter[h & 0x3]++;

    for(int j = 0; j < 4; j++){
      if(suitCounter[j] >= 5){
        int[] suitBinary = new int[4];

        suitBinary[a & 0x3] |= Evaluator.BINARIES_BY_ID[a];
        suitBinary[b & 0x3] |= Evaluator.BINARIES_BY_ID[b];
        suitBinary[c & 0x3] |= Evaluator.BINARIES_BY_ID[c];
        suitBinary[d & 0x3] |= Evaluator.BINARIES_BY_ID[d];
        suitBinary[e & 0x3] |= Evaluator.BINARIES_BY_ID[e];
        suitBinary[f & 0x3] |= Evaluator.BINARIES_BY_ID[f];
        suitBinary[g & 0x3] |= Evaluator.BINARIES_BY_ID[g];
        suitBinary[h & 0x3] |= Evaluator.BINARIES_BY_ID[h];

        valueFlush = HashTable.FLUSH()[suitBinary[j]];

        break;
      }
    }

    byte[] quinary = new byte[13];
    quinary[a >> 2]++;
    quinary[b >> 2]++;
    quinary[c >> 2]++;
    quinary[d >> 2]++;
    quinary[e >> 2]++;
    quinary[f >> 2]++;
    quinary[g >> 2]++;
    quinary[h >> 2]++;

    int hash = Hash.hashQuinary(quinary, 8);
    valueNoFlush = HashTable.NO_FLUSH_8()[hash];

    return Math.min(valueFlush, valueNoFlush);
  }
}
