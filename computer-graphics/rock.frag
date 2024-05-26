#version 330 compatibility

uniform vec4 uColor;            // color of obj
uniform vec4 uSpecularColor;    
uniform float uShininess;    

// light pos --------------------------------------------------------------------
uniform float uLightX;
uniform float uLightY; 
uniform float uLightZ;

// noise --------------------------------------------------------------------
uniform float uNoiseAmp;   
uniform float uNoiseFreq;  
uniform sampler3D Noise3;  

// lighting --------------------------------------------------------------------
uniform float uKa;         // ambient 
uniform float uKd;         // diffuse 
uniform float uKs;         // specular

// coords and input from vert --------------------------------------------------------------------
in vec2 vST;
in vec3 vMCposition; 
in vec3 vNormal;     
in float noiseFreq;  

// shader output --------------------------------------------------------------------
out vec4 fragColor;

// normal rotation based on noise -- directly from the proj desc --------------------------------------------------------------------
vec3 RotateNormal(float angx, float angy, vec3 n)
{
    float cx = cos(angx);
    float sx = sin(angx);
    float cy = cos(angy);
    float sy = sin(angy);
    // xrpt
    float yp = n.y * cx - n.z * sx; 
    n.z = n.y * sx + n.z * cx; 
    n.y = yp;
    // yrot
    float xp = n.x * cy + n.z * sy; 
    n.z = -n.x * sy + n.z * cy; 
    n.x = xp;
    return normalize(n);
}

void main()
{
    // normal with 3d noise --------------------------------------------------------------------
    vec4 nvx = texture(Noise3, uNoiseFreq * vMCposition);
    float angx = nvx.r + nvx.g + nvx.b + nvx.a - 2.;
    angx *= uNoiseAmp;
    vec4 nvy = texture(Noise3, uNoiseFreq * vec3(vMCposition.xy, vMCposition.z + 0.5));
    float angy = nvy.r + nvy.g + nvy.b + nvy.a - 2.;
    angy *= uNoiseAmp;
    vec3 pertNorm = RotateNormal(angx, angy, vNormal);

    // lighting pos and calcs --------------------------------------------------------------------
    vec3 lightPos = vec3(uLightX, uLightY, uLightZ);
    vec3 lightDir = normalize(lightPos - vMCposition);
    float diff = max(dot(pertNorm, lightDir), 0.0);
    vec3 diffuse = uKd * diff * uColor.rgb;

    // view direction, specular --------------------------------------------------------------------
    vec3 viewDir = normalize(-vMCposition);
    vec3 reflectDir = reflect(-lightDir, pertNorm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), uShininess);
    vec3 specular = uKs * uSpecularColor.rgb * spec;

    // ambient lighting and final color --------------------------------------------------------------------
    vec3 ambient = uKa * uColor.rgb;
    fragColor = vec4(ambient + diffuse + specular, uColor.a);
}
