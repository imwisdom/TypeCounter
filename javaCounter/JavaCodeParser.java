package com.codeparser;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.*;
import com.github.javaparser.ast.expr.AssignExpr;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.expr.SimpleName;
import com.github.javaparser.ast.stmt.ForStmt;
import com.github.javaparser.ast.stmt.WhileStmt;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;

public class JavaCodeParser {

    private final int LOOP_COUNT = 8;
    private final int RECV_COUNT = 4;
    private CompilationUnit compilationUnit;
    private TypeChecker typeChecker;
    private MethodChecker methodChecker;

    public JavaCodeParser(String code) throws FileNotFoundException {
        this.compilationUnit = StaticJavaParser.parse(new File(code));
        this.typeChecker = new TypeChecker();
        this.methodChecker = new MethodChecker();
    }
    public void parse() {
        countObjectTypeInEachClass(this.compilationUnit.getChildNodes());
    }
    private void countObjectTypeInEachClass(List<Node> nodeList){
        ClassOrInterfaceDeclaration mainClass = null;
        for(int i=0;i<nodeList.size();i++){
            Node node = nodeList.get(i);

            if(node instanceof ClassOrInterfaceDeclaration && node.toString().contains("public static void main"))
                mainClass = (ClassOrInterfaceDeclaration) node;
            else
                countObjectType(node.getChildNodes());
        }
        countObjectType(mainClass.getChildNodes());
    }
    private void countObjectType(List<Node> nodeList){
        MethodDeclaration mainNode = null;
        for(int i=0;i<nodeList.size();i++){
            Node node = nodeList.get(i);

            if(node instanceof ForStmt || node instanceof WhileStmt){
                for(int loop=0;loop<LOOP_COUNT;loop++){
                    countObjectType(node.getChildNodes());
                }
            }
            else if(node instanceof MethodDeclaration){
                MethodDeclaration methodNode = (MethodDeclaration) node;

                if(i<nodeList.size()-1 && methodNode.getName().asString().equals("main")){
                    mainNode = methodNode;
                }
                else if(methodNode.getName().asString().equals("main")){
                    countObjectType(methodNode.getChildNodes());
                }
                else {
                    methodChecker.countFunctionIntoMap((MethodDeclaration) node);
                }

            }
            else if(node instanceof MethodCallExpr){
                MethodCallExpr methodExprNode = (MethodCallExpr)node;
                String methodName = methodExprNode.getNameAsString();

                if(methodExprNode.getScope().isPresent() && methodExprNode.getScope().get().toString().equals("Math")){
                    countObjectType((List)methodExprNode.getArguments());
                    continue;
                }
                MethodDeclaration methodNode = methodChecker.getMethodNode(methodName);
                if(methodNode != null) {
                    countObjectTypeInMethod(methodNode.getChildNodes(), methodName, 0);
                    methodChecker.countFunctionIntoMap(methodNode);
                }
                else
                    countObjectType(methodExprNode.getChildNodes());
            }
            else if(node instanceof VariableDeclarator){
                VariableDeclarator varNode = (VariableDeclarator) node;

                String varName = varNode.getNameAsString();
                String varType = varNode.getTypeAsString();
                typeChecker.countVariableIntoMap(varName, varType);

                if(varNode.getChildNodes().size() > 2){
                    countObjectType(varNode.getChildNodes());
                }
            }
//            else if(node instanceof AssignExpr){
//                AssignExpr assNode = (AssignExpr) node;
//                Node targetNode = assNode.getTarget();
//                Node valueNode = assNode.getValue();
//
//                countObjectType(targetNode.getChildNodes());
//                countObjectType(valueNode.getChildNodes());
//            }
            else if(node instanceof FieldDeclaration){
                List<VariableDeclarator> varNodeList = ((FieldDeclaration)node).getVariables();
                for(VariableDeclarator varNode : varNodeList){
                    String varName = varNode.getNameAsString();
                    String varType = varNode.getTypeAsString();
                    typeChecker.countVariableIntoMap(varName, varType);
                }
            }
            else if(node instanceof SimpleName){
                SimpleName name = (SimpleName) node;
                typeChecker.countVariableIntoMap(name.asString());

            }
            else if(node.getChildNodes().size() > 0)
                countObjectType(node.getChildNodes());
        }
        if(mainNode != null){
            countObjectType(mainNode.getChildNodes());
        }
    }
    public void countObjectTypeInMethod(List<Node> nodeList, String funcName, int recv){

        if(recv==RECV_COUNT) {
            return;
        }

        for(int i=0;i<nodeList.size();i++){
            Node node = nodeList.get(i);

            if(node instanceof ForStmt || node instanceof WhileStmt){
                for(int loop=0;loop<LOOP_COUNT;loop++){
                    countObjectTypeInMethod(node.getChildNodes(), funcName, recv);
                }
            }
            else if(node instanceof MethodDeclaration){
                MethodDeclaration methodNode = (MethodDeclaration) node;
                methodChecker.countFunctionIntoMap(methodNode);
            }
            else if(node instanceof MethodCallExpr){
                MethodCallExpr methodExprNode = (MethodCallExpr)node;
                String methodName = methodExprNode.getNameAsString();

                if(methodExprNode.getScope().isPresent() && methodExprNode.getScope().get().toString().equals("Math")){
                    countObjectTypeInMethod((List)methodExprNode.getArguments(), funcName, recv);
                    continue;
                }
                MethodDeclaration methodNode = methodChecker.getMethodNode(methodName);
                if(methodNode != null) {

                    boolean isRecursive = methodName.equals(funcName);
                    if(!isRecursive){
                        countObjectTypeInMethod(methodNode.getChildNodes(), methodName, recv);
                    }
                    else{
                        countObjectTypeInMethod(methodNode.getChildNodes(), funcName, recv+1);
                    }
                    methodChecker.countFunctionIntoMap(methodNode);
                }
                else
                    countObjectTypeInMethod(methodExprNode.getChildNodes(), funcName, recv);
            }
            else if(node instanceof VariableDeclarator){
                VariableDeclarator varNode = (VariableDeclarator) node;

                String varName = varNode.getNameAsString();
                String varType = varNode.getTypeAsString();
                typeChecker.countVariableIntoMap(varName, varType);

                if(varNode.getChildNodes().size() > 2){
                    countObjectTypeInMethod(varNode.getChildNodes(), funcName, recv);
                }
            }
//            else if(node instanceof AssignExpr){
//                AssignExpr assNode = (AssignExpr) node;
//                Node targetNode = assNode.getTarget();
//                Node valueNode = assNode.getValue();
//
//                countObjectTypeInMethod(targetNode.getChildNodes());
//                countObjectTypeInMethod(valueNode.getChildNodes());
//            }
            else if(node instanceof FieldDeclaration){
                List<VariableDeclarator> varNodeList = ((FieldDeclaration)node).getVariables();
                for(VariableDeclarator varNode : varNodeList){
                    String varName = varNode.getNameAsString();
                    String varType = varNode.getTypeAsString();
                    typeChecker.countVariableIntoMap(varName, varType);
                }
            }
            else if(node instanceof SimpleName){
                SimpleName name = (SimpleName) node;
                typeChecker.countVariableIntoMap(name.asString());

            }
            else if(node instanceof Parameter){
                Parameter param = (Parameter) node;
                String varName = param.getNameAsString();
                String varType = param.getTypeAsString();
                typeChecker.countVariableIntoMap(varName, varType);

            }
            else if(node.getChildNodes().size() > 0)
                countObjectTypeInMethod(node.getChildNodes(), funcName, recv);
        }
    }

    public void printCountResult(){
        System.out.println("Map: "+typeChecker.countTotalMapData());
        System.out.println("Stack: "+typeChecker.countTotalStackData());
        System.out.println("Queue: "+typeChecker.countTotalQueueData());
        System.out.println("List: "+typeChecker.countTotalListData());
        System.out.println("Array: "+typeChecker.countTotalArrayData());
        System.out.println("Table: "+typeChecker.countTotalTableData());
        System.out.println("Set: "+typeChecker.countTotalSetData());
        System.out.println("Node: "+typeChecker.countTotalNodeData());
        System.out.println("Func: "+methodChecker.countTotalFunctionData());
    }
    public TypeChecker getTypeChecker(){
        return typeChecker;
    }
    public MethodChecker getMethodChecker(){
        return methodChecker;
    }

}
