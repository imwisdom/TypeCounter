import pymysql
from mapping_using_regex import error_to_solve
from mapping_wrong_answer import check_output, check_source_code, check_source_code_using_json

# db = pymysql.connect(host='192.168.56.103', port=3306, user='root', password='1234', db='domjudge', charset='utf8')
# cursor = db.cursor()
#
# #3471, 5470
#
# sql = '''
#
# select s.submitid, l.name, j.result from `submission` as s join `language` as l join `judging`
# as j on s.submitid=j.submitid and s.langid = l.langid where s.submitid>=3471 and s.submitid<=5470
# and j.result!="correct" order by s.submitid
#
# '''
# cursor.execute(sql)
# submission_data = cursor.fetchall()
# # 0 : submitid, 1 : lang, 2 : error-type
#
# check_wrong_output = 0
# for submit in submission_data :
#
#     submit_id = submit[0]
#     lang = submit[1]
#     error_type = submit[2]
#
#
#     print("===================================")
#     print(submit_id)
#     print(error_type)
#     if error_type == 'run-error':
#         sql = '''
#                 select j.submitid, jr.output_error from judging as j join judging_run as jr
#                 on j.judgingid = jr.judgingid where j.submitid=%s and jr.runresult="run-error";
#                 '''
#         cursor.execute(sql, submit_id)
#         run_data = cursor.fetchall()
#
#         detailed_error = run_data[0][1].decode().strip().split("\n")
#         run_error_msg = ""
#
#         if lang == "Java":
#             run_error_msg = detailed_error[0]
#         elif lang == "Python 3" or lang == "Python 2":
#             run_error_msg = detailed_error[-1]
#         else :
#             if len(detailed_error) <= 1:
#                 print("check this submission")
#                 continue
#             run_error_msg = detailed_error[1]
#
#         solve = error_to_solve(run_error_msg)
#         check_wrong_output = check_wrong_output + 1
#         print(solve)
#
#     elif error_type == 'compiler-error':
#         sql = '''
#                 select submitid, output_compile from judging where submitid=%s;
#                 '''
#
#         cursor.execute(sql, submit_id)
#         compile_data = cursor.fetchall()
#
#         detailed_error = compile_data[0][1].decode().strip().split("\n")
#
#         compile_error_msg = ""
#         if lang == "Java":
#             compile_error_msg = detailed_error[1]
#         else :
#             compile_error_msg = detailed_error[-1]
#         solve = error_to_solve(compile_error_msg)
#         check_wrong_output = check_wrong_output + 1
#         print(solve)
#
#     elif error_type == 'wrong-answer':
#         sql = '''
#             select j.submitid, t.testcaseid, jr.runresult, jr.output_run, t.output
#             from `judging` as j join `judging_run` as jr on j.judgingid = jr.judgingid
#             join `testcase` as t on jr.testcaseid=t.testcaseid
#             where j.submitid=%s and jr.runresult!="timelimit"
#         '''
#
#         cursor.execute(sql, submit_id)
#         wrong_answer_data = cursor.fetchall()
#         solve = check_output(wrong_answer_data)
#
#         if solve :
#             print(solve)
#
#         else :
#             sql = '''
#                 select w.submitid, c.submitid, w.probid from submission as w join submission as c on w.teamid=c.teamid
#                 join judging as j on c.submitid=j.submitid where w.submitid=%s and w.probid=c.probid
#                 and j.result="correct" and w.langid=c.langid and w.submitid<c.submitid limit 1
#             '''
#             cursor.execute(sql, submit_id)
#             submit_data = cursor.fetchall()
#
#             if len(submit_data) > 0 :
#
#                 sql = '''
#                     select sourcecode from submission_file where submitid=%s
#                 '''
#                 cursor.execute(sql, submit_id)
#                 wrong_source_code = cursor.fetchall()
#
#                 if submit_data[0][2] < 32 :
#                     continue
#
#                 # correct_submit_id = submit_data[0][1]
#                 # cursor.execute(sql, correct_submit_id)
#                 # correct_source_code = cursor.fetchall()
#                 #
#                 # solve = check_source_code(wrong_source_code[0][0].decode(), correct_source_code[0][0].decode(), lang)
#
#                 solve = check_source_code_using_json(wrong_source_code[0][0].decode(), lang, str(submit_data[0][2]))
#                 print("submitid : ", submit_id, " probid : ", submit_data[0][2])
#                 print(solve)
#                 print("============================================================")
#
#     else :
#         print(error_type)
#
# db.close()

source_code = '''
a = input()
b = input().split()

for i in range(len(b)):
    b[i] = int(b[i])

best_sum = float('-inf')
best_start = best_end = float('-inf')
current_sum = 0
for i in b:
    current_sum = max(0, current_sum + i)
    best_sum = max(best_sum, current_sum)

print(best_sum)


'''
solve = check_source_code_using_json(source_code, "Python 3", "45")
print(solve)


