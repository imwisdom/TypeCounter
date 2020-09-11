import pymysql
import subprocess
from python_checker import dict_total_data
import json


def get_data_in_java(cursor, problem_num):
    sql = '''

        select s.submitid, j.result from `submission` as s join `language` as l join `judging`
        as j on s.submitid=j.submitid and s.langid = l.langid where s.submitid>=3471 and s.submitid<=5470
        and j.result="correct" and l.name = "java" and s.probid = ''' + problem_num + ''' order by s.probid

        '''
    cursor.execute(sql)
    submission_data = cursor.fetchall()

    if len(submission_data) == 0:
        return None, None

    total_dict_data = {}
    min_dict_data = {}
    max_dict_data = {}
    count_dict_data = {}
    for submit in submission_data:
        submit_id = submit[0]

        code_sql = '''
                select sourcecode from submission_file where submitid=%s;
            '''
        cursor.execute(code_sql, submit_id)
        correct_source_code = cursor.fetchall()[0][0].decode()

        correct_source_code = correct_source_code.split("\n")
        f = open("/home/oem/Desktop/testJava.java", "w")

        for code in correct_source_code:
            f.write(code + "\n")
        f.close()

        proc = subprocess.check_output(
            ["java", "-jar", "/home/oem/IdeaProjects/MavenProject/out/artifacts/MavenProject_jar2/MavenProject.jar",
              "/home/oem/Desktop/testJava.java"])

        json_data = proc.decode().strip()
        print(submit_id, ":", json_data)
        dict_data = json.loads(json_data)

        for key in dict_data:
            if key in total_dict_data:
                total_dict_data[key] = total_dict_data[key] + dict_data[key]
            else:
                total_dict_data[key] = dict_data[key]

            if key not in max_dict_data or max_dict_data[key] < dict_data[key]:
                max_dict_data[key] = dict_data[key]

            if key not in min_dict_data or min_dict_data[key] > dict_data[key]:
                min_dict_data[key] = dict_data[key]

            if key not in count_dict_data:
                if dict_data[key] > 0:
                    count_dict_data[key] = 1
                else:
                    count_dict_data[key] = 0
            elif dict_data[key] > 0:
                count_dict_data[key] = count_dict_data[key] + 1

    for key in total_dict_data:
        if count_dict_data[key] > 4 :
            total_dict_data[key] = (total_dict_data[key] - max_dict_data[key])/(len(submission_data)-1)
    else :
        for key in total_dict_data:
            total_dict_data[key] = total_dict_data[key]/len(submission_data)

    for key in count_dict_data:
        count_dict_data[key] = count_dict_data[key] / len(submission_data)

    # for key in total_dict_data:
    #     total_dict_data[key] = (total_dict_data[key] / len(submission_data))

    return count_dict_data, total_dict_data


def get_data_in_python(cursor, problem_num) :

    sql = '''

            select s.submitid, j.result from `submission` as s join `language` as l join `judging`
            as j on s.submitid=j.submitid and s.langid = l.langid where s.submitid>=3471 and s.submitid<=5470
            and j.result="correct" and l.name = "Python 3" and s.probid = ''' + problem_num + ''' order by s.probid

            '''
    cursor.execute(sql)
    submission_data = cursor.fetchall()

    if len(submission_data) == 0:
        return None, None

    total_dict_data = {}
    min_dict_data = {}
    max_dict_data = {}
    count_dict_data = {}

    for submit in submission_data:
        submit_id = submit[0]

        code_sql = '''
                    select sourcecode from submission_file where submitid=%s;
                '''
        cursor.execute(code_sql, submit_id)
        correct_source_code = cursor.fetchall()[0][0].decode()

        dict_data = dict_total_data(correct_source_code)

        for key in dict_data:
            if key in total_dict_data:
                total_dict_data[key] = total_dict_data[key] + dict_data[key]
            else:
                total_dict_data[key] = dict_data[key]

            if key not in max_dict_data or max_dict_data[key] < dict_data[key]:
                max_dict_data[key] = dict_data[key]

            if key not in min_dict_data or min_dict_data[key] > dict_data[key]:
                min_dict_data[key] = dict_data[key]

            if key not in count_dict_data:
                if dict_data[key] > 0:
                    count_dict_data[key] = 1
                else:
                    count_dict_data[key] = 0
            elif dict_data[key] > 0:
                count_dict_data[key] = count_dict_data[key] + 1

    # if len(submission_data) > 3:
    #     for key in total_dict_data:
    #         total_dict_data[key] = (total_dict_data[key] - min_dict_data[key] - max_dict_data[key])/(len(submission_data)-2)
    # else :
    #     for key in total_dict_data:
    total_dict_data[key] = total_dict_data[key]/len(submission_data)

    for key in count_dict_data:
        count_dict_data[key] = count_dict_data[key] / len(submission_data)

    # for key in total_dict_data:
    #     total_dict_data[key] = (total_dict_data[key] / len(submission_data))*count_dict_data[key]

    return count_dict_data, total_dict_data


db = pymysql.connect(host='192.168.56.103', port=3306, user='root', password='1234', db='domjudge', charset='utf8')
cursor = db.cursor()

#32~56 : problem count
java_json = "{ "
python_json = "{ "
for i in range(32, 57) :
    #get all the correct submissions of one problem
    print("problem : ", i)

    count_java_dict, java_dict = get_data_in_java(cursor, str(i))
    count_data_json = json.dumps(count_java_dict)
    sum_data_json = json.dumps(java_dict)

    if sum_data_json is not "null":
        java_json = java_json + "\""+str(i) + "\" : { \"count\" : " + count_data_json + ", \"sum\" : "+sum_data_json+" }, \n"

    count_python_dict, python_dict = get_data_in_python(cursor, str(i))
    count_data_json = json.dumps(count_python_dict)
    sum_data_json = json.dumps(python_dict)

    if sum_data_json is not "null":
        python_json = python_json+ "\""+str(i) + "\" : { \"count\" : " + count_data_json + ", \"sum\" : "+sum_data_json+" }, \n"

java_json = java_json[:-3]+" }"
python_json = python_json[:-3]+" }"

print(java_json)
print(python_json)

f = open("/home/oem/Desktop/java_json.json", "w")
java_json_array = java_json.split("\n")

for data in java_json_array :
    f.write(data+"\n")
f.close()

f = open("/home/oem/Desktop/python_json.json", "w")
python_json_array = python_json.split("\n")

for data in python_json_array :
    f.write(data+"\n")
f.close()

print("finish")


#1. 문제 수마다 correct인 소스코드들 찾기
#필요한 정보 : 문제, 맞았는지, 언어, 소스코드
#probid>=32


#2. 이소스코드들 counting

#3. counting 결과를 json으로 만들기
