from config import *
from GUI.ASL_GUI import App
import os


class Geometry:
    def __init__(self, width = 0, height = 0):
        self.width = width
        self.height = height

class IDefinitelyDoNotHateUnitTesting:
    def __init__(self):
        pass

    def test_save_and_retrieve_attributes(self):
        # Create a Config instance
        app = App()
        cfg = Config("Test Config")

        # Define some attributes to save
        geometry = Geometry(800, 600)
        x = 42.0

        # Save the attributes
        cfg.save(geometry, ["width", "height"], "geo")
        cfg.save(app, ["s_title"], "app")
        cfg.save_var(x, "x")

        # Retrieve the attributes and verify they are correct
        assert cfg["geo"]["width"]["var"] == "800"
        assert cfg["geo"]["height"]["var"] == "600"
        assert cfg["app"]["s_title"]["var"] == "Test App Everyone Loves Unit Testing"
        assert cfg["x"]["var"] == 42.0

        os.system('color 2')
        print("""
       _
      ( |
    ___\\ \\
   (__()  `-|
   (___()   |
   (__()    |
   (_()__.--|
        """)


