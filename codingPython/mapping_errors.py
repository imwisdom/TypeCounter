import pymysql
from mapping_using_regex import error_to_solve
from mapping_wrong_answer import check_output, check_source_code
#
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
#                 select w.submitid, c.submitid from submission as w join submission as c on w.teamid=c.teamid
#                 join judging as j on c.submitid=j.submitid where w.submitid=%s and w.probid=c.probid
#                 and j.result="correct" and w.langid=c.langid and w.submitid<c.submitid limit 1
#             '''
#             cursor.execute(sql, submit_id)
#             correct_submit = cursor.fetchall()
#
#             if len(correct_submit) > 0 :
#                 correct_submit_id = correct_submit[0][1]
#                 sql = '''
#                     select sourcecode from submission_file where submitid=%s
#                 '''
#                 cursor.execute(sql, submit_id)
#                 wrong_source_code = cursor.fetchall()
#
#                 cursor.execute(sql, correct_submit_id)
#                 correct_source_code = cursor.fetchall()
#
#                 solve = check_source_code(wrong_source_code[0][0].decode(), correct_source_code[0][0].decode(), lang)
#                 print(solve)
#
#     else :
#         print(error_type)
#
# db.close()

wrong_source_code = '''

import java.util.Iterator;
import java.util.LinkedList;
import java.util.Scanner;

class Node{
	private String key;
	private int wait;
	private boolean visited;
	
	public Node(String key, int wait) {
		this.key = key;
		this.wait = wait;
		this.visited = false;
	}
	
	public String key_() {
		return key;
	}
	public int wait_() {
		return wait;
	}
	public void visited(boolean v) {
		this.visited = v;
	}
	
	public boolean getVisit() {
		return visited;
	}
}

class Path {
	private String des;
	private int dis;
	
	public Path(String des, int dis) {
		this.des = des;
		this.dis = dis;
	}
	
	public String des() {
		return des;
	}
	public int dis() {
		return dis;
	}
}

class Status {
	private String node;
	private int dis;
	private String course;
	
	public Status(String node, int dis, String course) {
		this.node = node;
		this.dis = dis;
		this.course = course + node + " ";
	}
	
	public String node() {
		return node;
	}
	public int dis() {
		return dis;
	}
	public String course() {
		return course;
	}
}

public class dron {
	private int N;
	private int M;
	private static int count = 0;
	
	private Node adj[];
	private LinkedList<Path>[] path;
	
	public dron(int N, int M) {
		this.N = N;
		this.M = M;
		
		adj = new Node[N];
		path = new LinkedList[N];
	}
	
	public void node(String key, int wait) {
		if(N>count) {
			adj[count] = new Node(key, wait);
			path[count] = new LinkedList();
			path[count].add(new Path(key, 0));
			count++;
		}
	}
	
	public void setEdge(String start, String des, int dis) {	
		boolean flag = true;
		for(int i=0; i<N; i++) {
			if(path[i].element().des().equals(start)){
				Iterator<Path> iter = path[i].listIterator();
				while(iter.hasNext()) {
					if(iter.next().des().equals(des)) {
						flag = false;
						break;
					}
				}
				
				if(flag)
					path[i].add(new Path(des, dis));
			}
		}
		
		flag = true;
		for(int i=0; i<N; i++) {
			if(path[i].element().des().equals(des)){
				Iterator<Path> iter = path[i].listIterator();
				while(iter.hasNext()) {
					if(iter.next().des().equals(start)) {
						flag = false;
						break;
					}
				}
				
				if(flag)
					path[i].add(new Path(start, dis));
			}
		}
	}
	
	public void search(String start, String destination) {
		LinkedList<Status> desList = new LinkedList();
		int index=0;
		for(int i=0; i<N; i++) {
			if(path[i].element().des().equals(start)) {
				index = i;
				break;
			}
		}
		
		adj[index].visited(true);
		
		LinkedList<Status> queue = new LinkedList();
		queue.add(new Status(path[index].element().des(), 0, ""));
		while(queue.size() != 0) {
			Status tmp = queue.poll();
			if(tmp.node().equals(destination)) {
				Iterator<Status> iter = desList.listIterator();
				int i = 0;
				while(iter.hasNext()) {
					if(tmp.dis() > iter.next().dis())
						i++;
				}
				desList.add(i, tmp);
			}
			else {
				for(int i=0;i<N;i++) {
					if(tmp.node().equals(adj[i].key_())) {
						adj[i].visited(true);
						break;
					}
				}
				
				int tmpIndex = -1;
				for(int i=0;i<N;i++) {
					if(path[i].element().des().equals(tmp.node())) {
						tmpIndex = i;
						break;
					}
				}
				
				Iterator<Path> iter = path[tmpIndex].listIterator();
				while(iter.hasNext()) {
					Path p = iter.next();
					int pIndex = -1;
					for(int i=0;i<N;i++) {
						if(p.des().equals(adj[i].key_())) {
							pIndex = i;
							break;
						}
					}
					
					if(!adj[pIndex].getVisit()) {
						int queueIndex = 0;
						Iterator<Status> i = queue.listIterator();
						while(i.hasNext()) {
							Status queueElement = i.next();
							
							if(p.dis()+tmp.dis() > queueElement.dis())
								queueIndex++;
						}
						if(tmp.node().equals(start)) {
							queue.add(queueIndex,new Status(p.des(), p.dis()+tmp.dis(), tmp.course()));
						}
						else {
							queue.add(queueIndex,new Status(p.des(), p.dis()+tmp.dis() + adj[tmpIndex].wait_(), tmp.course()));
						}
					}
				}
			}
		}
		System.out.println(desList.element().course());
		System.out.println(desList.element().dis());
	}
	
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		dron d;
		
		String nm_ = sc.nextLine();
		String[] nm__ = nm_.split(" ");
		int[] nm = new int[2];
		for(int i=0; i<2; i++) {
			nm[i] = Integer.parseInt(nm__[i]);
		}
		d = new dron(nm[0], nm[1]);
		
		String nodeList_ = sc.nextLine();
		String[] nodeList = nodeList_.split(" ");
		
		for(int i=0; i<nm[0]; i++) {
			String node_ = sc.nextLine();
			String[] node = node_.split(" ");
			
			d.node(node[0], Integer.parseInt(node[1]));
		}
		
		for(int i=0; i<nm[1]; i++) {
			String edge_ = sc.nextLine();
			String[] edge = edge_.split(" ");
			
			d.setEdge(edge[0], edge[1], Integer.parseInt(edge[2]));;
		}
		
		String start = sc.nextLine();
		String end = sc.nextLine();
		
		d.search(start, end);
	}
}


    
'''
correct_source_code = '''

import java.util.Iterator;
import java.util.LinkedList;
import java.util.Scanner;

class Node{
	private String key;
	private int wait;
	private boolean visited;
	
	public Node(String key, int wait) {
		this.key = key;
		this.wait = wait;
		this.visited = false;
	}
	
	public String key_() {
		return key;
	}
	public int wait_() {
		return wait;
	}
	public void visited(boolean v) {
		this.visited = v;
	}
	
	public boolean getVisit() {
		return visited;
	}
}

class Path {
	private String des;
	private int dis;
	
	public Path(String des, int dis) {
		this.des = des;
		this.dis = dis;
	}
	
	public String des() {
		return des;
	}
	public int dis() {
		return dis;
	}
}

class Status {
	private String node;
	private int dis;
	private String course;
	
	public Status(String node, int dis, String course) {
		this.node = node;
		this.dis = dis;
		this.course = course + node + " ";
	}
	
	public String node() {
		return node;
	}
	public int dis() {
		return dis;
	}
	public String course() {
		return course;
	}
}

public class dron {
	private int N;
	private int M;
	private static int count = 0;
	
	private Node adj[];
	private LinkedList<Path>[] path;
	
	public dron(int N, int M) {
		this.N = N;
		this.M = M;
		
		adj = new Node[N];
		path = new LinkedList[N];
	}
	
	public void node(String key, int wait) {
		if(N>count) {
			adj[count] = new Node(key, wait);
			path[count] = new LinkedList();
			path[count].add(new Path(key, 0));
			count++;
		}
	}
	
	public void setEdge(String start, String des, int dis) {	
		boolean flag = true;
		for(int i=0; i<N; i++) {
			if(path[i].element().des().equals(start)){
				Iterator<Path> iter = path[i].listIterator();
				while(iter.hasNext()) {
					if(iter.next().des().equals(des)) {
						flag = false;
						break;
					}
				}
				
				if(flag)
					path[i].add(new Path(des, dis));
			}
		}
		
		flag = true;
		for(int i=0; i<N; i++) {
			if(path[i].element().des().equals(des)){
				Iterator<Path> iter = path[i].listIterator();
				while(iter.hasNext()) {
					if(iter.next().des().equals(start)) {
						flag = false;
						break;
					}
				}
				
				if(flag)
					path[i].add(new Path(start, dis));
			}
		}
	}
	
	public void search(String start, String destination) {
		LinkedList<Status> desList = new LinkedList();
		int index=0;
		for(int i=0; i<N; i++) {
			if(path[i].element().des().equals(start)) {
				index = i;
				break;
			}
		}
		
		adj[index].visited(true);
		
		LinkedList<Status> queue = new LinkedList();
		queue.add(new Status(path[index].element().des(), 0, ""));
		while(queue.size() != 0) {
			Status tmp = queue.poll();
			if(tmp.node().equals(destination)) {
				Iterator<Status> iter = desList.listIterator();
				int i = 0;
				while(iter.hasNext()) {
					if(tmp.dis() > iter.next().dis())
						i++;
				}
				desList.add(i, tmp);
			}
			else {
				int tmpIndex = -1;
				for(int i=0;i<N;i++) {
					if(tmp.node().equals(adj[i].key_())) {
						adj[i].visited(true);
						tmpIndex = i;
						break;
					}
				}
				
				Iterator<Path> iter = path[tmpIndex].listIterator();
				while(iter.hasNext()) {
					Path p = iter.next();
					int pIndex = -1;
					for(int i=0;i<N;i++) {
						if(p.des().equals(adj[i].key_())) {
							pIndex = i;
							break;
						}
					}
					
					if(!adj[pIndex].getVisit()) {
						int queueIndex = 0;
						Iterator<Status> i = queue.listIterator();
						while(i.hasNext()) {
							Status queueElement = i.next();
							
							if(tmp.node().equals(start)) {
								if(p.dis()+tmp.dis() >= queueElement.dis())
									queueIndex++;
							}
							else {
								if(p.dis()+tmp.dis()+ adj[tmpIndex].wait_() >= queueElement.dis())
									queueIndex++;
							}
						}
						if(tmp.node().equals(start)) {
							queue.add(queueIndex,new Status(p.des(), p.dis()+tmp.dis(), tmp.course()));
						}
						else {
							queue.add(queueIndex,new Status(p.des(), p.dis()+tmp.dis() + adj[tmpIndex].wait_(), tmp.course()));
						}
					}
				}
			}
		}
		System.out.println(desList.element().course().trim());
		System.out.println(desList.element().dis());
	}
	
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		dron d;
		
		String nm_ = sc.nextLine();
		String[] nm__ = nm_.split(" ");
		int[] nm = new int[2];
		for(int i=0; i<2; i++) {
			nm[i] = Integer.parseInt(nm__[i]);
		}
		d = new dron(nm[0], nm[1]);
		
		String nodeList_ = sc.nextLine();
		String[] nodeList = nodeList_.split(" ");
		
		for(int i=0; i<nm[0]; i++) {
			String node_ = sc.nextLine();
			String[] node = node_.split(" ");
			
			d.node(node[0], Integer.parseInt(node[1]));
		}
		
		for(int i=0; i<nm[1]; i++) {
			String edge_ = sc.nextLine();
			String[] edge = edge_.split(" ");
			
			d.setEdge(edge[0], edge[1], Integer.parseInt(edge[2]));;
		}
		
		String start = sc.nextLine();
		String end = sc.nextLine();
		
		d.search(start, end);
	}
}

'''
solve = check_source_code(wrong_source_code, correct_source_code, "Java")
print(solve)




