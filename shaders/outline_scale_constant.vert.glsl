#version 330 core

layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec2 aTexture;
layout (location = 2) in vec3 aNormal;

out vec2 ourTexture;
out vec3 ourPosition;
out vec3 ourNormal;

uniform mat4 uModel;
uniform mat4 uTransposeInverseModel;
uniform mat4 uView;
uniform mat4 uProjection;
uniform float uOutlineWidth;

void main()
{
    ourPosition = vec3(uModel * vec4(aPosition, 1.0));
    ourNormal = aNormal;
    ourTexture = aTexture;

    vec4 worldSpacePosition = uProjection * uView * vec4(ourPosition, 1.0);
    vec4 worldSpaceNormal = uProjection * vec4(normalize(mat3(uTransposeInverseModel) * ourNormal), 1.0);
    worldSpacePosition += normalize(worldSpaceNormal) * worldSpacePosition.w * uOutlineWidth;

    gl_Position = worldSpacePosition;
}
