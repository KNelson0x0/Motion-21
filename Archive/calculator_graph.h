#pragma once
/*

enum HandLandMark {
	WRIST = 0,
	THUMB_CMC = 1,
	THUMB_MCP = 2,
	THUMB_IP = 3,
	THUMB_TIP = 4,
	INDEX_FINGER_MCP = 5,
	INDEX_FINGER_PIP = 6,
	INDEX_FINGER_DIP = 7,
	INDEX_FINGER_TIP = 8,
	MIDDLE_FINGER_MCP = 9,
	MIDDLE_FINGER_PIP = 10,
	MIDDLE_FINGER_DIP = 11,
	MIDDLE_FINGER_TIP = 12,
	RING_FINGER_MCP = 13,
	RING_FINGER_PIP = 14,
	RING_FINGER_DIP = 15,
	RING_FINGER_TIP = 16,
	PINKY_MCP = 17,
	PINKY_PIP = 18,
	PINKY_DIP = 19,
	PINKY_TIP = 20
};
*/

#ifndef CIRCULAR_IMPORTS // Why bother? These are included in tools/utilities that could be used in other projects. If no CI, this wouldn't work without this clause. Thats why.

#include <string>
#include "dictionary.h"
using namespace std;

#endif // !CIRCULAR_IMPORTS

typedef void* CalculatorGraphConfig; // need to rebuild

class CalculatorGraph {

	enum GraphInputStreamAddMode {
		WAIT_TILL_NOT_FULL,
		ADD_IF_NOT_FULL
	};

	/*
	CalculatorGraph(Dict<string, void*> args) {
		bool init_with_binary_graph = false;
		bool init_with_graph_proto = false;
		bool init_with_validated_graph_config = false;
		CalculatorGraphConfig graph_config_proto = nullptr;

		for (int i{}; args.size(); i++) {
			const std::string& key = kw.first.cast<std::string>();
			if (key == "binary_graph_path") {
				init_with_binary_graph = true;
				std::string file_name(kw.second.cast<py::object>().str());
				graph_config_proto = ReadCalculatorGraphConfigFromFile(file_name);
			} else if (key == "graph_config") {
				init_with_graph_proto = true;
				graph_config_proto =
					ParseProto<CalculatorGraphConfig>(kw.second.cast<py::object>());
			} else if (key == "validated_graph_config") {
				init_with_validated_graph_config = true;
				graph_config_proto =
					py::cast<ValidatedGraphConfig*>(kw.second)->Config();
			} else {
				throw RaisePyError(
					PyExc_RuntimeError,
					absl::StrCat("Unknown kwargs input argument: ", key).c_str());
			}
		}
	}*/

};