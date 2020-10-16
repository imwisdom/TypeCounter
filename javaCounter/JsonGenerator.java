package com.codeparser;

import java.io.FileNotFoundException;

public class JsonGenerator {

    public static void main(String[] args) throws FileNotFoundException {

        String fileName = "/home/oem/Desktop/testJava.java";
        //String fileName = args[0];
        JavaCodeParser javaCodeParser = new JavaCodeParser(fileName);
        javaCodeParser.parse();
        TypeChecker typeChecker = javaCodeParser.getTypeChecker();

        System.out.println(typeChecker.getJsonString());
    }
}
