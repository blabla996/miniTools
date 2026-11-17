#include <iostream>
#include <vector>
#include <random>
using namespace std;

int num_players = 2;
int level = 1;

void game_settings () { 
    cout << "number player (min 2): \n";
    cin >> num_players;
    cout << "level (min 1): \n";
    cin >> level;
}

int generated_number () {
    // FIX: Using the compilation time string to create a changing hash value.
    // This bypasses the broken random_device on Windows.
    string t = __TIME__; 
    unsigned int seed = 0;
    for (char c : t) {
        seed = seed * 31 + c;
    }

    static mt19937 gen(seed);
    uniform_int_distribution<int> distribution(1, 100);

    int random_number = distribution(gen);
    return random_number;
}

int main () {
    game_settings();
    vector<vector<int>> player_numbers(num_players);
    vector<bool> numbers(100, false);

    for (int i = 0; i < num_players; i++) {
        for (int j = 0; j < level; j++) {
            int n = generated_number();

            while (numbers[n-1]) n = generated_number();
            player_numbers[i].push_back(n);
            numbers[n-1] = true;
        }
    }

    for (int i = 0; i < num_players; i++) {
        cout << string(50, '\n');
        cout << "=== PLAYER " << (i + 1) << " ===\n";
        cout << "press y and enter to read your numbers\n";
        string enter;
        cin >> enter;
        
        for (int j = 0; j < level; j++) {
            cout << player_numbers[i][j] << " ";
        }

        cout << "\n\npress y for the next player\n";
        cin >> enter;
    }

    // Clear the screen one final time so the last player's cards are hidden
    cout << string(50, '\n');
    cout << "All players have seen their numbers! Ready to start the game.\n";
    
    return 0;
}
