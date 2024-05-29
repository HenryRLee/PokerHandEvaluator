package evaluator;

import com.opencsv.bean.CsvBindByName;

public class IdTestInputBean{

  public IdTestInputBean(){

  }

  @CsvBindByName
  int rank;

  @CsvBindByName
  private int card_1;

  @CsvBindByName
  private int card_2;

  @CsvBindByName
  private int card_3;

  @CsvBindByName
  private int card_4;

  @CsvBindByName
  private int card_5;

  @CsvBindByName
  private int card_6;

  @CsvBindByName
  private int card_7;

  // n is 1 indexed
  int[] arr(int n){
    int[] a = new int[n];
    a[0] = card_1;
    a[1] = card_2;
    a[2] = card_3;
    a[3] = card_4;
    a[4] = card_5;

    if(n >= 6){
      a[5] = card_6;
    }
    if(n >= 7){
      a[6] = card_7;
    }
    return a;
  }
}
