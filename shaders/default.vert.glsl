#version 330 core

layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec2 aTexture;
layout (location = 2) in vec3 aNormal;

out vec2 ourTexture;
out vec3 ourPosition;
out vec3 ourNormal;

uniform mat4 uModel;
uniform mat4 uTransposeInverseModel;
uniform mat4 uProjectionView;

void main()
{
    ourPosition = vec3(uModel * vec4(aPosition, 1.0));
    ourNormal = mat3(uTransposeInverseModel) * aNormal;
    ourTexture = aTexture;

    gl_Position = uProjectionView * vec4(ourPosition, 1.0);
}
