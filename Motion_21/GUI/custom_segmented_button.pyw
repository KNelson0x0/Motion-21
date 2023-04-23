import tkinter
from typing import Union, Tuple, List, Dict, Callable, Optional

from customtkinter.windows.widgets.font                 import CTkFont
from customtkinter.windows.widgets.ctk_segmented_button import CTkSegmentedButton

class CustomSegmentedButton(CTkSegmentedButton): # just needed to edit set so that it would allow me to call my callback
    def __init__(self,
                 master: any,
                 width: int = 140,
                 height: int = 28,
                 corner_radius: Optional[int] = None,
                 border_width: int = 3,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 selected_color: Optional[Union[str, Tuple[str, str]]] = None,
                 selected_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 unselected_color: Optional[Union[str, Tuple[str, str]]] = None,
                 unselected_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None,
                 background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,

                 font: Optional[Union[tuple, CTkFont]] = None,
                 values: Optional[list] = None,
                 variable: Union[tkinter.Variable, None] = None,
                 dynamic_resizing: bool = True,
                 command: Union[Callable[[str], None], None] = None,
                 state: str = "normal",
                 **kwargs):

        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, selected_color, selected_hover_color,
                         unselected_color, unselected_hover_color, text_color, text_color_disabled, background_corner_colors,
                         font, values, variable, dynamic_resizing, command, state, **kwargs)
        
    def set(self, value: str, from_variable_callback: bool = False, from_button_callback: bool = False):
        if value in self._buttons_dict:
            self._select_button_by_value(value)

            if self._variable is not None and not from_variable_callback:
                self._variable_callback_blocked = True
                self._variable.set(value)
                self._variable_callback_blocked = False
        else:
            if self._current_value in self._buttons_dict:
                self._unselect_button_by_value(self._current_value)
            self._current_value = value

            if self._variable is not None and not from_variable_callback:
                self._variable_callback_blocked = True
                self._variable.set(value)
                self._variable_callback_blocked = False

        if from_button_callback:
            if self._command is not None:
                self._command(self._current_value)

    def insert(self, index: int, value: str):
        if value not in self._buttons_dict:
            if value != "":
                self._value_list.insert(index, value)
                self._buttons_dict[value] = self._create_button(index, value)

                self._configure_button_corners_for_index(index)
                if index > 0:
                    self._configure_button_corners_for_index(index - 1)
                if index < len(self._buttons_dict) - 1:
                    self._configure_button_corners_for_index(index + 1)

                self._create_button_grid()

                if value == self._current_value:
                    self._select_button_by_value(self._current_value)

                self._buttons_dict[value].configure(fg_color=self._sb_selected_color, hover_color=self._sb_selected_hover_color) # activate color
            else:
                raise ValueError(f"CTkSegmentedButton can not insert value ''")
        else:
            raise ValueError(f"CTkSegmentedButton can not insert value '{value}', already part of the values")