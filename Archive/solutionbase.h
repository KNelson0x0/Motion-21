#pragma once
#ifndef CIRCULAR_IMPORTS // Why bother? These are included in tools/utilities that could be used in other projects. If no CI, this wouldn't work without this clause. Thats why.

#include "dictionary.h"
#include "calculator_graph.h"
#include <set>

#endif // !CIRCULAR_IMPORTS

#define RANGE(range) (int i{}; i<range; i++) // yes im this lazy
// TO MAKE Solution Base:
// > To Init <
// NEED: SIDE_INPUTS [Dictionary, maybe even unordered map]
// NEED: CALCULATOR_PARAMS [Dictionary or UMap]
// TO MAKE CALCULATOR PARAMS:
// NEED: CalculatorGraph and CalculatorGraphConfig
// NEED: OUTPUTS: str list [vector<string>]

// hands ->
// solution base -> 
// solution base inited with:
// 
// super().__init__(
// binary_graph_path = _BINARYPB_FILE_PATH,
// side_inputs = {
//     'model_complexity': model_complexity,
//     'num_hands' : max_num_hands,
//     'use_prev_landmarks' : not static_image_mode,
// },
// calculator_params = {
//     'palmdetectioncpu__TensorsToDetectionsCalculator.min_score_thresh':
//         min_detection_confidence,
//     'handlandmarkcpu__ThresholdingCalculator.threshold' :
//         min_tracking_confidence,
// },
// outputs = [
//     'multi_hand_landmarks', 'multi_hand_world_landmarks',
//         'multi_handedness'
// ])


// solution base: 
// 
// if calculator_params:
//      self._modify_calculator_options(canonical_graph_config_proto, calculator_params)
//da
/*
// def _modify_calculator_options(self, calculator_graph_config: calculator_pb2.CalculatorGraphConfig, calculator_params : Mapping[str, Any])->None:
     def generate_nested_calculator_params(flat_map):
          nested_map = {}
          for compound_name, field_value in flat_map.items():
            calculator_and_field_name = compound_name.split('.')
            if len(calculator_and_field_name) != 2:
              raise ValueError(
                  f'The key "{compound_name}" in the calculator_params is invalid.')
            calculator_name = calculator_and_field_name[0]
            field_name = calculator_and_field_name[1]
            if calculator_name in nested_map:
              nested_map[calculator_name].append((field_name, field_value))
            else:
              nested_map[calculator_name] = [(field_name, field_value)]
          return nested_map

    def modify_options_fields(calculator_options, options_field_list):
      for field_name, field_value in options_field_list:
        if field_value is None:
          calculator_options.ClearField(field_name)
        else:
          field_label = calculator_options.DESCRIPTOR.fields_by_name[
              field_name].label
          if field_label == descriptor.FieldDescriptor.LABEL_REPEATED:
            if not isinstance(field_value, Iterable):
              raise ValueError(
                  f'{field_name} is a repeated proto field but the value '
                  f'to be set is {type(field_value)}, which is not iterable.')
            calculator_options.ClearField(field_name)
            for elem in field_value:
              getattr(calculator_options, field_name).append(elem)
          else:
            setattr(calculator_options, field_name, field_value)

    nested_calculator_params = generate_nested_calculator_params(
        calculator_params)

    num_modified = 0
    for node in calculator_graph_config.node:
      if node.name not in nested_calculator_params:
        continue
      options_type = CALCULATOR_TO_OPTIONS.get(node.calculator)
      if options_type is None:
        raise ValueError(
            f'Modifying the calculator options of {node.name} is not supported.'
        )
      options_field_list = nested_calculator_params[node.name]
      if node.HasField('options') and node.node_options:
        raise ValueError(
            f'Cannot modify the calculator options of {node.name} because it '
            f'has both options and node_options fields.')
      if node.node_options:
        node_options_modified = False
        for elem in node.node_options:
          type_name = elem.type_url.split('/')[-1]
          if type_name == options_type.DESCRIPTOR.full_name:
            calculator_options = options_type.FromString(elem.value)
            modify_options_fields(calculator_options, options_field_list)
            elem.value = calculator_options.SerializeToString()
            node_options_modified = True
            break
        if not node_options_modified:
          calculator_options = options_type()
          modify_options_fields(calculator_options, options_field_list)
          node.node_options.add().Pack(calculator_options)
      else:
        modify_options_fields(node.options.Extensions[options_type.ext],
                              options_field_list)

      num_modified += 1
      if num_modified == len(nested_calculator_params):
        break
    if num_modified < len(nested_calculator_params):
      raise ValueError('Not all calculator params are valid.')
    */

class CalculatorGraphConfig {

};


class ValidatedGraphConfig { // ugh, i hate pybind: https://github.com/google/mediapipe/blob/master/mediapipe/python/pybind/validated_graph_config.cc
    void init(ValidatedGraphConfig* self, vector<string>) {
        bool init_with_binary_graph = false;
        bool init_with_graph_proto = false;

        CalculatorGraphConfig graph_config_proto; // ugh
    }
};


class SolutionBase {
public:
    typedef char IDK;
    typedef float IDKF; // idk float?
    
    struct SIDE_INPUTS {
        Dict<string, int>  int_params;
        Dict<string, bool> bool_params;
    };
    struct CALC_PARAMS {
        Dict<string, float> float_params;
        void clear_field() { cout << "Idk what this does yet\n"; }
    };
    struct OUTPUTS {
        vector<string> outs;
    };
public: 
    SolutionBase() {};
    SolutionBase(std::string binary_graph_path, SIDE_INPUTS side_inputs, CALC_PARAMS calculator_params, OUTPUTS outputs) {
        if (!binary_graph_path.empty()) {

        }
    };
private:
    Dict<string, vector<pair<string, IDKF>>> generate_nested_calculator_params(Dict<string, IDKF> flat_map) {
        Dict<string, vector<pair<string, IDKF>>> nested_map;
        vector<string> keys = flat_map.keys();
        vector<IDKF> values = flat_map.values();

        for RANGE(flat_map.size()) {
            vector<string> names = split(keys[i], ".");

            if (names.size() != 2) {
                i = flat_map.size(); // quit
                debug_log("Invalid calculator parms\n");
            }
               
            string calculator_name = names[0];
            string field_name = names[1];
            if (in_vector(nested_map.keys(), calculator_name)) {
                nested_map[calculator_name].push_back({ field_name, values[i] }); //  problem line 
            } else {
                nested_map.add({ calculator_name, { {field_name, values[i]} } }); // Dict(Vector(Pair)));
            }
        }

        return nested_map;
    };

    void modify_options_fields(CALC_PARAMS calculator_options, Dictionary<IDK, IDK> options_field_list) {
        //Dict<string, vector<pair<string, IDKF>>> nested_map;
        vector<IDK> field_names = options_field_list.keys();
        vector<IDK> field_values = options_field_list.values();

       for RANGE(options_field_list.size()) {
           if (field_values[i] == options_field_list.dict_null) {
               calculator_options.clear_field(); // dk what this does yet really
           } else {

           }
       }
    }
    //void modify_calc_options(CalculatorGraph calc_graph_config, Dict<string, IDK> calc_params) {

    //}
    
private: 
    IDK validated_graph; // validated_graph = validated_graph_config.ValidatedGraphConfig()
};