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
uniform Sun uSun;

uniform vec3 uViewPosition;

void main()
{
    // ambient
    vec3 ambient = uSun.ambientStrength * uSun.ambientColor * uMaterial.ambientColor;

    // diffuse 
    vec3 norm = normalize(ourNormal);
    vec3 lightDir = normalize(uSun.lightDirection);
    float diff = max(dot(norm, -lightDir), 0.0);
    vec3 diffuse = diff * uSun.diffuseStrength * uSun.diffuseColor * uMaterial.diffuseColor;

    // specular
    vec3 viewDir = normalize(uViewPosition - ourPosition);
    vec3 halfwayDir = normalize(-lightDir + viewDir);  
    float spec = pow(max(dot(norm, halfwayDir), 0.0), uMaterial.specularExponent);
    vec3 specular = spec * uSun.specularStrength * uSun.specularColor * uMaterial.specularColor;

    fragColor = vec4(ambient + diffuse + specular, uMaterial.alpha);
}
