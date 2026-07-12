package evaluator;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

/**
 * Contains all of the HashTables used for either no flush results or flush results.
 * <p>
 * Due to the size of the tables they're loaded lazily on demand.
 */
class HashTable{

  private static short[] FLUSH = null;

  private static short[] NO_FLUSH_5 = null;

  private static short[] NO_FLUSH_6 = null;

  private static short[] NO_FLUSH_7 = null;

  private static short[] NO_FLUSH_8 = null;

  private static short[] NO_FLUSH_9 = null;

  private static short[] loadFromFile(String fileName){
    var p = Path.of("src", "main", "resources", "hashes", fileName + ".txt");
    try{
      var s = Files.readString(p);
      var split = s.split("\n");
      int amount = Integer.parseInt(split[0]);
      short[] arr = new short[amount];
      String[] split2 = split[1].split(",");
      for(int i = 0; i < amount; i++){
        String f = split2[i];
        arr[i] = Short.parseShort(f);
      }
      return arr;

    }catch(IOException e){
      System.err.println(e.getMessage());
      throw new RuntimeException(e); //TODO make this suck less
    }
  }

  static short[] FLUSH(){
    if(FLUSH == null){
      FLUSH = loadFromFile("HashTable");
    }
    return FLUSH;
  }

  static short[] NO_FLUSH_5(){
    if(NO_FLUSH_5 == null){
      NO_FLUSH_5 = loadFromFile("HashTable5");
    }
    return NO_FLUSH_5;
  }

  static short[] NO_FLUSH_6(){
    if(NO_FLUSH_6 == null){
      NO_FLUSH_6 = loadFromFile("HashTable6");
    }
    return NO_FLUSH_6;
  }

  static short[] NO_FLUSH_7(){
    if(NO_FLUSH_7 == null){
      NO_FLUSH_7 = loadFromFile("HashTable7");
    }
    return NO_FLUSH_7;
  }

  static short[] NO_FLUSH_8(){
    if(NO_FLUSH_8 == null){
      NO_FLUSH_8 = loadFromFile("HashTable8");
    }
    return NO_FLUSH_8;
  }

  static short[] NO_FLUSH_9(){
    if(NO_FLUSH_9 == null){
      NO_FLUSH_9 = loadFromFile("HashTable9");
    }
    return NO_FLUSH_9;
  }

}
