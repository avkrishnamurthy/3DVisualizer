# 3D Visualizer

This is a project that I created after using CAD for the first time. I was in my engineering class, and having to learn CAD for a project. I was also taking Linear Algebra at the same time. Traditional CAD tools are extremely powerful but often required a steep learning curve and lack the simpler interaction I craved. This sparked the idea of leveraging Python, numpy, pynput, pygame, and linear algebra to create a solution that would make 3D visualization easy. This project offers a way to translate raw geometric data into interactive and visually appealing 3D renderings. Whether for educational purposes or creative exploration, this project opens up new avenues for users to understand and interact with complex 3D structures.

## How it works
This project is built in Python. It uses the numpy package for efficient numerical computations, including vector and matrix operations necessary for transforming and manipulating 3D coordinates. The project utilizes pynput to capture keyboard inputs and allow users to interactively control the view and orientation of the rendered 3D object, with click-and drag rotation of the object. It also leverages pygame to create a graphical user interface and rendering environment, with its capabilities to draw lines connecting vertices, creating the illusion of a 3D object when projected onto a 2D screen. The project also incorporates shading and perspective adjustments to enhance the visual realism of the 3D object.

## See it in action
[Watch the demo](https://youtu.be/dsEMaCYsBhw)

## How to run

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


If you want to use your own object, simply create a new .txt file in this directory with the following format:
- The first line should contain two integers, with the first being the number of vertices that define the 3D object, and the second being the number of faces
- Starting at the second line each line will define one vertex of the 3D object and will consist of an integer (which is the ID of the vertex) followed by three real numbers that define the (x, y, z) coordinates of the vertex. The number of these lines should match the first number of the first line.
- After the vertex section should be a section defining the faces of the object. The number of lines in this section should be equal to the second number on the first line of the file. Each line in this section should consist of three integers that define a triangle that is a face of the object, in which the three integers each refer to the ID of a vertex from the vertex section of the file.


## Technologies 

<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
<img src="https://custom-icon-badges.demolab.com/badge/pygame-150458.svg?logo=grey-pygame"/>

