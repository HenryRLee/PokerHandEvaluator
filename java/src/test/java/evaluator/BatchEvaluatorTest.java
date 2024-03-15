package evaluator;

import com.opencsv.bean.CsvToBeanBuilder;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertEquals;

public class BatchEvaluatorTest{

  private BatchEvaluator evaluator;

  private List<IdTestInputBean> beans;

  private static List<IdTestInputBean> readFile(String fileNumber) throws IOException{
    var path = Path.of("../", "test", fileNumber, "id_input_tests.csv");

    var beans = new CsvToBeanBuilder<IdTestInputBean>(new FileReader(path.toFile())).withType(IdTestInputBean.class);
    return beans.build().parse();
  }

  @Before
  public void setUp() throws Exception{
    evaluator = new BatchEvaluator(2);
    beans = readFile("seven");
  }

  @After
  public void tearDown() throws Exception{
    evaluator.close();
  }

  @Test
  public void submitBatch(){
    var batchElements = new ArrayList<BatchElement>();
    for(var bean : beans){
      batchElements.add(new BatchElement(0, bean.arr(7)));
    }
    evaluator.submitBatch(batchElements);

    for(int i = 0; i < batchElements.size(); i++){
      var ele = batchElements.get(i);
      var bean = beans.get(i);
      assertArrayEquals(ele.inputs, bean.arr(7));
      assertEquals(ele.getResult(), bean.rank);
    }
  }
}
