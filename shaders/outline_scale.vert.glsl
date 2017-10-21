#version 330 core

layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec2 aTexture;
layout (location = 2) in vec3 aNormal;

out vec2 ourTexture;
out vec3 ourPosition;
out vec3 ourNormal;

uniform mat4 uModel;
uniform mat4 uProjectionView;
uniform float uOutlineWidth;

void main()
{
    ourPosition = vec3(uModel * vec4(aPosition + aNormal * uOutlineWidth, 1.0));
    ourNormal = aNormal;
    ourTexture = aTexture;

    gl_Position = uProjectionView * vec4(ourPosition, 1.0);
}
