#version 330 core

layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec2 aTexture;
layout (location = 2) in vec3 aNormal;

out vec2 ourTexture;
out vec3 ourNormal;

void main()
{
    gl_Position = vec4(aPosition, 1.0);

    ourTexture = aTexture;
    ourNormal = aNormal;
}
