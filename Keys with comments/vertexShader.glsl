//written in GLSL version 3.30.
#version 330 core

// is a declaration of an input variable
// The "layout(location = 0)" specifies that this input variable is bound to location 0,
// which set by the code that sets up the vertex buffer object.
layout(location = 0) in vec3 vPos;

void main()
{
    // position of the vertex in clip space using the "gl_Position" variable.
    // It does this by creating a vec4 with the x, y, and z components of vPos and a w component of 1.0.
    // This w component is necessary because OpenGL expects homogeneous coordinates for vertices
    // The resulting vec4 is assigned to gl_Position,
    // which is a built-in output variable in the vertex shader that specifies the final position of the vertex in clip space.
    // gl_Position = vec4( vPos.xyz, 2.0); -- will be half of the opened window
    gl_Position = vec4( vPos.xyz, 1.0);
}