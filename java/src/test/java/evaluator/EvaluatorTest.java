package evaluator;

import com.opencsv.bean.CsvToBeanBuilder;
import org.junit.Test;

import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.assertEquals;

public class EvaluatorTest{

  private static List<IdTestInputBean> readFile(String fileNumber) throws IOException{
    var path = Path.of("../", "test", fileNumber, "id_input_tests.csv");

    var beans = new CsvToBeanBuilder<IdTestInputBean>(new FileReader(path.toFile())).withType(IdTestInputBean.class);
    return beans.build().parse();
  }

  @Test
  public void evaluate5() throws IOException{
    var tests = readFile("five");
    tests.forEach(bean -> assertEquals(bean.rank, Evaluator.evaluate(bean.arr(5))));
  }

  @Test
  public void evaluate6() throws IOException{
    var tests = readFile("six");
    tests.forEach(bean -> assertEquals(Arrays.toString(bean.arr(6)), bean.rank, Evaluator.evaluate(bean.arr(6))));
  }

  @Test
  public void evaluate7() throws IOException{
    var tests = readFile("seven");
    tests.forEach(bean -> assertEquals(bean.rank, Evaluator.evaluate(bean.arr(7))));
  }

}
