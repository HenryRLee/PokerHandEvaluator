package evaluator;

public class Evaluator{

  final static short[] BINARIES_BY_ID = {
    0x1, 0x1, 0x1, 0x1,
    0x2, 0x2, 0x2, 0x2,
    0x4, 0x4, 0x4, 0x4,
    0x8, 0x8, 0x8, 0x8,
    0x10, 0x10, 0x10, 0x10,
    0x20, 0x20, 0x20, 0x20,
    0x40, 0x40, 0x40, 0x40,
    0x80, 0x80, 0x80, 0x80,
    0x100, 0x100, 0x100, 0x100,
    0x200, 0x200, 0x200, 0x200,
    0x400, 0x400, 0x400, 0x400,
    0x800, 0x800, 0x800, 0x800,
    0x1000, 0x1000, 0x1000, 0x1000,
  };

  final static short[] SUITBIT_BY_ID = {
    0x1, 0x8, 0x40, 0x200,
    0x1, 0x8, 0x40, 0x200,
    0x1, 0x8, 0x40, 0x200,
    0x1, 0x8, 0x40, 0x200,
    0x1, 0x8, 0x40, 0x200,
    0x1, 0x8, 0x40, 0x200,
    0x1, 0x8, 0x40, 0x200,
    0x1, 0x8, 0x40, 0x200,
    0x1, 0x8, 0x40, 0x200,
    0x1, 0x8, 0x40, 0x200,
    0x1, 0x8, 0x40, 0x200,
    0x1, 0x8, 0x40, 0x200,
    0x1, 0x8, 0x40, 0x200,
  };

  public static int evaluate(int[] input){
    switch(input.length){
      case 5:
        return Evaluator.evaluate(input[0], input[1], input[2], input[3], input[4]);
      case 6:
        return Evaluator.evaluate(input[0], input[1], input[2], input[3], input[4], input[5]);
      case 7:
        return Evaluator.evaluate(input[0], input[1], input[2], input[3], input[4], input[5], input[6]);
      case 8:
        return Evaluator.evaluate(input[0], input[1], input[2], input[3], input[4], input[5], input[6],
          input[7]);
      case 9:
        return Evaluator.evaluate(input[0], input[1], input[2], input[3], input[4], input[5], input[6],
          input[7], input[8]);
    }
    throw new RuntimeException("" + input.length);
  }

  public static int evaluate(int a, int b, int c, int d, int e){
    return Evaluate5.evaluate5Cards(a, b, c, d, e);
  }

  public static int evaluate(int a, int b, int c, int d, int e, int f){
    return Evaluate6.evaluate6Cards(a, b, c, d, e, f);
  }

  public static int evaluate(int a, int b, int c, int d, int e, int f, int g){
    return Evaluate7.evaluate7Cards(a, b, c, d, e, f, g);
  }

  public static int evaluate(int a, int b, int c, int d, int e, int f, int g, int h){
    return Evaluate8.evaluate8Cards(a, b, c, d, e, f, g, h);
  }

  public static int evaluate(int a, int b, int c, int d, int e, int f, int g, int h, int i){
    return Evaluate9.evaluate9Cards(a, b, c, d, e, f, g, h, i);
  }
}
