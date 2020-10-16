import re
from python_checker import evaluate, evaluate_using_json_data, dict_total_data
import subprocess
import json

# submitid, testcaseid, runresult, output_run, output

solve = ""


def check_output(lists):

    for error_data in lists:
        if check_output_using_regex(error_data):
            return "output 형태가 잘못됨"
    if is_same(lists):
        return "고정된 input"
    return ""


def check_output_using_regex(data):
    error_res = data[3].decode().strip()
    correct_res = data[4].decode().strip()

    regex_list = [
        '[0-9]|inf|Inf|INF',
        '[a-z]^[inf]^[Inf]^[INF]',
        '[A-Z]^[Inf]^[Inf]^[INF]',
        '[=#/\?:^$.@*\"※~&%ㆍ』\\‘|\(\)\[\]\<\>`\'…》]'
    ]
    # '[0-9]|inf|Inf|negative|Negative|Not enough money!',
    # '[a-z]^[inf]^[negative]^[Not enough money!]',
    # '[A-Z]^[Inf]^[Negative]^[Not enough money!]',
    # '[=#/\?:^$.@*\"※~&%ㆍ』\\‘|\(\)\[\]\<\>`\'…》]'
    for rex in regex_list:
        check = re.compile(rex)
        if check.search(error_res) is None and error_res != "Negative Cycle!" and error_res != "Not enough money!" and check.search(correct_res):
            return True
        elif check.search(error_res) and check.search(correct_res) is None and correct_res != "Negative Cycle!" and correct_res != "Not enough money!":
            return True

        first_error_res = error_res.split("\n")[0]
        first_correct_res = correct_res.split("\n")[0]

        if check.search(first_error_res) is None and error_res != "Negative Cycle!" and error_res != "Not enough money!" and check.search(first_correct_res):
            return True
        elif check.search(first_error_res) and check.search(first_correct_res) is None and correct_res != "Negative Cycle!" and correct_res != "Not enough money!":
            return True

    if len(correct_res.split("\n")) < len(error_res.split("\n")) and error_res.find(correct_res) != -1:
        return True

    return False


def is_same(lists):
    checked_data = lists[0][3]
    for error_data in lists:
        if checked_data.decode() != error_data[3].decode():
            return False

    if checked_data.decode().strip() == "2147483647" or  checked_data.decode().strip() == "Negative Cycle!":
        return False
    return True


def check_source_code(wrong_source_code, correct_source_code, lang):

    #print(lang)
    if lang == 'Java' :
        wrong_source_code = wrong_source_code.split("\n")
        f = open("/home/oem/Desktop/trainingJava.java", "w")

        for code in wrong_source_code :
            f.write(code+"\n")
        f.close()

        correct_source_code = correct_source_code.split("\n")
        f = open("/home/oem/Desktop/testJava.java", "w")

        for code in correct_source_code:
            f.write(code + "\n")
        f.close()

        proc = subprocess.check_output(["java", "-jar", "/home/oem/IdeaProjects/MavenProject/out/artifacts/MavenProject_jar/MavenProject.jar", "/home/oem/Desktop/trainingJava.java", "/home/oem/Desktop/testJava.java"])

        return proc.decode().strip()


    elif lang == 'Python 3':

        return evaluate(wrong_source_code, correct_source_code)


def check_source_code_using_json(source_code, lang, probid) :
    cur_data = {}
    total_json_data = {}
    if lang == 'Java' :
        wrong_source_code = source_code.split("\n")
        f = open("/home/oem/Desktop/testJava.java", "w")

        for code in wrong_source_code :
            f.write(code+"\n")
        f.close()

        proc = subprocess.check_output(["java", "-jar", "/home/oem/IdeaProjects/MavenProject/out/artifacts/MavenProject_jar2/MavenProject.jar", "/home/oem/Desktop/testJava.java"])
        cur_data = proc.decode().strip()
        cur_data = json.loads(cur_data)

        with open("/home/oem/Desktop/java_json.json") as json_file:
            total_json_data = json.load(json_file)

        total_json_data = total_json_data[probid]
        json_file.close()

    elif lang == 'Python 3' :
        cur_data = dict_total_data(source_code)
        with open("/home/oem/Desktop/python_json.json") as json_file:
            total_json_data = json.load(json_file)

        total_json_data = total_json_data[probid]
        json_file.close()

    else :
        return None, None, None

    return evaluate_using_json_data(cur_data, total_json_data)









