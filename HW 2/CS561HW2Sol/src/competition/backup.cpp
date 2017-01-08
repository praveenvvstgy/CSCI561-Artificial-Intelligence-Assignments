//
//  main.cpp
//  HW2SolCPP
//
//  Created by Praveen Gowda I V on 10/12/16.
//  Copyright © 2016 Praveen Gowda I V. All rights reserved.
//

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <fstream>
#include <sstream>
#include <limits>
using namespace std;

typedef pair<int, int> position;
typedef pair<position, string > boardmove;
typedef tuple<vector<position>, vector<position>, vector<position>, string, int> gamestate;

#ifndef INFINITY
#define INFINITY numeric_limits<int>::max();
#endif

bool positionPresentIn(vector<position> positions, position pos) {
    return find(positions.begin(), positions.end(), pos) != positions.end();
}

void removeElement(vector<position> &positions, position pos) {
    auto it = find(positions.begin(), positions.end(), pos);
    if (it != positions.end()) {
        positions.erase(it);
    }
}

char move_to_alpha[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};

int n;
int maxdepth;
string youplay;
vector<vector<int>> scores;

vector<boardmove> actions(gamestate& state) {
    vector<boardmove> actions;
    string to_play = get<3>(state);
    for (auto pos: get<0>(state))
    {
        auto action = pair<position, string>(pos, "Stake");
        actions.push_back(action);
    }
    if (to_play == "X") {
        for(auto pos: get<1>(state)) {
            int x = pos.first;
            int y = pos.second;
            if (positionPresentIn(get<0>(state), position(x - 1, y))) {
                actions.push_back(pair<position, string>(position(x - 1, y), "Raid"));
            }
            if (positionPresentIn(get<0>(state), position(x + 1, y))) {
                actions.push_back(pair<position, string>(position(x + 1, y), "Raid"));
            }
            if (positionPresentIn(get<0>(state), position(x, y - 1))) {
                actions.push_back(pair<position, string>(position(x, y - 1), "Raid"));
            }
            if (positionPresentIn(get<0>(state), position(x, y + 1))) {
                actions.push_back(pair<position, string>(position(x, y + 1), "Raid"));
            }
        }
    } else {
        for(auto pos: get<2>(state)) {
            int x = pos.first;
            int y = pos.second;
            if (positionPresentIn(get<0>(state), position(x - 1, y))) {
                actions.push_back(pair<position, string>(position(x - 1, y), "Raid"));
            }
            if (positionPresentIn(get<0>(state), position(x + 1, y))) {
                actions.push_back(pair<position, string>(position(x + 1, y), "Raid"));
            }
            if (positionPresentIn(get<0>(state), position(x, y - 1))) {
                actions.push_back(pair<position, string>(position(x, y - 1), "Raid"));
            }
            if (positionPresentIn(get<0>(state), position(x, y + 1))) {
                actions.push_back(pair<position, string>(position(x, y + 1), "Raid"));
            }
        }
        
    }
    return actions;
}

bool terminal_test(gamestate& state) {

    return (get<0>(state).size() == 0) || (get<4>(state) == maxdepth);
}

gamestate result(boardmove move, gamestate& state) {
    position pos = move.first;
    int x = pos.first;
    int y = pos.second;
    string to_play = get<3>(state);
    int depth = get<4>(state);
    //cout<<x<<", "<<y<<", "<<move.second<<endl;
    if (move.second == "Stake") {
        if (to_play == "X") {
            vector<position> tmp_vacant_positions = get<0>(state);
            vector<position> tmp_x_positions = get<1>(state);
            vector<position> tmp_o_positions = get<2>(state);
            removeElement(tmp_vacant_positions, position(x, y));
            tmp_x_positions.push_back(position(x, y));
            return forward_as_tuple(tmp_vacant_positions, tmp_x_positions, tmp_o_positions, "O", depth + 1);
        } else {
            vector<position> tmp_vacant_positions = get<0>(state);
            vector<position> tmp_x_positions = get<1>(state);
            vector<position> tmp_o_positions = get<2>(state);
            removeElement(tmp_vacant_positions, position(x, y));
            tmp_o_positions.push_back(position(x, y));
            return forward_as_tuple(tmp_vacant_positions, tmp_x_positions, tmp_o_positions, "X", depth + 1);
        }
    } else {
        if (to_play == "X") {
            vector<position> tmp_vacant_positions = get<0>(state);
            vector<position> tmp_x_positions = get<1>(state);
            vector<position> tmp_o_positions = get<2>(state);
            removeElement(tmp_vacant_positions, position(x, y));
            tmp_x_positions.push_back(position(x, y));
            if (y > 0) {
                if (positionPresentIn(get<2>(state), position(x, y - 1))) {
                    removeElement(tmp_o_positions, position(x, y - 1));
                    tmp_x_positions.push_back(position(x, y - 1));
                }
            }
            if (y < n - 1) {
                if (positionPresentIn(get<2>(state), position(x, y + 1))) {
                    removeElement(tmp_o_positions, position(x, y + 1));
                    tmp_x_positions.push_back(position(x, y + 1));
                }
            }
            if (x > 0) {
                if (positionPresentIn(get<2>(state), position(x - 1, y))) {
                    removeElement(tmp_o_positions, position(x - 1, y));
                    tmp_x_positions.push_back(position(x - 1, y));
                }
            }
            if (x < n - 1) {
                if (positionPresentIn(get<2>(state), position(x + 1, y))) {
                    removeElement(tmp_o_positions, position(x + 1, y));
                    tmp_x_positions.push_back(position(x + 1, y));
                }
            }
            return forward_as_tuple(tmp_vacant_positions, tmp_x_positions, tmp_o_positions, "O", depth + 1);
        } else {
            vector<position> tmp_vacant_positions = get<0>(state);
            vector<position> tmp_x_positions = get<1>(state);
            vector<position> tmp_o_positions = get<2>(state);
            removeElement(tmp_vacant_positions, position(x, y));
            tmp_o_positions.push_back(position(x, y));
            if (y > 0) {
                if (positionPresentIn(get<1>(state), position(x, y - 1))) {
                    removeElement(tmp_x_positions, position(x, y - 1));
                    tmp_o_positions.push_back(position(x, y - 1));
                }
            }
            if (y < n - 1) {
                if (positionPresentIn(get<1>(state), position(x, y + 1))) {
                    removeElement(tmp_x_positions, position(x, y + 1));
                    tmp_o_positions.push_back(position(x, y + 1));
                }
            }
            if (x > 0) {
                if (positionPresentIn(get<1>(state), position(x - 1, y))) {
                    removeElement(tmp_x_positions, position(x - 1, y));
                    tmp_o_positions.push_back(position(x - 1, y));
                }
            }
            if (x < n - 1) {
                if (positionPresentIn(get<1>(state), position(x + 1, y))) {
                    removeElement(tmp_x_positions, position(x + 1, y));
                    tmp_o_positions.push_back(position(x + 1, y));
                }
            }
            return forward_as_tuple(tmp_vacant_positions, tmp_x_positions, tmp_o_positions, "X", depth + 1);
        }
    }
}

int utility(gamestate& state) {
//    for (int i = 0; i < n; i++) {
//        for (int j = 0; j < n; j++) {
//            if (positionPresentIn(get<0>(state), position(i, j))) {
//                //cout<<". ";
//            } else if (positionPresentIn(get<1>(state), position(i, j))) {
//                //cout<<"X ";
//            } else {
//                //cout<<"O ";
//            }
//        }
//        //cout<<endl;
//    }
    //cout<<endl<<endl;
    string to_play = get<3>(state);
    string just_played;
    if (to_play == "O") {
        just_played = "X";
    } else {
        just_played = "O";
    }
    
    int x_score = 0;
    for(auto pos: get<1>(state)) {
        x_score += scores[pos.first][pos.second];
    }
    
    int o_score = 0;
    for(auto pos: get<2>(state)) {
        o_score += scores[pos.first][pos.second];
    }
    if (youplay == "X") {
        //cout<<x_score - o_score<<endl;
        return x_score - o_score;
    } else {
        //cout<<o_score - x_score<<endl;
        return o_score - x_score;
    }
}

void printBoard(ofstream& file, gamestate& state) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            position pos = position(i, j);
            if (positionPresentIn(get<0>(state), pos)) {
                file<<".";
            } else {
                if (positionPresentIn(get<1>(state), pos)) {
                    file<<"X";
                } else file<<"O";
            }
        }
         if (i != n - 1) {
        file<<endl;
         }
    }
}

int ab_min_value(gamestate, int, int);
int ab_max_value(gamestate, int, int);

int ab_max_value(gamestate state, int alpha, int beta) {
    if (terminal_test(state)) {
        return utility(state);
    } else {
        int v = -INFINITY;
        for(auto a: actions(state)) {
            v = max(v, ab_min_value(result(a, state), alpha, beta));
            if (v >= beta) {
                return v;
            }
            alpha = max(alpha, v);
        }
        return v;
    }
}

int ab_min_value(gamestate state, int alpha, int beta) {
    if (terminal_test(state)) {
        return utility(state);
    } else {
        int v = INFINITY;
        for(auto a: actions(state)) {
            v = min(v, ab_max_value(result(a, state), alpha, beta));
            if (v <= alpha) {
                return v;
            }
            beta = min(beta, v);
        }
        return v;
    }
}

boardmove alpha_beta_search(tuple<vector<position>, vector<position>, vector<position>, string, int> state) {
    int alpha = -INFINITY;
    int beta = INFINITY;
    boardmove bestAction;
    for(auto action: actions(state)) {
        int v = ab_min_value(result(action, state), alpha, beta);
        if (v > alpha) {
            alpha = v;
            bestAction = action;
        }
    }
    return bestAction;
}

int min_value(gamestate state);
int max_value(gamestate state);

int min_value(gamestate state) {
    if (terminal_test(state)) {
        return utility(state);
    } else {
        int v = INFINITY;
        for(auto a: actions(state)) {
            v = min(v, max_value(result(a, state)));
        }
        return v;
    }
}

int max_value(gamestate state) {
    if (terminal_test(state)) {
        return utility(state);
    } else {
        int v = -INFINITY;
        for(auto a: actions(state)) {
            v = max(v, min_value(result(a, state)));
        }
        return v;
    }
}

boardmove minimax_decision(gamestate& state) {
    boardmove bestAction;
    int bestSoFar = -INFINITY;
    int count = 0;
    for(auto a: actions(state)) {
        if (count == 0) {
            bestAction = a;
            bestSoFar = min_value(result(a, state));
        } else {
            auto newResult = min_value(result(a, state));
            if (newResult > bestSoFar) {
                bestAction = a;
                bestSoFar = newResult;
            }
            
        }
        count++;
    }
    return bestAction;
}

int main(int argc, char const *argv[])
{
    ifstream file("input.txt");
    
    string str;
    getline(file, str);
    n = stoi(str);
    //cout<<"n is "<<n<<endl;
    
    string mode;
    getline(file, mode);
    //cout<<"Mode is "<<mode<<endl;
    
    getline(file, youplay);
    //cout<<"youplay is "<<youplay<<endl;
    
    getline(file, str);
    maxdepth = stoi(str);
    //cout<<"depth is "<<maxdepth<<endl;
    
    for (int i = 0; i < n; ++i)
    {
        getline(file, str);
        istringstream iss(str);
        vector<int> row;
        for (int j = 0; j < n; ++j)
        {
            int score;
            iss>>score;
            row.push_back(score);
        }
        scores.push_back(row);
    }
    //cout<<"Scores are"<<endl;
    for (int i = 0; i < n; ++i)
    {
        for (int j = 0; j < n; ++j)
        {
            //cout<<scores[i][j]<<" ";
        }
        //cout<<endl;
    }
    
    char board_state[n][n];
    for (int i = 0; i < n; ++i)
    {
        getline(file, str);
        istringstream iss(str);
        for (int j = 0; j < n; ++j)
        {
            char state;
            iss>>state;
            board_state[i][j] = state;
        }
    }
    //cout<<"Board State is"<<endl;
    for (int i = 0; i < n; ++i)
    {
        for (int j = 0; j < n; ++j)
        {
            //cout<<board_state[i][j]<<" ";
        }
        //cout<<endl;
    }
    
    file.close();
    
    vector<position> vacant_positions;
    vector<position> x_positions;
    vector<position> o_positions;
    
    for (int x = 0; x < n; ++x)
    {
        for (int y = 0; y < n; ++y)
        {
            if (board_state[x][y] != '.')
            {
                if (board_state[x][y] == 'X')
                {
                    x_positions.push_back(position(x, y));
                } else {
                    o_positions.push_back(position(x, y));
                }
            } else {
                vacant_positions.push_back(position(x, y));
            }
        }
    }
    
    gamestate game_state = forward_as_tuple(vacant_positions, x_positions, o_positions, youplay, 0);
    
    
    if (mode == "MINIMAX") {
        auto decision = minimax_decision(game_state);
        int x  = decision.first.first;
        int y = decision.first.second;
        string move = decision.second;
        cout<<move_to_alpha[y]<<x+1<<" "<<move<<endl;
        ofstream outfile;
        outfile.open("output.txt");
        outfile<<move_to_alpha[y]<<x+1<<" "<<move<<endl;
        
        auto output_state = result(decision, game_state);
        printBoard(outfile, output_state);
        outfile.close();
    } else if (mode == "ALPHABETA" || mode == "COMPETITION") {
        auto decision = alpha_beta_search(game_state);
        int x  = decision.first.first;
        int y = decision.first.second;
        string move = decision.second;
        cout<<move_to_alpha[y]<<x+1<<" "<<move<<endl;
        ofstream outfile;
        outfile.open("output.txt");
        outfile<<move_to_alpha[y]<<x+1<<" "<<move<<endl;
        
        auto output_state = result(decision, game_state);
        printBoard(outfile, output_state);
        outfile.close();
    }
    
    return 0;
}
