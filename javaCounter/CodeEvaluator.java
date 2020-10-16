package com.codeparser;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;

public class CodeEvaluator {

    private TypeChecker trainingTypeChecker;
    private TypeChecker testTypeChecker;
    private final int NUM_OF_TYPE = 9;

    public CodeEvaluator(TypeChecker trainingTypeChecker, TypeChecker testTypeChecker) {
        this.trainingTypeChecker = trainingTypeChecker;
        this.testTypeChecker = testTypeChecker;

    }

    private String evaluateAboutMapType() {
        HashMap<String, Integer> trainingMap = trainingTypeChecker.getTotalMapData();
        HashMap<String, Integer> testMap = testTypeChecker.getTotalMapData();
        if (trainingMap.size() == 0) return "";

        Set testMapkeySet = testMap.keySet();
        Iterator<String> iter = testMapkeySet.iterator();

        while (iter.hasNext()) {
            String curKey = iter.next();
            if (curKey.equals("null")) continue;
            if (!trainingMap.containsKey(curKey) && (curKey.contains("Integer") || curKey.contains("List")
                    || curKey.contains("String") || curKey.contains("Map") || curKey.contains("Character")))
                return "Map의 자료형을 " + curKey + "로 사용해 보세요";
        }
        return "";
    }

    private String evaluateAboutTypeCount(int[] trainingCount, int[] testCount) {

        int maxIndex = 0;
        double max = 0;
        for (int i = 0; i < NUM_OF_TYPE; i++) {
            double cur = (double) Math.abs(testCount[i] - trainingCount[i]) / (double) testCount[i];

            if (cur > max) {
                max = cur;
                maxIndex = i;
            }
        }
        if (max == 0.0) {
            return "사소한 값들이 잘못 설정되어있음";
        }
        switch (maxIndex) {
            case 0:
                return "Map 사용 방식이 잘못됨";
            case 1:
                return "List 사용 방식이 잘못됨";
            case 2:
                return "Array 사용 방식이 잘못됨";
            case 3:
                return "Stack 사용 방식이 잘못됨";
            case 4:
                return "Queue 사용 방식이 잘못됨";
            case 5:
                return "Set 사용 방식이 잘못됨";
            case 6:
                return "Table 사용 방식이 잘못됨";
//            case 7 :
//                return "Node 사용 방식이 잘못됨";
            case 7:
                return "PriorityQueue 사용 방식이 잘못됨";
            case 8:
                return "Deque 사용 방식이 잘못됨";
        }
        return "";

    }

    private String evaluateAboutUnusedType(int[] trainingCount, int[] testCount) {
        for (int i = 0; i < NUM_OF_TYPE; i++) {
            if (trainingCount[i] == 0 && testCount[i] > 0) {
                switch (i) {
                    case 0:
                        return "Map을 사용해 보세요";
                    case 1:
                        return "List를 사용해 보세요";
                    case 2:
                        return "Array를 사용해 보세요";
                    case 3:
                        return "Stack을 사용해 보세요";
                    case 4:
                        return "Queue를 사용해 보세요";
                    case 5:
                        return "Set을 사용해 보세요";
                    case 6:
                        return "Table을 사용해 보세요";
//                    case 7 :
//                        return "Node를 사용해 보세요";
                    case 7:
                        return "PriorityQueue를 사용해 보세요";
                    case 8:
                        return "Deque를 사용해 보세요";
                }
            }
        }
        return "";
    }

    public String evaluateWrongAnswer() {
        String evaluateAboutMapType = evaluateAboutMapType();
        if (!evaluateAboutMapType.equals("")) return evaluateAboutMapType;
        else {
            int[] trainingCount = new int[NUM_OF_TYPE];
            int[] testCount = new int[NUM_OF_TYPE];

            trainingCount[0] = trainingTypeChecker.countTotalMapData();
            testCount[0] = testTypeChecker.countTotalMapData();

            trainingCount[1] = trainingTypeChecker.countTotalListData();
            testCount[1] = testTypeChecker.countTotalListData();

            trainingCount[2] = trainingTypeChecker.countTotalArrayData();
            testCount[2] = testTypeChecker.countTotalArrayData();

            trainingCount[3] = trainingTypeChecker.countTotalStackData();
            testCount[3] = testTypeChecker.countTotalStackData();

            trainingCount[4] = trainingTypeChecker.countTotalQueueData();
            testCount[4] = testTypeChecker.countTotalQueueData();

            trainingCount[5] = trainingTypeChecker.countTotalSetData();
            testCount[5] = testTypeChecker.countTotalSetData();

            trainingCount[6] = trainingTypeChecker.countTotalTableData();
            testCount[6] = testTypeChecker.countTotalTableData();

//            trainingCount[7] = trainingTypeChecker.countTotalNodeData();
//            testCount[7] = testTypeChecker.countTotalNodeData();

            trainingCount[7] = trainingTypeChecker.countTotalPriorityQueueData();
            testCount[7] = testTypeChecker.countTotalPriorityQueueData();

            trainingCount[8] = trainingTypeChecker.countTotalDequeData();
            testCount[8] = testTypeChecker.countTotalDequeData();

            String evaluateAboutUnusedType = evaluateAboutUnusedType(trainingCount, testCount);

            if (!evaluateAboutUnusedType.equals(""))
                return evaluateAboutUnusedType;
            else return evaluateAboutTypeCount(trainingCount, testCount);
        }
    }
}
