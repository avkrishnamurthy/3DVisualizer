# 3D Visualizer

I used the numpy package for matrix/vector operations and interpolation, the pynput library to monitor mouse clicking and cursor location for click and drag functionality, and pygame as the window to graph 3D objects. 

## Running

### Usage Options

These options are used to run the visualization.

| option | effect | default |
| ----   |  ----- |  ----- |
| input | The .txt file to be displayed | object.txt |
| shaded | Show faces of object as shaded based on viewing angle. | False |

**Example:**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```python main.py --input object.txt```

To see a wireframe of the object represented by the data in object.txt

**OR**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```python main.py --input object.txt --shaded```

To see the object with shaded faces represented by the data in object.txt


