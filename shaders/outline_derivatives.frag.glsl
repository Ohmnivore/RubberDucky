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

    fragColor = vec4(ambient + diffuse + specular + uMaterial.emissiveColor, uMaterial.alpha);

    // Apply gamma correction
    fragColor.rgb = pow(fragColor.rgb, vec3(1.0 / uGamma));

    //vec3 tempColor = fragColor.rgb * 0.00001;
    //fragColor.rgb -= tempColor.rgb - length(fwidth(fragColor.rgb))*3.0;

    //float luminance = dot(fragColor.rgb, vec3(0.2126, 0.7152, 0.0722));
    //float gradient = fwidth(luminance);
    //if (gradient < 0.0000001)
    //    fragColor = vec4(0.0, 0.0, 0.0, 1.0);

    float luminance = dot(fragColor.rgb, vec3(0.2126, 0.7152, 0.0722));
    float gradient = fwidth(luminance);
    fragColor = vec4(gradient) * 6;
}
