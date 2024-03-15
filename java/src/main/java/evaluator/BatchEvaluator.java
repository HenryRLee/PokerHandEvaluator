package evaluator;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletionService;
import java.util.concurrent.ExecutorCompletionService;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.Collectors;

/**
 * Allows processing of large numbers of evaluations concurrently.
 */
public class BatchEvaluator{

  /**
   * @param nThreads <= 0 results in Runtime#availableProcessors as your thread amount. Otherwise the amount of threads
   *                 in the thread pool
   */
  public BatchEvaluator(int nThreads){
    if(nThreads <= 0){
      nThreads = Runtime.getRuntime().availableProcessors();
    }
    this.nThreads = nThreads;
    executor = Executors.newFixedThreadPool(nThreads);
  }

  public BatchEvaluator(){
    this(0);
  }

  private final int nThreads;

  private final ExecutorService executor;

  /**
   * Submits an batch to be processed. This will automatically break it into a larger amount of mini-batches based off the
   * number of threads. This function returns the input list and maintains the order of elements. Hangs until the entire
   * batch is completed.
   *
   * @param inputs List of batch elements
   * @return The same list of batch elements, with their result field populated
   */
  public List<BatchElement> submitBatch(List<BatchElement> inputs){
    int nBatches = nThreads;
    var batches = reduce(inputs, nBatches);
    System.out.println("Beginning processing of " + inputs.size() + " inputs.");

    CompletionService<BatchEvaluator> completionService = new ExecutorCompletionService<>(executor);
    var futures = batches.stream().map(r -> completionService.submit(r, null)).collect(Collectors.toList());
    for(Runnable r : batches){
      completionService.submit(r, this);
    }

    for(int i = 0; i < futures.size(); i++){
      try{
        completionService.take();
        System.out.println(String.format("Completed %d of %d batches.", i + 1, nBatches));

      }catch(InterruptedException e){
        e.printStackTrace();
      }
    }

    return inputs;
  }

  public void close(){
    executor.shutdown();
  }

  private List<Runnable> reduce(List<BatchElement> inputs, int nBatches){
    int batchSize = inputs.size() / nBatches;
    List<Runnable> batches = new ArrayList<>(nBatches);

    for(int i = 0; i < nBatches; i++){
      final int lowerBound = i * batchSize;
      final int upperBound = (i + 1) * batchSize;

      Runnable batch = () -> {
        for(int j = lowerBound; j < upperBound; j++){
          int res = Evaluator.evaluate(inputs.get(j).inputs);
          inputs.get(j).setResult(res);
        }
      };

      batches.add(batch);
    }

    return batches;
  }

}
