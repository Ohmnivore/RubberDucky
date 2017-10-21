#version 330 core

layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec2 aTexture;
layout (location = 2) in vec3 aNormal;

uniform mat4 uModel;
uniform mat4 uProjectionView;
uniform float uOutlineWidth;

void main()
{
    gl_Position = uProjectionView * uModel * vec4(aPosition + aNormal * uOutlineWidth, 1.0);
}
