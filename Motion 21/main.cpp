// APPLICATION MAIN
#define CIRCULAR_IMPORTS
#include "includes.h"
#include "tools.h"
#include "dictionary.h"
#include "solutionbase.h"
#include "none.h"

//#include "calculator_graph.h"




int main() {

	int a = 1, b = 2;
	int* a_ptr = &a, * b_ptr = &b;


	SolutionBase cool;
	Dict<int*, int> test(a_ptr, -1);

	test.add(b_ptr, b);

	cout << "start\n";

	unsigned long x = 696969;
	cout << "uhhh\n";
	if (a == x) cout << "swaggus\n";

	unsigned long* swag1 = &x;
	unsigned long* swag2 = &x;

	cout << "swag1: " << &swag1 << "\n";
	cout << "swag2: " << &swag2 << "\n";

	unsigned long* swag2_addy = (unsigned long*)(&swag2);

	cout << "swag2_addy_ptr: " << swag2_addy << "\n";
	if (swag2 == *(unsigned long**)swag2_addy) cout << "swaggus2\n";

	cout << "end\n";


	test.display();
	cout << split("Testing.This.Is.Much.More.Annoying.In.C", ".")[3] << "\n";	

	cout << "end\n";


	return 0;
}