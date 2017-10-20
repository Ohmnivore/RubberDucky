#version 330 core

out vec4 fragColor;

in vec2 ourTexture;
in vec3 ourPosition;
in vec3 ourNormal;

struct Material
{
    vec3 ambientColor;
    vec3 diffuseColor;
    vec3 specularColor;
    float specularExponent;
    vec3 emissiveColor;
    float alpha;
};
uniform Material uMaterial;

void main()
{
    // Ambient
    vec3 ambient = uMaterial.ambientColor;

    // Diffuse
    vec3 diffuse = uMaterial.diffuseColor;

    // Specular
    float spec = pow(0.01, uMaterial.specularExponent);
    vec3 specular = spec * uMaterial.specularColor;

    fragColor = vec4(ambient + diffuse + specular + uMaterial.emissiveColor, uMaterial.alpha) * 0.0000001;
}
