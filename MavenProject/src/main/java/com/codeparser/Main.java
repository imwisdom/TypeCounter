package com.codeparser;

import java.io.*;

public class Main {
    public static void main(String[] args) throws FileNotFoundException {

        String trainingFileName = args[0];
        String testFileName = args[1];
//        String trainingFileName = "/home/oem/Desktop/trainingJava.java";
//        String testFileName = "/home/oem/Desktop/testJava.java";

        JavaCodeParser javaCodeParser = new JavaCodeParser(trainingFileName);
        javaCodeParser.parse();
        TypeChecker trainingTypeChecker = javaCodeParser.getTypeChecker();

        javaCodeParser = new JavaCodeParser(testFileName);
        javaCodeParser.parse();
        TypeChecker testTypeChecker = javaCodeParser.getTypeChecker();

        CodeEvaluator codeEvaluator = new CodeEvaluator
                (trainingTypeChecker, testTypeChecker);

        System.out.println(codeEvaluator.evaluateWrongAnswer());
    }
}

