// do not want to risk integer collisions for checking against null but still want to support elements with "nothing" in them;
#pragma once

// macro abuse: https://i.pinimg.com/originals/92/77/ed/9277ed22bd2a2244ef3f0dbc4a4b1a04.jpg
// for any custom types add your own none_method entry into none
#define none_method(T, ret) bool operator==(T& anything) { return ret; } \
	bool operator==(T* anything) { return ret; }                         \
	bool operator==(const T& anything) { return ret; }                   \
	bool operator==(const T* anything) { return ret; }                   \
	bool operator==(volatile T& anything) { return ret; }                \
	bool operator==(volatile T* anything) { return ret; }

struct None { // only structing so i dont have to use the public keyword. yes I realize typing this was more effort.
	None() { /*nothing*/ };
	None(const void* none) {}; // sanity check more than anything

	operator int() { return -1; };

	none_method(None, true);
	none_method(int, false);
	none_method(unsigned int, false);
	none_method(float, false);
	none_method(double, false);
	none_method(long double, false);
	none_method(char, false);
	none_method(unsigned char, false);
	none_method(long, false);
	none_method(long long, false);
	none_method(unsigned long, false);
	none_method(unsigned long long, false);
	none_method(short, false);

	bool operator==(void* anything) { return false; }
	bool operator==(const void* anything) { return false; }
};

#undef none_method