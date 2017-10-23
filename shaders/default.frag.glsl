#version 330 core

out vec4 fragColor;

in vec2 ourTexture;
in vec3 ourPosition;
in vec3 ourNormal;

uniform sampler2D uTexAmbient;
uniform sampler2D uTexDiffuse;
uniform sampler2D uTexSpecular;
uniform sampler2D uTexEmissive;

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

vec3 alphaBlend(vec4 src, vec3 dst)
{
    return dst * (1.0 - src.a) + src.rgb;
}

void main()
{
    // Read textures
    vec4 texAmbient = texture(uTexAmbient, ourTexture);
    vec4 texDiffuse = texture(uTexDiffuse, ourTexture);
    vec4 texSpecular = texture(uTexSpecular, ourTexture);
    vec4 texEmissive = texture(uTexEmissive, ourTexture);

    // Ambient
    vec3 ambient = uSun.ambientColor * alphaBlend(texAmbient, uMaterial.ambientColor);

    // Diffuse 
    vec3 norm = normalize(ourNormal);
    vec3 lightDir = normalize(uSun.lightDirection);
    float diff = max(dot(norm, -lightDir), 0.0);
    vec3 diffuse = diff * uSun.diffuseColor * alphaBlend(texDiffuse, uMaterial.diffuseColor);

    // Specular
    vec3 viewDir = normalize(uViewPosition - ourPosition);
    vec3 halfwayDir = normalize(-lightDir + viewDir);  
    float spec = pow(max(dot(norm, halfwayDir), 0.0), uMaterial.specularExponent);
    vec3 specular = spec * uSun.specularColor * alphaBlend(texSpecular, uMaterial.specularColor);

    // Emissive
    vec3 emissive = alphaBlend(texEmissive, uMaterial.emissiveColor);

    // Combine
    fragColor = vec4(ambient + diffuse + specular + emissive, uMaterial.alpha);

    // Apply gamma correction
    fragColor.rgb = pow(fragColor.rgb, vec3(1.0 / uGamma));
}
