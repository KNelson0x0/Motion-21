#pragma once

#ifndef CIRCULAR_IMPORTS // Why bother? These are included in tools/utilities that could be used in other projects. If no CI, this wouldn't work without this clause. Thats why.
#include <vector>
#include <iostream>
#include <utility>
#include <cstdarg>
using namespace std;

void debug_log(const char* msg, ...) {
#ifdef _DEBUG
	static const auto MAX_BUFFER_SIZE = 1024;
	static char buffer[MAX_BUFFER_SIZE] = "";
	va_list va;
	va_start(va, msg);
	vsnprintf_s(buffer, MAX_BUFFER_SIZE, msg, va);
	va_end(va);
	printf("%s \n", buffer);
#endif
}
#endif // !CIRCULAR_IMPORTS

// not today ptrs.
template<class T>
struct is_ptr : std::false_type {};
template<class T>
struct is_ptr<T*> : std::true_type {};
template<class T>
struct is_ptr<T* const> : std::true_type {};
template<class T>
struct is_ptr<T* volatile> : std::true_type {};
template<class T>
struct is_ptr<T* const volatile> : std::true_type {};

template <typename K, typename V>
class Dictionary { // basically a wrapper around vector to emulate python dicts.
public: // p-types
	struct ENTRY { // basically just slimmed down pair
	public: // p-methods
		ENTRY(pair<K, V> entry) : key(entry.first), value(entry.second) {}; // pair "compatibility". neato.
		ENTRY(K key, V value) : key(key), value(value) {};
	public: // p-attributes
		K key;
		V value;
	};
public: // p-methods, some overloads for extra flexibility
	Dictionary() {};
	Dictionary(ENTRY entry) { dict.push_back(entry); };
	Dictionary(K key, V value) { dict.push_back({ key, value }); };

	bool add(ENTRY entry) { return add(entry.key, entry.value); }
	bool add(K key, V value) {
		long our_null = 0xFFFFFFFFFFFFFFFF; // 0's will often need to be stored i'd assume, int maxs' will not. less room for error.
		V result = (V)our_null;

		if (is_ptr<V>::value) result = nullptr;
		find(key, result);
		if (is_ptr<V>::value) {
			if (result == nullptr) {
				dict.push_back({ key, value });
				return true;
			}
		} else {
			if (result == (V)our_null) {
				dict.push_back({ key, value });
				return true;
			}
		}

		debug_log("[Dictionary]> Key already exists.");
		return false;
	}
	bool remove(ENTRY entry) { return remove(entry.key); }
	bool remove(K key) {
		int result = get_index(key);

		if (result == -1) {
			debug_log("[Dictionary]> Key does not exist.");
			return false;
		}

		dict.erase((dict.begin() + result));
		debug_log("[Dictionary]> Removed key");
		return true;
	}
	bool update(ENTRY entry) { return update(entry.key, entry.value); }
	bool update(K key, V new_value) {
		int result = get_index(key);

		if (result == -1) {
			debug_log("[Dictionary]> Key doesn't exist."); // would add it automatically but this is the update function. not the add.
			return false;
		}

		dict[result].value = new_value;

		return false;
	}
	void find(K key, V& out_value) {
		for (ENTRY i : dict) { // avoidin dem autos
			if (i.key == key) {
				out_value = i.value;
				return;
			};
		}
	}
	int get_index(ENTRY entry) { return get_index(entry.key); }
	int get_index(K key) {
		for (int i{}; i < dict.size(); i++)
			if (dict[i].key == key) return i;

		debug_log("[Dictionary]> Nothing found");
		return -1;
	}
	void display() {
		cout << "Dictionary_Object: {\n";
		for (ENTRY i : dict) cout << "\t" << i.key << " : " << i.value << ",\n";
		cout << "}\n";
	}

	V& operator[](K key) {
		for (ENTRY& i : dict) { // avoidin dem autos
			if (i.key == key) {
				return i.value;
			};
		}
	}
	ENTRY& operator[](int index) {
		return ((ENTRY&)dict[index]);
	}
private: // pv-attributes
	vector<ENTRY> dict;
};

template <typename K, typename V> // didn't want to have to always type out "Dictionary"
using Dict = Dictionary<K, V>;
