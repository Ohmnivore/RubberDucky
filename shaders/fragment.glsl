#version 330 core

out vec4 FragColor;

in vec2 ourTexture;
in vec3 ourNormal;

struct Material
{
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    float specularExponent;
    float alpha;
};
uniform Material uMaterial;

void main()
{
    FragColor = vec4(uMaterial.diffuse.rgb, 1.0);
}
