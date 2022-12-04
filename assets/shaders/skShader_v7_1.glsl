//    Custom shader for Substance Painter to better design textures for Skyrim
//    Copyright (C) 2022  Darkluke1111 (https://www.nexusmods.com/users/8086919)
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import lib-sparse.glsl
import lib-sampler.glsl
import lib-env.glsl
import lib-random.glsl
import lib-defines.glsl
import lib-vectors.glsl

//: state blend over


// -- Initialize Texture Channels from Substance Painter --
//: param auto channel_diffuse
uniform SamplerSparse diffuse_tex;
//: param auto channel_normal
uniform SamplerSparse normal_tex;
//: param auto channel_height
uniform SamplerSparse height_tex;
//: param auto channel_emissive
uniform SamplerSparse glow_tex;
//: param auto channel_specularlevel
uniform SamplerSparse spec_tex;
//: param auto channel_opacity
uniform SamplerSparse opacity_tex;
//: param auto channel_reflection
uniform SamplerSparse envMap_tex;
//: param auto channel_user0
uniform SamplerSparse material_tex;


// -- Initialize Properties from Substance Painter --
//: param auto world_eye_position
uniform vec3 world_eye_position;
//: param auto camera_view_matrix
uniform mat4 view_matrix;
//: param auto camera_view_matrix_it
uniform mat4 view_matrix_it;

//: param auto environment_matrix
uniform mat3 uniform_environment_matrix;

// -- Specular --
//: param custom {"visible": false, "default": true,"label": "Enable Specular Map", "group": "BSLightingShader Parameters/Specular"}
uniform bool specMapEnabled;

//: param custom { 
//:     "default": [1.0,1.0,1.0], 
//:     "label": "Specular Color", 
//:     "widget": "color", 
//:     "group": "BSLightingShader Parameters/Specular",
//:     "description": "Specular Color"
//: }
uniform vec3 specColor;

//: param custom { 
//:     "default": 1.0, 
//:     "min": 0.0, 
//:     "max": 10.0, 
//:     "label": "Specular Strength", 
//:     "group": "BSLightingShader Parameters/Specular",
//:     "description": "Increases/Decreases strength of specular highlight"
//: }
uniform float specStrength;

//: param custom { 
//:     "default": 80.0, 
//:     "min": 0.0, 
//:     "max": 1000.0, 
//:     "label": "Specular Glossiness", 
//:     "group": "BSLightingShader Parameters/Specular",
//:     "description": "Increases/Decreases falloff of specular highlight"
//: }
uniform float specGlossiness;

// -- Glow --
//: param custom {
//:     "default": false,
//:     "label": "Enable Glow", 
//:     "group": "BSLightingShader Parameters/Glow",
//:     "description": "Enables/Disables the emissive shading."
//: }
uniform bool glowEnabled;

//: param custom {
//:     "default": true,
//:     "label": "Enable Glow Map", 
//:     "group": "BSLightingShader Parameters/Glow",
//:     "description": "Enables/Disables the glow map. If disabled the whole mesh will glow!"
//: }
uniform bool glowMapEnabled;

//: param custom { 
//:     "default": [0.0,0.0,0.0], 
//:     "label": "Emissive Color", 
//:     "widget": "color", 
//:     "group": "BSLightingShader Parameters/Glow" ,
//:     "description": "Glow Color"
//: }
uniform vec3 glowColor;

//: param custom { 
//:     "default": 0.0, 
//:     "min": 0.0, 
//:     "max": 100.0, 
//:     "label": "Emissive Multiple", 
//:     "group": "BSLightingShader Parameters/Glow",
//:     "description": "Increases/Decreases the glow strength"
//: }
uniform float glowMult;

// -- Environment --

//: param custom { 
//:     "default": [1.0,0.0,0.0], 
//:     "label": "Material ID 1", 
//:     "widget": "color", 
//:     "group": "BSLightingShader Parameters/Environment" ,
//:     "description": "Material ID 1"
//: }
uniform vec3 materialID_1;

//: param custom { 
//:     "default": "", 
//:     "default_color": [1.0, 1.0, 0.0, 1.0], 
//:     "label": "Environment HDRI 1", 
//:     "usage": "texture" ,
//:     "group": "BSLightingShader Parameters/Environment",
//:     "description": "Use a HDRI generated from the cubemap you plan to use in Skyrim"
//:     }
uniform sampler2D environment_tex_1;

//: param custom { 
//:     "default": [0.0,1.0,0.0], 
//:     "label": "Material ID 2", 
//:     "widget": "color", 
//:     "group": "BSLightingShader Parameters/Environment" ,
//:     "description": "Material ID 2"
//: }
uniform vec3 materialID_2;

//: param custom { 
//:     "default": "", 
//:     "default_color": [1.0, 1.0, 0.0, 1.0], 
//:     "label": "Environment HDRI 2", 
//:     "usage": "texture" ,
//:     "group": "BSLightingShader Parameters/Environment",
//:     "description": "Use a HDRI generated from the cubemap you plan to use in Skyrim"
//:     }
uniform sampler2D environment_tex_2;

//: param custom { 
//:     "default": [0.0,0.0,1.0], 
//:     "label": "Material ID 3", 
//:     "widget": "color", 
//:     "group": "BSLightingShader Parameters/Environment" ,
//:     "description": "Material ID 3"
//: }
uniform vec3 materialID_3;

//: param custom { 
//:     "default": "", 
//:     "default_color": [1.0, 1.0, 0.0, 1.0], 
//:     "label": "Environment HDRI 3", 
//:     "usage": "texture" ,
//:     "group": "BSLightingShader Parameters/Environment",
//:     "description": "Use a HDRI generated from the cubemap you plan to use in Skyrim"
//:     }
uniform sampler2D environment_tex_3;

//: param custom {
//:     "visible": false, 
//:     "default": true,
//:     "label": "Enable Environment Mapping", 
//:     "group": "BSLightingShader Parameters/Environment",
//:     "description": "Increases/Decreases the environment reflection strength"
//: }
uniform bool envMapEnabled;

//: param custom { 
//:     "default": 1.0, 
//:     "min": 0.0, 
//:     "max": 10.0, 
//:     "label": "Environment Map Strength", 
//:     "group": "BSLightingShader Parameters/Environment",
//:     "description": "Increases/Decreases the glow strength"
//: }
uniform float envReflection;

// -- Opacity --
//: param custom {
//:     "default": false,
//:     "label": "Enable Alpha", 
//:     "group": "NiAlphaProperty",
//:     "description": "Enables/Disables opacity"
//: }
uniform bool alphaEnabled;

//: param custom {
//:     "default": 128.0,
//:     "label": "Alpha threshold",
//:     "min": 0.0,
//:     "max": 255.0,
//:     "group": "NiAlphaProperty",
//:     "description": "Increases/Decreases the threshold which needs to be surpassed by the opacity texture for something to be opaque"
//: }
uniform float alpha_threshold;

//: param custom {
//:     "default": false,
//:     "label": "Alpha blending",
//:     "group": "NiAlphaProperty",
//:     "description": "If enabled parts of your mesh can be semitransparent"
//: }
uniform bool alphaBlendingEnabled;


// -- Lighting Constants --
//: param custom { 
//:     "default": false, 
//:     "label": "Enable Frontal Lighting", 
//:     "group": "NifScope Lighting Parameters",
//:     "description": "If enabled the light source will be bound to your camera position"
//: }
uniform bool frontal_lighting;

//: param custom { 
//:     "default": [0.0,100.0,0.0] , 
//:     "min": -100.0, "max": 100.0, 
//:     "label": "Light Position",
//:     "group": "NifScope Lighting Parameters",
//:     "description": "Sets the Position of the light (Has no effect when Frontal Lighting is enabled)"
//: }
uniform vec3 world_lighting;

//: param custom { 
//:     "default": 0.5, 
//:     "min": 0.0, 
//:     "max": 1.0, 
//:     "label": "Ambient Light", 
//:     "group": "NifScope Lighting Parameters",
//:     "description": "Increases/Decreases ambient lighting"
//: }
uniform float A;

//: param custom { 
//:     "default": 0.5, 
//:     "min": 0.0, 
//:     "max": 1.0, 
//:     "label": "Diffuse Light", 
//:     "group": "NifScope Lighting Parameters",
//:     "description": "Increases/Decreases diffuse lighting"
//: }
uniform float D;

// Unused
//: param custom { "visible": false, "default": 1.0, "min": 0.0, "max": 1.0, "label": "Vertex Color" , "group": "NifScope Lighting Parameters"}
uniform float C;
//: param custom { "visible": false, "default": 1.0, "min": 0.0, "max": 1.0, "label": "Vertex Color alpha" , "group": "NifScope Lighting Parameters"}
uniform float Ca;


float environmentReflectionFactor = 1.0;
float brightnessFactor = 1.0;

float normal_intensity = 2.0;


vec3 tonemap(vec3 x)
{
	float _A = 0.15;
	float _B = 0.50;
	float _C = 0.10;
	float _D = 0.20;
	float _E = 0.02;
	float _F = 0.30;

	return ((x*(_A*x+_C*_B)+_D*_E)/(x*(_A*x+_B)+_D*_F))-_E/_F;
}

vec3 toGrayscale(vec3 color)
{
	return vec3(dot(vec3(0.3, 0.59, 0.11), color));
}

void alphaKill(float alpha)
{
  float threshold = alpha_threshold/255.0;
  if (alpha < threshold) discard;
}

void alphaKill(SparseCoord coord)
{
  alphaKill(getOpacity(opacity_tex, coord));
}

vec3 myGetTSNormal(SparseCoord coord)
{
  float height_force = 0.0;
  vec3 normalH = normalFromHeight(coord, height_force);
  return getTSNormal(coord, normalH);
}

vec3 myComputeWSNormal(SparseCoord coord, vec3 tangent, vec3 bitangent, vec3 normal)
{
  vec3 normal_vec = getTSNormal(coord) * vec3(1.0,normal_intensity,1.0);
  return normalize(
    normal_vec.x * tangent +
    normal_vec.y * bitangent +
    normal_vec.z * normal
  );
}

vec3 myEnvSampleLOD(vec3 dir, float lod, vec3 materialMap, sampler2D env1, vec3 matID1, sampler2D env2, vec3 matID2, sampler2D env3, vec3 matID3)
{
  dir = worldToEnvSpace(dir);
  vec2 pos = M_INV_PI * vec2(atan(-dir.z, -1.0 * dir.x), 2.0 * asin(dir.y));
  pos = 0.5 * pos + vec2(0.5);
  vec3 multiplexed = (textureLod(env1, pos, lod).rgb * step(0.5,1-length(materialMap - matID1))) + (textureLod(env2, pos, lod).rgb * step(0.5,1-length(materialMap - matID2))) + (textureLod(env3, pos, lod).rgb * step(0.5,1-length(materialMap - matID3)));
  return multiplexed;
}

vec3 myEnvIrradiance(vec3 dir)
{
  vec4 shDir = vec4(worldToEnvSpace(dir).xzy, 1.0);
  return max(vec3(0.0), vec3(
      dot(shDir, irrad_mat_red * shDir),
      dot(shDir, irrad_mat_green * shDir),
      dot(shDir, irrad_mat_blue * shDir)
    ));
}

void shade(V2F inputs) {
    
    vec3 N = normalize(inputs.normal); // Facenormal
    vec3 T = normalize(inputs.tangent); // Facetangent
    vec3 B = normalize(inputs.bitangent); // Facebitangent
    
    vec3 light_pos;
    if(frontal_lighting) {
        light_pos = world_eye_position;
    } else {
        light_pos = transpose(environment_matrix) * world_lighting;
    }
    vec3 camera_pos = world_eye_position;

    vec3 baseMap = getBaseColor(diffuse_tex, inputs.sparse_coord);
    vec3 normalMap = myComputeWSNormal(inputs.sparse_coord, T, B, N);
	vec3 glowMap = getBaseColor(glow_tex, inputs.sparse_coord);
    float specMap = getSpecularLevel(spec_tex, inputs.sparse_coord);
    vec3 envMap =  getBaseColor(envMap_tex, inputs.sparse_coord);
    float alphaMap = getOpacity(opacity_tex, inputs.sparse_coord);
    vec3 materialMap = getBaseColor(material_tex, inputs.sparse_coord);
    
    vec3 normal = normalize(normalMap);
	
    vec3 L = normalize(light_pos - inputs.position); //Light Directtion
    vec3 E = normalize(camera_pos - inputs.position); // View Direction
	vec3 H = normalize( L + E );
    
	float NdotL = max( dot(normal, L), 0.0 );
	float NdotH = max( dot(normal, H), 0.0 );
	float EdotN = max( dot(normal, E), 0.0 );
    

    // Init outputs
    vec3 color;
	vec3 albedo = baseMap * C * brightnessFactor;
	vec3 diffuse = vec3(A) + (NdotL * D);
    vec3 emissive = vec3(0.0);
    vec3 spec = vec3(0.0);
    float alpha = 0.0;
    
    // Calculate Reflection Direction
    vec3 reflected = reflect( -E, normal );
	vec3 reflectedVS = B * reflected.x + T * reflected.y + N * reflected.z;
    vec3 reflectedWS = vec3(view_matrix_it * vec4( reflectedVS, 0.0 ) );

    // Environment Reflections
    vec3 cube = myEnvSampleLOD(normalize(reflected), 1.0, materialMap, environment_tex_1, materialID_1, environment_tex_2, materialID_2, environment_tex_3, materialID_3) * myEnvIrradiance(normalize(reflectedWS));
    cube = cube * envMap.r * envReflection * environmentReflectionFactor;
    albedo += cube;

    // Glow
    if(glowEnabled) {
        emissive += glowColor * glowMult;
        emissive *= (glowMapEnabled ? glowMap : vec3(1.0));
    }
    
    // Specular
	spec = clamp( specColor * specStrength * specMap * pow(NdotH, specGlossiness), 0.0, 1.0 );
	spec *= D;
    
    // Mixing
    color = albedo * (diffuse + emissive) + spec;
	color = tonemap( color ) / tonemap( vec3(1.0) );
	
    
    // Opacity
    if(alphaEnabled) {
        alpha = Ca * alphaMap;
        if(alphaBlendingEnabled) {
            alphaOutput(alpha);
        }
        alphaKill(alpha);

    }
    
    specularShadingOutput(vec3(0.0));
    diffuseShadingOutput(color);
    albedoOutput(vec3(1.0));
    emissiveColorOutput(vec3(0.0));
}