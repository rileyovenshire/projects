#version 330 compatibility

// uniforms --------------------------------------------------------------------
uniform float uA;   // amp
uniform float uB;   // period
uniform float uC;   // phase shift
uniform float uD;   // decay 

uniform float uNoiseFreq;
out float noiseFreq;

// texture coords to frag --------------------------------------------------------------------
out vec2 vST;
out vec3 vMCposition;
out vec3 vNormal;    

void main()
{
    // get texture coords, pass noise --------------------------------------------------------------------
    vST = gl_MultiTexCoord0.st;
    noiseFreq = uNoiseFreq;

    // differentiate equation --------------------------------------------------------------------
    float r = sqrt(gl_Vertex.x * gl_Vertex.x + gl_Vertex.y * gl_Vertex.y);
    float displacementZ = uA * cos(2.0 * 3.14159 * uB * r + uC) * exp(-uD * r);

    // displaced vertex --------------------------------------------------------------------
    vec4 displacedPosition = vec4(gl_Vertex.x, gl_Vertex.y, displacementZ, 1.0);

    // calculating normal --------------------------------------------------------------------
    float dzdr = uA * (-sin(2.0 * 3.14159 * uB * r + uC) * 2.0 * 3.14159 * uB * exp(-uD * r) + cos(2.0 * 3.14159 * uB * r + uC) * -uD * exp(-uD * r));
    float dzdx = dzdr * (gl_Vertex.x / r);
    float dzdy = dzdr * (gl_Vertex.y / r);
    vec3 Tx = vec3(1., 0., dzdx);
    vec3 Ty = vec3(0., 1., dzdy);
    vNormal = normalize(cross(Tx, Ty));

    // normal to eye, update coords --------------------------------------------------------------------
    vNormal = normalize(gl_NormalMatrix * vNormal);
    vMCposition = displacedPosition.xyz;
    gl_Position = gl_ModelViewProjectionMatrix * displacedPosition;
}
