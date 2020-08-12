import com.codeparser.JavaCodeParser;
import org.junit.Test;

import java.io.FileNotFoundException;

class JavaCodeParserTest {

    @Test
    public void getRootCode() throws FileNotFoundException {
        JavaCodeParser javaCodeParser = new JavaCodeParser("/home/oem/Desktop/test4.java");

    }
}