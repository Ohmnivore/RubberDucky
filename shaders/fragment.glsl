#version 330 core

out vec4 FragColor;  

in vec2 ourTexture;
in vec3 ourNormal;
  
void main()
{
    FragColor = vec4(0, 0, 0, 1.0);
}
