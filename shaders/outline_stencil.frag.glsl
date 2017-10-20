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

struct Sun
{
    vec3 ambientColor;
    vec3 diffuseColor;
    vec3 specularColor;
    vec3 lightDirection;
};
uniform Sun uSun;

uniform vec3 uViewPosition;
uniform float uGamma;

void main()
{
    // Ambient
    vec3 ambient = uSun.ambientColor * uMaterial.ambientColor;

    // Diffuse 
    vec3 norm = normalize(ourNormal);
    vec3 lightDir = normalize(uSun.lightDirection);
    float diff = max(dot(norm, -lightDir), 0.0);
    vec3 diffuse = diff * uSun.diffuseColor * uMaterial.diffuseColor;

    // Specular
    vec3 viewDir = normalize(uViewPosition - ourPosition);
    vec3 halfwayDir = normalize(-lightDir + viewDir);  
    float spec = pow(max(dot(norm, halfwayDir), 0.0), uMaterial.specularExponent);
    vec3 specular = spec * uSun.specularColor * uMaterial.specularColor;

    fragColor = vec4(ambient + diffuse + specular + uMaterial.emissiveColor, uMaterial.alpha) * 0.2;

    // Apply gamma correction
    fragColor.rgb = pow(fragColor.rgb, vec3(1.0 / uGamma));
}
