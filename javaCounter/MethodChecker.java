package com.codeparser;

import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.MethodCallExpr;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;

public class MethodChecker {
    private HashMap<String, Integer> FUNCTION;
    private HashMap<String, MethodDeclaration> methodNodeMap;
    private MethodCallExpr curMethod;

    public MethodChecker(){
        FUNCTION = new HashMap<>();
        methodNodeMap = new HashMap<>();
        curMethod = null;
    }
    public HashMap<String, Integer> getFunctionMap(){
        return FUNCTION;
    }
    public void setCurMethod(MethodCallExpr method){
        curMethod = method;
    }
    public MethodCallExpr getCurMethod(){
        return curMethod;
    }

    public MethodDeclaration getMethodNode(String methodName){
        return methodNodeMap.getOrDefault(methodName, null);
    }

    public void countFunctionIntoMap(MethodDeclaration funcNode){
        String funcName = funcNode.getNameAsString();
        if(funcName.equals("compare")||funcName.equals("compareTo")||funcName.equals("toString")) return;
        if(FUNCTION.containsKey(funcName))
            FUNCTION.put(funcName, FUNCTION.get(funcName) + 1);

        else {
            FUNCTION.put(funcName, 1);
            methodNodeMap.put(funcName, funcNode);
        }
    }

    public int countTotalFunctionData(){
        Set keySet = FUNCTION.keySet();
        int sum = 0;
        Iterator iter = keySet.iterator();

        while(iter.hasNext()){
            String key = (String) iter.next();
            sum = sum + FUNCTION.get(key);
        }
        return sum;
    }
}
