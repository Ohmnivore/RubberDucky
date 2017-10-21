#version 330 core

out vec4 fragColor;

in vec2 ourTexture;
in vec3 ourPosition;
in vec3 ourNormal;

void main()
{
    fragColor = vec4(0.0, 0.0, 0.0, 1.0);
}
