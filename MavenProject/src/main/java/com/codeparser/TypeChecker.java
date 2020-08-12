package com.codeparser;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

public class TypeChecker {

    HashMap<String, Object[]> MAP; //{'map', ['<Integer, Integer>', 2]}
    HashMap<String, Integer> LIST;
    HashMap<String, Integer> ARRAY;
    HashMap<String, Integer> TABLE;
    HashMap<String, Integer> SET;
    HashMap<String, Integer> NODE;
    HashMap<String, Integer> STACK;
    HashMap<String, Integer> QUEUE;
    HashMap<String, Integer> PRIORITYQUEUE;
    HashMap<String, Integer> DEQUE;

    public TypeChecker(){
        MAP = new HashMap<>();
        LIST = new HashMap<>();
        ARRAY = new HashMap<>();
        TABLE = new HashMap<>();
        SET = new HashMap<>();
        NODE = new HashMap<>();
        STACK = new HashMap<>();
        QUEUE = new HashMap<>();
        PRIORITYQUEUE = new HashMap<>();
        DEQUE = new HashMap<>();

    }
    public void countVariableIntoMap(String varName, String varType){

        if(varType.contains("Map")){
            String mapType = "";
            if(varType.contains("<"))
                mapType = varType.substring(varType.indexOf("<"), varType.lastIndexOf(">")+1);
            else mapType = "null";
            if(MAP.containsKey(varName)) {
                Object[] mapValue = MAP.get(varName);
                mapValue[1] = (int)mapValue[1]+1;
                MAP.put(varName, mapValue);
            }
            else
                MAP.put(varName, new Object[]{mapType, 1});
        }
        else if(varType.contains("Stack")){
            if(STACK.containsKey(varName))
                STACK.put(varName, (STACK.get(varName)+1));
            else
                STACK.put(varName, 1);
        }
        else if(varType.contains("PriorityQueue")){
            if(PRIORITYQUEUE.containsKey(varName))
                PRIORITYQUEUE.put(varName, (PRIORITYQUEUE.get(varName)+1));
            else
                PRIORITYQUEUE.put(varName, 1);
        }
        else if(varType.contains("Deque")){
            if(DEQUE.containsKey(varName))
                DEQUE.put(varName, (DEQUE.get(varName)+1));
            else
                DEQUE.put(varName, 1);
        }
        else if(varType.contains("Queue")){
            if(QUEUE.containsKey(varName))
                QUEUE.put(varName, (QUEUE.get(varName)+1));
            else
                QUEUE.put(varName, 1);
        }
        else if(varType.contains("List")){
            if(LIST.containsKey(varName))
                LIST.put(varName, (LIST.get(varName)+1));
            else
                LIST.put(varName, 1);
        }
        else if(varType.contains("Table")){
            if(TABLE.containsKey(varName))
                TABLE.put(varName, (TABLE.get(varName)+1));
            else
                TABLE.put(varName, 1);
        }
        else if(varType.contains("Set")){
            if(SET.containsKey(varName))
                SET.put(varName, (SET.get(varName)+1));
            else
                SET.put(varName, 1);
        }
        else if(varType.contains("Node")){
            if(NODE.containsKey(varName))
                NODE.put(varName, (NODE.get(varName)+1));
            else
                NODE.put(varName, 1);
        }
        else if(varType.contains("[") && varType.contains("]")){
            if(ARRAY.containsKey(varName))
                ARRAY.put(varName, (ARRAY.get(varName)+1));
            else
                ARRAY.put(varName, 1);
        }
    }
    public void countVariableIntoMap(String varName){

        if(MAP.containsKey(varName)) {
            Object[] mapValue = MAP.get(varName);
            mapValue[1] = (int)mapValue[1]+1;

            MAP.put(varName, mapValue);
        }
        else if(STACK.containsKey(varName))
            STACK.put(varName, (STACK.get(varName)+1));
        else if(LIST.containsKey(varName))
            LIST.put(varName, (LIST.get(varName)+1));
        else if(ARRAY.containsKey(varName))
            ARRAY.put(varName, (ARRAY.get(varName)+1));
        else if(TABLE.containsKey(varName))
            TABLE.put(varName, (TABLE.get(varName)+1));
        else if(SET.containsKey(varName))
            SET.put(varName, (SET.get(varName)+1));
        else if(NODE.containsKey(varName))
            NODE.put(varName, (NODE.get(varName)+1));
        else if(PRIORITYQUEUE.containsKey(varName))
            PRIORITYQUEUE.put(varName, (PRIORITYQUEUE.get(varName)+1));
        else if(QUEUE.containsKey(varName))
            QUEUE.put(varName, (QUEUE.get(varName)+1));
        else if(DEQUE.containsKey(varName))
            DEQUE.put(varName, (DEQUE.get(varName)+1));

    }
    public HashMap<String, Integer> getTotalMapData(){
        HashMap<String, Integer> totalMap = new HashMap<>();

        Set keySet = MAP.keySet();

        Iterator iter = keySet.iterator();

        while(iter.hasNext()){
            String key = (String) iter.next();
            Object[] mapValue = MAP.get(key);

            String keyOfMapValue = (String)mapValue[0];
            if(totalMap.containsKey(keyOfMapValue)){
                totalMap.put(keyOfMapValue, totalMap.get(keyOfMapValue)+(int)mapValue[1]);
            }
            else{
                totalMap.put(keyOfMapValue, (int)mapValue[1]);
            }
        }
        return totalMap;
    }
    public int countTotalMapData(){
        int sum = 0;
        Set keySet = MAP.keySet();

        Iterator iter = keySet.iterator();

        while(iter.hasNext()){
            String key = (String) iter.next();
            Object[] mapValue = MAP.get(key);

            sum = sum + (int)mapValue[1];
        }
        return sum;
    }
    public int countTotalStackData(){
        Set keySet = STACK.keySet();
        int sum = 0;
        Iterator iter = keySet.iterator();

        while(iter.hasNext()){
            String key = (String) iter.next();
            sum = sum + STACK.get(key);
        }
        return sum;
    }
    public int countTotalQueueData(){
        Set keySet = QUEUE.keySet();
        int sum = 0;
        Iterator iter = keySet.iterator();

        while(iter.hasNext()){
            String key = (String) iter.next();
            sum = sum + QUEUE.get(key);
        }
        return sum;
    }
    public int countTotalListData(){
        Set keySet = LIST.keySet();
        int sum = 0;
        Iterator iter = keySet.iterator();

        while(iter.hasNext()){
            String key = (String) iter.next();
            sum = sum + LIST.get(key);
        }
        return sum;
    }
    public int countTotalArrayData(){
        Set keySet = ARRAY.keySet();
        int sum = 0;
        Iterator iter = keySet.iterator();

        while(iter.hasNext()){
            String key = (String) iter.next();
            sum = sum + ARRAY.get(key);
        }
        return sum;
    }
    public int countTotalTableData(){
        Set keySet = TABLE.keySet();
        int sum = 0;
        Iterator iter = keySet.iterator();

        while(iter.hasNext()){
            String key = (String) iter.next();
            sum = sum + TABLE.get(key);
        }
        return sum;
    }
    public int countTotalSetData(){
        Set keySet = SET.keySet();
        int sum = 0;
        Iterator iter = keySet.iterator();

        while(iter.hasNext()){
            String key = (String) iter.next();
            sum = sum + SET.get(key);
        }
        return sum;
    }
    public int countTotalNodeData(){
        Set keySet = NODE.keySet();
        int sum = 0;
        Iterator iter = keySet.iterator();

        while(iter.hasNext()){
            String key = (String) iter.next();
            sum = sum + NODE.get(key);
        }
        return sum;
    }
    public int countTotalPriorityQueueData(){
        Set keySet = PRIORITYQUEUE.keySet();
        int sum = 0;
        Iterator iter = keySet.iterator();

        while(iter.hasNext()){
            String key = (String) iter.next();
            sum = sum + PRIORITYQUEUE.get(key);
        }
        return sum;
    }
    public int countTotalDequeData(){
        Set keySet = DEQUE.keySet();
        int sum = 0;
        Iterator iter = keySet.iterator();

        while(iter.hasNext()){
            String key = (String) iter.next();
            sum = sum + DEQUE.get(key);
        }
        return sum;
    }

}
