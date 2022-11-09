#pragma once
#ifndef CIRCULAR_IMPORTS // Why bother? These are included in tools/utilities that could be used in other projects. If no CI, this wouldn't work without this clause. Thats why.

#include <string>
#include <vector>
//#include "windowslight.h"

using namespace std;
#endif // !CIRCULAR_IMPORTS


vector<string> split(string src, const char* delimeter) {
    vector<string> ret;
    char* copy = _strdup(src.c_str());
    char* token = nullptr, *dump_token = nullptr;

    token = strtok_s(copy, delimeter, &dump_token);

    while (token != nullptr) {
        if (token != nullptr) ret.push_back(token);
        token = strtok_s(nullptr, delimeter, &dump_token);
    }
    return ret;
}

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

template<typename T, typename V>
bool in_vector(vector<T> vec, V to_find) {
    for (int i{}; i < vec.size(); i++) 
        if (vec[i] == to_find) return true;

    return false;
}

template<typename T, typename V>
int in_vector_at(vector<T> vec, V to_find) {
    for (int i{}; i < vec.size(); i++)
        if (vec[i] == to_find) return i;

    return -1;
}