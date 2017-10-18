#version 330 core

out vec4 FragColor;

in vec2 ourTexture;
in vec3 ourNormal;

struct Material
{
    vec3 ambientColor;
    vec3 diffuseColor;
    vec3 specularColor;
    float specularExponent;
    float alpha;
};
uniform Material uMaterial;

struct Sun
{
    vec3 ambientColor;
    float ambientStrength;
    vec3 diffuseColor;
    float diffuseStrength;
    vec3 specularColor;
    float specularStrength;
    vec3 lightDirection;
};
uniform Material uSun;

void main()
{
    FragColor = vec4(uMaterial.diffuseColor.rgb, 1.0);
}
