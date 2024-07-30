//#include<iostream>
//using namespace std;
//
//static int cnt = 1;
//
//class qi {
//public:
//	int color;
//	int num;
//	qi() {
//		num = -1;
//		color = 0;//1 means black -1 means white
//	}
//	void ini(int col, int n) {
//		color = col;
//		num = n;
//	}
//};
//void printboard(qi q[3][3]) {
//	for (int i = 0; i < 3; i++) {
//		for (int j = 0; j < 3; j++) {
//			cout << "|" << " ";
//			if (q[i][j].color == -1) {
//				cout << "*" << " ";
//			}
//			else if (q[i][j].color == 1) {
//				cout << "o" << " ";
//			}
//			else {
//				cout << " " << " ";
//			}
//		}
//		cout << "|" << endl;
//	}
//}
//void ifwin(qi q[3][3]) {
//	for (int i = 0; i < 3; i++) {
//		// 检查行
//		if (q[i][0].color != 0 && q[i][0].color == q[i][1].color && q[i][0].color == q[i][2].color) {
//			if (q[i][0].color == -1)
//				cout << "black win" << endl;
//			else
//				cout << "white win" << endl;
//			return;
//		}
//		// 检查列
//		if (q[0][i].color != 0 && q[0][i].color == q[1][i].color && q[0][i].color == q[2][i].color) {
//			if (q[0][i].color == -1)
//				cout << "black win" << endl;
//			else
//				cout << "white win" << endl;
//			return;
//		}
//	}
//	// 检查对角线
//	if (q[0][0].color != 0 && q[0][0].color == q[1][1].color && q[0][0].color == q[2][2].color) {
//		if (q[0][0].color == -1)
//			cout << "black win" << endl;
//		else
//			cout << "white win" << endl;
//		return;
//	}
//	if (q[0][2].color != 0 && q[0][2].color == q[1][1].color && q[0][2].color == q[2][0].color) {
//		if (q[0][2].color == -1)
//			cout << "black win" << endl;
//		else
//			cout << "white win" << endl;
//		return;
//	}
//
//	// 没有一方获胜
//	cout << "no one win" << endl;
//}
//
//void setwhite(qi q[3][3]) {
//L1:cout << "white round" << endl;
//	int x = 0, y = 0;
//	cin >> x >> y;
//	if (x > 3 || y > 3) {
//		cout << "wrong" << endl;
//		goto L1;
//	}
//	if (q[x - 1][y - 1].color == 0) {
//		q[x - 1][y - 1].color = -1;
//		cout << "white success set!" << endl;
//		printboard(q);
//		cnt++;
//		ifwin(q);
//		return;
//	}
//	goto L1;
//	cout << "wrong" << endl;
//	printboard(q);
//}
//void setblack(qi q[3][3]) {
//L2:cout << "black round" << endl;
//	int x = 0, y = 0;
//	cin >> x >> y;
//	if (q[x - 1][y - 1].color == 0) {
//		q[x - 1][y - 1].color = 1;
//		cout << "black success set!" << endl;
//		printboard(q);
//		cnt++;
//		ifwin(q);
//		return;
//	}
//	goto L2;
//	cout << "wrong" << endl;
//	printboard(q);
//}
//int main() {
//	qi q[3][3];
//	for (int i = 0; i < 3; i++) {
//		for (int j = 0; j < 3; j++) {
//			q[i][j].color = 0;
//		}
//	}
//	//人人对弈
//	while (cnt != 9) {
//		setwhite(q);
//		setblack(q);
//	}
//	return 0;
//}


#include<iostream>
#include<limits.h>
using namespace std;

static int cnt = 1;

class qi {
public:
	int color;
	int num;
	qi() {
		num = -1;
		color = 0; // 1 means black, -1 means white
	}
	void ini(int col, int n) {
		color = col;
		num = n;
	}
	bool is_empty() {
		return color == 0;
	}
};

void printboard(qi q[3][3]) {
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++) {
			cout << "|" << " ";
			if (q[i][j].color == -1) {
				cout << "*" << " ";
			}
			else if (q[i][j].color == 1) {
				cout << "o" << " ";
			}
			else {
				cout << " " << " ";
			}
		}
		cout << "|" << endl;
	}
}

int evaluate(qi q[3][3]) {
	for (int i = 0; i < 3; i++) {
		// 检查行
		if (q[i][0].color != 0 && q[i][0].color == q[i][1].color && q[i][0].color == q[i][2].color) {
			return q[i][0].color;
		}
		// 检查列
		if (q[0][i].color != 0 && q[0][i].color == q[1][i].color && q[0][i].color == q[2][i].color) {
			return q[0][i].color;
		}
	}
	// 检查对角线
	if (q[0][0].color != 0 && q[0][0].color == q[1][1].color && q[0][0].color == q[2][2].color) {
		return q[0][0].color;
	}
	if (q[0][2].color != 0 && q[0][2].color == q[1][1].color && q[0][2].color == q[2][0].color) {
		return q[0][2].color;
	}
	return 0; // 没有一方获胜
}

bool is_moves_left(qi q[3][3]) {
	for (int i = 0; i < 3; i++)
		for (int j = 0; j < 3; j++)
			if (q[i][j].is_empty())
				return true;
	return false;
}

int minimax(qi q[3][3], int depth, bool is_max) {
	int score = evaluate(q);

	if (score == 1)
		return score;
	if (score == -1)
		return score;
	if (!is_moves_left(q))
		return 0;

	if (is_max) {
		int best = INT_MIN;
		for (int i = 0; i < 3; i++) {
			for (int j = 0; j < 3; j++) {
				if (q[i][j].is_empty()) {
					q[i][j].color = 1;
					best = max(best, minimax(q, depth + 1, !is_max));
					q[i][j].color = 0;
				}
			}
		}
		return best;
	}
	else {
		int best = INT_MAX;
		for (int i = 0; i < 3; i++) {
			for (int j = 0; j < 3; j++) {
				if (q[i][j].is_empty()) {
					q[i][j].color = -1;
					best = min(best, minimax(q, depth + 1, !is_max));
					q[i][j].color = 0;
				}
			}
		}
		return best;
	}
}

pair<int, int> find_best_move(qi q[3][3]) {
	int best_val = INT_MIN;
	pair<int, int> best_move = { -1, -1 };

	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++) {
			if (q[i][j].is_empty()) {
				q[i][j].color = 1;
				int move_val = minimax(q, 0, false);
				q[i][j].color = 0;
				if (move_val > best_val) {
					best_move = { i, j };
					best_val = move_val;
				}
			}
		}
	}
	return best_move;
}

void ifwin(qi q[3][3]) {
	int result = evaluate(q);
	if (result == 1) {
		cout << "black win" << endl;
		exit(0);
	}
	else if (result == -1) {
		cout << "white win" << endl;
		exit(0);
	}
	else if (!is_moves_left(q)) {
		cout << "no one win" << endl;
		exit(0);
	}
}

void setwhite(qi q[3][3]) {
L1: cout << "white round" << endl;
	int x = 0, y = 0;
	cin >> x >> y;
	if (x > 3 || y > 3 || x < 1 || y < 1 || !q[x - 1][y - 1].is_empty()) {
		cout << "wrong" << endl;
		goto L1;
	}
	q[x - 1][y - 1].color = -1;
	cout << "white success set!" << endl;
	printboard(q);
	cnt++;
	ifwin(q);
}

void setblack(qi q[3][3]) {
	cout << "black round" << endl;
	pair<int, int> best_move = find_best_move(q);
	q[best_move.first][best_move.second].color = 1;
	cout << "black success set!" << endl;
	printboard(q);
	cnt++;
	ifwin(q);
}

int main() {
	qi q[3][3];
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++) {
			q[i][j].color = 0;
		}
	}
	// 人机对弈，机先手
	while (cnt <= 9) {
		if (cnt % 2 == 1) {
			setblack(q);
		}
		else {
			setwhite(q);
		}
	}
	return 0;
}
