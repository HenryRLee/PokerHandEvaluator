package evaluator;

import java.util.Arrays;
import java.util.stream.Collectors;

public class Card{

  public enum Rank{
    STRAIGHT_FLUSH(10),
    FOUR_OF_A_KIND(166),
    FULL_HOUSE(322),
    FLUSH(1599),
    STRAIGHT(1609),
    THREE_OF_A_KIND(2467),
    TWO_PAIR(3325),
    ONE_PAIR(6185),
    HIGH_CARD(9000) //TODO: CHANGE TO MAXIMUM CARD VALUE
    ;

    Rank(int cardRank){
      this.cardRank = cardRank;
    }

    private final int cardRank;

    public static Rank getRankFromValue(int value){
      for(Rank r : values()){
        if(value <= r.cardRank){
          return r;
        }
      }
      throw new RuntimeException("Invalid value: " + value);
    }

    @Override
    public String toString(){
      String s = name().toLowerCase();
      String[] split = s.split("_");
      return Arrays.stream(split).map(str -> Character.toUpperCase(str.charAt(0)) + str.substring(1)).collect(Collectors.joining(" "));
    }
  }

  public static int GET_CARD(String s){
    return RANK_VAL(s.charAt(0)) * 4 + SUIT_VAL(s.charAt(1));
  }

  public static String CARD_VALUE(int c){
    return "" + RANK_FROM_CARD(c) + SUIT_FROM_CARD(c);
  }

  private static char SUIT_FROM_CARD(int c){
    switch(c % 4){
      case 0:
        return 'c';
      case 1:
        return 'd';
      case 2:
        return 'h';
      case 3:
        return 's';
      default:
        throw new RuntimeException("Unreachable I think?");
    }
  }

  private static char RANK_FROM_CARD(int c){
    switch(Math.floorDiv(c, 4)){
      case 0:
        return '2';
      case 1:
        return '3';
      case 2:
        return '4';
      case 3:
        return '5';
      case 4:
        return '6';
      case 5:
        return '7';
      case 6:
        return '8';
      case 7:
        return '9';
      case 8:
        return 'T';
      case 9:
        return 'J';
      case 10:
        return 'Q';
      case 11:
        return 'K';
      case 12:
        return 'A';
      default:
        throw new RuntimeException("Invalid card given: " + c);
    }
  }

  private static int RANK_VAL(char c){
    switch(c){
      case '2':
        return 0;
      case '3':
        return 1;
      case '4':
        return 2;
      case '5':
        return 3;
      case '6':
        return 4;
      case '7':
        return 5;
      case '8':
        return 6;
      case '9':
        return 7;
      case 'T':
        return 8;
      case 'J':
        return 9;
      case 'Q':
        return 10;
      case 'K':
        return 11;
      case 'A':
        return 12;
      default:
        throw new RuntimeException("Invalid rank given: " + c);
    }
  }

  private static int SUIT_VAL(char c){
    switch(c){
      case 'c':
        return 0;
      case 'd':
        return 1;
      case 'h':
        return 2;
      case 's':
        return 3;
      default:
        throw new RuntimeException("Invalid suit given: " + c);
    }
  }

}
