#include <iostream>

int factorial(int n) {
    if (n == 0 || n == 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

int main() {
    int num = 5;
    int result = factorial(num);
    
    std::cout << "The factorial of " << num << " is " << result << std::endl;
    
    return 0;
}
