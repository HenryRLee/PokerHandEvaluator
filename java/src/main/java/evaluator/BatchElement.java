package evaluator;

/**
 * A single operation in a batch. BatchId is mostly not needed but can be used as a method of keeping every element
 * unique however in general the inputs should guarantee uniqueness regardless.
 */
public class BatchElement{

  public BatchElement(int batchId, int[] inputs){
    this.batchId = batchId;
    this.inputs = inputs;
  }

  private final int batchId;

  /**
   * Inputs into our evaluator
   */
  public final int[] inputs;

  /**
   * The result of the evaluation function. Initialized at -1 to ensure that any other value means the evaluation was
   * successful.
   */
  private int result = -1;

  public int getResult(){
    return result;
  }

  void setResult(int result){
    this.result = result;
  }


}
