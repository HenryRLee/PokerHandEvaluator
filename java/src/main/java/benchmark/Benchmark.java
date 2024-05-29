package benchmark;

import evaluator.Evaluator;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.file.Path;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

/**
 * Benchmarks the evaluation methods. Iterates through every single possible hand (n choose k where k is the amount of cards
 * being evaluated) and prints to stdout. This reads from a default properties file to retrieve the settings.
 * When ran you can enter the file through command line args to use different properties than the default ones. Setting
 * threads=0 results in using Runtime#getAvailableProcessors for threads.
 */
public class Benchmark{

  private static final Path DEFAULT_CONFIG = Path.of("src", "main", "resources", "default_bench.properties");

  private static final Map<Integer, String> BENCH_CONFIG_TO_INDEX = new HashMap<>();

  private static final Properties BENCH_CONFIG = new Properties();

  static{
    BENCH_CONFIG_TO_INDEX.put(0, "a5c");
    BENCH_CONFIG_TO_INDEX.put(1, "a6c");
    BENCH_CONFIG_TO_INDEX.put(2, "a7c");
    BENCH_CONFIG_TO_INDEX.put(3, "a8c");
    BENCH_CONFIG_TO_INDEX.put(4, "a9c");
  }

  private static final String[] OSTRINGS = {"All 5-card Hands", "All 6-card Hands", "All 7-card Hands", "All 8-card Hands", "All 9-card Hands"};
  private static final Runnable[] ORUNNABLES = {Benchmark::eval5, Benchmark::eval6, Benchmark::eval7, Benchmark::eval8, Benchmark::eval9};
  private static final long[] OHANDS_PER_ITERATION = {2598960, 20358520, 133784560, 752538150, 3679075400L};

  private static PrintStream out;

  public static void main(String[] args){
    Path customProps = null;
    if(args.length > 0){
      customProps = Path.of(args[0]);
    }

    try{
      loadProperties(DEFAULT_CONFIG);
      if(customProps != null){
        loadProperties(customProps);
      }
    }catch(IOException e){
      e.printStackTrace();
      System.err.println("Unable to load property files.");
      System.exit(12);
    }

    initValues();

    for(int i = 0; i < BENCH_CONFIG_TO_INDEX.size(); i++){
      String s = BENCH_CONFIG_TO_INDEX.get(i);
      boolean run = Boolean.parseBoolean(BENCH_CONFIG.getProperty(s + ".run"));
      if(!run) continue;

      int iterations = Integer.parseInt(BENCH_CONFIG.getProperty(s + ".iterations"));

      runBenchmark(ORUNNABLES[i], OSTRINGS[i], OHANDS_PER_ITERATION[i], iterations, threads);
    }
  }

  private static long startTime;

  private static int threads;

  private static void loadProperties(Path p) throws IOException{
    BENCH_CONFIG.load(new FileReader(p.toFile()));
  }

  private static void initValues(){
    System.out.println("Initializing config.");

    if(BENCH_CONFIG.get("output").equals("std")){
      out = System.out;
      out.println("Output set to stdout.");
    }else{
      Path outPath = Path.of((String) BENCH_CONFIG.get("output"));
      try{
        out = new PrintStream(outPath.toFile());
      }catch(FileNotFoundException e){
        e.printStackTrace();
        System.err.println("Unable to load output file.");
        System.exit(11);
      }
      out.println("Out set to " + outPath.getFileName() + ".");
    }

    threads = Integer.parseInt((String) BENCH_CONFIG.get("threads"));
    if(threads < 0) threads = 1;
    if(threads == 0) threads = Runtime.getRuntime().availableProcessors();
    out.println("Running on " + threads + " threads.");

    int runs = 0;
    for(String s : BENCH_CONFIG_TO_INDEX.values()){
      if(BENCH_CONFIG.getProperty(s + ".run").equals("true")){
        runs++;
      }
    }
    out.println("Running " + runs + " different benchmarks.");
  }

  //TODO: Maybe impl, not sure how important this is
  private static int[][] randomCards(int samples, int cardsPerSample){
    int[][] retCards = new int[samples][cardsPerSample];

    List<Integer> cards = new ArrayList<>();
    for(int i = 0; i < 52; i++){
      cards.add(i);
    }

    for(int i = 0; i < samples; i++){
      Collections.shuffle(cards);
      for(int j = 0; j < cardsPerSample; j++){
        retCards[i][j] = cards.get(j);
      }
    }

    return retCards;
  }

  private static void initBenchmark(){
    startTime = System.currentTimeMillis();
  }

  private static long endBenchmarkTimer(){
    return System.currentTimeMillis() - startTime;
  }

  private static void runBenchmark(Runnable r, String type, long handsPerIteration, int iterations, int threads){
    out.println(String.format("Initializing %s benchmark running %d iterations at %d hands per iteration.", type, iterations, handsPerIteration));
    initBenchmark();
    ExecutorService es;
    if(threads == 1){
      es = null;
    }else{
      es = Executors.newFixedThreadPool(threads);
    }

    for(int i = 0; i < iterations; i++){
      if(es != null){
        es.submit(r);
      }else{
        r.run();
      }
    }

    if(es != null){
      es.shutdown();
      try{
        es.awaitTermination(20, TimeUnit.MINUTES);
      }catch(InterruptedException ignored){
      }
    }

    long benchMS = endBenchmarkTimer();
    long hands = handsPerIteration * iterations;
    hands /= 1000;
    hands /= benchMS;

    out.println(String.format("%s --- %dms --- %dM/s", type, benchMS, hands));

  }

  // 2,598,960 hands per iteration
  private static void eval5(){
    for(int i = 0; i < 46; i++){
      for(int j = i + 1; j < 47; j++){
        for(int k = j + 1; k < 48; k++){
          for(int l = k + 1; l < 49; l++){
            for(int m = l + 1; m < 50; m++){
              Evaluator.evaluate(i, j, k, l, m);
            }
          }
        }
      }
    }
  }

  private static void eval6(){
    for(int i = 0; i < 47; i++){
      for(int j = i + 1; j < 48; j++){
        for(int k = j + 1; k < 49; k++){
          for(int l = k + 1; l < 50; l++){
            for(int m = l + 1; m < 51; m++){
              for(int n = m + 1; n < 52; n++){
                Evaluator.evaluate(i, j, k, l, m, n);
              }
            }
          }
        }
      }
    }
  }

  // 133,784,560 hands per iteration
  private static void eval7(){
    int z = 0;
    for(int i = 0; i < 46; i++){
      for(int j = i + 1; j < 47; j++){
        for(int k = j + 1; k < 48; k++){
          for(int l = k + 1; l < 49; l++){
            for(int m = l + 1; m < 50; m++){
              for(int n = m + 1; n < 51; n++){
                for(int o = n + 1; o < 52; o++){
                  Evaluator.evaluate(i, j, k, l, m, n, o);
                }
              }
            }
          }
        }
      }
    }
  }

  private static void eval8(){
    for(int i = 0; i < 45; i++){
      for(int j = i + 1; j < 46; j++){
        for(int k = j + 1; k < 47; k++){
          for(int l = k + 1; l < 48; l++){
            for(int m = l + 1; m < 49; m++){
              for(int n = m + 1; n < 50; n++){
                for(int o = n + 1; o < 51; o++){
                  for(int p = o + 1; p < 52; p++){
                    Evaluator.evaluate(i, j, k, l, m, n, o, p);
                  }
                }
              }
            }
          }
        }
      }
    }
  }

  private static void eval9(){
    for(int i = 0; i < 44; i++){
      for(int j = i + 1; j < 45; j++){
        for(int k = j + 1; k < 46; k++){
          for(int l = k + 1; l < 47; l++){
            for(int m = l + 1; m < 48; m++){
              for(int n = m + 1; n < 49; n++){
                for(int o = n + 1; o < 50; o++){
                  for(int p = o + 1; p < 51; p++){
                    for(int q = p + 1; q < 52; q++){
                      Evaluator.evaluate(i, j, k, l, m, n, o, p, q);
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }

}
