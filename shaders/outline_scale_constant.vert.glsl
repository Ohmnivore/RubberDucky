#version 330 core

layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec2 aTexture;
layout (location = 2) in vec3 aNormal;

uniform mat4 uModel;
uniform mat4 uTransposeInverseModel;
uniform mat4 uView;
uniform mat4 uProjection;
uniform float uOutlineWidth;

void main()
{
    vec4 worldSpacePosition = uProjection * uView * vec4(aPosition, 1.0);
    vec4 worldSpaceNormal = uProjection * vec4(normalize(mat3(uTransposeInverseModel) * aNormal), 1.0);
    worldSpacePosition.z = 0.0;
    worldSpacePosition.xyz += normalize(worldSpaceNormal.xyz) * worldSpacePosition.w * uOutlineWidth;

    gl_Position = worldSpacePosition;
}
