#version 330 core

layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec2 aTexture;
layout (location = 2) in vec3 aNormal;

uniform mat4 uModel;
uniform mat4 uTransposeInverseModel;
uniform mat4 uView;
uniform mat4 uProjection;
uniform float uOutlineWidth;
uniform float uOutlineHeight;

void main()
{
    vec4 clipSpacePosition = uProjection * uView * uModel * vec4(aPosition, 1.0);
    vec4 clipSpaceNormal = uProjection * vec4(normalize(mat3(uTransposeInverseModel) * aNormal), 1.0);
    clipSpaceNormal.z = 0.0;
    vec3 clipSpaceNormalv3 = normalize(clipSpaceNormal.xyz) * clipSpacePosition.w;
    clipSpaceNormalv3.x *= uOutlineWidth;
    clipSpaceNormalv3.y *= uOutlineHeight;

    clipSpacePosition.xy += clipSpaceNormalv3.xy;
    clipSpacePosition.z += 0.00000001; // Nudge forward a tiny bit to barely pass the depth test
    gl_Position = clipSpacePosition;
}
