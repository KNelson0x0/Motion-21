import customtkinter as CT
from typing import Union, Tuple, List, Dict, Callable, Optional

from GUI.custom_segmented_button import CustomSegmentedButton

class CustomTabview(CT.CTkTabview): # minor modifications allow for callbacks where I wanted them
    def __init__(self,
                master: any,
                width: int = 300,
                height: int = 250,
                corner_radius: Optional[int] = None,
                border_width: Optional[int] = None,

                bg_color: Union[str, Tuple[str, str]] = "transparent",
                fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                border_color: Optional[Union[str, Tuple[str, str]]] = None,

                segmented_button_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                segmented_button_selected_color: Optional[Union[str, Tuple[str, str]]] = None,
                segmented_button_selected_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                segmented_button_unselected_color: Optional[Union[str, Tuple[str, str]]] = None,
                segmented_button_unselected_hover_color: Optional[Union[str, Tuple[str, str]]] = None,

                text_color: Optional[Union[str, Tuple[str, str]]] = None,
                text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None,

                command: Union[Callable, None] = None,
                state: str = "normal",
                **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, segmented_button_fg_color, segmented_button_selected_color,
                   segmented_button_selected_hover_color, segmented_button_unselected_color, segmented_button_unselected_hover_color, text_color, text_color_disabled,
                   command, state, **kwargs)

        
        self._segmented_button = CustomSegmentedButton(self,
                                                    values=[],
                                                    height=self._button_height,
                                                    fg_color=segmented_button_fg_color,
                                                    selected_color=segmented_button_selected_color,
                                                    selected_hover_color=segmented_button_selected_hover_color,
                                                    unselected_color=segmented_button_unselected_color,
                                                    unselected_hover_color=segmented_button_unselected_hover_color,
                                                    text_color=text_color,
                                                    text_color_disabled=text_color_disabled,
                                                    corner_radius=corner_radius,
                                                    border_width=self._segmented_button_border_width,
                                                    command=self._segmented_button_callback,
                                                    state=state)

    def add(self, name: str) -> CT.CTkFrame:
        return self.insert(len(self._tab_dict), name)

    def insert(self, index: int, name: str) -> CT.CTkFrame:
        """ creates new tab with given name at position index """

        if name not in self._tab_dict:
            # if no tab exists, set grid for segmented button
            if len(self._tab_dict) == 0:
                self._set_grid_segmented_button()

            self._name_list.insert(index, name)
            self._tab_dict[name] = self._create_tab()
            self._segmented_button.insert(index, name)
            self._configure_tab_background_corners_by_name(name)

            return self._tab_dict[name]
        else:
            raise ValueError(f"CTkTabview already has tab named '{name}'")
