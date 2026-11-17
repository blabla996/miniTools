#include <iostream>
#include <vector>
using namespace std;

vector<int> numbers (4);

void introduction ();
void calculation();
void inputs ();
bool calculation_helper (vector<bool>& used, double total, string& process);


int main () {
    introduction();
    bool next = true;
    char c;
    while (next) {
        calculation();
        cout << endl;

        cout << "Do you wanna next round? (y/n)" << endl;
        cin >> c;
        cout << endl;

        next = (c == 'y');
    }

    cout << "Good bye" << endl;
}


void introduction () {
    cout << "Welcome to the 24 game calculator" << endl;
    cout << "Please enter 4 number each one between 1-10" << endl;

    cout << "Calculation is from left to right" << endl;
}

void inputs () {
    int i = 0;
    while (i < 4) {
        cout << "Enter the number " << i+1 << ": ";
        cin >> numbers[i];
        cout << endl;

        if (numbers[i] < 1 or numbers[i] > 10) cout << "The number is not correct" << endl;
        else i++;
    }
}

void calculation() {
    inputs();

    bool found = false;
    for (int i = 0 ; i < 4; ++i) {
        string process = to_string(numbers[i]);
        vector<bool> used (4,false);
        used[i] = true;

        if (calculation_helper(used, numbers[i], process)) {
            cout << process << endl;
            found = true;
            break;
        }
    }
    if (not found) cout << "no" << endl;
}

bool calculation_helper(vector<bool>& used, double total, string& process) {
    bool allused = true; 
    for (bool b: used) {
        if (!b) allused = false;
    }

    if (total == 24 and allused) return true;
    
    for (int i = 0; i < 4; ++i) {
        if (!used[i]) {
            used[i] = true;
            string numStr = to_string(numbers[i]);
            string originalProcess = process;


        
            process = originalProcess + " + " + numStr;
            if (calculation_helper(used, total + numbers[i], process)) {
                return true;
            }

            
            process = originalProcess + " - " + numStr;
            if (calculation_helper(used, total - numbers[i], process)) {
                return true;
            }

            
            process = originalProcess + " * " + numStr;
            if (calculation_helper(used, total * numbers[i], process)) {
                return true;
            }

            
            if (numbers[i] != 0) {
                process = originalProcess + " / " + numStr;
                if (calculation_helper(used, total / numbers[i], process)) {
                    return true;
                }
            }

            
            process = originalProcess;
            used[i] = false;
        }
    }

    return false;  
}

