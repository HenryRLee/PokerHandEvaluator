package evaluator;

class Hash{

  private final static int LENGTH = 13;

  static int hashQuinary(final byte[] q, int k){
    int sum = 0;

    for(int i = 0; i < LENGTH; i++){
      sum += DPTables.DP[q[i]][LENGTH - i - 1][k];

      k -= q[i];

      if(k <= 0){
        break;
      }
    }

    return sum;
  }

}
